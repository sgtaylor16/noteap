import re
from os import listdir
from os.path import join
from dateutil.parser import parse
import numpy as np
import pandas as pd
import mistune

'''
TODO
-Sublist
'''

actiontest = re.compile("#[A-Z]")

def ReadinFiletoString(path):
    '''Reads in file as a single sting'''
    with open(path,'r') as filename:
        return filename.read()

#Functions that work on textlines

def SplitbyCarriage(string):
    '''Takes a sting and makes a list of lines seperated by carraige return'''
    return string.split('\n')

def DeleteEmptyLines(noteslist):
    '''Removes empty lines from a notelist'''
    return [line for line in noteslist if len(line) != 0]

def AddTag(textline,tag):
    '''Takes a textline and encloses it in an html tag'''
    starttag = '<' + tag + '>'
    endtag = '</' + tag + '>'
    return starttag + textline + endtag

def IsHeader(textline):
    '''Returns True if the textline is identified as a header according to Markdown 
    formatting'''
    return bool(re.match('#{1,}\s',textline))

def IsAction(textline):
    '''Function that returns True if textline has an #Name Tag.'''
    return bool(re.findall("#[A-Za-z]{1,}",textline))

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
    #Create the line
    md = mistune.Markdown()
    if IsAction(md(textline)):
        #return AddClass(md(textline),'Action')
        return AddStyle(md(textline),{'color':'red'})
    else:
        return md(textline)


#Functions that accept html lines

def AddClass(htmlline,class_name):
    '''Adds a class attribute to a line that already has html tags.'''
    templist = re.split('>',htmlline,maxsplit=1)
    return templist[0] + ' class="' + class_name + '">' + templist[1]

def AddID(htmlline,id_name):
    '''Adds an ID attribute to a line that already has an html tag.'''
    templist = re.split('>',htmlline,maxsplit = 1)
    return templist[0] + ' id="' + id_name + '">' + templist[1]

def AddStyle(htmlline,styledict):
    '''Adds inline style'''
    templist = re.split('>',htmlline,maxsplit=1)
    stylestring = "style ="
    newstring=' style='
    for k,v in styledict.items():
        newstring = newstring +'"' + k + ":" +v + '"' +";"

    return templist[0] + newstring +'>' + templist[1]
        
#Functions that accept a list of text lines.
def RenderNotes(textlist):
    '''Takes a list of lines and calls Renderline on each of them to put html 
    tags around each one'''
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

def InsertHTML(page,variableID,texttoinsert):
    restring = '{{ '+ variableID + ' }}'  #This has the potential to be a little buggy
    tempsplit = page.split(restring)
    return tempsplit[0] + texttoinsert + tempsplit[1]

def AddHeader(headertext,level=1):
    '''Adds a heater html tag to a textline
    headertext string - textline to enclose in header tag
    level int - header level number (h1,h2,etc)
    '''
    opentag = '<h' + str(level) + '>'
    closetag = '</h' + str(level) + '>'
    return opentag + headertext + closetag
    
def FindMeetings(folderpath):
    '''Looks in folderpath for meetings.  A meeting is any markdown file 
    with the following format: dd-mm-yy-[meetingname] returns a list of distinct meeting names'''
    mdfiles = [f for f in listdir(folderpath) if f[-3:] == ".md"]
    meetingslist1= []
    for file in mdfiles:
        meeting = re.split('-[0-9]{1,2}-[0-9]{1,2}-[0-9]{1,4}',file)[0]
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
        onedate = parse(re.search('[0-9]{1,2}-[0-9]{1,2}-[0-9]{2,4}(?=.md)',onemeeting)[0])
        datearray = np.append(datearray,onedate)
    maxindex = datearray.argmax()
    latestmeeting = thismeeting[maxindex]
    return join(folderpath,latestmeeting)

def ReadMeeting(meetingpath):
    '''Creates a htmllist from a meeting notes file'''
    with open(meetingpath) as fh:
        htmllist = RenderNotes(DeleteEmptyLines(SplitbyCarriage(fh.read())))
    return htmllist
    
def ComposePage(folderpath):
    '''Finds all the latest meetings in a given folder and returns a string with html tags'''
    #Get all the meetings
    allmeetings = FindMeetings(folderpath)
    finalstring = ''
    #For Each meeting compose a string of the meeting notes
    for meetingname in allmeetings:
        temp = WriteNotes(ReadMeeting(FindLatest(meetingname,folderpath)))
        temp = AddID(AddTag(AddHeader(meetingname) + temp,'div'),meetingname)
        finalstring = finalstring + temp + '<p></p>'
    #Add a div to link
    return finalstring

def WriteNotesHTMLPage(folderpath,htmlpath,finalpagename):
    '''Function to write the complete page.
    Arguments:
    folderpath string - path to the folder where the notes reside.
    htmlpath - path to the html header template
    finalpagename - name of the final page, it will reside in the folderpath.
    '''
    with open(htmlpath,'r') as fh:
        template = fh.read()

    #Read in all of the notes
    allnotes = ComposePage(folderpath)
    #Add in the actions
    allnotes = WriteActionsHTML(FindActions(folderpath)) + "<p></p>" + allnotes
    #Put a div around everything to fix margin with top menu bar
    allnotes = AddClass(AddTag(allnotes,'div'),'ActionsAndNotes')
    #Add the two together
    finalpage = InsertHTML(template,'meetings',allnotes)
    #Write the final page
    outfilepath = folderpath + '/' + finalpagename + '.html'
    with open(outfilepath,'w') as fh:
        fh.write(finalpage)
    
    return None

def FindActions(folderpath):
    '''
    Finds the Actions Marked with a Hashtag in the Notes
    '''
    meetinglist = FindMeetings(folderpath)
    actionslist =[]
    for meeting in meetinglist:
        textlist = SplitbyCarriage(ReadinFiletoString(FindLatest(meeting,folderpath)))
        for textline in textlist:
            if IsAction(textline):
                action = re.split('#[A-Z]',textline)[0]
                people = re.findall('(?<=#)[A-Za-z]{1,}',textline)
                for person in people:
                    actionslist.append([action,person])
    return pd.DataFrame(columns = ['Action','Name'],data = actionslist)

def WriteActionsHTML(actionsdf):
    people = actionsdf['Name'].unique()
    actionstringall = AddHeader('Actions')
    
    for person in people:
        persondf = actionsdf.query('Name == @person')
        actionstring1person = AddHeader(person,2)
        for index,action in persondf.iterrows():
            actionstring1person = actionstring1person + RenderLine(action['Action'])
        actionstringall = actionstringall + actionstring1person

    actionstringall = AddID(AddClass(AddTag(actionstringall,'div'),'actions'),'ActionList')
    
    return actionstringall     