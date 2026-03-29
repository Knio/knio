
import functools
import logging
import time
import typing
import re

import sqlite3


from .version import *


LOG = logging.getLogger('enorm')


class UnboundDBError:
  def __get__(self, obj, cls):
    n = cls.__name__
    raise UnboundLocalError(f'Attempted to access static `{cls!r}.db`; {obj} is not bound to a database instance. Instead use `mydb.{n}`')


R = typing.TypeVar('R', bound='Row')
class Row(sqlite3.Row):
  def dict(self):
    return {k:self[k] for k in self.keys()}

  def __repr__(self):
    kv = ', '.join(f'{k}={self[k]!r}' for k in self.keys())
    return f'<{type(self).__name__} {kv}>'

  db = UnboundDBError()

  @classmethod
  @functools.cache
  def tablename(cls):
    n = cls.__name__
    n = re.sub(r'(?<!^)(?=[A-Z])', '_', n).lower()
    return n + 's'

  @classmethod
  def _update(cls, id, **kv):
    updates = ',\n\t '.join(f'{k} = :{k}' for k in kv.keys())
    s = f'''
      UPDATE {cls}
      SET {updates}
      WHERE id = :id
    '''
    return cls.db.exec(None, s, id=id, **kv).rowcount

  def update(self, **kv):
    return type(self)._update(self['id'], **kv)

  @classmethod
  def get(cls: R, id) -> R:
    return cls.db.exec(cls, f'''
      SELECT *
      FROM {cls}
      WHERE id = :id
      ''', id=id).fetchone()

  @classmethod
  def where(cls, _order='', **kv):
    where = 'WHERE ' if kv else ''
    # TODO support sets
    clause = '\n\tAND  '.join(f'{k} {"IS" if v is None else "="} :{k}' for k,v in kv.items())
    return cls.db.exec(cls, f'''
      SELECT *
      FROM {cls}
      {where}
        {clause}
      {"ORDER BY " if _order else ""}{_order}
      ''', **kv)

  @classmethod
  def new(cls, **kv):
    ks = kv.keys()
    attrs = ', '.join(f'"{k}"' for k in ks)
    vals = ', '.join(f':{k}' for k in ks)
    return cls.db.exec(None, f'''
      INSERT INTO {cls} ({attrs})
      VALUES ({vals})
      ''', **kv).lastrowid

  def delete(self):
    return self.db.exec(None, f'''
      DELETE FROM {self}
      WHERE id = :id
    ''', id=self['id']).rowcount


class DBMeta(type):
  def __new__(db_cls, name, bases, dct):
    dct['row_types'] = {}
    dct['Row'] = None
    DB = super().__new__(db_cls, name, bases, dct)

    # register "MyDB.Row" types
    class RowMeta(type):
      def __new__(row_cls, name, bases, dct):
        T = super().__new__(row_cls, name, bases, dct)
        DB.row_types[name] = T
        return T
      def __str__(cls):
        return cls.tablename()

    class DBRow(Row, metaclass=RowMeta):
      pass

    DB.Row = DBRow

    return DB



class DB(metaclass=DBMeta):
  def __init__(self, con):
    self.con = con

  def bind_row(self, row_type):
    if 'db' in row_type.__dict__:
      return row_type
    BoundRow = type(row_type.__name__, (row_type,), dict(db=self))
    return BoundRow


  def __getattr__(self, name):
    # TODO: bind ourselves (db instance with con) & DBRow types into scope
    for db_type in type(self).__mro__:
      if not (dct := getattr(db_type, 'row_types')):
        continue
      if not (row_type := dct.get(name)):
        continue
      return self.bind_row(row_type)
    raise AttributeError(name)


  def exec(self, row, sql, _many=None, _params=None, _script=None, **kw):
    LOG.debug(sql)
    backoff = 0.09
    while 1:
      cur = self.con.cursor()
      cur.row_factory = self.bind_row(row)
      cur.arraysize = 1000
      try:
        if _script:
          cur.executescript(sql)
        elif _many:
          assert not kw
          cur.executemany(sql, _many)
        else:
          cur.execute(sql, _params or kw)
        break
      except sqlite3.OperationalError as e:
        if e.sqlite_errorcode == sqlite3.SQLITE_BUSY:
          backoff *= 1.37
          backoff = min(backoff, 57.3)
          LOG.info(f'db is busy, waiting {backoff:.2f}s..')
          time.sleep(backoff)
          continue
        raise NotImplementedError(
          (e, repr(e), repr(e.sqlite_errorname), repr(e.sqlite_errorcode))
        )
    return cur


  def check_or_create(self, reference_schema, create=True):
    '''
    Check if the db matches the given schema, and creates it if not.
    Raises ValueError if it does not match, returns False if it matches, returns True if it was created.
    '''
    actual_schema = self.get_schema()
    if not actual_schema and create:
      with self.con:
        for stmt in reference_schema.split(';'):
          self.exec(None, stmt)
      return True

    reference_schema = reference_schema.replace('\r\n', '\n').strip(' \t\r\n')

    if actual_schema == reference_schema:
      return False

    raise ValueError(f'Schema for database does not match! reference:\n{reference_schema!r}\n\ndatabase has:\n{actual_schema!r}')


  def get_schema(self):
    s = '''
      SELECT *
      FROM sqlite_schema
      WHERE
        name NOT LIKE 'sqlite_%'
      ORDER BY tbl_name DESC, type DESC, sql DESC
    '''
    tables = self.exec(Row, s).fetchall()
    schema = '\n\n'.join(t['sql'] + ';' for t in tables)
    schema = schema.replace('\r\n', '\n').strip(' \t\r\n')
    return schema


