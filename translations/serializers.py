"""
Translation Serializers.

This module will contain the serializers that relate to the translation views
"""
from rest_framework import serializers


class PlainTextTranslationSerializer(serializers.Serializer):
    """Plain Text Translation Serializer

    This serializer will be used to deserialize the incoming text and language
    code that will be sent to the Google Translate API

    Args:
        language_code (str): A ISO 639-1 code that will be used to inform \
        Google Translate of the target language
        text (str): The text that is needed to be translated
    """
    language_code = serializers.CharField(required=True)
    text = serializers.CharField(required=True)

    def validate_language_code(self, language_code):
        if len(language_code) <= 1:
            raise serializers.ValidationError(
                "The language code provided is too short. Please ensure the code is in ISO 639-1 format")
        elif len(language_code) > 2:
            raise serializers.ValidationError(
                "The language code provided is too long. Please ensure the code is in ISO 639-1 format")
        return language_code


class TranslatedTextSerializer(serializers.Serializer):
    """
    The translated information that will come back from the Google Translate
    API

    Args:
        translated_text (str): The newly translated text
    """
    translated_text = serializers.CharField(required=True)