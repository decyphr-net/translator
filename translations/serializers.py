"""
Translation Serializers.

This module will contain the serializers that relate to the translation views
"""
from rest_framework import serializers


class FullTranslationSerializer(serializers.Serializer):
    """Full Translation Serializer

    This serializer will be used to deserialize the incoming text and language
    code that will be sent to the Google Translate API

    Args:
        target_language_code (str): A ISO 639-1 code that will be used to inform \
        Google Translate of the target language
        text (str): The text that is needed to be translated
    """
    initial_language_code = serializers.CharField(required=True)
    target_language_code = serializers.CharField(required=True)
    text = serializers.CharField(required=True)

    def validate_initial_language_code(self, initial_language_code):
        if len(initial_language_code) <= 3:
            raise serializers.ValidationError(
                "The language code provided is too short. Please ensure the code is in ISO 639-1 format")
        elif len(initial_language_code) > 5:
            raise serializers.ValidationError(
                "The language code provided is too long. Please ensure the code is in ISO 639-1 format")
        return initial_language_code

    def validate_target_language_code(self, target_language_code):
        if len(target_language_code) <= 1:
            raise serializers.ValidationError(
                "The language code provided is too short. Please ensure the code is in ISO 639-1 format")
        elif len(target_language_code) > 2:
            raise serializers.ValidationError(
                "The language code provided is too long. Please ensure the code is in ISO 639-1 format")
        return target_language_code


class FullyTranslatedTextSerializer(serializers.Serializer):
    """
    The translated information that will come back from the Google Translate
    API

    Args:
        translated_text (str): The newly translated text
    """
    translated_text = serializers.CharField(required=True)
    audio_location = serializers.CharField(required=True)
    analyzed_text = serializers.JSONField()