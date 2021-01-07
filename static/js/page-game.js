/* Jogo */
function hide(word){
	const string = new Array();
	for (const letter in word){
		string.push('_');
	}
	return string;
}

function createGame(word, category){
	const state = {
		'category': category,
		'hideWord': hide(word),
		'letters': new Array(),
		'errors': 0,
		'ended': false
	}

	const observers = new Array();

	function subscribe(observerFunction){
		observers.push(observerFunction);
	}

	function notifyAll(command){
		for (const observer of observers){
			observer(command);
		}
	}

	function addInLetters(letter){
		if (state.letters.indexOf(letter) === -1){
			state.letters.push(letter);
		}
	}

	function addInHideWord(letter){
		for (const l in word){
			if (letter === word[l]){
				state.hideWord[l] = letter;
			}
		}
	}

	function checkSituation(){
		if (state.errors === 6 || state.hideWord.indexOf('_') === -1){
			state.ended = true;
			state.word = word;
			state.errors === 6 ? (state.situation = 'Você perdeu!') : (state.situation = 'Você venceu!');
		}
	}

	function play(letter){
		if (!state.ended && state.letters.indexOf(letter) === -1){
			addInLetters(letter);
			if (word.indexOf(letter) === -1){
				state.errors += 1;
			} else {
				addInHideWord(letter);
			}
			checkSituation();
			notifyAll(state);
		}
	}

	return {
		state,
		subscribe,
		play
	}
}


/* Keyboard */
function createKeyboardLettersListener(){
	const keyboardContainer = document.getElementById('virtualKeyboard');
	let state = false;
	const observers = new Array();

	function subscribe(observerFunction){
		observers.push(observerFunction);
	}

	function notifyAll(command){
		for (const observer of observers){
			observer(command);
		}
	}

	function allowComputerKeyboard(){
		function checkLetter(letter){
			const alphabet = 'abcdefghijklmnopqrstuvwxyz';
			if (alphabet.indexOf(letter) !== -1){
				notifyAll(letter);
			}
		}

		document.addEventListener('keypress', (event) => {
			const keypress = event.key;
			checkLetter(keypress.toLowerCase());
		});
	}

	function createVirtualKeyboard(){
		const rows = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm'];

		for (const string of rows){
			const row = document.createElement('div');
			for (const letter of string){
				const button = document.createElement('button');
				button.addEventListener('click', () => {
					notifyAll(letter);
				});
				button.innerText = letter;
				button.className = 'key';
				
				row.appendChild(button);
			}
			keyboardContainer.appendChild(row);
		}
	}

	function changeVirtualKeyboardState(){
		if (state === false){
			createVirtualKeyboard();
			state = true;
		} else {
			keyboardContainer.innerHTML = "";
			state = false;
		}
	}

	const divButtonVirtualKeyboard = document.getElementById('buttonVirtualKeyboard');
	const buttonVirtualKeyboard = document.createElement('button');
	buttonVirtualKeyboard.innerHTML = '<img src="static/images/keyboard.png" class="imageKeyboard" />';
	buttonVirtualKeyboard.addEventListener('click', changeVirtualKeyboardState);
	divButtonVirtualKeyboard.appendChild(buttonVirtualKeyboard);

	return {
		subscribe,
		allowComputerKeyboard
	}
}


/* Interface */
function showList(list){
	let string = '';
	for (const element in list){
		if (element == 0){
			string += list[element];
		} else {
			string += ` ${list[element]}`;
		}
	}
	return string
}

function createScreen(){
	const word = document.getElementById('word');
	const category = document.getElementById('wordCategory');
	const letters = document.getElementById('letters');
	const picture = document.getElementById('image');
	const sourcePictures = ['static/images/start.png', 'static/images/defeat1.png', 'static/images/defeat2.png', 'static/images/defeat3.png', 'static/images/defeat4.png', 'static/images/defeat5.png', 'static/images/defeat6.png'];

	function showFinishWindow(state){
		const divFinishWindow = document.getElementById('finishWindow');
		divFinishWindow.classList.add("finish");

		const imageSource = state.situation === 'Você venceu!' ? 'static/images/youwin.png' : 'static/images/youlost.png';

		const html = `
			<div class="container">
				<div>
					<h1>${state.situation}</h1>
					<img src="${imageSource}" alt="${state.situation}" />
					<p>A palavra era: ${state.word.toUpperCase()}</p>
					<a href="/">jogar novamente</a>
				<div>
			</div>
		`
		divFinishWindow.innerHTML = html;
	}

	function updateScreen(state){
		word.innerText = showList(state.hideWord);	
		category.innerText = `Essa palavra é um(a): ${state.category}`;
		letters.innerText = showList(state.letters);
		picture.innerHTML = `<img src="${sourcePictures[state.errors]}" alt="erros=${state.errors}" />`;

		if (state.ended === true){
			showFinishWindow(state);
		}
	}

	return {
		updateScreen
	}
}

