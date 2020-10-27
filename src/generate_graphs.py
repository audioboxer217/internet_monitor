import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import sqlite3
import argparse

def get_numbers(dbFile, type):
  db = sqlite3.connect(dbFile)
  dbc = db.cursor()

  query = f'SELECT {type} FROM speedtests'
  res_list = []
  for entry in dbc.execute(query):
    res_list.append(entry[0])

  dbc.close()

  return res_list

def gen_line_graph(name, times, downspeeds, upspeeds, output):
  # plt.figure(30, 30)
  plt.plot(times, downspeeds, label='download', color='r')
  plt.plot(times, upspeeds, label='upload', color='b')
  plt.xlabel('time')
  plt.ylabel('speed in Mb/s')
  plt.title(name)
  plt.legend()
  plt.savefig(output + "/" + name.lower().replace(' ','_') + ".png", bbox_inches='tight')


def main(dbFile, output):
  times = get_numbers(dbFile, 'time')
  downspeeds = get_numbers(dbFile, 'downspeed')
  upspeeds = get_numbers(dbFile, 'upspeed')

  gen_line_graph("Internet Speeds", times, downspeeds, upspeeds, output)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--dbfile", dest="sqliteFile", help="Specify a SQLite File", default="/db/internet_monitor.db")
  parser.add_argument("--output", help="Location to store the generated graphs", default="/output")
  args = parser.parse_args()

  main(args.sqliteFile, args.output)
