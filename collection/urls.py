from django.urls import path
from collection.views import CreateCollectionView, RetrieveCollectionView, UpdateCitizenView

urlpatterns = [
    path('import', CreateCollectionView.as_view()),
    path('imports/<int:pk>/citizens', RetrieveCollectionView.as_view()),
    path('imports/<int:col_id>/citizens/<int:pk>', UpdateCitizenView.as_view()),
]