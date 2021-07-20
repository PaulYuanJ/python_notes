"""notification_backend URL Configuration
fatal: refusing to merge unrelated histories
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import include, url, re_path
from django.urls import path
from django.views.static import serve
from django.conf.urls import include, url, re_path
from oncall_department.views import *
from rest_framework import routers
from rest_framework.documentation import include_docs_urls

router = routers.DefaultRouter(trailing_slash=False)
API_TITLE = 'Oncall API Documents'
API_DESCRIPTION = 'Oncall API Information'

router.register(r'department' , DepartmentViewSet)
router.register(r'employee' , EmployeeViewSet)

urlpatterns = [
    url('^oncall/list/', include_docs_urls(title=API_TITLE,
                                           description=API_DESCRIPTION,
                                           authentication_classes=[], permission_classes=[])),
    url('^oncall/', include(router.urls)),
]
from OncallSysManagement.settings import STATIC_ROOT

urlpatterns += [url(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT})]