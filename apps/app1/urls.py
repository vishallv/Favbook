from django.conf.urls import url
from . import views

urlpatterns =[
    url(r'^$',views.index),
    url(r'^registeruser$',views.registerUser),
    url(r'^books$',views.books),
    url(r'^show/(?P<uid>\d+)$',views.showBook),
    url(r'^edit/(?P<uid>\d+)$',views.editBook),
    url(r'^loginuser$',views.loginUser),
    url(r'^addbook$',views.addBook),
    url(r'^booksverify/(?P<uid>\d+)$',views.verify),
    url(r'^makeedit/(?P<uid>\d+)$',views.makeEdit),
    url(r'^addtofav/(?P<uid>\d+)$',views.addFavorite)
    
    
    
    
    
    
    
]