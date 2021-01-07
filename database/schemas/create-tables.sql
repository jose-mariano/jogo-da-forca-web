CREATE TABLE IF NOT EXISTS tbl_category_words (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	category TEXT
);

CREATE TABLE IF NOT EXISTS tbl_words (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	word TEXT,
	category_word INTEGER NOT NULL,
	FOREIGN KEY(category_word) REFERENCES tbl_category_words(id)
);
