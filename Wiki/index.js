keepforce=true;

function waitForMs(ms) {
    return new Promise(resolve => setTimeout(resolve, ms))
}

async function typeSentence(sentence, eleRef, delay = 50, randomamount=300) {
    const letters = sentence.split("");
    let i = 0;
    while(i < letters.length) {
        await waitForMs(delay+Math.random()*randomamount);
        $(eleRef).append(letters[i]);
        i++
    }
    return;
}

async function Clear(spd=0.5){
    $("#console").html("");
    await waitForMs(300*spd);
    $("#console").append("<p>⠀</p>");
    $("#console").append("<p style='text-align:center;'>WELCOME TO THE BASIC++ WIKI</p>");
    await waitForMs(200*spd);
    $("#console").append("<p>⠀</p>");
    $("#console").append('<p style="text-align:center;">TYPE "HELP" FOR A LIST OF COMMANDS</p>');
    $("#console").append("<p>⠀</p>");
    await waitForMs(200*spd);
}

async function Adduserinput(){
    $("#console").append('<span id="userinp"></span><span id="curs"></span>');
}
async function Removeuserinput(){
    $("#userinp").remove();
    $("#curs").remove();
}

async function RunCommand(cmd){
    await Removeuserinput();
    $("#console").append("<p>"+cmd+"</p>");

    $("#type").val("");
    if (cmd=="") {
        $("#console").append("<p>⠀</p>");
    }
    else if (cmd.startsWith("HELP")) {
        $("#console").append("<p>COMMANDS:</p>");
        $("#console").append("<p>CLEAR: CLEARS THE CONSOLE</p>");
        $("#console").append("<p>⠀</p>");
        $("#console").append("<p>BPP [COMMAND]: GET HELP ON A BASIC++ COMMAND</p>");
        $("#console").append("<p>BPP COMMANDS:</p>");
        $("#console").append("<p>• CONSTANTS</p>");
        $("#console").append("<p>• COMMENTS</p>");
        $("#console").append("<p>• EXTENSIONS</p>");
        $("#console").append("<p>• FILEFLAGS</p>");
        $("#console").append("<p>• FLAGS</p>");
        $("#console").append("<p>• FUNCTIONS</p>");
        $("#console").append("<p>• GOTOPOINTERS</p>");
        $("#console").append("<p>• USECONSTANDFUNC</p>");
    }
    else if (cmd.startsWith("CLEAR")) {
        await Clear();
    }
    else if (cmd.startsWith("BPP")) {
        cmd2=cmd.split(" ")[1].replace("\n","");
        if (cmd2=="") {
            $("#console").append("<p>⠀</p>");
            $("#console").append("<p>BPP COMMANDS:</p>");
            $("#console").append("<p>• CONSTANTS</p>");
            $("#console").append("<p>• COMMENTS</p>");
            $("#console").append("<p>• EXTENSIONS</p>");
            $("#console").append("<p>• FILEFLAGS</p>");
            $("#console").append("<p>• FLAGS</p>");
            $("#console").append("<p>• FUNCTIONS</p>");
            $("#console").append("<p>• GOTOPOINTERS</p>");
            $("#console").append("<p>• USECONSTANDFUNC</p>");
        }
        else if (cmd2=="CONSTANTS") {
            $("#console").append("<p>OPENING WIKI...</p>");
            window.open("https://github.com/AGO061/BASICPP/wiki#namevalue---constant-definition---since-r1", "_blank");
        }
        else if (cmd2=="COMMENTS") {
            $("#console").append("<p>OPENING WIKI...</p>");
            window.open("https://github.com/AGO061/BASICPP/wiki#rem-string---comment---since-r1", "_blank");
        }
        else if (cmd2=="EXTENSIONS") {
            $("#console").append("<p>OPENING WIKI...</p>");
            window.open("https://github.com/AGO061/BASICPP/wiki#the-extensions---since-r3", "_blank");
        }
        else if (cmd2=="FILEFLAGS") {
            $("#console").append("<p>OPENING WIKI...</p>");
            window.open("https://github.com/AGO061/BASICPP/wiki#flagsflag-flag----in-file-flags---since-r3", "_blank");
        }
        else if (cmd2=="FLAGS") {
            $("#console").append("<p>OPENING WIKI...</p>");
            window.open("https://github.com/AGO061/BASICPP/wiki#more-on-flags", "_blank");
        }
        else if (cmd2=="FUNCTIONS") {
            $("#console").append("<p>OPENING WIKI...</p>");
            window.open("https://github.com/AGO061/BASICPP/wiki#namecode---function---since-r1", "_blank");
        }
        else if (cmd2=="GOTOPOINTERS") {
            $("#console").append("<p>OPENING WIKI...</p>");
            window.open("https://github.com/AGO061/BASICPP/wiki#name---goto-pointer---since-r1", "_blank");
        }
        else if (cmd2=="USECONSTANDFUNC") {
            $("#console").append("<p>OPENING WIKI...</p>");
            window.open("https://github.com/AGO061/BASICPP/wiki#name---use-functionsconstants---since-r1", "_blank");
        }

        else {
            $("#console").append("<p>⠀</p>");
            $("#console").append("<p>BPP COMMANDS:</p>");
            $("#console").append("<p>• CONSTANTS</p>");
            $("#console").append("<p>• COMMENTS</p>");
            $("#console").append("<p>• EXTENSIONS</p>");
            $("#console").append("<p>• FILEFLAGS</p>");
            $("#console").append("<p>• FLAGS</p>");
            $("#console").append("<p>• FUNCTIONS</p>");
            $("#console").append("<p>• GOTOPOINTERS</p>");
            $("#console").append("<p>• USECONSTANDFUNC</p>");
        }
        } else {
        $("#console").append("<p>?SYNTAX ERROR</p>");
        }
    $("#console").append("<p>⠀</p>");
    await Adduserinput();
    
}

async function Type(){
    hasendline=$("#type").val().includes("\n");
    // allow for multiple lines and all letters and numbers to be typed
    filtered=$("#type").val().toUpperCase().replace(/[^A-Z0-9\n ]/g, "");
    $("#type").val(filtered);
    $("#userinp").text(filtered);
    if (hasendline){
        await RunCommand(filtered)
    }
}
async function ForceFocus(){
    keepforce=true;
    while (keepforce){
        await waitForMs(100);
        $("#type").focus();
        await Type();
    }
    
}



function Unfocus(){
    keepforce=false;
    $("#type").disabled=true;
    $("#type").disabled=false;
}

async function Begin(){
    await typeSentence('LOAD "BASIC++WIKI", 8', "#text");
    $("#console").append("<p>⠀</p>");
    $("#curs").remove();
    await waitForMs(300);
    $("#console").append("<p>SEARCHING FOR BASIC++WIKI</p>");
    await waitForMs(1000);
    $("#console").append("<p>LOADING</p>");
    await waitForMs(2000);
    $("#console").append("<p>READY.</p>");
    $("#console").append('<span id="runtxt"></span><span id="curs"></span>');
    await typeSentence("RUN", "#runtxt");
    await waitForMs(1000);
    await Clear()
    $("#console").append('<span id="userinp"></span><span id="curs"></span>');
    ForceFocus();
}
Begin();