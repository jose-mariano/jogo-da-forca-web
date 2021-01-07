from flask import Flask, render_template
from root import root_pages
from datas import getRandomWord


server = Flask(__name__)
server.register_blueprint(root_pages, url_prefix='/root')


@server.route('/')
def index():
	data = getRandomWord()
	return render_template('game.html', word=data['word'], category=data['category'])


if __name__ == "__main__":
	server.run()
