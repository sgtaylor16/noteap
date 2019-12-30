import re
from os import listdir

actiontest = re.compile("#[A-Z]")

def ReadinFile(path):
    with open(path,'r') as filename:
        return filename.read()

def SplitbyCarriage(text):
     return text.split('\n')

def DeleteEmptyLines(noteslist):
    return [line for line in noteslist if len(line) != 0]

def AddTag(textline,tag):
    starttag = '<' + tag + '>'
    endtag = '</' + tag + '>'
    return starttag + textline + endtag

def AddClass(htmlline,class_name):
    templist = re.split('>',htmlline,maxsplit=1)
    return templist[0] + ' class="' + class_name + '">' + templist[1]

def IsHeader(textline):
    return bool(re.match('#{1,} ',textline))

def StripHead(textline):
    return re.split('#{1,} ',textline,maxsplit=1)[1]

def IsAction(textline):
    return bool(re.search("#[A-Z]",textline))

def RenderLine(textline):
    if IsHeader(textline):
        return AddTag(StripHead(textline),'h2')
    elif IsAction(textline):
        return AddClass(AddTag(textline,'li'),"Action")
    else:
        return AddTag(textline,'p')

def RenderLines(linelist):
    htmllist = []
    for line in linelist:
        htmllist.append(RenderLine(line))
    return htmllist

def FindMeetings(folderpath):
    allfiles = listdir(folderpath)
    mdfiles = [f for f in listdir(folderpath) if f[-3:] == ".md"]
    meetingslist1= []
    for file in mdfiles:
        meeting = re.split('[0-9]{1,2}-[0-9]{1,2}-[0-9]{1,4}-',file)[1]
        meeting = meeting.split('.')[0]
        meetingslist1.append(meeting)
    meetingslist2 = []
    for meeting in meetingslist1:
        if meeting not in meetingslist2:
            meetingslist2.append(meeting)
    return meetingslist2


    




    
