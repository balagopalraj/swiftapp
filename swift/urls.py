from django.conf.urls import patterns, url

urlpatterns = patterns('swift.portal.views',
    # Examples:
    url(r'^$', 'portal_page', {'page': 'Home'}),
    url(r'^(Home|Login|Logout)/$', 'portal_page'),
    url(r'^LogMeIn/$', 'log_me_in'),
    url(r'^Files/(\w+)/$', 'show_files'),
    url(r'^Download/(.+?)/(.+?)/$', 'download_file'),
    url(r'^NewFile/$', 'upload_file'),
    url(r'^UploadFile/$', 'do_upload'),
)
