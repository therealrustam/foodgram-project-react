from django.shortcuts import get_object_or_404
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
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class FavoriteSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    cooking_time = serializers.IntegerField()

    def create(self, validated_data):
        request = self.context.get('request')
        #user = get_object_or_404(User, id=request.user.id)
        id_data = validated_data.pop('id')
        recipe = get_object_or_404(Recipe, id=id_data)
        Favorite.objects.create(
            user_id=request.user.id, recipes_id=id_data)
        return recipe

    def update(self, instance, validated_data):
        request = self.context.get('request')
        #user = get_object_or_404(User, id=request.user.id)
        id_data = validated_data.pop('id')
        recipe = get_object_or_404(Recipe, id=id_data)
        favorite = Favorite.objects.delete(
            user_id=request.user.id, recipes_id=id_data)
        return recipe


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'cooking_time')

    def create(self, validated_data):
        request = self.context.get('request', None)
        user = get_object_or_404(User, id=request.user.id)
        recipe = get_object_or_404(Recipe, **validated_data)
        Cart.objects.create(user=user, recipe=recipe)
        return user


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Recipe.
    """
    author = RegistrationSerializer(read_only=True)
    tags = TagSerializer(many=True)
    ingredients = IngredientSerializer(many=True)
    image = Base64ImageField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'name', 'image', 'text', 'ingredients',
                  'tags', 'cooking_time', 'is_in_shopping_cart', 'is_favorited')

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        recipe_id = self.context.get('id')
        recipe = Recipe.objects.filter(id=recipe_id)
        if Favorite.objects.filter(user=request.user, recipes=recipe).exists:
            return True
        else:
            return False

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        recipe_id = self.context.get('id')
        recipe = Recipe.objects.filter(id=recipe_id)
        if Cart.objects.filter(user=request.user, recipes=recipe).exists:
            return True
        else:
            return False


class SubscribeSerializer(serializers.Serializer):
    """
    Сериализатор модели подписок.
    """
    class Meta:
        model = Subscribe
        fields = '__all__'
