from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static





urlpatterns = [
    path('accounts/profile/', views.profile, name='profile'),
    path('update-profile-pic/', views.update_profile_pic, name='update_profile_pic'),
    path('backtopage/',views.BackToPage,name='backtopage'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
