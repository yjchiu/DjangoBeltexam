from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^create$', views.create),
    url(r'^login_process$', views.login_process),
    url(r'^dashboard$', views.showall),
    url(r'^wish_items/(?P<item_id>\d+)$', views.show),
    url(r'^delete/(?P<item_id>\d+)$', views.delete),
    url(r'^add_to_wishlist/(?P<item_id>\d+)$', views.addtowishlist),
    url(r'^remove_from_wishlist/(?P<item_id>\d+)$', views.removefromwishlist),
    url(r'^wish_items/create$', views.add),
    url(r'^items/create$', views.additem),
    url(r'^logout$', views.logoff),
]