import re
import sys

# STATUS 1 NO FILE CHOSEN
# STATUS 2 WRONG FILE EXTENSION

# Compiler output information
outinfo = {"errors": 0, "warnings": 0, "info": ""}
# Program specific data
programdata = {
    "fileflags": False,
    "args": [],
    "step": 10,
    "functions": {},
    "constants": {},
    "pointers": {}
}


# Defining base functions
def quit(status="", errorcode=1):  # Print status in red, then quit
  print(u"\u001b[31m" + status + "\u001b[0m")
  sys.exit(errorcode)


def prgend():
  outp = "\u001b[32mCompilation complete! \u001b[31mErrors: " + str(
      outinfo["errors"]) + " \u001b[33mWarnings: " + str(
          outinfo["warnings"]) + "\u001b[0m"
  print("\n" + outp)
  if outinfo["errors"] > 0:
    print(
        "\u001b[31m" +
        "Compiler encountered too many errors, please fix and retry compiling"
        + "\u001b[0m")
  quit("", 0)


# Check if input file has been chosen
infile = ""  # Input file name
try:
  infile = sys.argv[1]
  if infile.split(".")[-1] != "bpp":
    quit("Error: Wrong file extension", 2)
except (IndexError, FileNotFoundError):
  quit("Error: No file chosen", 1)

print("Parsing flags...")

with open(infile) as f:
  args = f.readline().rstrip()

if "///FLAGS:" in args:
  programdata["fileflags"] = True
  print("Found flags in file, ignoring command line flags")
  programdata["args"] = args.replace("///FLAGS:", "").split(" ")
else:
  programdata["args"] = sys.argv[2:]

flags = {
    "userem": "-ur" in args or "--userem" in args,
    "removecolon": not ("-rmc" in args or "--removecolon" in args),
    "keepcomments": "-kc" in args or "--keepcomments" in args,
    "run": "-r" in args or "--run" in args,
    "printerrors": not ("-ne" in args or "--noerrors" in args)
}

del args  # removing args variable as we don't need it

with open(infile, "r") as f:  # opening the code

  code = ""
  splitcode = f.read().split("\n")
  newcode = []

  for i in splitcode:
    if "///FLAGS" not in i:
      newcode.append(i)

  code = "\n".join(newcode)
  if flags["removecolon"]:  # Replacing colons with newlines if needed
    code = code.replace(":", "\n")

print("Parsing Constants/Functions...")

result = re.findall('///{(.*?)}///', code, flags=re.S)

funcnum = code.count("///{")

if funcnum != code.count("}///"):
  print("ERROR: One or more functions were not closed or opened")
  outinfo["errors"] += 1
for i in result:
  name = i.split("\n", 1)[0]
  value = i.split("\n", 1)[1]
  programdata["functions"][name] = value
  code = code.replace("///{" + i + "}///", "")  # Delete definition
  code = code.replace("///" + name + "///", value)  # Replace with value

del funcnum  # remove unused

# At this point the variable "code" contains the code with functions replaced
#Let's work on constants now

# Predefined constants
programdata["constants"] = {  #setup predefined constants
    # c64 colors for poking
    "black": "0",
    "white": "1",
    "red": "2",
    "cyan": "3",
    "purple": "4",
    "green": "5",
    "blue": "6",
    "yellow": "7",
    "orange": "8",
    "brown": "9",
    "lightred": "10",
    "darkgray": "11",
    "gray": "12",
    "lightgreen": "13",
    "lightblue": "14",
    "lightgray": "15",
    #c64 color address
    "txtcolor": "646",
    "framecolor": "53280",
    "bgcolor": "53281",
    #screen memory addresses
    "charmemory": "1024",
    "colormemory": "55296",
    #useful functions
    "clear": "print chr$(147)"
}

# find all the constant definitions using regex
result = re.findall(r'(///,\s*(.*?)\s*=\s*(.*))', code)

for i in result:
  programdata["constants"][i[1]] = i[2]
  code = code.replace(i[0], "")

# Now find the remaining usages and return an error if there are any undefined calls
result = re.findall('///([^.,;].*)///', code)

for i in result:
  try:
    code = code.replace("///" + i + "///", programdata["constants"][i])
  except KeyError:
    code = code.replace("///" + i + "///", "")
    print("ERROR: Constant/Function definition of \"" + i + "\" not found")
    outinfo["errors"] += 1
del result

# Finishing touches with line by line processing
code = code.split("\n")
currentline = programdata["step"]
currentstep = 1

if outinfo["errors"] > 0:
  prgend()  # end programs because there are too many errors

outname = ".".join(infile.split(".")[:-1]) + ".bas"
with open(outname, "w") as outfile:  # wipe output file before use
  outfile.write("")
for line in code:
  line.lstrip(" \t")  # remove indentation
  line.rstrip(" \t")  # remove right spaces

  if line == "":
    pass

  else:
    print("Line parsing progress [" + "#" * int(currentstep / len(code) * 20) +
          " " * (20 - int(currentstep / len(code) * 20)) + "]",
          end="\r")
    if "rem" in line:  # Remove rems
      result = re.findall(r"rem\s+.*", line)
      if result:
        line = line.replace(result[0], "")

    # Line skip manager
    result = re.findall(r"(///;\s*([^ ]*))", line)
    if result:
      currentline -= programdata["step"]
    for i in result:
      line = line.replace(i[0], "")
      currentline += int(i[1])
    if line == "":
      line = " "
    # Goto pointers manager
    result = re.findall(r"(///\.\s*([^ ]*))", line)
    pointernames = ""
    for i in result:
      programdata["pointers"][i[1]] = currentline
      line = line.replace(i[0], "")
      pointernames += i[1] + ", "
    if line == "":  # add rem in case it gets cleared
      line = "rem pointer " + pointernames.rstrip(", ")
    del result

    # Write to file
    if line.rstrip(" \t") != "":
      with open(outname, "a") as out:
        out.write(str(currentline) + " " + line + "\n")
      currentline += programdata["step"]
  currentstep += 1

# manage goto pointers in a separate file run as they need to work up and down the file
with open(outname, "r") as outfile:
  code = outfile.read()
  code = code.split("\n")
codeout = []
for line in code:
  if "goto" in line:
    result = re.findall(r"goto\s+([^ ]*)", line)
    for i in result:
      line = line.replace(i, str(programdata["pointers"][i]))
  codeout.append(line)
with open(outname, "w") as out:
  out.write("\n".join(codeout))
prgend()
