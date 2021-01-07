from flask import Blueprint, render_template, redirect, url_for, request
from datas import *

root_pages = Blueprint('root_pages', __name__, template_folder='templates')
createDatabase()


@root_pages.route('/viewWords')
def viewWords():
	words = selectAllJoin()

	return render_template('view-words.html', words=words)


@root_pages.route('/addWords')
def addWords():
	category_words = select('SELECT * FROM tbl_category_words')

	return render_template('add-items.html', categoryWords=category_words)


@root_pages.route('/viewNewItems', methods=["GET", "POST"])
def viewNewItems():
	if request.method == "POST":
		newCategory = request.form['newCategory']
		newWord = request.form['newWords']
		categories = validateAndAddNewCategories(newCategory)
		words = validateAndAddNewWords(newWord)

		return render_template('view-new-items.html', addWords=words["add"], notAddWords=words["notAdd"], addCategories=categories["add"], notAddCategories=categories["notAdd"])
	else:
		return redirect(url_for('root_pages.addWords'))

