import json
from django.shortcuts import render, redirect, get_object_or_404
from .models import FlashCard, Card
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth import logout
from .models import FlashCard
from .forms import SignUpForm, FlashCardForm, FlashCardFormUpdate, CardUpdateForm
from random import shuffle
from django.contrib.auth.decorators import login_required


def dangnhap(request):
    return render(request, 'study/dangnhap.html')

class Login_SignUpClass(View):
    def get(self, request):
        form_signup = SignUpForm()
        return render(request, 'study/dangnhap.html', {'form_signup': form_signup})
    def post(self, request):
        if 'username' in request.POST:
            form_signup = SignUpForm(request.POST)
            if form_signup.is_valid():
                user = form_signup.save()
                login(request, user)
                print("dang ky thanh cong")
                return redirect('user:hoso')
            else:
                form_signup = SignUpForm()
                print("dang ky khong thanh cong")
                request.POST = {}
                messages.error(request, 'Thông tin đăng ký không đúng', extra_tags='signup')
                return self.get(request)
        else:    
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                print("dang nhap thanh cong")
                return trangchu(request)
            else:
                print("dang nhap khong thanh cong")
                request.POST = {}
                messages.error(request, 'Địa chỉ email hoặc mật khẩu không đúng', extra_tags='login')
                return self.get(request)



def trangchu(request):
    if request.user.is_authenticated:
        print("da dang nhap")
        flashcard_recent = FlashCard.objects.all().order_by('-time_update')[:12]
        context = {'flashcard_data_recent': flashcard_recent, 'user_login': request.user}
    else:
        print("chua dang nhap")
        context = {'user_login': None, 'flashcard_data_recent': None}
    
    return render(request, 'study/trangchu.html', context)

def logout_view(request):
    logout(request)
    return redirect('study:dangnhap')

def study_flashcard_view(request, flashcard_id):
    flashcard = get_object_or_404(FlashCard, id=flashcard_id)
    cards = flashcard.card_set.all()
    context = {
        'flashcard': flashcard,
        'cards': cards,
        'user_login': request.user,
        'cards_order': cards,
        'isSortABC': False,
        'isShuffle': False
    }
    return render(request, 'study/flashcard.html', context)

def sort_flashcard(request, sort):
    if sort == 'alphabet':
        flashcard = FlashCard.objects.order_by('title')
    elif sort == 'newest':
        flashcard = FlashCard.objects.order_by('-created_at')
    elif sort == 'oldest':
        flashcard = FlashCard.objects.order_by('created_at')
    else:
        flashcard = FlashCard.objects.all()
    context = {'flashcard_data': flashcard, 'user_login': request.user}
    return render(request, 'study/trangchu.html', context)

def sort_tuvung_ABC(request, flashcard_id):
    flashcard = get_object_or_404(FlashCard, id=flashcard_id)
    cards = flashcard.card_set.all()
    cards_order = flashcard.card_set.order_by('word')
    context = {
        'flashcard': flashcard,
        'cards': cards,
        'user_login': request.user,
        'cards_order': cards_order,
        'isSortABC': True,
        'isShuffle': False
    }
    return render(request, 'study/flashcard.html', context)

def shuffle_card_show(request, flashcard_id):
    flashcard = get_object_or_404(FlashCard, id=flashcard_id)
    cards = flashcard.card_set.all()
    cards_list = list(cards)
    shuffle(cards_list)
    context = {
        'flashcard': flashcard,
        'cards': cards_list,
        'user_login': request.user,
        'cards_order': cards,
        'isSortABC': False,
        'isShuffle': True
    } 
    
    return render(request, 'study/flashcard.html', context)

def shuffle_card_show_sort_ABC(request, flashcard_id):
    flashcard = get_object_or_404(FlashCard, id=flashcard_id)
    cards = flashcard.card_set.all()
    cards_order = flashcard.card_set.order_by('word')
    cards_list = list(cards)
    shuffle(cards_list)
    context = {
        'flashcard': flashcard,
        'cards': cards_list,
        'user_login': request.user,
        'cards_order': cards_order,
        'isSortABC': True,
        'isShuffle': True
    } 
    
    return render(request, 'study/flashcard.html', context)

def study_theghinho(request, flashcard_id):
    flashcard = get_object_or_404(FlashCard, id=flashcard_id)
    cards = flashcard.card_set.all()
    context = {
        'flashcard': flashcard,
        'cards': cards,
        'user_login': request.user,
    } 
    return render(request, 'study/mode/mode_study.html', context)

import random
def study_quiz(request, flashcard_id):
    flashcard = get_object_or_404(FlashCard, id=flashcard_id)
    cards_quiz = flashcard.card_set.all().order_by('?')[:10]

    question_ids = [card.id for card in cards_quiz]
    other_cards = Card.objects.filter(flash_card=flashcard).exclude(id__in=question_ids)
    questions = []
    for card in cards_quiz:
        question = {
            'word': card.word,
            'answers': [card.meaning],
            'correct_answer_index': 0
        }
        if len(other_cards) >= 3:
            # Lấy ngẫu nhiên 3 đáp án khác từ danh sách other_cards
            three_other_cards = random.sample(list(other_cards), 3)
            question['answers'].extend([other_answer.meaning for other_answer in three_other_cards])
        else:
            # Nếu số lượng other_cards không đủ, lấy tất cả các đáp án khác từ danh sách other_cards
            question['answers'].extend([other_card.meaning for other_card in other_cards])

        # Xáo trộn thứ tự của các đáp án
        random.shuffle(question['answers'])

        # Update correct_answer_index based on shuffled answers
        question['correct_answer_index'] = question['answers'].index(card.meaning)

        # Lưu câu hỏi vào danh sách các câu hỏi
        questions.append(question)
    context = {
        'flashcard': flashcard,
        'user_login': request.user,
        'questions': questions,
    } 
    return render(request, 'study/mode/mode_quiz.html', context)

def study_kiemtra(request, flashcard_id):
    flashcard = get_object_or_404(FlashCard, id=flashcard_id)
    cards_test_yesno = flashcard.card_set.all().order_by('?')[:10]
    question_yesno_ids = [card.id for card in cards_test_yesno]
    cards_test_quiz = Card.objects.filter(flash_card=flashcard).exclude(id__in=question_yesno_ids).order_by('?')[:10]
    
    question_ids = question_yesno_ids + [card.id for card in cards_test_quiz]
    other_cards = Card.objects.filter(flash_card=flashcard).exclude(id__in=question_ids)
    questions_yesno = []
    questions_quiz = []

    
    for card in cards_test_yesno:
        other_card_yn = random.sample(list(other_cards), 1)[0]
        stat_queston = random.choice(["yes", "no"])
        if stat_queston == "no":
            question = {
                'word': card.word,
                'meaning': other_card_yn.meaning,
                'correct_answer': 'no',
            }            
            questions_yesno.append(question)
        else:
            question = {
                'word': card.word,
                'meaning': card.meaning,
                'correct_answer': 'yes',
            }
            questions_yesno.append(question)
    
    for card in cards_test_quiz:
        question = {
            'word': card.word,
            'answers': [card.meaning],
            'correct_answer_index': 0
        }
        if len(other_cards) >= 3:
            # Lấy ngẫu nhiên 3 đáp án khác từ danh sách other_cards
            three_other_cards = random.sample(list(other_cards), 3)
            question['answers'].extend([other_answer.meaning for other_answer in three_other_cards])
        else:
            # Nếu số lượng other_cards không đủ, lấy tất cả các đáp án khác từ danh sách other_cards
            question['answers'].extend([other_card.meaning for other_card in other_cards])

        # Xáo trộn thứ tự của các đáp án
        random.shuffle(question['answers'])

        # Update correct_answer_index based on shuffled answers
        question['correct_answer_index'] = question['answers'].index(card.meaning)
        
        # Lưu câu hỏi vào danh sách các câu hỏi
        questions_quiz.append(question)


    context = {
        'flashcard': flashcard,
        'user_login': request.user,
        'questions_yesno': questions_yesno,
        'questions_quiz': questions_quiz,
    } 
    return render(request, 'study/mode/mode_test.html', context)

def study_shuffle(request, flashcard_id):
    flashcard = get_object_or_404(FlashCard, id=flashcard_id)
    cards = flashcard.card_set.all()
    cards_list = list(cards)
    shuffle(cards_list)
    context = {
        'flashcard': flashcard,
        'cards': cards_list,
        'user_login': request.user,
        'isShuffle': True
    } 
    return render(request, 'study/mode/mode_study.html', context)

def my_flashcard(request):
    user_flashcards = FlashCard.objects.filter(user=request.user)
    if request.method == 'POST':
        flashcard_form = FlashCardForm(request.POST, user=request.user)
        if flashcard_form.is_valid():
            flashcard = flashcard_form.save(commit=False)
            flashcard.user = request.user  # Gán người dùng hiện tại cho trường user
            flashcard.save()
            return redirect('study:them-cards-flashcard', flashcard_id=flashcard.id)
    else:
        flashcard_form = FlashCardForm(user=request.user)
    if request.method == 'POST' and 'flashcard_id_delete' in request.POST:
        flashcard_id = request.POST.get('flashcard_id_delete')
        flashcard = FlashCard.objects.filter(id=flashcard_id)
        flashcard.delete()
        print("Xóa thành công flashcard", flashcard_id)
    context = {
        'user_login': request.user,
        'my_flashcards': user_flashcards,
        'flashcard_form': flashcard_form,
    }

    return render(request, 'study/my_flashcard.html', context)

def create_cards_for_flashcard(request, flashcard_id):
    flashcard = get_object_or_404(FlashCard, id=flashcard_id)
    if request.method == 'POST':
        card_data_word = request.POST.getlist("card_data['word']")
        card_data_meaning = request.POST.getlist("card_data['meaning']")
        cards = []
        for word, meaning in zip(card_data_word, card_data_meaning):
            card = Card(word=word, meaning=meaning, flash_card=flashcard)
            cards.append(card)

        Card.objects.bulk_create(cards)  # Tạo các Card một cách tối ưu

            # Tiếp tục xử lý hoặc redirect đến trang khác
        return redirect('study:thenho', flashcard_id=flashcard_id)

    context = {
        'flashcard': flashcard,
        'user_login': request.user,
    }
    return render(request, 'study/chucnangcoban/create_cards.html', context)

def edit_flashcard(request, flashcard_id):
    user_flashcard = get_object_or_404(FlashCard, id=flashcard_id)
    word_count = user_flashcard.word_count()
    word_range = range(word_count)
    cards = user_flashcard.card_set.all()
    card_forms = []
    if request.method == 'POST':
        flashcard_form = FlashCardFormUpdate(request.POST, instance=user_flashcard)
        if flashcard_form.is_valid():
            flashcard_form.save()
        
        card_data_word = request.POST.getlist('word')
        card_data_meaning = request.POST.getlist('meaning')

        # Xử lý xóa card
        card_ids = request.POST.getlist('card_id_delete')  # Lấy danh sách ID của các card
        cards_to_delete = Card.objects.filter(id__in=card_ids)  # Lấy các card cần xóa
        cards_to_delete.delete()  # Xóa các card

        for i in range(len(card_data_word)):
            if i < len(cards):
                card_data = {
                    'word': card_data_word[i],
                    'meaning': card_data_meaning[i]
                }
                # Cập nhật card hiện có
                card_form = CardUpdateForm(
                    data=card_data,
                    instance=cards[i]
                )
            else:
                # Tạo card mới
                Card.objects.create(word=card_data_word[i], meaning=card_data_meaning[i], flash_card=user_flashcard)
            card_forms.append(card_form)

        if all(card_form.is_valid() for card_form in card_forms):
            for card_form in card_forms:
                card_form.save()
            print('update success')
            return redirect('study:thenho', flashcard_id=flashcard_id)
    else:
        flashcard_form = FlashCardFormUpdate(instance=user_flashcard)
        for i, card in enumerate(cards, start=1):
            card_form = CardUpdateForm(instance=card)
            card_forms.append(card_form)
    context = {
        'word_range': word_range,
        'flashcard_form_edit': flashcard_form,
        'card_forms_edit': card_forms,
        'user_flashcard': user_flashcard,
        'my_cards':cards,
        'user_login': request.user,
    }
    return render(request, 'study/chucnangcoban/edit_flashcard.html', context)


def edit_clone_flashcard(request, flashcard_id):
    user_flashcard = get_object_or_404(FlashCard, id=flashcard_id)
    word_count = user_flashcard.word_count()
    word_range = range(word_count)
    cards = user_flashcard.card_set.all()
    card_forms = []    
    if request.method == 'POST':
        # Clone FlashCard
        new_flashcard = FlashCard.objects.create(
            user=request.user,
            title=f"Clone of {user_flashcard.title}",
            time_create=user_flashcard.time_create,
            time_update=user_flashcard.time_update
        )
        print(f"{new_flashcard}"+" cloned successfully")
        # Clone Cards
        cards = user_flashcard.card_set.all()
        for card in cards:
            Card.objects.create(
                word=card.word,
                meaning=card.meaning,
                flash_card=new_flashcard
            )

        # Edit clone flashcard
        flashcard_form = FlashCardFormUpdate(request.POST, instance=new_flashcard)
        if flashcard_form.is_valid():
            flashcard_form.save()
        
        card_data_word = request.POST.getlist('word')
        card_data_meaning = request.POST.getlist('meaning')

        # Xử lý xóa card
        card_ids = request.POST.getlist('card_id_delete')  # Lấy danh sách ID của các card
        cards_to_delete = Card.objects.filter(id__in=card_ids)  # Lấy các card cần xóa
        cards_to_delete.delete()  # Xóa các card

        for i in range(len(card_data_word)):
            if i < len(cards):
                card_data = {
                    'word': card_data_word[i],
                    'meaning': card_data_meaning[i]
                }
                # Cập nhật card hiện có
                card_form = CardUpdateForm(
                    data=card_data,
                    instance=cards[i]
                )
            else:
                # Tạo card mới
                Card.objects.create(word=card_data_word[i], meaning=card_data_meaning[i], flash_card=new_flashcard)
            card_forms.append(card_form)

        if all(card_form.is_valid() for card_form in card_forms):
            for card_form in card_forms:
                card_form.save()
            print('update success clone flashcard')
            return redirect('study:thenho', flashcard_id=new_flashcard.id)
    else:
        flashcard_form = FlashCardFormUpdate(instance=user_flashcard)
        for i, card in enumerate(cards, start=1):
            card_form = CardUpdateForm(instance=card)
            card_forms.append(card_form)
    context = {
        'word_range': word_range,
        'flashcard_form_edit': flashcard_form,
        'card_forms_edit': card_forms,
        'user_flashcard': user_flashcard,
        'my_cards':cards,
        'user_login': request.user,
    }
    return render(request, 'study/chucnangcoban/edit_flashcard.html', context)

def search_flashcards(request):
    if request.method == 'GET':
        search_text = request.GET.get('search_text')
        flashcards_search = FlashCard.objects.filter(title__icontains=search_text)
        context = {
            'flashcards_search': flashcards_search,
            'user_login': request.user,
            'search_text': search_text,
        }
        return render(request, 'study/chucnangcoban/flashcards_search.html', context)
    else:
        return render(request, 'study/chucnangcoban/flashcards_search.html')
    