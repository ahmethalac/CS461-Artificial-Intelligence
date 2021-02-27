from tkinter import * 
from parsePuzzle import parsePuzzle

def showAnswers(boxList):
    i = 0
    for cell in puzzleInformation['cells']:
        if(cell["cellNumber"] != -1):
            boxList[i].config(text = cell['letter'])
            boxList[i].config(anchor = "c")
            boxList[i].config(fg="black")
        i += 1
       
puzzleInformation = parsePuzzle()

# creating main tkinter window/toplevel 
master = Tk()

# Creating Title of Across Clues
l0 = Label(master, text = "ACROSS", font = 'franklin 13 bold')
l0.grid(row = 0, column = 5, rowspan = 1, sticky = W)

# Creating Across Clues
i = 0
acrossClues = []
for clueNumber, clue in puzzleInformation['acrossClues'].items():
    acrossClues.append(Label(master, text = '%d. %s' % (clueNumber, clue), font = 'franklin 12'))
    acrossClues[i].grid(row = i + 1, column = 5, sticky = W, rowspan = 1)
    i += 1

# Creating Title of Down Clues
i += 3
l1 = Label(master, text = "DOWN", font = 'franklin 13 bold')
l1.grid(row = i, column = 5, rowspan = 1, sticky = W)

# Creating Down Clues
downClues = []
j = 0
for clueNumber, clue in puzzleInformation['downClues'].items():
    downClues.append(Label(master, text = '%d. %s' % (clueNumber, clue), font = 'franklin 12'))
    downClues[j].grid(row = i + 1, column = 5, sticky = W, rowspan = 1)
    i += 1
    j += 1

# Creating puzzle Information
k = 0
boxList = []
for cell in puzzleInformation['cells']:
    if(cell["cellNumber"] == -1):
        boxList.append(Label(master, bg="black", borderwidth=4, relief="solid", height=5, width=10, font = 'franklin 12'))
    else:
        if(cell["cellNumber"] != 0):
            boxList.append(Button(master, bg="white", relief="solid", height=5, width=10, text = cell['cellNumber'], anchor = "nw", font = 'franklin 12'))
        else:
            boxList.append(Button(master, bg="white", relief="solid", height=5, width=10, fg="white", font = 'franklin 12'))
    boxList[k].grid(row = (int(k / 5) * 3), column = (k % 5), rowspan = 3)
    k += 1
    
# Button for showing actions
button1 = Button(master, bg="white", relief="solid", text = "Click for Anwers", command=lambda: showAnswers(boxList))
button1.grid(row = i + 3, column = 5, pady = 10)
  
mainloop() 
