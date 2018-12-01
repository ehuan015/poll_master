from django.urls import path
from . import views

app_name="polls"
urlpatterns = [
    path('list/', views.polls_list, name="list"),
    path('details/<int:poll_id>/', views.poll_detail, name='detail'),
    path('details/<int:poll_id>/vote/', views.poll_vote, name='vote'),
]
