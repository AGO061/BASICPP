import sys
import re
errors=0
warnings=0
step=10
def quit(status=""):
    print(u"\u001b[31m"+status+"\u001b[0m")
    sys.exit()

try:
    fl=sys.argv[1]
    if not fl.split(".")[1]=="bpp":
        input("Please choose a .bpp file to compile")
        quit("Error: No file chosen") 
except:
    input("Please choose a .bpp file to compile")
    quit("Error: No file chosen")

print("Parsing flags...")
with open(fl) as f:
    args = f.readline().rstrip()
if "///FLAGS:" in args:
    fileflags=True
    print("Found args in file, ignoring command line flags")
    args=args.replace("///FLAGS:","").split(" ")
else:
    fileflags=False
    args=sys.argv


userem="-ur" in args or "--userem" in args
usecolumn= not ("-rmc" in args or "--removecolon" in args)
keepcomments="-kc" in args or "--keepcomments" in args
run="-r" in args or "--run" in args
printerrors= not ("-ne" in args or "--noerrors" in args)


print("Running first parse...")
f=open(fl,"r")
code=f.read()
f.close()

print("Parsing functions...")
functions={}
result = re.findall('///{(.*?)}///', code,flags=re.S)
funcnum=code.count("///{")
if not funcnum==code.count("}///"):
    print("ERROR: One or more functions were not closed or opened")
    errors+=1
for i in result:
    functions[i.split("\n",1)[0]]=i.split("\n",1)[1]
    code=code.replace("///{"+i+"}///","")


#first parse, for stuff that has to change before parsing
code=code.split("\n")
if (fileflags):
    code=code[1:]
c=[]
for line in code:
    for func in functions:
        if f"///{func}///" in line:
            line=line.replace(f"///{func}///",functions[func])
    c.append(line)
code="\n".join(c)




if usecolumn:
    code=code.split("\n")
else:
    code=code.replace("\n","§ò*§").replace(":","§ò*§").split("§ò*§")
i=1

out=open(fl.split(".")[0]+".bas","w")
out.write("")
out.close()

out=open(fl.split(".")[0]+".bas","a")

bases=[]
lines=[]


constants={ #setup predefined constants
    # c64 colors for poking
    "black":"0",
    "white":"1",
    "red":"2",
    "cyan":"3",
    "purple":"4",
    "green":"5",
    "blue":"6",
    "yellow":"7",
    "orange":"8",
    "brown":"9",
    "lightred":"10",
    "darkgray":"11",
    "gray":"12",
    "lightgreen":"13",
    "lightblue":"14",
    "lightgray":"15",
    #c64 color address
    "txtcolor":"646",
    "framecolor":"53280",
    "bgcolor":"53281",
    #screen memory addresses
    "charmemory":"1024",
    "colormemory":"55296",
    #useful functions
    "clear":"print chr$(147)"
}

print("Running second parse...")

for line in code: # adding bases and lines
    line=line.lstrip(' ') #removing the indents

    

    if line.startswith("///."):
            bases.append(line.split("///.")[1])
            lines.append(i*step)
            if userem==False:
                i-=1
    
    if line=="":
        pass


    elif line.startswith("///,"):
        constants[line.replace("///,","").split("=",1)[0]]=line.replace("///,","").split("=",1)[1]


    elif line.startswith("///;"):
        i+=int(line.split("///;")[1])

    elif line.startswith("rem"):
        pass

    else:
        i+=1

c=1
i=1
print("Parsing code...")
for line in code:
    line=line.lstrip(' ') #removing the indents
    try:
        linee=line.split("goto ") #adding line number instead of the code
        line=linee[0]+"goto "+str(lines[bases.index(linee[1])])
    except:
        pass

    for const in constants: #parse constants
        if f"///{const}///" in line:
            line=constants[const].join(line.split(f"///{const}///"))
    
    

    if line=="":
        pass

    elif line.startswith("///."):
        if userem==True:
            out.write(str(i*step)+" "+"rem "+line.split("///.")[1]+"\n")
            i+=1
        else:
            pass
    
    elif line.startswith("///,"):
        pass
    
    elif line.startswith("///FLAGS:"):
        pass

    
    elif line.startswith("///;"):
        i+=int(line.split("///;")[1])

    elif line.startswith("rem") and not keepcomments:
        pass

    elif "///" in line:
        print("ERROR: There was an error processing all the compiler commands! at line:",c)
        errors+=1

    else:
        out.write(str(i*step)+" "+line+"\n")
        i+=1
    c+=1
    
if run:
    out.write("run\n")

out.close()

outp="\u001b[32mCompilation complete! \u001b[31mErrors: "+str(errors)+" \u001b[33mWarnings: "+str(warnings)
if printerrors: input(outp)
else: quit(outp)