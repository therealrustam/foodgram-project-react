from django.shortcuts import get_list_or_404, get_object_or_404
from djoser.serializers import \
    UserCreateSerializer as BaseUserRegistrationSerializer
from drf_extra_fields.fields import Base64ImageField
from importlib_metadata import requires
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
        id_data = validated_data.pop('id')
        recipe = get_object_or_404(Recipe, id=id_data)
        Favorite.objects.create(
            user_id=request.user.id, recipes_id=id_data)
        return recipe


class CartSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    cooking_time = serializers.IntegerField()

    def create(self, validated_data):
        request = self.context.get('request')
        id_data = validated_data.pop('id')
        recipe = get_object_or_404(Recipe, id=id_data)
        Cart.objects.create(
            user_id=request.user.id, recipes_id=id_data)
        return recipe


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


class RecipeShortSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Recipe.
    """

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'cooking_time')


class SubscribeSerializer(serializers.Serializer):
    """
    Сериализатор подписок.
    """
    email = serializers.EmailField()
    id = serializers.IntegerField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    is_subscribed = serializers.BooleanField()
    #recipes = RecipeShortSerializer(required=False)
    recipes_count = serializers.SerializerMethodField()

    def get_recipes_count(self, obj):
        author_id = self.context.get('id')
        return len(get_list_or_404(Recipe, author__id=author_id))

    def create(self, validated_data):
        request = self.context.get('request')
        id_data = self.context.get('view').kwargs.get('users_id')
        user = get_object_or_404(User, pk=id_data)
        Subscribe.objects.create(
            user_id=id_data, following_id=request.user.id)
        return user
