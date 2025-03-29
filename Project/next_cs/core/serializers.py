from rest_framework import serializers
from .models import QuizTopic, QuizSubTopic, QuizQuestion, UserQuizScore

class QuizTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizTopic
        fields = '__all__'

class QuizSubTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizSubTopic
        fields = '__all__'

class QuizQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizQuestion
        fields = '__all__'

class UserQuizScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserQuizScore
        fields = '__all__'
