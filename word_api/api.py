from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from random import randint


app = Flask(__name__)

# Estruturando o banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wordsDatabase.sqlite3'
db = SQLAlchemy(app)
key_change_database = '16k3n9zo'

class Word(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(46), unique=True, nullable=False)
	category_id = db.Column(db.Integer, db.ForeignKey('category_word.id'), nullable=False)
	category = db.relationship('Category_word', backref=db.backref('words', lazy=True))

	def __repr__(self):
		return "<Word {}>".format(self.name)

class Category_word(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(46), unique=True, nullable=False)

	def __repr__(self):
		return "<Category_word {}>".format(self.name)

db.create_all()


# Adicionando categorias de palavras no banco de dados
if (len(Category_word.query.all()) == 0):
	categories = ('fruta', 'objeto', 'animal', 'comida', 'bebida')
	for item in categories:
		element = Category_word(name=item)
		db.session.add(element)
	db.session.commit()

# Adicionando palavras no banco de dados
if (len(Word.query.all()) == 0):
	words = [('abacaxi', '1'), ('banana', '1'), ('abacate', '1'), ('tangerina', '1'), ('laranja', '1'), ('morango', '1'), ('framboesa', '1'), ('amora', '1'), ('jaca', '1'), ('caju', '1'), ('faca', '2'), ('mesa', '2'), ('bola', '2'), ('televisao', '2'), ('caixa', '2'), ('caneta', '2'), ('janela', '2'), ('porta', '2'), ('cobertor', '2'), ('cadeira', '2'), ('panda', '3'), ('morcego', '3'), ('jabuti', '3'), ('tartaruga', '3'), ('vaca', '3'), ('touro', '3'), ('rinoceronte', '3'), ('elefante', '3'), ('hipopotamo', '3'), ('aranha', '3'), ('lasanha', '4'), ('arroz', '4'), ('feijoada', '4'), ('carne', '4'), ('sorvete', '4'), ('pastel', '4'), ('bolo', '4'), ('bala', '4'), ('chocolate', '4'), ('biscoito', '4'), ('vinho', '5'), ('cerveja', '5'), ('caipirinha', '5'), ('vodka', '5'), ('refrigerante', '5'), ('cafe', '5'), ('leite', '5'), ('agua', '5'), ('suco', '5'), ('champanhe', '5')]
	for item in words:
		element = Word(name=item[0], category_id=item[1])
		db.session.add(element)
	db.session.commit()


# Estrutura da API
# Transformando uma query em Json
def query_for_json(queryList, formatJson):
	jsonList = list()
	for item in queryList:
		json = formatJson.copy()
		for key in formatJson.keys():
			json[key] = item[json[key]]
		jsonList.append(json)
	return jsonList


# Criando rotas
@app.route('/word-api/words', methods=['GET'])
def get_all_words():
	words = Category_word.query.join(Word, Category_word.id==Word.category_id).add_columns(Word.id, Word.name, Category_word.name).all()

	return jsonify(query_for_json(words, {"id": 1, "word": 2, "category": 3})), 200


@app.route('/word-api/words/<int:id>', methods=['GET'])
def filter_words_by_id(id):
	words = Category_word.query.join(Word, Category_word.id==Word.category_id).add_columns(Word.id, Word.name, Category_word.name).all()
	filtered_words = [word for word in words if word[1] == id]
	if (len(filtered_words) != 0):
		return jsonify(query_for_json(filtered_words, {"id": 1, "name": 2, "category": 3})), 200

	return jsonify({"error": "word not found"}), 404


@app.route('/word-api/words/<string:category>', methods=['GET'])
def filter_words_by_category(category):
	words = Category_word.query.join(Word, Category_word.id==Word.category_id).add_columns(Word.id, Word.name, Category_word.name).all()
	filtered_words = [word for word in words if word[3] == category]
	if (len(filtered_words) != 0):
		return jsonify(query_for_json(filtered_words, {"id": 1, "name":2, "category": 3})), 200

	return jsonify({"error": "word not found"}), 404


@app.route('/word-api/words', methods=['POST'])
def add_word():
	data = request.get_json()
	# Obs diminuir esse código, crie uma função que verifique se há algum erro e retorne para o usuário, caso contrário, adicione a palavra.
	if (('word' in data.keys()) and ('category_id' in data.keys()) and ('key' in data.keys())):
		if (data['key'] == key_change_database):
			category = Category_word.query.filter(Category_word.id==data['category_id']).all()
			if (len(Word.query.filter(Word.name==data['word']).all()) == 0 and len(category) != 0):
				new_word = Word(name=data['word'], category_id=category[0].id)
				db.session.add(new_word)
				db.session.commit()

				data['category_name'] = category[0].name
				return jsonify(data), 202

			return jsonify({"error": "word already exists or category does not exist"}), 206
		
		return jsonify({"error": "incorrect key"}), 401

	return jsonify({"error": "unidentified object"}), 404


# Criando rotas para manipular as categorias
@app.route('/word-api/categories', methods=['GET'])
def get_all_categories():
	categories = Category_word.query.add_columns(Category_word.id, Category_word.name).all()
	
	return jsonify(query_for_json(categories, {"id": 1, "category": 2})), 200


@app.route('/word-api/categories/<int:id>', methods=['GET'])
def filter_categories_by_id(id):
	categories = Category_word.query.add_columns(Category_word.id, Category_word.name).all()
	filtered_cotegories = [category for category in categories if category[1] == id]
	if (len(filtered_cotegories) != 0):
		return jsonify(query_for_json(filtered_cotegories, {"id": 1, "category": 2})), 200

	return jsonify({"error": "category not found"}), 404


@app.route('/word-api/categories', methods=['POST'])
def add_category():
	data = request.get_json()

	if (('category' in data.keys()) and ('key' in data.keys())):
		if (data['key'] == key_change_database):
			if (len(Category_word.query.filter(Category_word.name==data['category']).all()) == 0):
				new_category_word = Category_word(name=data['category'])
				db.session.add(new_category_word)
				db.session.commit()
				return jsonify(data), 202

			return jsonify({"error": "category already exists"}), 206

		return jsonify({"error": "incorrect key"}), 401

	return jsonify({"error": "unidentified object"}), 404


@app.route('/word-api/randomWord', methods=['GET'])
def get_a_random_word():
	words = Category_word.query.join(Word, Category_word.id==Word.category_id).add_columns(Word.id, Word.name, Category_word.name).all()
	tot_words = len(words)
	if (tot_words > 0):
		index_word = randint(0, (tot_words - 1))
		return jsonify(query_for_json([words[index_word]], {"id": 1, "word": 2, "category": 3})), 200
	else:
		return jsonify({"error": "there are no words on the server"}), 404




if (__name__ == '__main__'):
	app.run(port='4000')
