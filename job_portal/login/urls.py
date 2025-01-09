from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/register/', views.user_register, name='register'),
    path('accounts/login/', views.login_view, name='login'),
    path('logout/', views.logoutview, name='logout'),
    path('testing/<int:pk>/',views.apply,name='apply'),

    #message URL
    path('api/inbox/<int:user_id>/', views.MyInbox.as_view(), name='inbox'),
    path('api/messages/<int:sender_id>/<int:receiver_id>/', views.GetMessage.as_view(), name='get_messages'),
    path('profiledetails/<int:pk>/',views.ProfileDetails.as_view()),
    path('searchuser/<username>/',views.SearchUser.as_view(), name='searchuser'),   
    path('messages/', views.MessageListCreateView.as_view(), name='message-list-create'),
    path('messages/<int:pk>/', views.MessageRetrieveUpdateDestroyView.as_view(), name='message-detail'),
    path('messagespage/', views.messagePage, name='messages'),
    path('api/messages/send/', views.SendMessage.as_view(), name='send_message'),


    # path('profile/', views.profile_view, name='profile_view'),  # Ensure this line is present


    # path('chat/<int:other_user_id>/', views.chat_view, name='chat_view'),
    # path('api/users/', views.UserListView.as_view(), name='user-list'),
    # path('api/messages/', views.get_messages, name='get_messages'),
    # path('chat/<int:other_user_id>/', views.chat_view, name='chat_view'),
    # ... other URL patterns ...

    # test--------->

    


    # ----------->




    path('create-job/',views.jobVacanciesViews,name='create-job'),
    path('messagepage/',views.messagePage,name='messagepage'),
    path('messages/', views.messagePage, name='messages'),
    path('job-listings/',views.job_listings,name='job_listings')

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)