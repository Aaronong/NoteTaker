# Prompt

1. What is your problem that you are trying to solve/improve
2. What are the existing solutions and why are they not "good" or what are their flaws
3. Your proposed solution (general concept)
4. Describe your design process including:
   a. Observation
   b. Low fidelity prototyping
   c. Iterations
   d. High fidelity prototype
5. Present potential feedback that you may have gathered for your final iteration
6. Explain what is left and suggest some directions for future work



# Presentation style

- Telling multiple stories. For each problem, present a relatable and funny story that sticks. 
- Find images, cartoons that fit the story. Alternate between text and stories.
  - Eg. This is cephas's story -> scenario -> proper explanation of the problem



## FIRST AND FORMOST WE NEED TO DISTINGUISH BETWEEN NOTE-TAKING AND DOCUMENT WRITING. There are many document writing software, but do they serve note-taking well?



# The Problems

We all take notes on a daily basis; be it a way to condense information from another source, organise our lives, or record our thoughts, we cannot deny the value of note-taking. However, a quick scan of your surroundings will reveal that many individual, even laptop owners, still choose not to use note-taking software. This suggests that there is a pronounced segment of the market who are willing to take notes on a software platform but feel that the current note-taking software offerings are not good enough. 

# Why can't we just stick to handwritten notes?

While handwritten notes offer the most in terms of flexibility, most individuals who handwrite their notes have reported that they experience difficulty retrieving information from handwritten notes. Handwritten notes are also unable to respond to the emerging note taking needs of the tech savvy generation. To put it simply, there is no search function and no way to include pictures and hyperlinks into ther notes. Sharing handwritten notes is also difficult, and limited to geographical constraints. 



```perl
Even ppl who have only been taking notes by hand complain that they tend to lose their notes, or that they find difficulty retrieving information from different pages of the note.



supply gap in note-taking software. Those who do use note-taking software, use a variety of different software.

- Ineffective information retrieval across documents
- Inconvenience of typing notes
- Lack of control over written content in collaborative documents
- Constantly have to toggle between screens to read from a note to write another

```



# Why existing solutions are not cutting it

When we think of note-taking software, a few big providers come to mind. Google docs, microsoft words, Evernote, OneNote. I shall first discuss the problems common to all note taking software then move on to discuss each in more detail. FIRST AND FORMOST WE NEED TO DISTINGUISH BETWEEN NOTE-TAKING AND DOCUMENT WRITING. There are many document writing software, but do they serve note-taking well?

### Inconvenience of typing notes

Individuals who hand write their notes cited unintuitive shortcuts and the lack of shortcuts for key features such as colour coding and text highlighting as the largest stumbling block to the usability of note-taking applications. Popular features such as colour coding and text highlighting must be available for shortcut binding. Unfortunately, none of the note-taking software giants have responded to this preeminent need yet.

```python
A possible solution is to make shortcuts configurable and increase the range of functions that can be bound to shortcuts. Popular features such as colour coding and text highlighting must be available for shortcut binding. 
```

For note taking, you need a few colours quickly available, they help you to structure your content. Let us port over the biggest advantage of taking hand written notes over to software first. 

```python
- Provide 4 shortcuts, for pencolour 1, 2, 3, 4
- Provide shortcut for changing font size
```



### Ineffective information retrieval across documents

While users have been satisfied searching through multiple documents to find the information they need, they now find information retrieval a cumbersome process and want a way to retrieve all related snippets of information across multiple documents more effectively. 

```python
Inspiration for my solution was drawn from how databases function. Relational databases were born from the understanding that we do not always want to view data in the order that we key them in, we want to sort them according to parameters that we deem are important and hide irrelevant entries. 

I posit that note-taking would benefit from a similar approach. While we continue to write notes in the same way, we could benefit from the ability to view notes in different ways.

Hence, I introduce the note-centric model to note-taking and note-retrieval. Current applications adopt a document-centric model to organise notes. They expect a one to one correspondence between notes and documents and support all functions on a document level. This is where the breakdown occurs. 

Consider the following scenario:

A software developer has been servicing a client for three months. At every meeting, he opens a fresh document to record notes of his client’s requirements and feedback. Now he wishes to develop a specific feature of the software and wants to pull out all related requirements and feedback on the feature. He now needs to open all his meeting notes, scan through all of them, and collate relevant sections manually to obtain the information he wants.

The note-centric model views a document as a container of multiple notes. Each note corresponds to a unit of information which can be tagged. The software will centrally manage all documents written in it, similar to the way that OneNote and Evernote operate. Users will be able to perform tag searches across all documents written in the software and retrieve only the notes tagged with the search parameter. Tags can be set up to follow an inheritance structure to empower more effective searching. Any tag created by any collaborator will show up on the sidebar of all users, thus, all users are able to synchronise the tags used in categorizing their notes.
This note centric model also empowers the software to be a better collaboration tool, which I will elaborate upon in a later breakdown.

```



### Difficulty discerning the authorship of content in collaborative documents

Many users wish for a way to discern between the authorship of content written in collaborative documents more easily. It is important to know who wrote what for accountability, and to make it easier to know who to direct questions to. 

```python
The solution would be to leverage upon the note-centric model and display the author of each note more clearly in a shared document. INSERT picture here.
```



### Lack of control over written content in collaborative documents

My observations revealed that most users experience a lack of control over the content that they have written in collaborative documents. Parts that they have written in collaborative documents have dissapeared without a trace, or have been modified without their consent. While the onus is on team to communicate more effectively, many users view the ability to provide read and write access to different parts of a shared document a useful feature to have.

```python
leverage upon the note-centric model to support collaborative access rights on both the document and the note level. Document level read access would allow a collaborator to read all notes within a shared document. Document level write access would allow a collaborator to create new notes and change the order of notes within the document. 
Collaborators who chose to create a note within a shared document would have the option to give read, annotate, or write access to other collaborators working on the shared document. Collaborators who are given write access to a note is able to modify the note directly. They are only limited from deleting the note and sharing its access rights. Collaborators who are given annotate access can drop comment bubbles on the note and suggest edits that the author has to approve or reject. 
```

### problem with evernote

- Each document has so many tags. And 90% of a document consists of information not related to the tag. We want to hide away unneccessary information.

### Problem with Google Docs

- Addresses collaborative document writing well but not really note-taking.

```python
The biggest reason cited as to why individuals are not switching over to note-taking software is that 

- Slide with all the logos, google docs, evernote, one note

- Provide 4 shortcuts, for pencolour 1, 2, 3, 4, highlight 1,2,3,4

- Handwritten too slow
- Most software are too well developed. Long feature list that makes it more difficult for you to use the note.
- Lack of good collaborative note-taking tools.
-  Hence everyone is using different things.
- Software lacks flexibility.
```



### Design Inspiration

The inspiration for my prototypes comes mainly from three applications: Google Docs, Evernote, andTrello. First and foremost, I wish for users to experience minimal disruptionin their workflow. Since Google Docs captures the largest market share in thecollaborative note-taking industry, design principles that align with GoogleDocs will make it easier for users to transition towards my software.

Evernote is also amarket leader in the note-taking industry with a platform which is arguablymuch more powerful than that of Google Docs. While Evernote contains a rich setof features, few have found its user interface clunky. Since my note-takingsoftware also contains a rich set of features which are uncommon to itscompetitors, I choose to draw inspiration from Evernote, which I feel havemanaged the trade-off between complex features and usability well.

Trello is a collaborative tool that I use often with asimple and effective user interface. While Trello performs a differentfunction, I found that its boards, lists, and cards structure is rather similarto the notebooks, documents, and notes structure that I am proposing. Ipersonally found the user flow of creating, managing, and reading boards,lists, and cards very intuitive in Trello and wish to apply some of its designprinciples in my software.

```python
Show screenshots for all three
```



### Document Parchment

I first designed the document parchment, which I felt was the most crucial element of the note-taking software that users would interact with. While document parchment design is fairly standard across applications in the market, I was introducinga new note-centric paradigm and hence had the task to distinguish between each note clearly without sacrificing the readability of the document. The first iteration of my document parchment design can be found in Appendix C. 

While I was fairly satisfied with how the colour coding and bordering of the prototype made the authorship and demarcation of each note clear, I still felt dissatisfied withthe prototype. Firstly, it does not offer a way for authors to change the access rights of their notes. Secondly, users do not always want view the authors of notes in the top right corner, especially in the case where there is no collaboration involved in the notebook/document. In the case where users are performing tag searches they might want to view the notebook/documentinformation of the note instead.  





### High Fidelity



# CHANGING KEYMAP

```CSS
keyMap: {
  pc: {
    'ENTER': 'insertParagraph',
    'CTRL+Z': 'undo',
    'CTRL+Y': 'redo',
    'TAB': 'tab',
    'SHIFT+TAB': 'untab',
    'CTRL+B': 'bold',
    'CTRL+I': 'italic',
    'CTRL+U': 'underline',
    'CTRL+SHIFT+S': 'strikethrough',
    'CTRL+BACKSLASH': 'removeFormat',
    'CTRL+SHIFT+L': 'justifyLeft',
    'CTRL+SHIFT+E': 'justifyCenter',
    'CTRL+SHIFT+R': 'justifyRight',
    'CTRL+SHIFT+J': 'justifyFull',
    'CTRL+SHIFT+NUM7': 'insertUnorderedList',
    'CTRL+SHIFT+NUM8': 'insertOrderedList',
    'CTRL+LEFTBRACKET': 'outdent',
    'CTRL+RIGHTBRACKET': 'indent',
    'CTRL+NUM0': 'formatPara',
    'CTRL+NUM1': 'formatH1',
    'CTRL+NUM2': 'formatH2',
    'CTRL+NUM3': 'formatH3',
    'CTRL+NUM4': 'formatH4',
    'CTRL+NUM5': 'formatH5',
    'CTRL+NUM6': 'formatH6',
    'CTRL+ENTER': 'insertHorizontalRule',
    'CTRL+K': 'showLinkDialog'
  },
  mac: {
    'ENTER': 'insertParagraph',
    'CMD+Z': 'undo',
    'CMD+SHIFT+Z': 'redo',
    'TAB': 'tab',
    'SHIFT+TAB': 'untab',
    'CMD+B': 'bold',
    'CMD+I': 'italic',
    'CMD+U': 'underline',
    'CMD+SHIFT+S': 'strikethrough',
    'CMD+BACKSLASH': 'removeFormat',
    'CMD+SHIFT+L': 'justifyLeft',
    'CMD+SHIFT+E': 'justifyCenter',
    'CMD+SHIFT+R': 'justifyRight',
    'CMD+SHIFT+J': 'justifyFull',
    'CMD+SHIFT+NUM7': 'insertUnorderedList',
    'CMD+SHIFT+NUM8': 'insertOrderedList',
    'CMD+LEFTBRACKET': 'outdent',
    'CMD+RIGHTBRACKET': 'indent',
    'CMD+NUM0': 'formatPara',
    'CMD+NUM1': 'formatH1',
    'CMD+NUM2': 'formatH2',
    'CMD+NUM3': 'formatH3',
    'CMD+NUM4': 'formatH4',
    'CMD+NUM5': 'formatH5',
    'CMD+NUM6': 'formatH6',
    'CMD+ENTER': 'insertHorizontalRule',
    'CMD+K': 'showLinkDialog'
  }
}
```

