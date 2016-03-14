#!/usr/bin/python3
import os
import csv
import sys
import getopt
import logging
import logging.config

def readCsvFile(filename):
   if os.path.isfile(filename):
      with open(filename, newline='') as csvFile:
         data = list(csv.reader(csvFile, delimiter='\t', quotechar='"'))
   else:
      # logger.error("Failed to open {}!".format(filename))
      print("Failed to open {}!".format(filename))

   return data

def filterData(data, upperMatch, lowerMatch, minLength):
   filtered = []
   for row in data:
      if float(row[2]) > lowerMatch and float(row[2]) < upperMatch and float(row[3]) > minLength:
         filtered.append(row)

   return filtered

def matchData(data1, data2):
   matched = []
   for row1 in data1:
      for row2 in data2:
         if row1[0] == row2[0]:
            matched.append(row1)
#            matched.append(row2)

   return matched

def main(argv):
   try:
      opts, args = getopt.getopt(argv, "hvd", ["help", "version", "debug", "upper-match=", "lower-match=", "min-length="])

      print(opts)
      print(args)
   except getopt.GetoptError as err:
      # Print usage information and exit.
      print(err)
      usage()
      sys.exit(2)

   debugging = False
   upperMatch = 90
   lowerMatch = 80
   minLength = 500

   for o, a in opts:
      if o in ("-h", "--help"):
         usage()
         sys.exit(1)
      elif o in ("-v", "--version"):
         print("Version 0.1")
         sys.exit(1)
      elif o in ("-d", "--debug"):
         debugging = True
      elif o in ("--upper-match"):
         upperMatch = float(a)
      elif o in ("--lower-match"):
         lowerMatch = float(a)
      elif o in ("--min-length"):
         minLength = float(a)
      else:
         assert False, "unhandled option"

   # Inititalize the logging api ...
   logging.config.fileConfig('config/logging.conf')

   # ... and fetch a logger.
   if debugging:
      logger = logging.getLogger('development')
   else:
      logger = logging.getLogger('production')	

   # Check given bounds.
   if upperMatch < 0 or upperMatch > 100:
      logger.error("Upper Match must be in range [0, 100]!")

   if upperMatch < 0 or upperMatch > 100:
      logger.error("Lower Match must be in range [0, 100]!")
   
   if upperMatch < lowerMatch:
      logger.error("Upper match has to be greater than lower match!")

   filteredData = []
   for filename in args:
      data = readCsvFile(filename)
      filteredData.append(filterData(data, upperMatch, lowerMatch, minLength))

   resultData = matchData(filteredData[0], filteredData[1])

   for row in resultData:
      print(", ".join(row))

   print("\n----------------------------------\n")

if __name__ == "__main__":
	main(sys.argv[1:])
