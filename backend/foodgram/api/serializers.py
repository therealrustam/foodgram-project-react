from django.shortcuts import get_list_or_404, get_object_or_404
from djoser.serializers import \
    UserCreateSerializer as BaseUserRegistrationSerializer
from drf_extra_fields.fields import Base64ImageField
from recipes.models import Cart, Favorite, Ingredient, Recipe, Subscribe, Tag
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from users.models import User


class RegistrationSerializer(BaseUserRegistrationSerializer):

    class Meta():
        model = User
        fields = ('id', 'username', 'email',
                  'first_name', 'last_name', 'password')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def to_representation(self, obj):
        rep = super(RegistrationSerializer, self).to_representation(obj)
        rep.pop('password', None)
        return rep


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit', 'amount')
        extra_kwargs = {'name': {'required': False},
                        'measurement_unit': {'required': False}}


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'
        extra_kwargs = {'name': {'required': False},
                        'slug': {'required': False},
                        'color': {'required': False}}


class FavoriteSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    cooking_time = serializers.IntegerField()
    image = Base64ImageField()

    def create(self, validated_data):
        request = self.context.get('request')
        id_data = validated_data.pop('id')
        recipe = get_object_or_404(Recipe, id=id_data)
        Favorite.objects.create(
            user_id=request.user.id, recipes_id=id_data)
        return recipe


class CartSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    cooking_time = serializers.IntegerField()
    image = Base64ImageField()

    def create(self, validated_data):
        request = self.context.get('request')
        recipe_id = self.kwargs.get('recipes_id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        Cart.objects.create(
            user_id=request.user.id, recipes_id=recipe_id)
        return recipe


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Recipe.
    """
    author = RegistrationSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)
    image = Base64ImageField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'name', 'image', 'text', 'ingredients',
                  'tags', 'cooking_time', 'is_in_shopping_cart', 'is_favorited')

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        recipe = get_object_or_404(Recipe, id=obj.id)
        if Favorite.objects.filter(user=request.user, recipes=recipe).exists():
            return True
        else:
            return False

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        recipe = get_object_or_404(Recipe, id=obj.id)
        if Cart.objects.filter(user=request.user, recipes=recipe).exists():
            return True
        else:
            return False


class RecipeWriteSerializer(RecipeReadSerializer):
    tags = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        author = validated_data.get('author')
        name = validated_data.get('name')
        image = validated_data.get('image')
        text = validated_data.get('text')
        cooking_time = validated_data.get('cooking_time')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(
            author=author,
            name=name,
            image=image,
            text=text,
            cooking_time=cooking_time,
        )
        recipe.save()
        for tag in tags_data:
            recipe.tags.add(tag)
            recipe.save()
        for count_ingredient in ingredients:
            current_ingredient = Ingredient.objects.get(
                id=count_ingredient.id
            )
            Ingredient.objects.create(
                ingredient=current_ingredient,
                recipe=recipe,
                amount=count_ingredient.amount,
            )
        return recipe


class RecipeMinifieldSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Recipe.
    """
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'cooking_time', 'image')


class SubscribeSerializer(serializers.Serializer):
    """
    Сериализатор подписок.
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
        following_id = obj.id
        return (Recipe.objects.filter(following__id=following_id).count())

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if Subscribe.objects.filter(
                user__id=obj.id, follower=request.user).exists():
            return True
        else:
            return False

    def create(self, validated_data):
        request = self.context.get('request')
        user_id = self.context.get('view').kwargs.get('users_id')
        user = get_object_or_404(User, id=user_id)
        Subscribe.objects.create(
            user_id=user_id, following_id=request.user.id)
        return user


class SubscriptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
