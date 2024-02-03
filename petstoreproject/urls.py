"""petstoreproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from petstoreapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.register,name="register"),
    path('login/',views.loginuser,name="login"),
    path('logout',views.loginuser),
    path('footer',views.footer),
    path('about',views.about),
    path('contact',views.contact),
    path('index',views.indexpage),
    path("home",views.home),
    path("catfilter/<cv>",views.catfilter),
    path("sort/<sv>",views.sort),
    path('range',views.range),
    path("pdetails/<pid>",views.product_details),
    path('addtocart/<pid>',views.addtocart),
    path('viewcart',views.viewcart),
    path("remove/<cid>",views.remove),
    path("updateqty/<qv>/<cid>",views.updateqty),
    path('placeorder',views.placeorder),
    path("makepayment",views.makepayment),
    path('sendmail',views.sendusermail),
]

if settings.DEBUG:
  urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
