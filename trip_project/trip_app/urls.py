from django .urls import path
from .views import *
from . import views

urlpatterns = [
    
    path('create/',TripCreateView.as_view(),name='create'),
    path('detail/<int:pk>/',TripDetail.as_view(),name='detail'),
    path('update/<int:pk>/',TripUpdateView.as_view(),name='update'),
    path('delete/<int:pk>/',TripDelete.as_view(),name='delete'),
    path('search_api/<str:place_name>/', TripSearchViewset.as_view(), name='search'),

    path('',views.index,name='index'),
    path('create_trip/',views.create_trip,name='create_trip'),
    path('update_detail/<int:id>/',views.update_detail,name="update_detail"),
    path('update_trip/<int:id>/',views.update_trip,name='update_trip'),
    path('trip_fetch/<int:id>/',views.trip_fetch,name='trip_fetch'),
    path('trip_delete/<int:id>/',views.trip_delete,name='trip_delete'),
    path('trip_search/',views.trip_search,name='trip_search')
    
]

