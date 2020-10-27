import argparse
import generate_graphs
import monitor

def main(dbFile, output):
  monitor.main(dbFile)
  generate_graphs.main(dbFile, output)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--dbfile", dest="sqliteFile", help="Specify a SQLite File", default="/db/internet_monitor.db")
  parser.add_argument("--output", help="Location to store the generated graphs", default="/output")
  args = parser.parse_args()

  main(args.sqliteFile, args.output)