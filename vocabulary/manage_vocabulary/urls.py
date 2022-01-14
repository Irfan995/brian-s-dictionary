from django.urls import path
from manage_vocabulary.views import VocabularyListView, WordInformation, WordList


app_name = 'manage_vocabulary'
urlpatterns = [
    path('vocabulary-list/', VocabularyListView.as_view(), name='vocabulary-list'),
    path('word-list/', WordList.as_view(), name='word-list'),
    path('word-information/', WordInformation.as_view(), name='word-information')
]