from django.urls import path, include
from . import views
urlpatterns = [
    path('index', views.index, name='index'),
    path('login', views.handlelogin, name='handlelogin'),
    path('logout', views.handlelogout, name='handlelogout'),
    path('', views.handlesignup, name='handlesignup'),
    path('Adm', views.Adm, name='Adm'),
    path('insert', views.insertData, name='insertData'),
    path('update/<id>', views.updateDate, name='updateData'),
    path('delete/<id>', views.deleteData, name='deleteData'),

]
