from rest_framework import serializers
from .models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('lastName', 'firstName', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # return User.objects.create(**validated_data)
        user = User(
            firstName=validated_data['firstName'],
            lastName=validated_data['lastName'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')


class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    token = serializers.CharField(max_length=255)


class DomaineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domaine
        fields = ['id', 'name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = ['id', 'nom']


class ParcoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcours
        fields = ['id', 'name', 'categorie', 'domaine']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'html', 'is_published', 'maximum_marks', 'categorie']
        # depth = 1


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'html', 'is_correct', 'question']
        # depth = 1


class AttemptedQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttemptedQuestion
        fields = ['id', 'question', 'quiz_profile',
                  'is_correct', 'selected_choice', 'marks_obtained']


class QuizProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizProfile
        fields = ['id', 'user', 'total_score', 'parcours', 'completed']


class TutorialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tutorial
        fields = ['id', 'categorie', 'contenu', 'link']


class FileUploadSerializer(serializers.Serializer):
    csv_file = serializers.FileField()
