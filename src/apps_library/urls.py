from django.urls import path

from . import views
from .apps import AppsLibraryConfig

app_name = AppsLibraryConfig.name
urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path(
        "deployments/<selected_environment>/",
        views.DeploymentsListView.as_view(),
        name="deployments-list",
    ),
]
