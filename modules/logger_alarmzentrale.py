#!/bin/python3

import sys
import os
from datetime import *
import csv

# Script zum Bereinigen und Füllen des Logfiles
# sys.argv[1] --> event
# sys.argv[2] --> message


# Function to create a CSV line from parameters
def create_csv_line(isodatetime, eventtyp, logmessage):
    return f"{isodatetime};{eventtyp};{logmessage}\n"

# Parameters to create the CSV line from
isodatetime = datetime.now().isoformat()
eventtyp = str(sys.argv[1])
logmessage = str(sys.argv[2])

# logfile
logfile = "/opt/alarmzentrale/logs/logfile.csv"

# Create the CSV line
csv_line = create_csv_line(isodatetime, eventtyp, logmessage)

# Set the maximum number of lines for the CSV file
MAX_LINES = 500

# Write the CSV line to a file
with open(logfile, "r+") as csvfile:
    # Check if the file already contains MAX_LINES lines
    lines = csvfile.readlines()
    if len(lines) > MAX_LINES:
        # If the file is too large, delete the oldest lines (excluding the header)
        csvfile.seek(0)
        csvfile.truncate()
        csvfile.write(lines[0])
        csvfile.write("".join(lines[-(MAX_LINES - 1):]))

    # Append the new line to the file
    csvfile.seek(0, 2)
    if csvfile.tell() == 0:
        # If the file is empty, add the header before the first data line
        csvfile.write("isodatetime;eventtyp;logmessage\n")
    csvfile.write(csv_line)
