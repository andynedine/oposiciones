// Importar todos los temas
import tema1 from './tema1.js';
import tema2 from './tema2.js';
import tema3 from './tema3.js';
import tema4 from './tema4.js';
import tema5 from './tema5.js';
import tema6 from './tema6.js';
import tema7 from './tema7.js';
import tema8 from './tema8.js';
import tema9 from './tema9.js';

// Almacenar los temas en un objeto para acceso dinámico
const temas = {
    1: tema1,
    2: tema2,
    3: tema3,
    4: tema4,
    5: tema5,
    6: tema6,
    7: tema7,
    8: tema8,
    9: tema9,
};

// Selección de elementos del DOM
const selectorTema = document.getElementById('selectorTema');
const startButton = document.getElementById('startButton');
const tiempoSelector = document.getElementById('tiempoSelector');
const numeroPreguntasInput = document.getElementById('numeroPreguntas');
const questionContainer = document.getElementById('questionContainer');
const temaElement = document.getElementById('temaActual');
const questionElement = document.getElementById('question');
const optionsContainer = document.getElementById('options');
const feedbackElement = document.getElementById('feedback');
const timerElement = document.getElementById('timer');
const capa_pregunta = document.getElementById('capa_pregunta');

// Variables de control
let preguntas = [];
let preguntaActual = null;
let temaActual = null;
let fallos = 0;
let aciertos = 0;
let falladoPreguntaActual = false;
let tiempoRestante = 0;
let temporizador = null;
let preguntasRealizadas = new Set(); // Preguntas ya realizadas
let numeroPreguntasMax = null;

// Función para iniciar el test
startButton.addEventListener('click', () => {
    // Limpiar mensajes y reiniciar todo
    clearInterval(temporizador); // Detener cualquier temporizador existente
    feedbackElement.textContent = '';
    feedbackElement.className = '';
    timerElement.textContent = '';
    questionContainer.classList.add('hidden'); // Ocultar preguntas mientras validamos

    // Validar la configuración del test
    const numeroPreguntas = numeroPreguntasInput.value;
    if (numeroPreguntas !== "" && (!/^\d+$/.test(numeroPreguntas) || parseInt(numeroPreguntas) <= 0)) {
        feedbackElement.textContent = "Por favor, introduce un número válido para el número de preguntas.";
        feedbackElement.className = 'error';
        capa_pregunta.classList.add('ocultar');

        return; // Salir sin iniciar el test ni el temporizador
    }else{        
        capa_pregunta.classList.remove('ocultar');
    }

    // Configuración válida: iniciar el test
    numeroPreguntasMax = numeroPreguntas !== "" ? parseInt(numeroPreguntas) : null;
    iniciarTest();
});

// Función para iniciar el test
function iniciarTest() {
    const temaSeleccionado = selectorTema.value;
    preguntaActual = null;

    // Cargar preguntas según el tema seleccionado
    if (temaSeleccionado === 'random') {
        // Combinar preguntas de todos los temas de forma aleatoria
        preguntas = Object.entries(temas).flatMap(([tema, preguntas]) =>
            preguntas.map(pregunta => ({ ...pregunta, tema }))
        );
    } else {
        // Cargar preguntas del tema seleccionado
        preguntas = temas[temaSeleccionado].map(pregunta => ({ ...pregunta, tema: temaSeleccionado }));
    }

    // Barajar preguntas
    preguntas.sort(() => Math.random() - 0.5);

    // Reiniciar variables de control
    fallos = 0;
    aciertos = 0;
    preguntasRealizadas.clear();

    // Mostrar el contenedor de preguntas
    questionContainer.classList.remove('hidden');

    // Mostrar la primera pregunta
    mostrarPregunta();
}

// Función para mostrar una pregunta
function mostrarPregunta() {
    console.log("nueva pregunta")
    // Verificar si ya se realizaron todas las preguntas configuradas
    if (numeroPreguntasMax !== null && preguntasRealizadas.size >= numeroPreguntasMax) {
        finalizarTest();
        return;
    }

    // Seleccionar una pregunta aleatoria que no haya sido realizada
    console.log(1)
    console.log(preguntaActual)
    while (!preguntaActual || preguntasRealizadas.has(preguntaActual)) {
        preguntaActual = preguntas[Math.floor(Math.random() * preguntas.length)];
        console.log(preguntaActual)
    }
    preguntasRealizadas.add(preguntaActual);

    // Reiniciar estado de la pregunta actual
    falladoPreguntaActual = false;

    // Mostrar el tema, la pregunta y sus opciones
    temaActual = preguntaActual.tema;
    temaElement.textContent = `Tema ${temaActual}`;
    questionElement.textContent = preguntaActual.pregunta;
    optionsContainer.innerHTML = '';
    preguntaActual.opciones.forEach(opcion => {
        const button = document.createElement('button');
        button.textContent = opcion;
        button.classList.add('option');
        button.style.color = 'black'; // Color inicial
        button.addEventListener('click', () => verificarRespuesta(button, opcion));
        optionsContainer.appendChild(button);
    });

    // Reiniciar el temporizador
    reiniciarTemporizador();
}

// Función para verificar la respuesta
function verificarRespuesta(button, opcionSeleccionada) {
    clearInterval(temporizador); // Detener el temporizador

    if (opcionSeleccionada === preguntaActual.respuesta) {
        if (!falladoPreguntaActual) {
            // Contar como acierto solo si no se falló antes
            aciertos++;
        }
        feedbackElement.textContent = ''; // Limpiar cualquier mensaje previo
        button.style.color = 'darkgreen'; // Respuesta correcta en verde oscuro
        setTimeout(() => {
            mostrarPregunta();
        }, 1000);
    } else {
        // Marcar la pregunta como fallada si no se ha fallado antes
        if (!falladoPreguntaActual) {
            fallos++;
            falladoPreguntaActual = true;
        }
        feedbackElement.textContent = 'Incorrecto. Inténtalo de nuevo.';
        feedbackElement.className = 'incorrect';
        button.style.color = 'red'; // Respuesta incorrecta en rojo
    }
}

// Función para reiniciar el temporizador
function reiniciarTemporizador() {
    tiempoRestante = parseInt(tiempoSelector.value);
    timerElement.textContent = `Tiempo restante: ${tiempoRestante} segundos`;

    temporizador = setInterval(() => {
        tiempoRestante--;
        timerElement.textContent = `Tiempo restante: ${tiempoRestante} segundos`;

        if (tiempoRestante <= 0) {
            clearInterval(temporizador);
            feedbackElement.textContent = 'Tiempo agotado.';
            feedbackElement.className = 'timeout';
            if (!falladoPreguntaActual) {
                fallos++;
                falladoPreguntaActual = true;
            }
            setTimeout(() => {
                mostrarPregunta();
            }, 1500); // Espera de 1.5 segundos antes de pasar a la siguiente pregunta
        }
    }, 1000);
}

// Función para finalizar el test
function finalizarTest() {
    clearInterval(temporizador); // Detener el temporizador definitivamente
    questionContainer.classList.add('hidden');

    const totalPreguntas = preguntasRealizadas.size;
    const aprobado = aciertos >= Math.ceil(totalPreguntas / 2);

    feedbackElement.innerHTML = `
        <strong>Resultados finales:</strong><br>
        Total de preguntas: ${totalPreguntas}<br>
        Aciertos: ${aciertos}<br>
        Fallos: ${fallos}<br>
        <strong>${aprobado ? '¡Has aprobado!' : 'Has suspendido.'}</strong>
    `;
    feedbackElement.className = aprobado ? 'final correct' : 'final incorrect';
}
