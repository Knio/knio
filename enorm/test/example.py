import logging
import pathlib
import sqlite3

import enorm


class Library(enorm.DB):
  pass


class Author(Library.Row):
  def books(self):
    return self.db.Book.where(author_id=self['id'])


class Book(Library.Row):
  def loans(self):
    return self.db.Loan.where(book_id=self['id'])


class Member(Library.Row):
  def loans(self):
    return self.db.Loan.where(member_id=self['id'])

  def favorite_author(self):
    fav = self.db.exec(Library.Row, f'''
      SELECT author_id, count(author_id) FROM {Loan}
      INNER JOIN {Book} ON {Book}.id = book_id
      INNER JOIN {Author} ON {Author}.id = author_id
      WHERE member_id = :id
      GROUP BY author_id
      ORDER BY count(author_id) DESC
      LIMIT 1
    ''', id=self['id']).fetchone()
    return self.db.Author.get(fav['author_id'])


class Loan(Library.Row):
  def book(self):
    return self.db.Book.where(id=self['book_id']).fetchone()

  def member(self):
    return self.db.Book.where(id=self['member_id']).fetchone()


def main():
  dir = pathlib.Path(__file__).parent
  db = Library(sqlite3.connect(dir/'example.sqlite'))
  if db.check_or_create((dir / 'example.sql').read_text()):
    db.exec(None, (dir / 'example_data.sql').read_text(), _script=True)
    db.con.commit()

  bob = db.Member.where(name='Bob').fetchone()

  titles = [l.book()['title'] for l in bob.loans()]
  print(f"Bob's loans: \n\t{'\n\t'.join(titles)}\n")

  print(f"Bob's favourite author's: {bob.favorite_author()['name']}\n")

  books = bob.favorite_author().books()
  books_str = '\n\t'.join(b['title'] for b in books)
  print(f"Recommended books for Bob:\n\t{books_str}\n")



if __name__ == '__main__':
  logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(lineno)d %(message)s',
    level=logging.INFO,
  )
  main()
