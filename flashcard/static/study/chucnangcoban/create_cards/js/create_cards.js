window.addEventListener('DOMContentLoaded', function() {
    var flashcardTitle = document.querySelector('.titleDisplay h2').innerText;
    document.documentElement.style.setProperty('--title-length', flashcardTitle.length);

    const addCardButton = document.getElementById('add-card-button');
    const cardDataContainer = document.getElementById('card-data-container');
    var counter = 1;

    addCardButton.addEventListener('click', function () {
        counter += 1;
        const currentCounter = counter;
        const cardData = document.createElement('div');
        cardData.classList.add('TermContent-inner');
        cardData.innerHTML = `
        <div class="TermContent-inner">
            <div class="StudiableItemToolbar d-flex justify-content-between">
            <div id="counter-card" class="d-flex">
                <h5 style="padding-left: 10px; color: #868789;">${currentCounter}</h5>
            </div>
            <div class="d-flex gap-3">
                <i class="fas fa-grip-lines"></i>
                <i class="far fa-trash-alt"></i>
            </div>
            </div>
            <div class="TermContent-inner-padding">
            <div class="TermContent-sides">
                <div class="TermContent-sideWrap">
                <div class="TermContent-side TermContent-side--word">
                    <div class="WordSide">
                    <input type="text" name="card_data['word']" placeholder="Từ vựng" required />
                    <div class="underlineInput"></div>
                    </div>
                </div>
                <div class="TermContent-side TermContent-side--definition">
                    <div class="DefinitionSide">
                    <input type="text" name="card_data['meaning']" placeholder="Định nghĩa" required />
                    <div class="underlineInput"></div>
                    </div>
                </div>
                </div>
            </div>
            </div>
        </div>
        `;
        cardDataContainer.appendChild(cardData);    
    });
    });

    window.addEventListener('click', function() {
    // Lấy danh sách tất cả các thẻ card đã được thêm vào
    var allCardData = document.querySelectorAll('.TermContent-inner');
        
    // Duyệt qua từng thẻ card và thêm sự kiện focus và blur cho các ô input
    allCardData.forEach(function(cardData) {
        var wordInput = cardData.querySelector('.TermContent-side--word input');
        var definitionInput = cardData.querySelector('.TermContent-side--definition input');
        var wordUnderline = cardData.querySelector('.TermContent-side--word .underlineInput');
        var definitionUnderline = cardData.querySelector('.TermContent-side--definition .underlineInput');

        wordInput.addEventListener('focus', function() {
        wordUnderline.style.backgroundColor = '#09aa59';
        });

        wordInput.addEventListener('blur', function() {
        wordUnderline.style.backgroundColor = '';
        });

        definitionInput.addEventListener('focus', function() {
        definitionUnderline.style.backgroundColor = '#09aa59';
        });

        definitionInput.addEventListener('blur', function() {
        definitionUnderline.style.backgroundColor = '';
        });
    });
});