from tkinter import Listbox,\
Entry,\
Button,\
END

class AddCardFrame():
    txt_PISearchQuery = None
    btn_search = None
    listbox_results = None
    btn_assignToCard = None

    root = None

    searchResults = []

    buzzcardID = None # Buzzcard Hardware ID that is being assigned by this window

    humanity = None

    def __init__(self,root,humanity,buzzcardID):
        self.root = root
        self.root.title("Register new Buzzcard ID: " + str(buzzcardID))

        self.buzzcardID = buzzcardID
        self.humanity = humanity
        
        self.txt_PISearchQuery = Entry(self.root,width=30)
        self.txt_PISearchQuery.grid(column=0,row=0,padx=10,pady=10)

        self.btn_search = Button(self.root, text="Search PIs", command=self.btnSearchClicked)
        self.btn_search.grid(column=1,row=0,padx=10,pady=10)

        self.listbox_results = Listbox(self.root,width=60)
        self.listbox_results.grid(column=0,columnspan=2,row=2,padx=10,pady=10)

        self.btn_assignToCard = Button(self.root,command=self.btnAssignClicked,text="Assign to Card",height=2,width=40,bg='green')
        self.btn_assignToCard.grid(column=0,columnspan=2,row=3,padx=10,pady=10)

    def btnSearchClicked(self):
        query = self.txt_PISearchQuery.get()

        self.searchResults = self.humanity.searchPIs(query)

        # clear results listbox
        self.listbox_results.delete(0, END)

        #TODO pad fields to the longest of each to create columns
        for e in self.searchResults:
            if e is not None \
            and e['firstname'] is not None\
            and e['lastname']  is not None\
            and e['email'] is not None:
                self.listbox_results.insert(END,e['firstname'] + ' ' + e['lastname'] + ' ' + e['email'])

    def btnAssignClicked(self):
        #print(self.listbox_results.curselection())

        # Retrieve selection information
        selectedResultIndex = self.listbox_results.curselection()[0]
        selectedPI = self.searchResults[selectedResultIndex]
        selectedPI_ID = selectedPI['id']

        # Assign the card to the PI account on humanity
        self.humanity.updateEmployeeBuzzcardId(selectedPI_ID,str(self.buzzcardID))

        # Close assigning window
        self.root.destroy()
