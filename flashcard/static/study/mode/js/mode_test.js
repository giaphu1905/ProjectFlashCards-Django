const yesnoContainer = document.getElementById("kiemtra-yesno");
const yesnoAnswerButtons = yesnoContainer.querySelectorAll(".boxContent");
yesnoAnswerButtons.forEach(function(button) {
    var isAnsweredCorrectly = false;
    button.addEventListener("click", function() {
        var questionNumber = this.parentNode.getAttribute('id').split('-')[1];
        this.classList.add("selected");

        if (button.id == "answer-yes-" + questionNumber) {
            var otherButton = document.getElementById("answer-no-"+ questionNumber);
        } else if (button.id == "answer-no-" + questionNumber) {
            var otherButton = document.getElementById("answer-yes-"+ questionNumber);
        }
        otherButton.classList.remove("selected");
    });
});

const quizContainer = document.getElementById("kiemtra-quiz");
const quizAnswerButtons = quizContainer.querySelectorAll(".boxContent");
quizAnswerButtons.forEach(function(button) {
    button.addEventListener('click', function() {
        if (!this.classList.contains('selected')) {
            // Lấy ID của nút đáp án được nhấn
            var answerId = this.parentNode.getAttribute('id');
            if (answerId) {
                var questionNumber = answerId.split('-')[2];

                var allBoxContents = document.querySelectorAll('#answer-quiz-' + questionNumber + ' .boxContent');
                for (var i = 0; i < allBoxContents.length; i++) {
                    if (allBoxContents[i].classList.contains('selected')) {
                        allBoxContents[i].classList.remove('selected');
                    }
                }
                this.classList.add('selected');


            }
        }
    });
});