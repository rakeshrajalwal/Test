from django.conf.urls import patterns,url

from classic_models import views

urlpatterns = patterns('', 
                       url(r'^groups/',views.groups,name='groups'),
                       url(r'campaigns/',views.campaigns,name='campaigns'),
                       url(r'^view_schedule',views.view_schedule,name='view_schedule'),
                       url(r'^Dashboard',views.Dashboard,name='Dashboard'),
                       url(r'^$',views.home,name='home'),
                       ) 