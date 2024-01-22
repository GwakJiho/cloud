from django.urls import path, include
from . import views
from .views import DocumentView, UserView, DocumentFileViewSet, PathViewSet

#url 라우터
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'document', DocumentView)
router.register(r'user', UserView)
router.register(r'file', DocumentFileViewSet)
router.register(r'path', PathViewSet)

urlpatterns = [
    #path('hello/', views.hello_world),
    #path('document/', DocumentView.as_view(), name='document'),
    path('', include(router.urls)),
    path('documents/', views.document_upload_view)
]


#url pattern router 사용