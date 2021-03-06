import speedtest
import sqlite3
import argparse


def run_speedtest():
  s = speedtest.Speedtest()
  downspeed = round((round(s.download()) / 1048576), 2)
  upspeed = round((round(s.upload()) / 1048576), 2)

  return downspeed, upspeed

def init_db(dbFile):
  db = sqlite3.connect(dbFile)
  dbc = db.cursor()

  try:
    dbc.execute('SELECT * FROM speedtests;')
  except:
    print("Initiating DB")
    dbc.execute('CREATE TABLE "speedtests" ("entry_num"	INTEGER NOT NULL UNIQUE, "date" TEXT, "time"	TEXT, "downspeed"	INTEGER, "upspeed"	INTEGER, PRIMARY KEY("entry_num" AUTOINCREMENT));')

  db.commit()
  dbc.close()

def update_db(dbFile, downspeed, upspeed):
  db = sqlite3.connect(dbFile)
  dbc = db.cursor()
  
  dbc.execute("INSERT INTO speedtests ('date', 'time', 'downspeed', 'upspeed') VALUES (date('now', '-6 hour'),strftime('%H:%M', 'now', '-6 hour'),  ?, ?);", (downspeed, upspeed))

  db.commit()
  dbc.close()

def clean_db(dbFile):
  db = sqlite3.connect(dbFile)
  dbc = db.cursor()

  dbc.execute("DELETE FROM speedtests WHERE date <= date('now','-30 day')")

  db.commit()
  dbc.close()

def main(dbFile):
  init_db(dbFile)

  print("Executing speed test")
  downspeed, upspeed = run_speedtest()
  print("  Downspeed: %s", downspeed)
  print("  Upspeed: %s", upspeed)
  print("Updating DB with speeds")
  update_db(dbFile, downspeed, upspeed)
  print("Cleaning DB")
  clean_db(dbFile)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--dbfile", dest="sqliteFile", help="Specify a SQLite File", default="/db/internet_monitor.db")
  args = parser.parse_args()

  main(args.sqliteFile)