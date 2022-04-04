"""
Создание необходимых сериализаторов.
"""

from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer
from drf_extra_fields.fields import Base64ImageField
from recipes.models import (Cart, Favorite, Ingredient, IngredientRecipe,
                            Recipe, Subscribe, Tag, TagRecipe, ShoppingCart)
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from users.models import User


class RegistrationSerializer(UserCreateSerializer):
    """
    Создание сериализатора модели пользователя.
    """
    is_subscribed = serializers.SerializerMethodField()

    class Meta():
        model = User
        fields = ('id', 'username', 'email', 'first_name',
                  'last_name', 'is_subscribed', 'password')
        write_only_fields = ('password',)
        read_only_fields = ('id',)
        extra_kwargs = {'is_subscribed': {'required': False}}

    def to_representation(self, obj):
        rep = super(RegistrationSerializer, self).to_representation(obj)
        rep.pop('password', None)
        return rep

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request.user.username == '':
            return False
        if Subscribe.objects.filter(
                user=request.user, following__id=obj.id).exists():
            return True
        else:
            return False


class IngredientSerializer(serializers.ModelSerializer):
    """
    Создание сериализатора модели продуктов.
    """
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
        extra_kwargs = {'name': {'required': False},
                        'measurement_unit': {'required': False}}


class IngredientAmountSerializer(serializers.ModelSerializer):
    """
    Создание сериализатора модели продуктов в рецепте.
    """
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit',
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class IngredientAmountRecipeSerializer(serializers.ModelSerializer):
    """
    Создание сериализатора продуктов вместе с количеством.
    """
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = Ingredient
        fields = ('id', 'amount')


class TagSerializer(serializers.ModelSerializer):
    """
    Создание сериализатора модели тэгов.
    """
    class Meta:
        model = Tag
        fields = '__all__'
        extra_kwargs = {'name': {'required': False},
                        'slug': {'required': False},
                        'color': {'required': False}}


class FavoriteSerializer(serializers.Serializer):
    """
    Создание сериализатора избранных рецептов.
    """
    id = serializers.IntegerField()
    name = serializers.CharField()
    cooking_time = serializers.IntegerField()
    image = Base64ImageField()

    def create(self, validated_data):
        request = self.context.get('request')
        id_data = validated_data.pop('id')
        recipe = get_object_or_404(Recipe, id=id_data)
        Favorite.objects.create(
            user=request.user, recipes_id=id_data)
        return recipe


class CartSerializer(serializers.Serializer):
    """
    Создание сериализатора корзины.
    """
    id = serializers.IntegerField()
    name = serializers.CharField()
    cooking_time = serializers.IntegerField()
    image = Base64ImageField()

    def create(self, validated_data):
        request = self.context.get('request')
        recipe_id = self.kwargs.get('recipes_id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        Cart.objects.create(
            user=request.user, recipes_id=recipe_id)
        return recipe


class RecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели рецептов.
    """
    author = RegistrationSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True)
    ingredients = IngredientAmountRecipeSerializer(
        source='ingredientrecipes', many=True)
    image = Base64ImageField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'name', 'image', 'text',
                  'ingredients', 'tags', 'cooking_time',
                  'is_in_shopping_cart', 'is_favorited')

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        recipe = get_object_or_404(Recipe, id=obj.id)
        if request.user.username == '':
            return False
        if Favorite.objects.filter(user=request.user, recipes=recipe).exists():
            return True
        else:
            return False

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        recipe = get_object_or_404(Recipe, id=obj.id)
        if request.user.username == '':
            return False
        if Cart.objects.filter(user=request.user, recipes=recipe).exists():
            return True
        else:
            return False

    def to_representation(self, obj):
        self.fields['tags'] = TagSerializer(many=True, read_only=True)
        self.fields['ingredients'] = IngredientAmountSerializer(
            source='ingredientrecipes',
            many=True, read_only=True)
        return super(RecipeSerializer, self).to_representation(obj)

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        author = validated_data.get('author')
        name = validated_data.get('name')
        image = validated_data.get('image')
        text = validated_data.get('text')
        cooking_time = validated_data.get('cooking_time')
        ingredients = validated_data.pop('ingredientrecipes')
        recipe = Recipe.objects.create(
            author=author,
            name=name,
            image=image,
            text=text,
            cooking_time=cooking_time,
        )
        for tag in tags_data:
            recipe.tags.add(tag)
        for ingredient in ingredients:
            IngredientRecipe.objects.create(
                ingredient_id=ingredient['id'],
                recipe=recipe,
                amount=ingredient['amount'],
            )
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time)
        instance.save()
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.get(name=instance.name)
        TagRecipe.objects.filter(recipe=recipe).delete()
        for tag in tags_data:
            recipe.tags.add(tag)
            recipe.save()
        ingredients = validated_data.pop('ingredientrecipes')
        IngredientRecipe.objects.filter(recipe=recipe).delete()
        for ingredient in ingredients:
            ingredientrecipe = IngredientRecipe.objects.create(
                ingredient_id=ingredient['id'],
                recipe=recipe)
            ingredientrecipe.amount = ingredient['amount']
            ingredientrecipe.save()
        instance.save()
        return instance


class RecipeMinifieldSerializer(serializers.ModelSerializer):
    """
    Сериализатор для упрощенного отображения модели рецептов.
    """
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'cooking_time', 'image')


class SubscribeSerializer(serializers.Serializer):
    """
    Сериализатор создания подписок.
    """
    email = serializers.EmailField()
    id = serializers.IntegerField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    is_subscribed = serializers.SerializerMethodField()
    recipes = RecipeMinifieldSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField()

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author__id=obj.id).count()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request.user.username == '':
            return False
        if Subscribe.objects.filter(
                user=request.user, following__id=obj.id).exists():
            return True
        else:
            return False

    def create(self, validated_data):
        request = self.context.get('request')
        user_id = self.context.get('view').kwargs.get('users_id')
        user = get_object_or_404(User, id=user_id)
        Subscribe.objects.create(
            user__id=user_id, following__id=request.user.id)
        return user


class SubscriptionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для списка подписок.
    """
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes(self, obj):
        request = self.context.get('request')
        if request.GET.get('recipes_limit'):
            recipes_limit = int(request.GET.get('recipes_limit'))
            queryset = Recipe.objects.filter(author__id=obj.id).order_by('id')[
                :recipes_limit]
        else:
            queryset = Recipe.objects.filter(author__id=obj.id).order_by('id')
        return RecipeMinifieldSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author__id=obj.id).count()

    def get_is_subscribed(self, obj):
        if self.context['request'].user.username == '':
            return False
        if Subscribe.objects.filter(
                user=self.context['request'].user,
                following__id=obj.id).exists():
            return True
        else:
            return False


class ShoppingSerializer(serializers.ModelSerializer):
    """
    Сериализатор для списка покупок.
    """
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = ShoppingCart
        fields = ('name', 'amount', 'measurement_unit')
