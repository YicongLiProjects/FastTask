from django.urls import path
from application import views
urlpatterns = [
    path('', views.index, name='index'),
    path('signup/submit/', views.signup, name='signup_submit'),
    path('signup/', views.signup_view, name='signup_view'),
    path('login/submit/', views.login_user, name='login_submit'),
    path('login/', views.login_view, name='login_view'),
    path('get_profile/', views.get_profile, name='get_profile'),
    path('app/', views.app_view, name='app_view'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('get_tasks/', views.get_tasks, name='get_tasks'),
    path('add_task/', views.add_task, name='add_task'),
    path('remove_task/', views.remove_task, name='remove_task'),
    path('edit_task/', views.edit_task, name='edit_task'),
    path('account_info/', views.account_info_view, name='account_info_view'),
    path('help/', views.help_view, name='help_view'),
    path('password_recovery/', views.password_reset_email_view, name='password_reset_email_view')
]
