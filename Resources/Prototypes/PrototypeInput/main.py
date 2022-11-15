from tkinter import *
from tkinter import ttk, filedialog
from tkinter import messagebox
import json
import pandas as pd
from pathlib import Path

#method called to create error popups
def PopUpMessage(message):
    messagebox.showerror("Error", message)

#method called to open json file
def OpenModel():
    global modelFile
    global model
    #get file selected (prompt user to select one)
    file = filedialog.askopenfile(mode='r')
    #if valid rename label underneath to file name and set modelFile
    if file:
        modelFileLabel.configure(text=file.name)
        modelFile = file
        #take in the file as a string
        jsonContents = Path(modelFile.name).read_text()
        #replace lines with empty space
        jsonContents = jsonContents.replace('\n', '')
        #convert to a json
        model = json.loads(jsonContents)

#method called to open csv / excel file for dataframe
def OpenDataFrame():
    global dataframeFile
    global dataframe
    global featuresArray
    #get file selected (prompt user to select one)
    file = filedialog.askopenfile(mode='r', filetypes=[('Excel', '*.xlsx *.xls'), ('CSV', '*.csv')])
    #if valid rename label underneath to file name and set dataframeFile
    if file:
        dfFileLabel.configure(text=file.name)
        dataframeFile = file

        #create a new window so user can select features used to train the model
        featuresWindow = Toplevel(window)
        #set window size
        featuresWindow.configure(width=200, height=200)
        #set window title
        featuresWindow.title("Features Select")
        #set window background colour
        featuresWindow.configure(bg="#121212")
        #add title label
        Label(featuresWindow, bg='#121212', fg='#ebebeb', text="Feature Select", font=("Arial", 16)).grid(row=0, column=2, padx=20, pady=5, sticky=W)

        #if excel file read it as excel else read it as csv
        if (dataframeFile.name.split('.')[1] == 'xlsx') or (dataframeFile.name.split('.')[1] == 'xls'):
            dataframe = pd.read_excel(dataframeFile.name)
        else:
            dataframe = pd.read_csv(dataframeFile.name)

        #for every header make a new tickbox so user can select what features were used
        for i in range (0, len(dataframe.columns)):
            featuresArray.append(IntVar())
            Checkbutton(featuresWindow, bg='#121212', variable=featuresArray[i], fg='#ebebeb', text=dataframe.columns[i], highlightcolor = '#121212', selectcolor='#121212', activebackground='#121212').grid(row=i + 1, column=2, padx=5, pady=5, sticky=W)
        #add confirm button
        Button(featuresWindow, bg='#121212', fg='#ebebeb', text="Confirm", command=lambda: ConfirmDF(featuresWindow)).grid(row=len(dataframe.columns) + 1, column=2, padx=5, pady=5, sticky=W)

        #keep window in a loop so it updates
        featuresWindow.mainloop()

#method used to confirm feature select
def ConfirmDF(window):
    global featuresArray
    global dataframe

    #destroy the feature select window
    window.destroy()
    toDrop = []
    #create an array of strings containing the columns to drop
    for i in range(0, len(dataframe.columns)):
        if featuresArray[i].get() == 0:
            toDrop.append(dataframe.columns[i])
    #drop them, dataframe is now only the training data
    dataframe = dataframe.drop(toDrop, axis=1)

#method used to confirm users selection of files and features
def Confirm():
    #return error is either is not selected
    if(modelFile==None):
        PopUpMessage("Error : Select A Model.")
        return
    elif(dataframeFile==None):
        PopUpMessage("Error : Select A Dataframe.")
        return
    SummaryScreen()

#method used to show the summary of information imported
def SummaryScreen():
    #create a new window and set all relevant information
    featuresWindow = Toplevel(window)
    featuresWindow.configure(width=500, height=300)
    featuresWindow.title("Summary")
    featuresWindow.configure(bg="#121212")
    featuresWindow.grid_propagate(False)

    #add summary labels and table headers
    Label(featuresWindow, bg='#121212', fg='#ebebeb', text="Summary", font=("Arial", 16)).grid(row=0, column=2, padx=20, pady=5, sticky=W)
    Label(featuresWindow, bg='#121212', fg='#ebebeb', text="Info", font=("Arial", 12)).grid(row=1, column=2, padx=5, pady=5, sticky=W)
    Label(featuresWindow, bg='#121212', fg='#ebebeb', text="Data", font=("Arial", 12)).grid(row=1, column=3, padx=5, pady=5, sticky=W)

    #for each item in the json file add a new label containing the information title and the relevant data
    i = 1
    for item in model:
        i = i+1
        Label(featuresWindow, bg='#121212', fg='#ebebeb', text=item).grid(row=i, column=2, padx=5, pady=5, sticky=W)
        Label(featuresWindow, bg='#121212', fg='#ebebeb', text=model[item]).grid(row=i, column=3, padx=5, pady=5, sticky=W)

    #add the data used from the dataframe created earlier
    Label(featuresWindow, bg='#121212', fg='#ebebeb', text="Data Used").grid(row=i+1, column=2, padx=5, pady=5, sticky=W)
    Label(featuresWindow, bg='#121212', fg='#ebebeb', text=dataframe.columns).grid(row=i+1, column=3, padx=5, pady=5, sticky=W)

    #keep it in a loop to update
    featuresWindow.mainloop()


#create the initial ui window
window = Tk()

#initialise variables that will be used during importing
modelFile = None
dataframeFile = None
model = None
dataframe = None
featuresArray = []

#set window information
window.title("Data Visualisation")
window.configure(width=450, height=300)
window.configure(bg="#121212")

#add labels and buttons used for heading, browsing etc.
Label(window, bg='#121212', fg='#ebebeb', text="Project Setup", font=("Arial", 18)).grid(row=0, column=2, padx=20, pady=5, sticky=W)
Label(window, bg='#121212', fg='#ebebeb', text="Trained Model (json) : ").grid(row=1, column=2, padx=20, pady=5, sticky=W)
Button(window, bg='#121212', fg='#ebebeb', text="Browse...", command=OpenModel).grid(row=1, column=3, padx=20, pady=5, sticky=W)
modelFileLabel = Label(window, bg='#121212', fg='#ebebeb', text="")
modelFileLabel.grid(row=2, column=2, padx=20, pady=5)

Label(window, bg='#121212', fg='#ebebeb', text="Dataframe (xlsx / csv) : ").grid(row=3, column=2, padx=20, pady=5, sticky=W)
Button(window, bg='#121212', fg='#ebebeb', text="Browse...", command=OpenDataFrame).grid(row=3, column=3, padx=20, pady=5, sticky=W)
dfFileLabel = Label(window, bg='#121212', fg='#ebebeb', text="")
dfFileLabel.grid(row=4, column=2, padx=20, pady=5, sticky=W)

#add a button to confirm user selection - calls 'Confirm()'
Button(window, bg='#121212', fg='#ebebeb', text="Confirm", command=Confirm).grid(row=5, column=2, padx=20, pady=5, sticky=W)

window.mainloop()