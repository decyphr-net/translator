"""
The Google wrapper class is a mixin that will be used in all of the endpoints
relating to the interaction with Google Cloud services.
"""
import uuid
import json
from django.conf import settings
from google.cloud import translate
from google.cloud import texttospeech
from google.cloud import storage
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from google.protobuf.json_format import MessageToJson


class GoogleMixin:
    """Google Cloud Mixin Class

    This mixin will contain all of the necessary functionality required to
    integrate with the relevant Google Cloud services.

    Examples:
        In order to take advantage of this mixin, simple extended it::
            class TranslationEndpoint(viewsets.ViewSet, GoogleMixin):
    """
    translation_client = translate.TranslationServiceClient()
    text_to_speech_client = texttospeech.TextToSpeechClient()
    natural_language_client = language.LanguageServiceClient()
    storage_client = storage.Client()
    bucket = storage_client.bucket(settings.BUCKET_NAME)
    
    parent = translation_client.location_path(
        settings.GOOGLE_PROJECT, "global")
    
    def upload_to_bucket(self, audio_content):
        """Upload audio to Storage

        Upload audio file to Cloud Storage. Files name don't need to contain
        any specific information, but do need to be unique so we'll generate
        a UUID for each new file being created

        Args:
            audio_content (str): The string of information that gets returned \
            from the text to speech API
        
        Returns:
            str: The path to the newly generated file
        """
        blob_name = uuid.uuid4().hex
        blob = self.bucket.blob(blob_name)
        blob.upload_from_string(audio_content)
        return "https://storage.cloud.google.com/{}/{}".format(
            settings.BUCKET_NAME, blob_name)
        
        
    def translate_text(self, target_language_code, text):
        """Translate Text

        The interface into Google's Translation API.

        Args:
            target_language_code : A ISO 639-1 code that will be used to \
            inform Google Translate of the target language
            text (str): The text that is needed to be translated
        
        Returns:
            translated_text (str): The text that was returned by the \
            Google Translate API
        
        Examples:
            translated_text = self.translate_text(language_code, text)
        """
        response = self.translation_client.translate_text(
            parent=self.parent,
            contents=[text],
            mime_type="text/plain",
            target_language_code=target_language_code
        )

        return response.translations[0].translated_text
    
    def text_to_speech(self, text, language_code="en-US"):
        """Text to Speech

        Convert the text into an audio file for users to be able to hear
        samples of the text in the intended language.

        Args:
            text (str): The text to be converted to audio
            language_code (str): The full language code for the target language
        
        Returns:
            location (str): The path to the location of the audio file
        """
        input_text = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        response = self.text_to_speech_client.synthesize_speech(
            request={
                "input": input_text,
                "voice": voice,
                "audio_config": audio_config}
        )        
        return self.upload_to_bucket(response.audio_content)
    
    def parse_text(self, text):
        """
        Parse the text from the original language
        """
        type_ = enums.Document.Type.PLAIN_TEXT
        document = {"content": text, "type": type_}
        encoding_type = enums.EncodingType.UTF8
        response = self.natural_language_client.analyze_syntax(
            document, encoding_type=encoding_type)
        return MessageToJson(response)