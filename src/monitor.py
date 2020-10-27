import speedtest
import datetime
import sqlite3
import argparse


def update_db(dbFile, downspeed, upspeed):
  db = sqlite3.connect(dbFile)
  dbc = db.cursor()
  
  dbc.execute("INSERT INTO speedtests ('time', 'downspeed', 'upspeed') VALUES (datetime('now'), ?, ?);", (downspeed, upspeed))

  db.commit()
  dbc.close()

def clean_db(dbFile):
  db = sqlite3.connect(dbFile)
  dbc = db.cursor()

  dbc.execute("DELETE FROM speedtests WHERE time <= datetime('now','-30 day')")

  db.commit()
  dbc.close()

def main(dbFile):
  s = speedtest.Speedtest()
  downspeed = round((round(s.download()) / 1048576), 2)
  upspeed = round((round(s.upload()) / 1048576), 2)

  update_db(dbFile, downspeed, upspeed)
  clean_db(args.sqliteFile)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--dbfile", dest="sqliteFile", help="Specify a SQLite File", default="/db/internet_monitor.db")
  args = parser.parse_args()

  main(args.sqliteFile)