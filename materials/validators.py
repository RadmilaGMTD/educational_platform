import re

from rest_framework.validators import ValidationError


class UrlsValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        urls = re.findall(r"https?://[^\s]+", str(value))
        for url in urls:
            if not re.search(r"(youtube\.com|youtu\.be)", url):
                raise ValidationError(f"Запрещенная ссылка: {url}. " "Разрешены только youtube.com и youtu.be")
