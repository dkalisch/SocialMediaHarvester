from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    #------ HOME
    url(r'^$', 'SocialMediaHarvester.database.views.home_view', name='home'),
    
    #------ Query View
    url(r'^queries/$', 'SocialMediaHarvester.database.views.query_view', name='query_view'),
    
    #------ Configure Harvesters
    url(r'configuration/$','SocialMediaHarvester.database.views.configuration_view', name='configuration_view'),
    
    #------ UPLOAD HARVESTER
    url(r'^uploadHarvester/$', 'SocialMediaHarvester.database.views.uploadHarvester_view', name='uploadHarvester_view'),
    
    #------ LOGIN/LOGOUT/PERMISSION_DENIED
    url(r'^accounts/login/$',  'SocialMediaHarvester.database.views.login_view',name='login_view'),
    url(r'^accounts/logout/$', 'SocialMediaHarvester.database.views.logout_view', name='logout_view'),

    #------ CHANGE PASSWORD
    url(r'^accounts/password/$', 'SocialMediaHarvester.database.views.password_view', name='password_view'),
                       
    #------ ADMIN
    url(r'^admin/', include(admin.site.urls)),
)

#add the static links to the urlpattern for static serves
urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
urlpatterns+=url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
