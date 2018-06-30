from django.urls import path

from . import views

app_name = 'tasks'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('closed/', views.ClosedTasksView.as_view(), name='closedTasks'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('create/', views.NewTaskView.as_view(), name='create'),
    path('newlabel/', views.NewLabelView.as_view(), name='newlabel'),
    path('<int:pk>/edit/', views.EditTaskView.as_view(), name='edit'),
    path('<int:task_id>/finish/', views.finishTask, name='finishTask'),
    path('<int:task_id>/reopen/', views.finishTask, name='reopen'),
    path('impressum/', views.ImpressumView.as_view(), name='impressum'),
    path('protocolparse/', views.ProtocolParse.as_view(), name='protocolParse'),
]
