from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("<str:lang>/", views.home_lang, name="home-lang"),
    path("<str:book>/<int:chapter>/<int:verse>/", views.verse_lang, name="verse"),
    path(
        "<str:book>/<int:chapter>/<int:verse>/<str:lang>/",
        views.verse_lang,
        name="verse-lang",
    ),
]
