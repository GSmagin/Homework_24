from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = '������� ������ ��� �����������'

    def handle(self, *args, **kwargs):
        Group.objects.get_or_create(name='Moderators')
        self.stdout.write(self.style.SUCCESS('������ "����������" �������'))
