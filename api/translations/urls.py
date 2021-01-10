""" Tranlations urls. """

# Django REST framework
from rest_framework.routers import DefaultRouter

# views
from api.translations.views import TranslateView

router = DefaultRouter(trailing_slash=False)
router.register(r'translations', TranslateView, basename='translations')
urlpatterns = router.urls
