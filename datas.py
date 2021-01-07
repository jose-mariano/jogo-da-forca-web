import sqlite3
from random import randint

# Database functions:
def get_db_connection():
	database = sqlite3.connect('database/words.sqlite3')
	return database


def addWord(word, category):
	value = (word, category,)

	database = get_db_connection()
	cursor = database.cursor()

	cursor.execute("""
		INSERT INTO tbl_words (word, category_word)
		VALUES (?, ?);
	""", value)

	database.commit()
	database.close()


def addCategoryWord(category):
	value = (category,)

	database = get_db_connection()
	cursor = database.cursor()

	cursor.execute("""
		INSERT INTO tbl_category_words (category)
		VALUES (?);
	""", value)

	database.commit()
	database.close()


def select(command):
	database = get_db_connection()
	cursor = database.cursor()

	cursor.execute(command)
	data = cursor.fetchall()

	database.close()
	return data


def selectAllJoin():
	database = get_db_connection()
	cursor = database.cursor()

	cursor.execute("""
		SELECT tbl_words.word, tbl_category_words.category
		FROM tbl_words INNER JOIN tbl_category_words
		ON tbl_words.category_word = tbl_category_words.id;
	""")
	data = cursor.fetchall()

	database.close()
	return data


def createDatabase():
	database = get_db_connection()

	with open('database/schemas/create-tables.sql') as schema:
		database.executescript(schema.read())

	len_words = select('SELECT count(*) FROM tbl_words')[0][0]
	len_category_words = select('SELECT count(*) FROM tbl_category_words')[0][0]

	if len_words == 0 and len_category_words == 0:
		with open('database/schemas/insert-words.sql') as schema:
			database.executescript(schema.read())

	database.commit()
	database.close()


# Other functions:
def getRandomWord():
	numberWordsInDatabase = select("SELECT count(*) FROM tbl_words")[0][0]
	randomWord = randint(1, numberWordsInDatabase)
	
	word = select(f"SELECT word, category_word FROM tbl_words WHERE id = {randomWord}")
	category = select(f"SELECT category FROM tbl_category_words WHERE id = {word[0][1]}")[0][0]

	return {'word': word[0][0], 'category': category}


def validateAndAddNewWords(wordList):
	destinyWords = {"add": list(), "notAdd": list()}
	separateWords = wordList[:].lower().split(',')
	newListSeparateWords = list()

	itemCounter = 0
	listCounter = 0
	for item in separateWords:
		if itemCounter == 0:
			newListSeparateWords.append(list())
		itemCounter += 1
		newListSeparateWords[listCounter].append(item)
		if itemCounter >= 2:
			listCounter += 1
			itemCounter = 0

	for word in newListSeparateWords:
		if len(word) == 2 and select(f"SELECT count(*) FROM tbl_category_words WHERE id = '{word[1]}'")[0][0] >= 1 and select(f"SELECT count(*) FROM tbl_words WHERE word = '{word[0]}'")[0][0] == 0:
			addWord(word[0], word[1])
			word[1] = select(f"SELECT category FROM tbl_category_words WHERE id = '{word[1]}'")[0][0]
			destinyWords["add"].append(word)
		else:
			destinyWords["notAdd"].append(word)

	return destinyWords


def validateAndAddNewCategories(categoryList):
	destinyCategories = {"add": list(), "notAdd": list()}
	separateCategories = categoryList[:].lower().split(',')

	for item in separateCategories:
		if select(f"SELECT count(*) FROM tbl_category_words WHERE category = '{item}'")[0][0] == 0 and len(item) != 0:
			addCategoryWord(item)
			destinyCategories["add"].append(item)
		else:
			destinyCategories["notAdd"].append(item)

	return destinyCategories
