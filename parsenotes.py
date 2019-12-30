import re
from os import listdir
from os.path import join
from dateutil.parser import parse
import numpy as np

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

def RenderNotes(linelist):
    htmllist = []
    for line in linelist:
        htmllist.append(RenderLine(line))
    return htmllist

def WriteNotes(noteslist):
    totalstring = ''
    for line in noteslist:
        totalstring = totalstring + line + '\n'
    return totalstring
    
def FindMeetings(folderpath):
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

def FindLatest(meetingname,folderpath):
    allfiles = listdir(folderpath)
    thismeeting = [file for file in allfiles if meetingname in file]
    datearray = np.array([])
    for onemeeting in thismeeting:
        onedate = parse(re.match('[0-9]{1,2}-[0-9]{1,2}-[0-9]{1,4}',onemeeting)[0])
        alldates = np.append(datearray,onedate)
    maxindex = alldates.argmax()
    latestmeeting = thismeeting[maxindex]
    return join(folderpath,latestmeeting)

def ReadMeeting(meetingpath):
    with open(meetingpath) as fh:
        noteslist = RenderNotes(SplitbyCarriage(fh.read()))
    return noteslist
    