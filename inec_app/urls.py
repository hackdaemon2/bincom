"""inec URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from . import views

app_name = 'inec_app'
urlpatterns = [
    # general view url mapping
    path('', views.IndexView.as_view(), name = views.IndexView.name),
    path('question1', views.Question1View.as_view(), name = views.Question1View.name),
    path('question1-result/<int:pk>', views.Question1ResultView.as_view(), name = views.Question1ResultView.name),
    path('question2', views.Question2View.as_view(), name = views.Question2View.name),
    path('question3', views.Question3View.as_view(), name = views.Question3View.name),
    path('search', views.PollingUnitSearchView.as_view(), name = views.PollingUnitSearchView.name),
    path('ajax/load_lga', views.load_lga, name = 'ajax_load_lga'),
    path('ajax/pu/sum', views.get_sum, name = 'ajax_sum')
]
