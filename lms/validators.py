from rest_framework import serializers
from typing import Dict, Any


class CheckLinkVideo:
    """
    Проверка, что поле содержит ссылку на видео с определенного домена.

    Attributes:
        field (str): Имя поля, которое содержит URL видео.
        allowed_domains (list): Список доменов, которые разрешены.
    """

    def __init__(self, field: str, allowed_domains: list = None):
        self.field = field
        self.allowed_domains = allowed_domains or ['youtube.com']

    def __call__(self, data: Dict[str, Any]):
        """
        Проверка, что URL в поле начинается с одного из разрешенных доменов.

        Args:
            data (dict): Словарь данных, содержащий поле с URL видео.

        Raises:
            serializers.ValidationError: Если URL не соответствует разрешенным доменам.
        """
        link_video = data.get(self.field)
        if link_video and not self._is_valid_link(link_video):
            raise serializers.ValidationError(
                {self.field: f'Размещать видео-ссылки можно только с ресурсов: {", ".join(self.allowed_domains)}'}
            )

    def _is_valid_link(self, link: str) -> bool:
        """
        Проверка, что ссылка начинается с одного из разрешенных доменов.

        Args:
            link (str): URL для проверки.

        Returns:
            bool: Истина, если URL соответствует разрешенным доменам, иначе ложь.
        """
        return any(link.startswith(f'https://www.{domain}') for domain in self.allowed_domains)


    # def __init__(self, field):
    #     self.field = field
    #
    # def __call__(self, data):
    #     link_video = data.get(self.field)
    #     if link_video and not link_video.startswith('https://www.youtube.com'):
    #         raise serializers.ValidationError(
    #             {self.field: 'Размещать видео-ссылки можно только с ресурсов youtube.com'}
    #         )
