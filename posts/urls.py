from rest_framework import routers

from posts.views import PostView

app_name = 'posts'

router = routers.SimpleRouter()
router.register(r'', PostView)

urlpatterns = [

]

urlpatterns += router.urls