import os, sys
sys.path.append('var/www/smh/html/SocialMediaHarvester')
os.environ['DJANGO_SETTINGS_MODULE']='SocialMediaHarvester.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
