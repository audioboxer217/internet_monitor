import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import sqlite3
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--dbfile", dest="sqliteFile", help="Specify a SQLite File", default="/db/internet_monitor.db")
parser.add_argument("--output", help="Location to store the generated graphs", default="/output")
args = parser.parse_args()
db = sqlite3.connect(args.sqliteFile)

def get_numbers(type):
  dbc = db.cursor()

  query = f'SELECT {type} FROM speedtests'
  res_list = []
  for entry in dbc.execute(query):
    res_list.append(entry[0])

  dbc.close()

  return res_list

def gen_line_graph(name, times, downspeeds, upspeeds):
  # plt.figure(30, 30)
  plt.plot(times, downspeeds, label='download', color='r')
  plt.plot(times, upspeeds, label='upload', color='b')
  plt.xlabel('time')
  plt.ylabel('speed in Mb/s')
  plt.title(name)
  plt.legend()
  plt.savefig(args.output + "/" + name.lower().replace(' ','_') + ".png", bbox_inches='tight')


def main():
  times = get_numbers('time')
  downspeeds = get_numbers('downspeed')
  upspeeds = get_numbers('upspeed')

  gen_line_graph("Internet Speeds", times, downspeeds, upspeeds)

if __name__ == "__main__":
  main()
