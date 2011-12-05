#!/usr/bin/python

import otbApplication
import os
import sys

##############################################################################
# Parameters

linesep = os.linesep

tagslevel = "\\section"
applevel ="\\subsection"
appdetailslevel = "\\subsubsection"
paramlevel = "\\paragraph"

pixeltypes = {' int8' : 0, ' uint8' : 1, ' int16' : 2, ' uint16': 3, ' int32' : 4, ' uint32' : 5, ' float' : 6, ' double': 7}

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

        firstlevelparams = set(firstlevelparams)

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

    output+= "$ otbcli_" + ConvertString(app.GetName())

    for i in range(0, app.GetExampleNumberOfParameters(idx)):
        output+=" -" + app.GetExampleParameterKey(idx,i)+ " " + app.GetExampleParameterValue(idx,i)

    output += linesep

    output+= "\\end{lstlisting}" + linesep

    return output


def GetApplicationExamplePythonSnippet(app,idx):
    
    output= "#!/usr/bin/python" + linesep

    output+= linesep
    
    output+= "# Import the otb applications package" + linesep
    
    output+= "import otbApplication" + linesep + linesep
    
    output+= "# The following line creates an instance of the " + ConvertString(app.GetName()) + " application " + linesep

    output+= ConvertString(app.GetName()) + " = otbApplication.Registry.CreateApplication(\"" + ConvertString(app.GetName()) + "\")" + linesep + linesep 

    output+= "# The following lines set the application parameters" + linesep

    for i in range(0, app.GetExampleNumberOfParameters(idx)):

        param = app.GetExampleParameterKey(idx,i)
        value = app.GetExampleParameterValue(idx,i)
        paramtype = app.GetParameterType(param)
        
        # Handle the int case
        if(paramtype == otbApplication.ParameterType_Int \
               or paramtype == otbApplication.ParameterType_Radius \
               or paramtype == otbApplication.ParameterType_RAM):

            output+= ConvertString(app.GetName()) + ".SetParameterInt(\"" + param + "\"," + value +") " + linesep

        elif paramtype == otbApplication.ParameterType_Float:

            output+= ConvertString(app.GetName()) + ".SetParameterFloat(\"" + param + "\"," + value +") " + linesep

        elif paramtype == otbApplication.ParameterType_StringList \
                or paramtype == otbApplication.ParameterType_InputImageList \
                or paramtype == otbApplication.ParameterType_InputVectorDataList:

            values = value.split(" ")

            output+= ConvertString(app.GetName()) + ".SetParameterStringList(\"" + param + "\", {"

            for val in values[:-1]:

                output+= EncloseString(val) + ", "

            output+= EncloseString(values[-1]) + "})" + linesep

        else:
            if paramtype == otbApplication.ParameterType_OutputImage:
                
                # look for type
                foundcode = -1
                foudname = ""
                for ptypename, ptypecode in pixeltypes.iteritems():
                
                    if value.endswith(ptypename):
                    
                        foundcode = ptypecode
                        
                        foundname = ptypename
                        
                        break
                
                if foundcode != -1 :
                    output+= ConvertString(app.GetName()) + ".SetParameterString(\"" + param + "\"," + EncloseString(value[:-len(foundname)]) +") " + linesep
                    
                    output+= "# The following line sets the output image type for parameter " + param + " to " + foundname + linesep
                    
                    output += ConvertString(app.GetName()) + ".SetParameterOutputImagePixelType(\"" + param + "\", " + str(foundcode) + ")" + linesep
                    
            else:

                output+= ConvertString(app.GetName()) + ".SetParameterString(\"" + param + "\", " + EncloseString(value) +") " + linesep

        output += linesep

    output += "# The following line triggers the application execution" + linesep
    
    output += ConvertString(app.GetName()) + ".ExecuteAndWriteOutput()" + linesep
    
    return output

def GetApplicationExamplePython(app,idx):

    output= "\\begin{lstlisting}[language=python,breaklines=true,breakatwhitespace=true,frame = tb,framerule = 0.25pt,fontadjust,backgroundcolor={\\color{listlightgray}},basicstyle = {\\ttfamily\\scriptsize},keywordstyle = {\\ttfamily\\color{listkeyword}\\textbf},identifierstyle = {\\ttfamily},commentstyle = {\\ttfamily\\color{listcomment}\\textit},stringstyle = {\\ttfamily},showstringspaces = false,showtabs = false,numbers = none,numbersep = 6pt, numberstyle={\\ttfamily\\color{listnumbers}},tabsize = 2]" + linesep
    
    output += GetApplicationExamplePythonSnippet(app,idx)
    
    output+= "\\end{lstlisting}" + linesep

    return output

def ApplicationToLatex(appname):

    output = ""
    
    app = otbApplication.Registry.CreateApplication(appname)
    
    app.Init()
    
    output += applevel + "{" + ConvertString(app.GetDocName()) + "}" + linesep
    
    output += ConvertString(app.GetDescription()) + linesep

    output += appdetailslevel + "{Detailed description}" + linesep

    output += ConvertString(app.GetDocLongDescription()) + linesep
    
    limitations = app.GetDocLimitations()

    output += appdetailslevel + "{Parameters}" + linesep

    depth = GetParametersDepth(app.GetParametersKeys())

    deep = depth > 0

    output += ApplicationParametersToLatex(app,app.GetParametersKeys(),deep) + linesep

    if app.GetNumberOfExamples() > 1:

        output += appdetailslevel + "{Examples}" + linesep

        for i in range(0,app.GetNumberOfExamples()):
            output += paramlevel + "{Example " + str(i+1) +"}" + linesep

            output += app.GetExampleComment(i)

            label = ConvertString(app.GetName()) + "clex" + str(i+1)

            pylabel = ConvertString(app.GetName()) + "pyex" + str(i+1)

            output+= "To run this example in command-line, use the following: " + linesep
            
            output += GetApplicationExampleCommandLine(app,i)

            output+= "To run this example from Python, use the following code snippet: " + linesep
            
            output += GetApplicationExamplePython(app,i)

    elif app.GetNumberOfExamples() == 1:

        output += appdetailslevel + "{Example}" + linesep

        if( len(app.GetExampleComment(0)) > 1):

            output += app.GetExampleComment(0) + linesep

        output+= "To run this example in command-line, use the following: " + linesep

        output += GetApplicationExampleCommandLine(app,0)

        output+= "To run this example from Python, use the following code snippet: " + linesep

        output += GetApplicationExamplePython(app,0)

    if len(limitations)>=2:
        
        output += appdetailslevel + "{Limitations}" + linesep
        
        output += ConvertString(app.GetDocLimitations()) + linesep

    output += appdetailslevel + "{Authors}" + linesep

    output += "This application has been written by " + ConvertString(app.GetDocAuthors()) + "." + linesep

    seealso = app.GetDocSeeAlso()

    if len(seealso) >=2:
        
        output += appdetailslevel + "{See also}" + linesep

        output += "These additional ressources can be useful for further information: " + linesep
        output += "\\begin{itemize}" + linesep
        
        output += "\\item " + ConvertString(app.GetDocSeeAlso()) + linesep

        output += "\\end{itemize}" + linesep

    return output

def GetApplicationTags(appname):

     app = otbApplication.Registry.CreateApplication(appname)

     return app.GetDocTags()

if len(sys.argv) != 2:
    
    print "Usage: " + sys.argv[0] + " target_dir\n"

    sys.exit()

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




blackList = ["TestApplication"]

appNames = [app for app in otbApplication.Registry.GetAvailableApplications() if app not in blackList]

sectionTags = ["Image manipulation","Calibration","Geometry", "Image Filtering","Learning"]

outdir = sys.argv[1]

wrapperstexdir = outdir + "applications/"

picturesdir = wrapperstexdir + "Pictures/"

outfile = outdir + "Wrappers.tex"

for tag in sectionTags:

    out +="\\section{" + tag + "}" + linesep

    for appName in appNames:

        apptags = GetApplicationTags(appName)

        if apptags.count(tag) > 0:

            apptexfile = wrapperstexdir + appName + ".tex"

            print "Generating " + appName + ".tex"

            ifstream = open(apptexfile,'w')

            ifstream.write(ApplicationToLatex(appName))

            ifstream.close()

            out += "\input{applications/"+appName + ".tex}" + linesep
            
            appNames.remove(appName)

out+= "\\section{Miscellanous}" + linesep

for appName in appNames:

    print "Generating " + appName + ".tex"

    apptexfile = wrapperstexdir + appName + ".tex"

    ifstream = open(apptexfile,'w')
    
    ifstream.write(ApplicationToLatex(appName))
    
    ifstream.close()
    
    out += "\input{applications/"+appName + "}" + linesep

out += "\\end{document}"


ifstream = open(outfile,'w')

ifstream.write(out)

ifstream.close()
