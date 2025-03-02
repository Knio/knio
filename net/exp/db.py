import logging
from collections import namedtuple
import sqlite3

LOG = logging.getLogger(__name__)


class DB:
  @staticmethod
  def namedtuple_factory(cursor, row):
    t = str.maketrans(
      '() ',
      '___'
    )
    fields = [column[0].translate(t) for column in cursor.description]
    cls = namedtuple("Row", fields)
    return cls._make(row)

  def __init__(self, path, *a, **kw):
    self.conn = sqlite3.connect(path, *a, **kw)
    self.conn.row_factory = self.namedtuple_factory
    self.init()

  def init(self):
    pass

  def close(self):
    self.conn.commit()
    self.conn.close()

  def __enter__(self):
    return self.conn.cursor()

  def __exit__(self, et, ev, tb):
    if ev is None:
      self.conn.commit()
    else:
      self.conn.rollback()


class FlowDB(DB):
  def init(self):
    with self as c:
      c.execute('''
        CREATE TABLE IF NOT EXISTS flow (
          time DATETIME NOT NULL,
          ip_a INTEGER,
          ip_b INTEGER,
          bytes INTEGER NOT NULL
        );
      ''')
      c.execute('CREATE INDEX IF NOT EXISTS index_time ON flow (time);')
      c.execute('CREATE INDEX IF NOT EXISTS index_ip_a ON flow (ip_a);')
      c.execute('CREATE INDEX IF NOT EXISTS index_ip_b ON flow (ip_b);')
      c.execute('CREATE INDEX IF NOT EXISTS index_t_ip_a ON flow (time, ip_a);')
      c.execute('CREATE INDEX IF NOT EXISTS index_t_ip_b ON flow (time, ip_b);')

      c.execute('''
        CREATE TABLE IF NOT EXISTS ipapi (
          time DATETIME NOT NULL,
          ip INTEGER PRIMARY KEY NOT NULL,
          json TEXT
        );
      ''')
      c.execute('CREATE INDEX IF NOT EXISTS index_time ON ipapi (time);')
      # c.execute('CREATE UNIQUE INDEX IF NOT EXISTS index_ip ON ipapi (ip);')

      LOG.info('database ok')
