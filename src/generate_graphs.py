import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import statistics
import sqlite3
import argparse

def get_numbers(dbFile, date_offset):
  db = sqlite3.connect(dbFile)
  dbc = db.cursor()

  query = f'SELECT time, downspeed, upspeed FROM speedtests WHERE date=date("now", "-6 hour", "-{date_offset} day")'
  times = []
  downspeeds = []
  upspeeds = []
  for entry in dbc.execute(query):
    times.append(entry[0])
    downspeeds.append(entry[1])
    upspeeds.append(entry[2])

  dbc.close()

  res_list = [times, downspeeds, upspeeds]
  return res_list

def gen_line_graph(name, times, downspeeds, upspeeds, output):
  # plt.figure(30, 30)
  plt.plot(times, downspeeds, label='download', color='r')
  plt.plot(times, upspeeds, label='upload', color='b')
  if name.find("Daily") != -1:
    plt.xlabel('days ago')
  else:
    plt.xlabel('time')
  plt.ylabel('speed in Mb/s')
  plt.title(name)
  plt.legend()
  plt.savefig(output + "/" + name.lower().replace(' ','_') + ".png", bbox_inches='tight')
  plt.close()


def main(dbFile, output):
  today = get_numbers(dbFile, 0)
  yesterday = get_numbers(dbFile, 1)
  two_days = get_numbers(dbFile, 2)
  three_days = get_numbers(dbFile, 3)
  four_days = get_numbers(dbFile, 4)
  five_days = get_numbers(dbFile, 5)
  six_days = get_numbers(dbFile, 6)
  # seven_days = get_numbers(dbFile, 7)

  gen_line_graph("Today", today[0], today[1], today[2], output)
  gen_line_graph("Yesterday", yesterday[0], yesterday[1], yesterday[2], output)
  gen_line_graph("Two Days Ago", two_days[0], two_days[1], two_days[2], output)

  avg_down = [statistics.mean(yesterday[1]), statistics.mean(two_days[1]), statistics.mean(three_days[1]), statistics.mean(four_days[1]), statistics.mean(five_days[1]), statistics.mean(six_days[1])] #, statistics.mean(seven_days[1])]
  avg_up = [statistics.mean(yesterday[2]), statistics.mean(two_days[2]), statistics.mean(three_days[2]), statistics.mean(four_days[2]), statistics.mean(five_days[2]), statistics.mean(six_days[2])] #, statistics.mean(seven_days[2])]

  gen_line_graph("Daily Average", ["6","5","4","3","2","1"], avg_down, avg_up, output)


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--dbfile", dest="sqliteFile", help="Specify a SQLite File", default="/db/internet_monitor.db")
  parser.add_argument("--output", help="Location to store the generated graphs", default="/output")
  args = parser.parse_args()

  main(args.sqliteFile, args.output)
