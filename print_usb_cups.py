import sys
import os
import cups

conn = cups.Connection()
printers = conn.getPrinters()
for printer in printers:
 print(printer,printers[printer]["device-uri"])
printer_name = printers.keys()[0]
outF = open("/home/pi/Ticket", "w")
#textList = ["\x48","\x65","\x6c","\x6c","\x6f","\x20","\x57","\x6f","\x72","\x6c","\x64","\x21"]
textList = ["\x1D","\xF6",
"\x1D","\x21","\x21",
"\x1B","\x61","\x31",
"\x1D","\x77","\x02",
"\x1D","\x6B","\x04","123456789","\x00",
"\x1B","\x56","\x01",
"\xAE","\x20","\xAE","\x20","\xAE","\x0A",
"\x1B","\x56","\x00",
"POLISPARK","\x0A","\x0A",
"\x1D","\x21","\x11",
"DOUKISSIS","\x0A",
"PLAKENTIAS","\x0A",
"\x0A","\x0A",
"\x1D","\x21","\x00",
"TEL: 217-7000541","\x0A",
"DATE: 04-09-2019","\x0A",
"TIME: 00:00:00","\x0A",
"PLATE: YMN1679","\x0A",
"\x1D","\xF8","\x1B","\x69"]
for line in textList:
  # write line to output file
  outF.write(line)
 # outF.write("\n")
outF.close()
#os.system("lpr -P CUSTOM_Engineering_KPM150-H HelloWorld")
#sys.stdout.write("lpr -P CUSTOM_Engineering_KPM150-H HelloWorld")
fileName = "/home/pi/Ticket"
conn.printFile(printer_name,fileName,"",{})
