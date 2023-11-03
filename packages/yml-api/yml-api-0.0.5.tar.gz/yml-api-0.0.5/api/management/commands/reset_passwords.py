# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.first()
        user.set_password(settings.DEFAULT_PASSWORD(user))
        User.objects.update(password=user.password)
