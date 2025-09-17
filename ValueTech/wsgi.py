# ValueTech/wsgi.py
import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ValueTech.settings")

application = get_wsgi_application()
static_root = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'staticfiles')
application = WhiteNoise(application, root=static_root)
