from tkinter import Button,\
Entry, \
Listbox, \
TOP, \
X, \
Label

class DevFrame():
    humanity = None

    homeFrame = None
    root = None

    width = 200
    height = 200

    btn_updateOnNow = None

    def __init__(self,root,_humanity,homeFrame):
        self.humanity = _humanity

        self.root = root

        #root.geometry(str(self.width) + 'x' + str(self.height))
        root.title('Dev')

        self.homeFrame = homeFrame

        self.btn_updateOnNow = Button(self.root, text="Update OnNow", command=self.homeFrame.fetchOnNow)
        self.btn_updateOnNow.grid(pady = 10, padx = 10,column=0,row=0,columnspan = 2,sticky='WE')

        self.lbl_simBuzzcardId = Label(self.root, text = "Buzzcard Id (eid)")
        self.lbl_simBuzzcardId.grid(pady = 10, padx = 10, column=0, row=1)

        self.txt_simBuzzcardId = Entry(self.root,text="111")
        self.txt_simBuzzcardId.grid(pady = 10, padx = 10,column=1, row=1, columnspan = 2)
        test_id = self.humanity.me()['id']
        
        self.txt_simBuzzcardId.insert(0,test_id)

        self.btn_simulateCardScan = Button(self.root, text="Simulate Card Scan", command=self.simBuzzcardScan)
        self.btn_simulateCardScan.grid(column=0,row=2,pady = 10, padx = 10,columnspan = 1,sticky='EW')

        self.btn_clearBuzzcard = Button(self.root, text="Clear Buzzcard", command=self.clearBuzzcard)
        self.btn_clearBuzzcard.grid(column=1,row=2,pady = 10, padx = 10,columnspan = 1,sticky='EW')

    def simBuzzcardScan(self):
        self.homeFrame.processBuzzcardScan(self.txt_simBuzzcardId.get())

    def clearBuzzcard(self):
        buzzcardId = self.txt_simBuzzcardId.get()

        pi = self.humanity.getPIFromBuzzcard(buzzcardId)

        self.humanity.updateEmployeeBuzzcardId(pi['id'],'')