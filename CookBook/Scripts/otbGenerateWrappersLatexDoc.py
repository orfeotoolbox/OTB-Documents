#!/usr/bin/python
import otbApplication
import os
import sys
import glob
from optparse import OptionParser

##############################################################################
# Parameters
linesep = os.linesep
tagslevel = "\\section"
applevel ="\\subsection"
appdetailslevel = "\\subsubsection"
paramlevel = "\\paragraph"
pixeltypes = {' uchar' : 1, ' int8' : 0, ' uint8' : 1, ' int16' : 2, ' uint16': 3, ' int32' : 4, ' uint32' : 5, ' float' : 6, ' double': 7}

def ConvertString(s):
    '''Convert a string for compatibility in txt dump'''
    s = s.replace('\n', '\\\\ ')
    s = s.replace('_', '\\_')
    return s

def EncloseString(s):
    if not s.startswith("\"") :
        s = "\"" + s
    if not s.endswith("\""):
        s = s + "\""
    return s

def ExpandPath(filename,path,exp):
    if not exp:
        return filename
    else:
        # Avoid chasing our tails
        (head,tail) = os.path.split(filename)
        if len(tail) > 0:
            filename = tail
        for dir,dirs,files in os.walk(path):
            for file in files:
                if file == filename:
                    return os.path.join(dir,file)
        return os.path.join(path,filename)

def GetPixelType(value):
    # look for type
    foundcode = -1
    foundname = ""
    for ptypename, ptypecode in pixeltypes.iteritems():
        if value.endswith(ptypename):
            foundcode = ptypecode
            foundname = ptypename
            break
    return foundcode,foundname

def GetParametersDepth(paramlist):
    depth = 0
    for param in paramlist:
        depth = max(param.count("."),depth)
    return depth

def GenerateChoice(app,param):
    output = "Available choices are: " + linesep
    output+= "\\begin{itemize}" + linesep
    for (choicekey,choicename) in zip(app.GetChoiceKeys(param),app.GetChoiceNames(param)):
        output += "\\item \\textbf{"+ ConvertString(choicename) + "}"
        choicedesc = app.GetParameterDescription(param+"."+choicekey)
        if len(choicedesc) >= 2:
            output+= ": " + choicedesc + linesep
    output+= "\\end{itemize}" + linesep
    return output

def GenerateParameterType(app,param):
    if app.GetParameterType(param) == otbApplication.ParameterType_ListView:
        return "List"
    if app.GetParameterType(param) == otbApplication.ParameterType_Group:
        return "Group"
    if app.GetParameterType(param) ==  otbApplication.ParameterType_Choice:
        return "Choices"
    if app.GetParameterType(param) == otbApplication.ParameterType_Empty:
        return "Boolean"
    if app.GetParameterType(param) == otbApplication.ParameterType_Int \
       or app.GetParameterType(param) == otbApplication.ParameterType_Radius \
       or app.GetParameterType(param) == otbApplication.ParameterType_RAM:
        return "Int"
    if app.GetParameterType(param) == otbApplication.ParameterType_Float:
        return "Float"
    if app.GetParameterType(param) == otbApplication.ParameterType_String:
        return "String"
    if app.GetParameterType(param) == otbApplication.ParameterType_StringList:
        return "String list"
    if app.GetParameterType(param) == otbApplication.ParameterType_Filename :
        return "File name"
    if app.GetParameterType(param) == otbApplication.ParameterType_Directory :
        return "Directory"
    if app.GetParameterType(param) == otbApplication.ParameterType_InputImage \
            or app.GetParameterType(param) == otbApplication.ParameterType_ComplexInputImage:
        return "Input image"
    if app.GetParameterType(param) == otbApplication.ParameterType_InputVectorData:
        return "Input vector data"
    if app.GetParameterType(param) == otbApplication.ParameterType_OutputImage \
            or app.GetParameterType(param) == otbApplication.ParameterType_ComplexOutputImage :
        return "Output image"
    if app.GetParameterType(param) == otbApplication.ParameterType_OutputVectorData:
        return "Output vector data"
    if app.GetParameterType(param) == otbApplication.ParameterType_InputImageList:
        return "Input image list"
    if app.GetParameterType(param) == otbApplication.ParameterType_InputVectorDataList:
        return "Input vector data list"

def GenerateParametersTable(app,paramlist,label):
    output = "\\begin{table}[!htbp]" + linesep
    output += "\\begin{center}" + linesep
    output += "\\begin{small}" + linesep
    output += "\\begin{tabular}{|p{0.4\\textwidth}|l|p{0.4\\textwidth}|}" + linesep
    output += "\\hline" + linesep
    output += "Parameter key & Parameter type & Parameter description \\\\" + linesep
    output += "\\hline" + linesep
    for param in paramlist:
        output+= "\\verb|"+param + "| & "
        output += GenerateParameterType(app,param) + " & "
        output+= ConvertString(app.GetParameterName(param)) + "\\\\" + linesep
        if app.GetParameterType(param) ==  otbApplication.ParameterType_Choice:
            for (choicekey,choicename) in zip(app.GetChoiceKeys(param),app.GetChoiceNames(param)):
                output +="\\verb|" + param + " " + choicekey +"| & \\emph{Choice} & " + choicename + "\\\\" + linesep
    output += "\\hline" + linesep
    output += "\\end{tabular}"
    output += "\\end{small}" + linesep
    output += "\\end{center}" + linesep
    output += "\\caption{Parameters table for " + ConvertString(app.GetDocName()) + ".} "
    output += "\\label{" + label + "}" + linesep
    output += "\\end{table} " + linesep
    return output

def unique(seq): 
    # order preserving
    checked = []
    for e in seq:
        if e not in checked:
            checked.append(e)
    return checked

def ApplicationParametersToLatex(app,paramlist,deep = False,current=""):
    output = ""
    # First run
    if len(current)==0:
        label = ConvertString(app.GetName())+"_param_table"
        output += "This section describes in details the parameters available for this application. Table~\\ref{" + label + "}, page~\\pageref{" + label + "} presents a summary of these parameters and the parameters keys to be used in command-line and programming languages. Application key is \\verb+" + ConvertString(app.GetName()) + "+."  + linesep
        output += GenerateParametersTable(app,paramlist,label)
        firstlevelparams = []
        for param in paramlist:
            paramsplit = param.partition(".")
            firstlevelparams.append(paramsplit[0])
        firstlevelparams = unique(firstlevelparams)
        if deep:
            for param in firstlevelparams:
                output += paramlevel + "{" + ConvertString(app.GetParameterName(param)) + "}" + linesep
                output += ConvertString(app.GetParameterDescription(param)) + linesep
                if app.GetParameterType(param) ==  otbApplication.ParameterType_Choice:
                    output += GenerateChoice(app,param)
                output += ApplicationParametersToLatex(app,paramlist,deep,param)
        else:
            output+= "\\begin{itemize}" + linesep
            for param in firstlevelparams:
                output+= "\\item \\textbf{"+ ConvertString(app.GetParameterName(param))+ ": } " + ConvertString(app.GetParameterDescription(param)) + linesep
                if app.GetParameterType(param) ==  otbApplication.ParameterType_Choice:
                    output += GenerateChoice(app,param)
            output+= "\\end{itemize}" + linesep
    else:
        currentlevelparams = []
        for param in paramlist:
            if param.startswith(current+".") and param.count(".") == current.count(".")+1:
                currentlevelparams.append(param)
        if len(currentlevelparams) > 0:
            output+= "\\begin{itemize}" + linesep
            for param in currentlevelparams:
                output+= "\\item \\textbf{"+ ConvertString(app.GetParameterName(param))+ ": } " + ConvertString(app.GetParameterDescription(param)) + linesep
                output+= ApplicationParametersToLatex(app,paramlist,deep,param) + linesep
                if app.GetParameterType(param) ==  otbApplication.ParameterType_Choice:
                    output += GenerateChoice(app,param) 
            output+= "\\end{itemize}" + linesep
    return output

def GetApplicationExampleCommandLine(app,idx):
    output= "\\begin{lstlisting}[language=ksh,breaklines=true,breakatwhitespace=true,frame = tb,framerule = 0.25pt,fontadjust,backgroundcolor={\\color{listlightgray}},basicstyle = {\\ttfamily\\scriptsize},keywordstyle = {\\ttfamily\\color{listkeyword}\\textbf},identifierstyle = {\\ttfamily},commentstyle = {\\ttfamily\\color{listcomment}\\textit},stringstyle = {\\ttfamily},showstringspaces = false,showtabs = false,numbers = none,numbersep = 6pt, numberstyle={\\ttfamily\\color{listnumbers}},tabsize = 2]" + linesep
    output+= "otbcli_" + ConvertString(app.GetName())
    for i in range(0, app.GetExampleNumberOfParameters(idx)):
        output+=" -" + app.GetExampleParameterKey(idx,i)+ " " + app.GetExampleParameterValue(idx,i)
    output += linesep
    output+= "\\end{lstlisting}" + linesep
    return output

def GetApplicationExamplePythonSnippet(app,idx,expand = False, inputpath="",outputpath=""):
    appname = app.GetName()
    printable = []
    output= "#!/usr/bin/python" + linesep
    output+= linesep
    output+= "# Import the otb applications package" + linesep
    output+= "import otbApplication" + linesep + linesep
    output+= "# The following line creates an instance of the " + ConvertString(app.GetName()) + " application " + linesep
    output+= ConvertString(app.GetName()) + " = otbApplication.Registry.CreateApplication(\"" + ConvertString(app.GetName()) + "\")" + linesep + linesep 
    output+= "# The following lines set all the application parameters:" + linesep
    for i in range(0, app.GetExampleNumberOfParameters(idx)):
        param = app.GetExampleParameterKey(idx,i)
        value = app.GetExampleParameterValue(idx,i)
        paramtype = app.GetParameterType(param)
        paramrole = app.GetParameterRole(param)
        if paramtype == otbApplication.ParameterType_ListView:
            break
        if paramtype == otbApplication.ParameterType_Group:
            break
        if paramtype ==  otbApplication.ParameterType_Choice:
            #app.SetParameterString(param,value)
            output+= appname + ".SetParameterString(" + EncloseString(param) + "," + EncloseString(value) + ")" + linesep
        if paramtype == otbApplication.ParameterType_Empty:
            app.SetParameterString(param,"1")
            output+= appname + ".SetParameterString("+EncloseString(param)+",\"1\")" + linesep
        if paramtype == otbApplication.ParameterType_Int \
                or paramtype == otbApplication.ParameterType_Radius \
                or paramtype == otbApplication.ParameterType_RAM:
            # app.SetParameterString(param,value)
            output += appname + ".SetParameterInt("+EncloseString(param)+", "+value+")" + linesep
        if paramtype == otbApplication.ParameterType_Float:
            # app.SetParameterString(param,value)
            output += appname + ".SetParameterFloat("+EncloseString(param)+", "+value + ")" + linesep
        if paramtype == otbApplication.ParameterType_String:
            # app.SetParameterString(param,value)
            output+= appname + ".SetParameterString("+EncloseString(param)+", "+EncloseString(value)+")" + linesep
        if paramtype == otbApplication.ParameterType_StringList:
            values = value.split(" ")
            # app.SetParameterStringList(param,values)
            output += appname + ".SetParameterStringList("+EncloseString(param)+", "+str(values)+")" + linesep
        if paramtype == otbApplication.ParameterType_Filename \
            or paramtype == otbApplication.ParameterType_Directory:
            if paramrole == 0:
                # app.SetParameterString(param,EncloseString(ExpandPath(value,inputpath,expand)))
                output += appname + ".SetParameterString("+EncloseString(param)+", "+EncloseString(ExpandPath(value,inputpath,expand)) + ")" + linesep
                printable.append(["in","file",ExpandPath(value,inputpath,expand)])
            elif paramrole == 1:
                # app.SetParameterString(param,EncloseString(ExpandPath(value,outputpath,expand)))
                output += appname + ".SetParameterString("+EncloseString(param)+", "+EncloseString(ExpandPath(value,outputpath,expand))+")" + linesep
                printable.append(["out","file",ExpandPath(value,inputpath,expand)])
        if paramtype == otbApplication.ParameterType_InputImage :
            # app.SetParameterString(param,EncloseString(ExpandPath(value,inputpath,expand)))
            output += appname + ".SetParameterString("+EncloseString(param)+", "+EncloseString(ExpandPath(value,inputpath,expand))+")"+linesep
            printable.append(["in","img",ExpandPath(value,inputpath,expand)])
        if paramtype == otbApplication.ParameterType_ComplexInputImage:
            # app.SetParameterString(param,EncloseString(ExpandPath(value,inputpath,expand)))
            output += appname + ".SetParameterString("+EncloseString(param)+", "+EncloseString(ExpandPath(value,inputpath,expand))+")" + linesep
            printable.append(["in","cimg",ExpandPath(value,inputpath,expand)])
        if paramtype == otbApplication.ParameterType_InputVectorData:
            # app.SetParameterString(param,EncloseString(ExpandPath(value,inputpath,expand)))
            output += appname + ".SetParameterString("+EncloseString(param)+", "+EncloseString(ExpandPath(value,inputpath,expand))+")" + linesep
            printable.append(["in","vdata",ExpandPath(value,inputpath,expand)])
        if paramtype == otbApplication.ParameterType_OutputImage :
            foundcode,foundname = GetPixelType(value)
            if foundcode != -1:
                # app.SetParameterString(param,EncloseString(ExpandPath(value[:-len(foundname),outputpath,expand))))
                output += appname + ".SetParameterString("+EncloseString(param)+", "+EncloseString(ExpandPath(value[:-len(foundname)],outputpath,expand))+")" + linesep
           #app.SetParameterOutputImagePixelType(param,foundcode)
                if foundcode == 1:
                    printable.append(["out","ucimg",ExpandPath(value[:len(foundname)],inputpath,expand)])
                else:
                    printable.append(["out","img",ExpandPath(value[:len(foundname)],inputpath,expand)])
                output += appname + ".SetParameterOutputImagePixelType("+EncloseString(param)+", "+str(foundcode)+")" + linesep
            else:
                # app.SetParameterString(param,EncloseString(ExpandPath(value,outputpath,expand)))
                output += appname +".SetParameterString("+EncloseString(param)+", "+ EncloseString(ExpandPath(value,outputpath,expand)) + ")" + linesep
                printable.append(["out","img",ExpandPath(value,outputpath,expand)])
        if paramtype == otbApplication.ParameterType_ComplexOutputImage :
            # TODO: handle complex type properly
            # app.SetParameterString(param,EncloseString(ExpandPath(value,outputpath,expand)))
            output += appname +".SetParameterString("+EncloseString(param)+", "+ EncloseString(ExpandPath(value,outputpath,expand)) + ")" + linesep
            printable.append(["out","cimg",ExpandPath(value,outputpath,expand)])
        if paramtype == otbApplication.ParameterType_OutputVectorData:
            # app.SetParameterString(param,EncloseString(ExpandPath(value,outputpath,expand)))
            output += appname +".SetParameterString("+EncloseString(param)+", "+ EncloseString(ExpandPath(value,outputpath,expand)) + ")" + linesep
            printable.append(["out","vdata",ExpandPath(value,outputpath,expand)])
        if paramtype == otbApplication.ParameterType_InputImageList:
            values = value.split(" ")
            values = [ExpandPath(val,inputpath,expand) for val in values]
            # app.SetParameterStringList(param,values)
            output += appname + ".SetParameterStringList("+EncloseString(param) + ", " + str(values) + ")" + linesep 
        if paramtype == otbApplication.ParameterType_InputVectorDataList:
            values = value.split(" ")
            values = [ExpandPath(val,inputpath,expand) for val in values]
#app.SetParameterStringList(param,values)
            output += appname + ".SetParameterStringList("+EncloseString(param)+ ", " + str(values) + ")" + linesep 
        output+=linesep
    output += "# The following line execute the application" + linesep
    output+= appname + ".ExecuteAndWriteOutput()"+ linesep
    return output,printable

def GetApplicationExamplePython(app,idx):
    output= "\\begin{lstlisting}[language=python,breaklines=true,breakatwhitespace=true,frame = tb,framerule = 0.25pt,fontadjust,backgroundcolor={\\color{listlightgray}},basicstyle = {\\ttfamily\\scriptsize},keywordstyle = {\\ttfamily\\color{listkeyword}\\textbf},identifierstyle = {\\ttfamily},commentstyle = {\\ttfamily\\color{listcomment}\\textit},stringstyle = {\\ttfamily},showstringspaces = false,showtabs = false,numbers = none,numbersep = 6pt, numberstyle={\\ttfamily\\color{listnumbers}},tabsize = 2]" + linesep
    script,printable = GetApplicationExamplePythonSnippet(app,idx)
    output += script
    output+= "\\end{lstlisting}" + linesep
    return output

def GetApplicationExampleResults(app,idx):
    pyscript,printable = GetApplicationExamplePythonSnippet(app,idx,True,"/home/jmichel/Projets/otb/src/OTB-Data","/home/jmichel/Temporary/wrappers-doc/outputs")
    #scriptfilename = "pyscripts/"+ConvertString(app.GetName())+str(idx)+".py"
    #scriptfile = open(scriptfilename,'w')
    #scriptfile.write(pyscript)
    #scriptfile.close()
    print "Generating outputs for example "+ str(idx+1) + " of application "+app.GetName() + "..."
    try:
        exec pyscript
        print "Printable results are : ", printable
        print "Done."
    except:
        print "Failed."
        pass

def ApplicationToLatex(appname):
    output = ""
    app = otbApplication.Registry.CreateApplication(appname)
    # TODO: remove this when bug 440 is fixed
    app.Init()
    output += applevel + "{" + ConvertString(app.GetDocName()) + "}" + "\\label{app:" + appname + "}" + linesep
    output += ConvertString(app.GetDescription()) + linesep
    output += appdetailslevel + "{Detailed description}" + "\\label{appdesc:" + appname + "}" + linesep
    output += ConvertString(app.GetDocLongDescription()) + linesep
    limitations = app.GetDocLimitations()
    output += appdetailslevel + "{Parameters}" + "\\label{appparam:" + appname + "}" + linesep
    depth = GetParametersDepth(app.GetParametersKeys())
    deep = depth > 0
    output += ApplicationParametersToLatex(app,app.GetParametersKeys(),deep) + linesep
    if app.GetNumberOfExamples() > 1:
        output += appdetailslevel + "{Examples}" + "\\label{appexamples:" + appname + "}" + linesep
        for i in range(0,app.GetNumberOfExamples()):
            output += paramlevel + "{Example " + str(i+1) +"}" + "\\label{appexample:" + appname + str(i+1) +"}" + linesep
            output += app.GetExampleComment(i)
            label = ConvertString(app.GetName()) + "clex" + str(i+1)
            pylabel = ConvertString(app.GetName()) + "pyex" + str(i+1)
            output+= "To run this example in command-line, use the following: " + linesep
            output += GetApplicationExampleCommandLine(app,i)
            output+= "To run this example from Python, use the following code snippet: " + linesep
            output += GetApplicationExamplePython(app,i)
    elif app.GetNumberOfExamples() == 1:
        output += appdetailslevel + "{Example}" + "\\label{appexample:" + appname + "}" + linesep
        if( len(app.GetExampleComment(0)) > 1):
            output += app.GetExampleComment(0) + linesep
        output+= "To run this example in command-line, use the following: " + linesep
        output += GetApplicationExampleCommandLine(app,0)
        output+= "To run this example from Python, use the following code snippet: " + linesep
        output += GetApplicationExamplePython(app,0)
    if len(limitations)>=2:
        output += appdetailslevel + "{Limitations}" + "\\label{applim:" + appname + "}" + linesep
        output += ConvertString(app.GetDocLimitations()) + linesep
    output += appdetailslevel + "{Authors}" + "\\label{appauthors:" + appname + "}" + linesep
    output += "This application has been written by " + ConvertString(app.GetDocAuthors()) + "." + linesep
    seealso = app.GetDocSeeAlso()
    if len(seealso) >=2:
        output += appdetailslevel + "{See also}" + "\\label{appseealso:" + appname + "}" + linesep
        output += "These additional ressources can be useful for further information: " + linesep
        output += "\\begin{itemize}" + linesep
        output += "\\item " + ConvertString(app.GetDocSeeAlso()) + linesep
        output += "\\end{itemize}" + linesep
    return output

def GetApplicationTags(appname):
     app = otbApplication.Registry.CreateApplication(appname)
     return app.GetDocTags()

def GetFullDocumentHeader():
    out = "\\documentclass{report}" + linesep
    out += "\\usepackage{listings,color}" + linesep
    out+="\\definecolor{listcomment}{rgb}{0.0,0.5,0.0}" + linesep
    out+="\\definecolor{listkeyword}{rgb}{0.0,0.0,0.5}" + linesep
    out+="\\definecolor{listnumbers}{gray}{0.65}" + linesep
    out+="\\definecolor{listlightgray}{gray}{0.955}" + linesep
    out+="\\definecolor{listwhite}{gray}{1.0}" + linesep
    out += "\\begin{document}" + linesep
    out += "\\tableofcontents" + linesep
    out += "\\listoftables" + linesep
    out += "\\chapter{Applications delivered with OTB}" + linesep
    return out

def GetSingleAppDocumentHeader():
    out = "\\documentclass{article}" + linesep
    out += "\\usepackage{listings,color}" + linesep
    out+="\\definecolor{listcomment}{rgb}{0.0,0.5,0.0}" + linesep
    out+="\\definecolor{listkeyword}{rgb}{0.0,0.0,0.5}" + linesep
    out+="\\definecolor{listnumbers}{gray}{0.65}" + linesep
    out+="\\definecolor{listlightgray}{gray}{0.955}" + linesep
    out+="\\definecolor{listwhite}{gray}{1.0}" + linesep
    out += "\\begin{document}" + linesep
    return out

def GetApplicationsSections():
    out = ""
    blackList = ["TestApplication"]
    appNames = [app for app in otbApplication.Registry.GetAvailableApplications() if app not in blackList]
    sectionTags = ["Image Manipulation","Vector Data Manipulation", "Calibration","Geometry", "Image Filtering","Feature Extraction","Stereo","Learning","Segmentation"]
    for tag in sectionTags:
        out +=tagslevel + "{" + tag + "}" + "\\label{apptag:" + tag + "}" + linesep
        appsRemoved = []
        for appName in appNames:
            apptags = GetApplicationTags(appName)
            if apptags.count(tag) > 0:
                print "Generating " + appName + " section"
                out += ApplicationToLatex(appName)

                appsRemoved.append(appName)
        for appName in appsRemoved:
            appNames.remove(appName)
    out+= tagslevel+"{Miscellanous}" + "\\label{apptag:Miscellanous" + "}"  + linesep
    for appName in appNames:
        print "Generating " + appName + " section"
        out += ApplicationToLatex(appName)
    return out

# Start parsing options
parser = OptionParser(usage="Export application(s) to tex or pdf file.")
parser.add_option("-o","--out",dest="filename",help="Output tex or pdf file",metavar="FILE")
parser.add_option("-t","--type",dest="filetype",help="Output type: tex or baretex (default: %default)",default="tex",choices=["tex","baretex"]) 
parser.add_option("-n","--name",dest="name",help="Name of the application to export. If empty, all available applications in path will be exported.",default="")
parser.add_option("-l","--level",dest="level",help="Handle level of tag in documentation (default: %default)", default = "section", choices= ["section","subsection"])
(options, args) = parser.parse_args()

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit()

# Handle the level parameter
if options.name == "":
    if options.level == "section":
        print "Tags will start at section level, and application at subsection level"
        tagslevel = "\\section"
        applevel ="\\subsection"
        appdetailslevel = "\\subsubsection"
        paramlevel = "\\paragraph"
    elif options.level == "subsection":
        print "Tags will start at subsection level, and application at paragraph level"
        tagslevel = "\\subsection"
        applevel ="\\susubsection"
        appdetailslevel = "\\paragraph"
        paramlevel = "\\subparagraph"

# Handle the name parameter
else:
    print "Applications will start at section level, and sections will not be numbered."
    applevel ="\\section*"
    appdetailslevel = "\\subsection*"
    paramlevel = "\\subsubsection*"
output = ""

# If tex or pdf output
if options.filetype == "tex":
    if options.name == "":
        print "Generating full document with header."
        output+=GetFullDocumentHeader()
        output+=GetApplicationsSections()
    else:
        print "Generating single application document with header."
        output+=GetSingleAppDocumentHeader()
        output+=ApplicationToLatex(options.name)
    output+= "\\end{document}"
    outfile = open(options.filename,'w')
    outfile.write(output)
    outfile.close()
elif options.filetype == "baretex":
    if options.name == "":
        print "Generating full document without header."
        output+=GetApplicationsSections()
    else:
        print "Generating single application document without header."
        output+=ApplicationToLatex(options.name)
    outfile = open(options.filename,'w')
    outfile.write(output)
    outfile.close()

print "Output written to " + options.filename

