"""
Translation Serializers.

This module will contain the serializers that relate to the translation views
"""
from rest_framework import serializers


class PlainTextTranslationSerializer(serializers.Serializer):
    """Plain Text Translation Serializer

    This serializer will be used to deserialize the incoming text and language
    code and once the the translation has been completed by Google Translate,
    the translated text will be included in the information in the response

    Args:
        language_code (str): A ISO 639-1 code that will be used to inform
        Google Translate of the target language
        text (str): The text that is needed to be translated
        translated_text (str): The translated text will only be populated once
        the translation has been performed by Google Translate
    """
    language_code = serializers.CharField(required=True)
    text = serializers.CharField(required=True)
    translated_text = serializers.CharField(required=False)