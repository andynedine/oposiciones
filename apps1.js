import tema1 from './tema1.js';

const temas = { tema1 }; // Agrega más temas si es necesario

const startButton = document.getElementById('start');
const temaSelector = document.getElementById('tema');
const quizSection = document.getElementById('quiz');
const questionElement = document.getElementById('question');
const optionsElement = document.getElementById('options');
let currentTema = [];
let currentQuestionIndex = 0;

startButton.addEventListener('click', () => {
    console.log("Botón pulsado"); // Debug
    const selectedTema = temaSelector.value;
    console.log("Tema seleccionado:", selectedTema); // Debug

    currentTema = selectedTema === 'random' ? getRandomQuestions() : temas[selectedTema];
    currentQuestionIndex = 0;

    quizSection.classList.remove('hidden'); // Mostrar la sección del test
    showNextQuestion();
});

function showNextQuestion() {
    const currentQuestion = currentTema[currentQuestionIndex];
    questionElement.textContent = currentQuestion.pregunta;
    optionsElement.innerHTML = '';

    currentQuestion.opciones.forEach(opcion => {
        const li = document.createElement('li');
        li.textContent = opcion;
        li.addEventListener('click', () => checkAnswer(opcion, currentQuestion.respuesta));
        optionsElement.appendChild(li);
    });
}

function checkAnswer(selected, correct) {
    if (selected === correct) {
        console.log("Respuesta correcta");
        currentQuestionIndex++;
        if (currentQuestionIndex < currentTema.length) showNextQuestion();
    } else {
        console.log("Respuesta incorrecta");
    }
}

function getRandomQuestions() {
    const allQuestions = Object.values(temas).flat();
    return allQuestions.sort(() => Math.random() - 0.5).slice(0, 10);
}
