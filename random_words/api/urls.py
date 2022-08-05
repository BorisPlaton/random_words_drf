from rest_framework import routers

from api.views import WordsViewSet


router = routers.SimpleRouter()
router.register('words', WordsViewSet, basename='words')
urlpatterns = router.urls
