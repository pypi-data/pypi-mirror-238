from django.urls import path

from spruce_ui import views

urlpatterns = [
    path('login/', views.login_, name='login'),
    path('logout/', views.logout_, name='logout'),
    path('workplace/', views.workplace, name='workplace'),
    path('console/', views.console, name='console'),
    path('404/', views.custom_404, name='custom_404'),
    path('403/', views.custom_403, name='custom_403'),
    path('500/', views.custom_500, name='custom_500'),
    path('success/', views.success, name='success'),
    path('info/', views.info, name='info'),
    path('fail/', views.fail, name='fail'),
    path('comp/form/basic/', views.basic, name='basic'),
    path('account/', views.account, name='account'),
    path('system/', views.system, name='system'),
]
