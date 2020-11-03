import json
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .utils import LanguageProcessingMixin


class TranslationView(View, LanguageProcessingMixin):
    template_name = "translate.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        json_data = json.loads(request.body)

        translated_text = self._translate_text(
            json_data["text"],
            json_data["source"],
            json_data["target"],
        )

        data = {
            "initial_text": json_data["text"],
            "translated_text": translated_text,
        }
        return JsonResponse(data)