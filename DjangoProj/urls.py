from django.urls import path,include
from django.contrib import admin
from molbank import views
from molbank.urls import urlpatterns as molbank_urls
urlpatterns = [
	path('admin/', admin.site.urls),
	path('molbank/',include(molbank_urls)),
]

