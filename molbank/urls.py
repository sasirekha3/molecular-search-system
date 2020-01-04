from django.contrib import admin
from django.urls import path,re_path,include
from . import views

from django.conf import settings
from django.conf.urls.static import static


# from django.utils.functional import curry
# handler404 = 'molbank.views.my_custom_page_not_found_view'
# handler500 = 'mysite.views.my_custom_error_view'
# handler403 = 'mysite.views.my_custom_permission_denied_view'
# handler400 = 'mysite.views.my_custom_bad_request_view'


# handler404 = 'molbank.views.handler404'
# handler500 = 'molbank.views.handler500'

urlpatterns = [
    path('', views.home, name='home'),
    path('',views.loadhome,name='loadhome'),
    # path('molbank/<int:mol_id>/', views.detail),
    # path('molbank/',include('molbank.urls')),
    path('search',views.search_mol,name='search_mol'),
    path('index',views.index,name='index'),
    path('advancedSearch',views.advancedSearch, name='advancedSearch'),
    path('simpleSearch',views.simpleSearch, name='simpleSearch'),
    path('add_mols',views.add_mols, name='add_mols'),
    path('add',views.add, name='add'),
    path('login',views.loginHTML, name='login'),
    path('logout',views.logoutHTML,name='logoutHTML'),
    path('uploadCSV',views.uploadCSV,name='uploadCSV'),
    path('updateDB',views.updateDB,name='updateDB'),
    path('status',views.status_of_pending_files,name='status'),
    path('spectral_files',views.spectral_files,name='spectral_files'),
    path('report/<str:report>',views.report,name='report'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)