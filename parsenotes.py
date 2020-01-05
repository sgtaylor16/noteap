import re
from os import listdir
from os.path import join
from dateutil.parser import parse
import numpy as np
import pandas as pd

actiontest = re.compile("#[A-Z]")

def ReadinFile(path):
    with open(path,'r') as filename:
        return filename.read()

def DeleteEmptyLines(noteslist):
    return [line for line in noteslist if len(line) != 0]

#Functions that work on textlines

def SplitbyCarriage(textline):
     return textline.split('\n')

def AddTag(textline,tag):
    starttag = '<' + tag + '>'
    endtag = '</' + tag + '>'
    return starttag + textline + endtag

def IsHeader(textline):
    return bool(re.match('#{1,}\s',textline))

def IsAction(textline):
    '''Function that returns True if textline has an #Name Tag.'''
    return bool(re.search("#[A-Z]",textline))

def StripHead(textline):
    '''Function to strip a markdown # or * from the beginning of a line'''
    if bool(re.split('(#|\*){1,}\s',textline,maxsplit=1)):
        return re.split('(#|\*){1,}\s',textline,maxsplit=1)[-1]
    else:
        return textline

def SplitAction(textline):
    return re.split('#(?=[A-Z])',textline)
    
def RenderLine(textline):
    '''Function that turns a text line into an html line with tags'''
    if IsHeader(textline):
        return AddTag(StripHead(textline),'h2')
    elif IsAction(textline):
        return AddClass(AddTag(StripHead(textline),'li'),"Action")
    else:
        return AddTag(StripHead(textline),'li')

#Functions that accept html lines

def AddClass(htmlline,class_name):
    '''Adds a class attribute to an html line.'''
    templist = re.split('>',htmlline,maxsplit=1)
    return templist[0] + ' class="' + class_name + '">' + templist[1]

#Functions that accept a list of text lines.
def RenderNotes(textlist):
    htmllist = []
    for line in textlist:
        htmllist.append(RenderLine(line))
    return htmllist

def WriteNotes(textlist):
    '''Takes a texlist, removes empty lines and returns a single string with newlines between
    old list elements'''
    totalstring = ''
    for line in DeleteEmptyLines(textlist):
        totalstring = totalstring + line + '\n'
    return totalstring

#Other stuff
def AddHeader(headertext,level=1):
    opentag = '<h' + str(level) + '>'
    closetag = '</h' + str(level) + '>'
    return opentag + headertext + closetag
    
def FindMeetings(folderpath):
    '''Looks in folderpath for meetings.  A meeting is any markdown file 
    with the following format: dd-mm-yy.[meetingname] returns a list of distinct meeting names'''
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
    '''Returns a full pathname to the latest file of meetingname'''
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
        textlist = RenderNotes(DeleteEmptyLines(SplitbyCarriage(fh.read())))
    return textlist
    
def ComposePage(folderpath):
    #Get all the meetings
    allmeetings = FindMeetings(folderpath)
    finalstring = ''
    #For Each meeting compose a string of the meeting notes
    for meetingname in allmeetings:
        temp = WriteNotes(ReadMeeting(FindLatest(meetingname,folderpath)))
        temp = AddClass(AddTag(AddHeader(meetingname) + temp,'div'),'meeting')
        finalstring = finalstring + temp
    return finalstring

def WriteNotesHTMLPage(folderpath,htmlpath,finalpagename):
    with open(htmlpath,'r') as fh:
        template = fh.read()
    #Split the template between the body tags
    split_template = re.split("</body>",template)   #Rember that the /body is missing
    #Read in all of the notes
    allnotes = ComposePage(folderpath)
    #Add in the actions
    allnotes = allnotes + WriteActionsHTML(FindActions(folderpath))
    #Add the two together
    finalpage = split_template[0]  + allnotes  + '</body>' + split_template[1]
    #Write the final page
    outfilepath = folderpath + '/' + finalpagename + '.html'
    with open(outfilepath,'w') as fh:
        fh.write(finalpage)
    
    return None

def FindActions(folderpath):
    meetinglist = FindMeetings(folderpath)
    actionslist =[]
    for meeting in meetinglist:
        textlist = SplitbyCarriage(ReadinFile(FindLatest(meeting,folderpath)))
        for textline in textlist:
            if IsAction(textline):
                actionslist.append(SplitAction(StripHead(textline)))
    return pd.DataFrame(columns = ['Action','Name'],data = actionslist)

def WriteActionsHTML(actionsdf):
    people = actionsdf['Name'].unique()
    actionstringall = AddHeader('Actions')
    
    for person in people:
        persondf = actionsdf.query('Name == @person')
        actionstring1person = AddHeader(person,2)
        for index,action in persondf.iterrows():
            actionstring1person = actionstring1person + AddTag(action['Action'],'ul')
        actionstringall = actionstringall + actionstring1person
    
    return actionstringall     