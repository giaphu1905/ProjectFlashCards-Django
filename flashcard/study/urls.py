from django.urls import path
from . import views
from django.views.generic import RedirectView

app_name = "study"

urlpatterns = [
    path("login/", views.Login_SignUpClass.as_view(), name="dangnhap"),
    path("", RedirectView.as_view(url='login/', permanent=True)),
    path("logout/", views.logout_view, name="dangxuat"),

    path("home/", views.trangchu, name="trangchu"),
    path("my-flashcard", views.my_flashcard, name="my-flashcard"),
    path("flashcards-search", views.search_flashcards, name="timkiem-flashcard"),
    path("my-flashcard/<int:flashcard_id>/add-cards", views.create_cards_for_flashcard, name="them-cards-flashcard"),
    path("my-flashcard/<int:flashcard_id>/edit", views.edit_flashcard, name="sua-flashcard"),
    path("my-flashcard/<int:flashcard_id>/edit-clone", views.edit_clone_flashcard, name="sua-clone-flashcard"),


    path("flashcard/<int:flashcard_id>/", views.study_flashcard_view, name="thenho"),
    path("flashcard/<int:flashcard_id>/shuffle", views.shuffle_card_show, name="tron-the"),

    path("flashcard/<int:flashcard_id>/sort-abc", views.sort_tuvung_ABC, name="sapxep-tuvungABC"),
    path("flashcard/<int:flashcard_id>/sort-abc/shuffle", views.shuffle_card_show_sort_ABC, name="sapxep-tuvungABC-tron-the"),

    path("flashcard/<int:flashcard_id>/study", views.study_theghinho, name="the-ghi-nho"),
    path("flashcard/<int:flashcard_id>/study/shuffle", views.study_shuffle, name="the-ghi-nho-tron-the"),
    path("flashcard/<int:flashcard_id>/quiz", views.study_quiz, name="quiz"),
    path("flashcard/<int:flashcard_id>/test", views.study_kiemtra, name="kiem-tra"),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)