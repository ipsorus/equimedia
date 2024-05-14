# -*- coding: utf-8 -*-
import os
import sys

sys.path.insert(0, '/home/i/ipsoru68/ipsoru68.beget.tech/equimedia')
sys.path.insert(1, '/home/i/ipsoru68/ipsoru68.beget.tech/djangoenv/lib/python3.10/site-package')
os.environ['DJANGO_SETTINGS_MODULE'] = 'equimedia.settings'
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
