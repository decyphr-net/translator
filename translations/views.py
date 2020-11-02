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
        data = {
            "initial_text": request.POST.get("input"),
            "translated_text": self._translate_text(
                request.POST.get("input"), "en", "pt"
            ),
        }
        return render(request, self.template_name, context=data)