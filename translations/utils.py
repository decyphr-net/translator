"""
This class is a mixin that will be used in all of the endpoints relating to
the interaction with AWS services.
"""
import boto3
from django.conf import settings

_region = settings.REGION
_access_key = settings.ACCESS_KEY_ID
_secret_key = settings.SECRET_ACCESS_KEY


class LanguageProcessingMixin:
    """The language processing mixin

    This mixin will contain all of the necessary functionality required to
    integrate with the relevant services.

    The purpose of this mixin os to provide an into the external services in a
    single class. A class extending this class will be able to translate text
    convert it to speech and provide a breakdown of the text.

    Examples:
        In order to take advantage of this mixin, simple extended it::
            class TranslationEndpoint(viewsets.ViewSet, LanguageProcessingMixin):
    """

    _translator = boto3.client(
        "translate",
        _region,
        aws_access_key_id=_access_key,
        aws_secret_access_key=_secret_key,
    )

    _polly = boto3.client(
        "polly",
        _region,
        aws_access_key_id=_access_key,
        aws_secret_access_key=_secret_key,
    )

    _comprehend = boto3.client(
        "comprehend",
        _region,
        aws_access_key_id=_access_key,
        aws_secret_access_key=_secret_key,
    )

    def _get_text_analysis(self, text, language):
        """Analyse text

        Send the text to AWS Comprehend to be analysed.

        Args:
            text (str): The text to be analysed
            language (str): The code for the language that the text is written in

        Returns:
            The syntactical structure of the text (dict)
        """
        response = self._comprehend.detect_syntax(Text=text, LanguageCode=language)
        return response["SyntaxTokens"]

    def _generate_audio_file(self, text, new_language):
        """Generate audio file

        The audio file that is necessary for playing back the audio for a user
        to listen, is generated by Polly and stored on S3. The function invokes
        the service to generate the audio file and returns the location.

        Args:
            text (str): The text to be converted to audio
            new_language (str): The ISO 639-1 code of the text language

        Returns:
            The URI to the mp3 (str)
        """
        response = self._polly.start_speech_synthesis_task(
            Engine=settings.POLLY_CONFIG["engine"],
            LanguageCode=new_language,
            OutputFormat=settings.POLLY_CONFIG["output_format"],
            OutputS3BucketName=settings.BUCKET_NAME,
            Text=text,
            TextType=settings.POLLY_CONFIG["text_type"],
            VoiceId="Ricardo",
        )
        return response["SynthesisTask"]["OutputUri"]

    def _translate_text(self, text, first_language, new_language):
        """Translate text

        Translate the text from the provided language into the user's
        language.

        Args:
            text (str): The piece of text to be translated first
            first_language: The ISO 639-1 code of the text language
            new_language: The ISO 639-1 code of the language to translate to

        Returns:
            The translated text (str)
        """
        response = self._translator.translate_text(
            Text=text,
            SourceLanguageCode=new_language,
            TargetLanguageCode=first_language,
        )
        return response["TranslatedText"]

    def bundle_full_translation_response(self, serializer):
        """
        Collects the data from the two primary AWS interface functions
        and bundles it up into a dictionary and returns that dictionary
        """
        translated_text = self._translate_text(
            serializer.data["text"],
            serializer.data["initial_language_code"],
            serializer.data["target_language_code"],
        )
        audio_location = self._generate_audio_file(
            serializer.data["text"], serializer.data["initial_language_code_long"]
        )
        analyzed_text = self._get_text_analysis(
            serializer.data["text"], serializer.data["initial_language_code"]
        )

        translated_data = {
            "translated_text": translated_text,
            "audio_location": audio_location,
            "analyzed_text": analyzed_text,
        }
        translated_text_serializer = self.output_serializer(data=translated_data)

        if translated_text_serializer.is_valid():
            return translated_text_serializer.data
        else:
            return translated_text_serializer.errors