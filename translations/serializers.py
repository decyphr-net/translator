"""
Translation Serializers.

This module will contain the serializers that relate to the translation views.
There are two main serializer types - Input serializers and Output serializers.

Input serializers will handle the deserialization and validation of incoming
information.

Output serializers will serialize the information that comes back from Google
Cloud and serialize it to send it back to the client.
"""
from rest_framework import serializers

CODE_MSG = "The language code is too {}. Please use ISO 639-1 format"


class BaseInputTranslation(serializers.Serializer):
    """Base Input Serializer

    The base translation serializer that will implement the basic fields and
    validations that will be required on all incoming data.

    At it's most basic, a translation task will require a piece of text and
    the target language the client needs the text translated to.

    In the event that the properties of this class are sufficient, it may
    still be better to create a new class that inherits this class, rather
    than using this class directly

    Args:
        target_language_code (str): A 2 digit ISO 639-1 code
        text (str): The piece of text that is to be translated
    """

    target_language_code = serializers.CharField(required=True)
    text = serializers.CharField(required=True)

    def validate_target_language_code(self, target_language_code):
        """Validate target language code

        Validate the target language code to ensure that the string is 2
        digits. If the string is too long or too short then the consumer of
        the API needs to be informed
        """
        if len(target_language_code) <= 1:
            raise serializers.ValidationError(CODE_MSG.format("short"))
        elif len(target_language_code) > 2:
            raise serializers.ValidationError(CODE_MSG.format("long"))
        return target_language_code


class FullTranslationSerializer(BaseInputTranslation):
    """Full Translation Serializer

    This serializer will be used to deserialize the incoming text and language
    code that will be sent to the Google Translate API.

    This serializer will be used for the specific purpose of translating text,
    getting creating an audio representation of the text and a text anaylsis.
    For this reason, it is necessary to provide the initial language code to
    inform Google's Text to Speech service which language it will be
    converting to speech

    Args:
        initial_language_code (str): A 4 digit ISO 639-1 code
        target_language_code (str): A 2 digit ISO 639-1 code
        text (str): The piece of text that is to be translated
    """

    initial_language_code = serializers.CharField(required=True)
    initial_language_code_long = serializers.CharField(required=True)

    def validate_initial_language_code(self, initial_language_code):
        """Validate initial language code

        Validate the initial language code to ensure that the string is 5
        digits. If the string is too long or too short then the consumer of
        the API needs to be informed
        """
        if len(initial_language_code) <= 1:
            raise serializers.ValidationError(CODE_MSG.format("short"))
        elif len(initial_language_code) > 2:
            raise serializers.ValidationError(CODE_MSG.format("long"))
        return initial_language_code

    def validate_initial_language_code_long(self, initial_language_code_long):
        """Validate initial language code

        Validate the initial language code to ensure that the string is 5
        digits. If the string is too long or too short then the consumer of
        the API needs to be informed
        """
        if len(initial_language_code_long) <= 3:
            raise serializers.ValidationError(CODE_MSG.format("short"))
        elif len(initial_language_code_long) > 5:
            raise serializers.ValidationError(CODE_MSG.format("long"))
        return initial_language_code_long


class TextToTextSerializer(BaseInputTranslation):
    """Text To Text Serializer

    This serializer will receive the text that needs to be translated and the
    language that it needs to be translated to.

    This serializer will be used solely for straighforward text to text
    translations where the only requirement is to translate the text from the
    initial language to the specified target language.

    For this reason, it is enough to use only the fields provided by the
    parent.
    """

    pass


class BaseOutputSerializer(serializers.Serializer):
    """Base Output Serializer

    The base translation serializer that will implement the basic fields and
    validations that will be required on all outgoing data.

    The simplest implementation of this will only require the result of the
    translation.

    In the event that the properties of this class are sufficient, it may
    still be better to create a new class that inherits this class, rather
    than using this class directly

    Args:
        translated_text (str): The text returned from Cloud Translate
    """

    translated_text = serializers.CharField(required=True)


class FullTranslatedSerializer(BaseOutputSerializer):
    """Full Translated Serializer

    This serializer will handle the serialization of the information that
    comes back from the Cloud APIs.

    The purpose of this serializer is to serializer the information that comes
    back from the following services:
    - Translate
    - Text To Speech & Cloud Storage
    - Natural language

    Args:
        translated_text (str): The newly translated text
        audio_location (str): The URL to the generated audio file
        analyzed_text (JSON): A JSON representation of Google's analysis
        of the text
    """

    audio_location = serializers.CharField(required=True)
    analyzed_text = serializers.JSONField()


class TextToTextTranslatedSerializer(BaseOutputSerializer):
    """Text To Text Translated Serializer

    This serializer will be used solely for straighforward text to text
    translations where the only requirement is to return the translated text
    to the client.

    For this reason, it is enough to use only the fields provided by the
    parent.
    """

    pass