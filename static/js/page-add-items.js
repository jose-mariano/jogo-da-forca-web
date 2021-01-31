const categorySelect = document.querySelector('select#categoryWord');

const buttonAddWord = document.querySelector('#addWord');
buttonAddWord.addEventListener('click', addWord);

const buttonAddCategory = document.querySelector('#addCategory');
buttonAddCategory.addEventListener('click', addCategory);

function addWord(event){
	const wordInput = document.querySelector('input#word');
	const word = wordInput.value;

	if (word.length > 0 && justOneWord(word) && !specialCharacter(word)){
		const optionSelected = categorySelect[categorySelect.selectedIndex];
		const categoryWordValue = optionSelected.value;
		const categoryWordText = optionSelected.innerText;

		addWordInViewItems(word, categoryWordText, categoryWordValue);
		wordInput.value = '';
		wordInput.focus();
	} else {
		console.log('[Error] word not allowed!');
	}
}

function addCategory(event){
	const categoryInput = document.querySelector('input#category');
	const category = categoryInput.value;

	const existingCategories = categorySelect.innerText.split('\n');

	if (category.length > 0 && justOneWord(category) && existingCategories.indexOf(category) === -1){
		const newOption = document.createElement('option');
		newOption.innerText = category;
		newOption.value = categorySelect.length + 1;

		categorySelect.appendChild(newOption);
		addCategoryInViewItems(category);
		categoryInput.value = '';
	} else {
		console.log('[Error] category not allowed!');
	}
}

function justOneWord(word){
	if (word.indexOf(' ') != -1){
		return false;
	} else {
		return true;
	}
}

function specialCharacter(word){
	for (let l in word){
		const letter = word[l];
		const codLetter = letter.charCodeAt();
		if (codLetter < 65 || (codLetter > 90 && codLetter < 97) || codLetter > 122){
			return true;
		}
	}
	return false;
}

function addCategoryInViewItems(category){
	const viewItems = document.querySelector('#viewItems');

	const html = `
	<div data-item="${category}" class="newCategory">
		<p>New category: ${category}</p>
	</div>
	`;

	viewItems.innerHTML += html;
}

function addWordInViewItems(word, category, value){
	const viewItems = document.querySelector('#viewItems');

	const html = `
	<div data-item="${word},${value}" class="newWord">
		<div>
			<p>Word: ${word}</p>
			<p>Category: ${category}</p>
		</div>
		<button onclick='removeWord(event)'>X</button>
	</div>
	`;

	viewItems.innerHTML += html;
}

function removeWord(event){
	const viewItems = document.querySelector('#viewItems');
	const button = event.currentTarget;
	const divParent = button.parentElement;

	viewItems.removeChild(divParent);
}


const formViewItems = document.querySelector('#formViewItems');
formViewItems.addEventListener('submit', getDatas);

function getDatas(event){
	const data = {
		"words": new Array(),
		"categories": new Array()
	}

	const items = document.querySelectorAll('div.newWord');
	items.forEach((item) => {
		const dataWord = item.dataset.item;
		data.words.push(dataWord.split(","));
	});

	const category = document.querySelectorAll('div.newCategory');
	category.forEach((category) => {
		const dataCategory = category.dataset.item;
		data.categories.push(dataCategory);
	});

	// Evitando o envio do formulário.
	if ((data.words.length === 0) && (data.categories.length === 0)){
		window.alert("O formulário não pode ser enviado estando em branco!");
		event.preventDefault();
	}

	const inputItems = document.querySelector('input#items');
	inputItems.value = JSON.stringify(data);
}
