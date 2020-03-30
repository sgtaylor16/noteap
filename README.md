# Introduction (The Problem)

Keeping track of all the different decisions, facts and actions on a program becomes more and more difficult as the size of the program and team grows. Once a program kicks-off it usually quickly becomes impractical or inefficient to hold just one standing meeting that an entire team attends. Instead there are usually multiple standing meetings throughout the week where only certain subsets of your team attend. Additionally, different people may lead different meetings.

There are several problems arise when projects/programs get to this point. First, especially in today's world remote teaming, it becomes more difficult to keep team members aware of what is happening outside of their area of direct responsibilities. Situational awareness is important. People make better independent decisions if they are well-informed about the bigger picture. Second, when people are assigned actions in multiple meetings, with multiple meeting leaders, it is difficult to know when people are overloaded or what their top priorities should be.

# Application

To try and tackle these problems, I have coded a fairly simple application. I take all my meeting notes in [markdown](https://www.markdownguide.org/) format. Writing notes in simple markdown allowed me to write code that quickly turns the notes into html for a web page. The code also provides another ability. Any line in the markdown that ends with a "#" immediately followed by a name like "#Taylor" is taken as an action item. Action items are gathered across all of the different meetings and groups them by name. A separate section in the html page then displays the actions for each person.

# Instructions

All of the code in for meeting amalgamation is contained within one python file called parsenotes. Running the application requires the following:

* An HTML template file that contains at a minimum the css styling to use within the generated web page. Within the <body> of the html template file their must be a line that includes the line:

```
{{ meetings }}
```

The code will append the html generated from the meeting notes markdown an place it where the meetings tag is placed.

* A folder where all of the meeting notes, written in markdown format are stored. Each standing meeting should use a consistent name followed by the date in MM-DD-YY or MM-DD-YYYY format. For example, if a meeting entitled DesignMeeting would need to have a series of meeting notes in the folder like:

DesignMeeting-01-05-2020.md
DesignMeeting-01-12-2020.md
DesignMeeting-01-17-2020.md

* Call the function:

```
parsenotes.WriteNotesHTMLPage(folderpath,htmlpath,finalpagename)
```

The folderpath is a string argument that directs the function to the folder with all of the meeting notes in it.

The htmlpath is a string argument that directs to the location of the html template.

The finalpagename argument is simply the name (not the path) of the final html page.