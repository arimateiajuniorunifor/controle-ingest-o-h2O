document.getElementById('agua-form').onsubmit = function (event) {
	event.preventDefault();
	const idadeGrupo = document.getElementById('idade_grupo').value;
	const peso = parseFloat(document.getElementById('peso').value); // Convertendo para número
	const spinner = document.getElementById('spinner');
	const result = document.getElementById('result').value;
	const send = document.getElementById('button_send');
	const username = document.getElementById('username').value;

	// Texto do overlay
	document.getElementById(
		'userDisplay',
	).innerText = `Olá ${username}, a quantidade de água que você precisa tomar por dia é de: ${result} litros por dia`;

	// Validações adicionais no frontend
	if (isNaN(peso) || peso <= 0) {
		result.innerText = 'Peso deve ser maior que 0';
		return;
	}

	spinner.classList.add('show'); // Mostra o spinner
	send.classList.add('active'); // botão de enviar
	result.innerHTML = ''; // Limpa resultados anteriores
	const startTime = Date.now(); // Registra o tempo de início da requisição

	fetch('http://calculadoradeagua.online:5000/calcular', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({ idade_grupo: idadeGrupo, peso: peso }),
	})
		.then((response) => {
			if (!response.ok) {
				throw new Error('Erro ao calcular ingestão de água');
			}
			return response.json();
		})
		.then((data) => {
			const elapsedTime = Date.now() - startTime; // Calcula o tempo decorrido
			const remainingTime = Math.max(0, 2000 - elapsedTime); // Calcula o tempo restante para completar os 2 segundos

			// Define um atraso para garantir que o spinner fique visível por pelo menos 2 segundos
			setTimeout(() => {
				spinner.classList.remove('show'); // Esconde o spinner
				send.classList.add('active'); // Mostra o botão de enviar
				if (data.error) {
					result.innerText = data.error;
				} else {
					result.innerText =
						'Ingestão diária de água: ' + data.total + ' ml por dia';
				}
			}, remainingTime);
			// Exibir resultado no overlay
			showResultInOverlay(data);
		})
		.catch((error) => {
			console.error('Erro:', error);
			const elapsedTime = Date.now() - startTime; // Calcula o tempo decorrido
			const remainingTime = Math.max(0, 4000 - elapsedTime); // Calcula o tempo restante para completar os 4 segundos

			// Define um atraso para garantir que o spinner fique visível por pelo menos 4 segundos
			setTimeout(() => {
				spinner.classList.remove('show'); // Esconde o spinner
				send.classList.remove('active'); // Esconde o botão de enviar
				result.innerText = 'Erro ao calcular ingestão de água';
			}, remainingTime);
		});
};

const send = document.getElementById('button_send');
const overlay = document.getElementById('overlay');
const closeButton = document.getElementById('close-btn');
const form = document.getElementById('overlay-form');

send.onclick = function () {
	overlay.style.display = 'flex';
};

closeButton.onclick = function () {
	clearOverlayInputs();
	overlay.style.display = 'none';
};

form.onsubmit = function (event) {
	event.preventDefault();
	const email = document.getElementById('email').value;

	if (!email) {
		alert('Por favor, preencha todos os campos.');
		return;
	}

	clearOverlayInputs();
	overlay.style.display = 'none';
	alert('Informações enviadas com sucesso!');
};

//limpa os inputs do overlay
function clearOverlayInputs() {
	document.getElementById('nome').value = '';
	document.getElementById('email').value = '';
}
