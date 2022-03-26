from djoser.serializers import \
    UserCreateSerializer as BaseUserRegistrationSerializer
from recipes.models import Follow, Ingredient, Recipe, Tag
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


class RecipeSerializer(serializers.ModelSerializer):
    author = RegistrationSerializer()
    tags = TagSerializer(many=True)
    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели подписок.
    """
    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault())

    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = '__all__'
        validators = [UniqueTogetherValidator(
            queryset=Follow.objects.all(),
            fields=['user', 'following']), ]

    def validate(self, data):
        if data['user'] == data['following']:
            raise serializers.ValidationError(
                'Нельзя подписываться на себя!'
            )
        return data
