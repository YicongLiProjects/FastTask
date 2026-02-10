from django.urls import path
from application import views
urlpatterns = [path('signup', views.signup, name='signup'),
                path('login', views.login_user, name='login'),
                path('get_profile', views.get_profile, name='get_profile'),
                path('update_profile', views.update_profile, name='update_profile'),
                path('get_task', views.get_task, name='get_task'),
                path('add_task', views.add_task, name='add_task'),
                path('remove_task', views.remove_task, name='remove_task'),
                path('edit_task', views.edit_task, name='edit_task')]
