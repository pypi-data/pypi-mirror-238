from django.urls import path

from . import views

app_name = "secretsanta"

urlpatterns = [
    path("", views.index, name="index"),
    path("apply/<int:year>/", views.apply, name="apply"),
    path("mark_received/<int:year>/", views.mark_received, name="mark_received"),
    path("pairs/<int:year>/", views.pairs, name="pairs"),
    path("applications/<int:year>/", views.applications, name="applications"),
    path("generate_pairs/<int:year>/", views.queue_generate_pairs, name="generate_pairs"),
]
