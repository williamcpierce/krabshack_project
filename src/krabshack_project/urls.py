from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path


urlpatterns = [
    path('', include('site_app.urls'), name='home'),
    path('admin/', admin.site.urls),
    path('data/', include('data_app.urls'), name='data'),
    path('esi/', include('esi_app.urls'), name='esi'),
    path('fit/', include('fit_app.urls'), name='fit'),
    path('services/', include('site_app.urls'), name='site'),
    url(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^oauth/', include('social_django.urls', namespace='social'))
]


# Admin site personalization
admin.site.site_header = 'Krab Shack Site Admin'
admin.site.site_title = 'Krab Shack Site Admin Portal'
admin.site.index_title = 'Welcome to Krab Shack Site Admin Portal'
