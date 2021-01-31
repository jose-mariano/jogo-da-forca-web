from flask import Flask, render_template, redirect, url_for, request
import requests
import json


aplication = Flask(__name__)

@aplication.route('/', methods=["GET"])
@aplication.route('/home', methods=["GET"])
def page_game():
	try:
		data = requests.get('http://127.0.0.1:4000/word-api/randomWord').json()[0]
	except:
		return "Error Not Found", 404
	else:
		if (("word" in data.keys()) and ("category" in data.keys())):
			return render_template('game.html', word=data["word"], category=data["category"]), 200
		else:
			return "Error Not Found", 404


@aplication.route('/config/viewWords', methods=["GET"])
def page_view_all_words():
	try:
		data = requests.get('http://127.0.0.1:4000/word-api/words').json()
	except:
		return "Error Not Found", 404
	else:
		return render_template('view-words.html', words=data), 200


@aplication.route('/config/addWords', methods=["GET"])
def page_add_items():
	try:
		data = requests.get('http://127.0.0.1:4000/word-api/categories').json()
	except:
		return "Error Not Found", 404
	else:
		return render_template('add-items.html', categories=data), 200


@aplication.route('/config/viewNewItems', methods=["GET"])
def redirect_for_add_items():
	return redirect(url_for('page_add_items'))


@aplication.route('/config/viewNewItems', methods=["POST"])
def page_view_new_items():
	items = json.loads(request.form["items"])
	new_items = {
		"words": {
			"add": list(),
			"not_add": list()},
		"categories": {
			"add": list(),
			"not_add": list()}}

	for category in items["categories"]:
		categoryObjectJson = {"key": "16k3n9zo", "category": category}
		result = requests.post('http://127.0.0.1:4000/word-api/categories', json=categoryObjectJson)
		if ("error" in result.json().keys()):
			new_items["categories"]["not_add"].append(category)
		else:
			new_items["categories"]["add"].append(category)

	for word in items["words"]:
		if (len(word) == 2):
			wordObjectJson = {"key": "16k3n9zo", "word": word[0], "category_id": word[1]}
			result = requests.post('http://127.0.0.1:4000/word-api/words', json=wordObjectJson)
			if ("error" in result.json().keys()):
				new_items["words"]["not_add"].append(word)
			else:
				word[1] = result.json()["category_name"]
				new_items["words"]["add"].append(word)

	return render_template("view-new-items.html", items=new_items), 200


if (__name__ == "__main__"):
	aplication.run(debug=True, port='5000')
