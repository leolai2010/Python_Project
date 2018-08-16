from django.conf.urls import url
from . import views           
urlpatterns = [
    url(r'^$', views.index),  
    url(r'^registration$', views.registration),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^dashboard$', views.dashboard),
    url(r'^ailmentherb/(?P<ailmentid>\d+)$', views.ailmentherb),
    url(r'^allherbs$', views.allherbs),
    url(r'^consult$', views.consult),
    url(r'^addJob$', views.addJob),
    url(r'^addJobfunction$', views.addJobfunction),
    url(r'^addSol/(?P<number>\d+)$', views.addSol),
    url(r'^addSolfunction$', views.addSolfunction),
    url(r'^editJob/(?P<number>\d+)$', views.editJob),
    url(r'^editJobfunction$', views.editJobfunction),
    url(r'^editSol/(?P<number>\d+)$', views.editSol),
    url(r'^editSolfunction$', views.editSolfunction),
    url(r'^destroy/(?P<number>\d+)$', views.destroy),
    url(r'^deletesol/(?P<number>\d+)$', views.deletesol),
    url(r'^deletecart/(?P<number>\d+)$', views.deletecart),
    url(r'^cart$', views.cart),
    url(r'^addcart$', views.addcart),
    url(r'^checkout$', views.checkout),
    url(r'^about$', views.about),
    url(r'^contact$', views.contact)
]