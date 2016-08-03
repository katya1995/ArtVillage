from django.conf.urls import patterns, url
import views
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^about/$', views.about, name='about'),

                       # URLs for users' access to the website
                       url(r'^register/$', views.register, name='register'),
                       url(r'^login/$', views.user_login, name="login"),
                       url(r'^logout/$', views.user_logout, name="logout"),

                       # URLs for editing users' info
                       url(r'^profile/(?P<user>[-\w.]+)/$', views.profile, name='profile'),
                       url(r'^edit-details/', views.edit_details, name='edit_details'),
                       url(r'^password-change/$', auth_views.password_change,
                           {'template_name': 'ArtVillage/changepassword.html'}, name='userauth_password_change'),
                       url(r'^password-change-done/$', auth_views.password_change_done,
                           {'template_name': 'ArtVillage/changepassworddone.html'}, name='password_change_done'),
                       url(r'^edit-shipping-details/$', views.edit_shipping_details, name="edit_shipping_details"),

                       # Media URL
                       url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                           {'document_root': settings.MEDIA_ROOT, }),

                       # URLs for searching
                       url(r'^search/$', views.search, name='search'),
                       url(r'^suggest-art/$', views.suggest_art, name='suggest_art'),

                       # Filtering URLs
                       url(r'^apply_filtering/$', views.apply_filtering, name='apply_filtering'),

                       # URLs for each piece of art
                       url(r'^art/(?P<art_name_slug>[\w\-]+)/(?P<id>[0-9]+)/$', views.piece_of_art, name='art'),
                       url(r'^suggest_art/$', views.suggest_art, name='suggest_art'),
                       url(r'^goto/$', views.track_art, name='goto'),

                       # Pagination
                       url(r'^get_new_page/$', views.get_new_page, name='/get_new_page/'),

                       # Cart URLs
                       url(r'^cart/$', views.cart_detail, name='cart_detail'),
                       url(r'^add/(?P<product_id>\d+)/$', views.cart_add, name='cart_add'),
                       url(r'^remove/(?P<product_id>\d+)/$', views.cart_remove, name='cart_remove'),

                       # PayPal related pages
                       url(r'^cancel/$', views.cancel, name='cancel'),
                       url(r'^success/$', views.success, name='success'),
                       url(r'^ipn/$', views.ipn, name='ipn')
                       )

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'^media/(?P<path>.*)',
         'serve',
         {'document_root': settings.MEDIA_ROOT}), )
