"""
Translation Serializers.

This module will contain the serializers that relate to the translation views.
"""
from rest_framework import serializers

CODE_MSG = "The language code is too {}. Please use ISO 639-1 format"


class BaseInputTranslation(serializers.Serializer):
    """
    The base translation serializer that will implement the basic fields and
    validations that will be required on all incoming data
    """
    target_language_code = serializers.CharField(required=True)
    text = serializers.CharField(required=True)

    def validate_initial_language_code(self, initial_language_code):
        if len(initial_language_code) <= 3:
            raise serializers.ValidationError(CODE_MSG.format("short"))
        elif len(initial_language_code) > 5:
            raise serializers.ValidationError(CODE_MSG.format("long"))
        return initial_language_code

    def validate_target_language_code(self, target_language_code):
        if len(target_language_code) <= 1:
            raise serializers.ValidationError(CODE_MSG.format("short"))
        elif len(target_language_code) > 2:
            raise serializers.ValidationError(CODE_MSG.format("long"))
        return target_language_code


class FullTranslationSerializer(BaseInputTranslation):
    """Full Translation Serializer

    This serializer will be used to deserialize the incoming text and language
    code that will be sent to the Google Translate API

    Args:
        target_language_code (str): A ISO 639-1 code that will be used to inform \
        Google Translate of the target language
        text (str): The text that is needed to be translated
    """
    initial_language_code = serializers.CharField(required=True)


class PlainTranslationSerializer(BaseInputTranslation):
    """
    This serializer will receive the text that needs to be translated and the
    language that it needs to be translated to
    """
    pass


class BaseOutputSerializer(serializers.Serializer):
    """
    """
    translated_text = serializers.CharField(required=True)


class FullTranslatedSerializer(BaseOutputSerializer):
    """
    The translated information that will come back from the Google Translate
    API

    Args:
        translated_text (str): The newly translated text
    """
    translated_text = serializers.CharField(required=True)
    audio_location = serializers.CharField(required=True)
    analyzed_text = serializers.JSONField()


class PlainTranslatedSerializer(BaseOutputSerializer):
    """
    """
    pass