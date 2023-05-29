document.getElementById('btn-create-flsc').addEventListener('click', function() {
    $('#staticBackdrop').modal('show');
});

let selectedFlashcardId;
function closeModal() {
    
    document.getElementById('del-card-modal').style.display = 'none';
}

function openModal(flashcard_id) {
    selectedFlashcardId = flashcard_id;
    add_inputHidden_idcard_del(flashcard_id);
    document.getElementById('del-card-modal').style.display = 'block';
}

const my_flashcards = document.getElementById('delete-card-form');
function add_inputHidden_idcard_del(flashcard_id) {
    var hiddenInput = document.createElement('input');
    hiddenInput.type = 'hidden';
    hiddenInput.name = 'flashcard_id_delete';
    hiddenInput.value = flashcard_id;

    my_flashcards.appendChild(hiddenInput);
}