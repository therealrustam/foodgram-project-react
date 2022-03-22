from djoser.serializers import \
    UserCreateSerializer as BaseUserRegistrationSerializer
from recipes.models import Follow, Ingredient, Recipe, Tag
from rest_framework import serializers
from users.models import User


class RegistrationSerializer(BaseUserRegistrationSerializer):

    class Meta(BaseUserRegistrationSerializer.Meta):
        model = User
        fields = ('id', 'username', 'email',
                  'first_name', 'last_name', 'password')
        write_only_fields = ('password',)
        read_only_fields = ('id',)
        extra_kwargs = {'password': {'required': True}}

    # def create(self, validated_data):
    #    user = User.objects.create(
    #        username=validated_data['username'],
    #        email=validated_data['email'],
    #        first_name=validated_data['first_name'],
    #        last_name=validated_data['last_name'],
    #        password=validated_data['password']
    #    )
    #    user.save()
     #   return user


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = '__all__'
