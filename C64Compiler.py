import sys
import re
errors=0
step=10

try:
    fl=sys.argv[1]
    if not fl.split(".")[1]=="bas":
        input("Only .bas files are accepted")
        exit()
except:
    input("Please choose a .bas file to compile")
    exit()

print("Parsing flags...")

if "-ur" in sys.argv:
    userem=True
else:
    userem=False

if "-rmc" in sys.argv:
    usecolumn=False
else:
    usecolumn=True

if "-kc" in sys.argv:
    keepcomments=True
else:
    keepcomments=False

print("Running first parse...")
f=open(fl,"r")
code=f.read()
f.close()
functions={}
result = re.findall('///{(.*?)}///', code,flags=re.S)
funcnum=code.count("///{")
if not funcnum==code.count("}///"):
    print("One or more functions were not closed or opened")
    errors+=1
for i in result:
    functions[i.split("\n",1)[0]]=i.split("\n",1)[1]
    code=code.replace("///{"+i+"}///","")


#first parse, for stuff that has to change before parsing
code=code.replace("\n","§ò*§").split("§ò*§")
c=[]
for line in code:
    for func in functions:
        if f"///{func}///" in line:
            line=line.replace(f"///{func}///",functions[func])
    c.append(line)
code="\n".join(c)




if usecolumn:
    code=code.replace("\n","§ò*§").split("§ò*§")
else:
    code=code.replace("\n","§ò*§").replace(":","§ò*§").split("§ò*§")
i=1

out=open(fl.split(".")[0]+".cbas","w")
out.write("")
out.close()

out=open(fl.split(".")[0]+".cbas","a")

bases=[]
lines=[]


constants={}

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

    elif line.startswith("///;"):
        i+=int(line.split("///;")[1])

    elif line.startswith("rem") and not keepcomments:
        pass

    else:
        out.write(str(i*step)+" "+line+"\n")
        i+=1
    
    

out.close()

input("Compilation complete! Errors:"+str(errors))