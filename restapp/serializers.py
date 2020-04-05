from rest_framework import serializers
from .models import Question, LANGUAGE_CHOICES


# serializer serializes the queryset or model instances into python readable objects & then into JSON represented data

class QuestionSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=100)
    name = serializers.CharField(max_length=20)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='PYTHON')
    address = serializers.CharField(style={'base_template': 'textarea.html'})

    def create(self, validated_data):
        queryset = Question.objects.create(**validated_data)
        return queryset

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.name = validated_data.get('name', instance.name)
        instance.language = validated_data.get('language', instance.language)
        instance.address = validated_data.get('address', instance.address)
        instance.save()

        return instance
