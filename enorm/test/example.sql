CREATE TABLE "members" (
	id INTEGER PRIMARY KEY,
	"name"	TEXT
);

CREATE TABLE "loans" (
	id INTEGER PRIMARY KEY,
	"member_id"	INTEGER NOT NULL,
	"book_id"	INTEGER NOT NULL,
	"begin"	DATE,
	"expires"	DATE
);

CREATE TABLE "books" (
	id INTEGER PRIMARY KEY,
	"author_id"	INTEGER NOT NULL,
	"title"	TEXT NOT NULL
);

CREATE TABLE "authors" (
	id INTEGER PRIMARY KEY,
	"name"	TEXT NOT NULL
);
