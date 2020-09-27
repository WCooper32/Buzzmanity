from tkinter import Listbox,\
    Entry,\
    Button,\
    Frame,\
    Label,\
    LEFT,\
    TOP,\
    Y,\
    BOTH,\
    Toplevel

from frames.AddCardFrame import AddCardFrame


class HomeFrame():
    humanity = None

    width = 800
    height = 480

    addCardFrame = None

    root = None

    onNowEmployees = []
    pendingEmployees = []

    onNowBG = '#78FFAC'
    provisionalBG = '#ffa454'
    pendingBG = '#FFFFFF'
    onNowEntryFontSize = 16

    onNowFrame = None
    onNowListFrame = None
    provisionalFrame = None
    provisionalListFrame = None

    def __init__(self, root, humanity):
        self.humanity = humanity

        self.root = root

        root.geometry('800x480')
        root.title('Buzzmanity')

        self.onNowFrame = Frame(root)
        self.onNowFrame.pack(side=LEFT, fill=Y)

        onNowTitle = Label(self.onNowFrame, text='On Now',
                           font=("Helvetica", 20))
        onNowTitle.pack(side=TOP, padx=100, pady=2)

        self.provisionalFrame = Frame(root)
        self.provisionalFrame.pack(side=LEFT, fill=Y)
        provisionalTitle = Label(self.provisionalFrame, text='Provisional',
                                 font=("Helvetica", 20))
        provisionalTitle.pack(side=TOP, padx=80, pady=2)

        self.fetchOnNow()
        self.updateOnNowFrame()

        infoFrame = Frame(root, bg='#999999')
        infoFrame.pack(side=LEFT, fill=Y)

        infoTitle = Label(
            infoFrame, text='Scan your\n Buzzcard\nto prompt \none-time \nregistration', font=("Helvetica", 16))
        infoTitle.pack(side=TOP, padx=20, pady=20)

        infoContent = Label(
            infoFrame, text='After registering,\n\n just scan \n\nto clock in/out', font=("Helvetica", 14))
        infoContent.pack(side=TOP, padx=20, pady=20)

        #newCardButton = Button(onNowFrame,text='test card window',command=self.spawnAddCardWindow)
        # newCardButton.pack()

    def spawnAddCardWindow(self, buzzcardID=None):
        # Testing constant
        if buzzcardID is None:
            buzzcardID = '7777777'

        # Destroy old addCard frame if there already is one
        if self.addCardFrame is not None:
            try:
                self.addCardFrame.destroy()
            except AttributeError:
                pass

        # Create separate window
        self.addCardFrame = Toplevel()
        self.addCardFrame = AddCardFrame(
            self.addCardFrame, self.humanity, buzzcardID)

    def processBuzzcardScan(self, buzzcardID):
        PI = self.humanity.getPIFromBuzzcard(buzzcardID)

        if self.PIisInOnNowDisplay(PI):
            print('already on')
            self.removePIFromOnNow(PI)
            self.addPendingPIToOnNowFrame(PI)
        else:
            self.addPendingPIToOnNowFrame(PI)

        if PI is not None:
            PI_id = PI['id']

            print(self.onNowEmployees)

            # Card is assigned to a PI
            if self.humanity.isOnNow(PI_id):
                self.humanity.clockoutPI(PI_id)
            else:
                self.humanity.clockinPI(PI_id)

            self.fetchOnNow()
        else:
            # Card isn't assigned to a PI yet
            self.spawnAddCardWindow(buzzcardID)

    def fetchOnNow(self):
        self.onNowEmployees = []
        self.onNowEmployees = self.humanity.getOnNow()

        self.pendingEmployees = []

        self.updateOnNowFrame()

    def updateOnNowFrame(self):
        if self.onNowListFrame is not None:
            self.onNowListFrame.destroy()

        if self.provisionalListFrame is not None:
            self.provisionalListFrame.destroy()

        self.onNowListFrame = Frame(self.onNowFrame, bg=self.onNowBG)
        self.onNowListFrame.pack(side=TOP, fill=BOTH)

        self.provisionalListFrame = Frame(
            self.provisionalFrame, bg=self.provisionalBG)
        self.provisionalListFrame.pack(side=TOP, fill=BOTH)

        for PI in self.onNowEmployees:
            self.addPIToOnNowFrame(PI)

        self.updateRootWindowNow()

        return True

    def addPIToOnNowFrame(self, PI):
        target_frame = self.onNowListFrame
        target_bg = self.onNowBG

        if(PI['schedule_name'] == 'Provisional'):
            target_frame = self.provisionalListFrame
            target_bg = self.provisionalBG

        PILabel = Label(target_frame, text=PI['employee_name'], bg=target_bg, font=(
            "Helvetica", self.onNowEntryFontSize))
        PILabel.pack(side=TOP, pady=1)

    def addPendingPIToOnNowFrame(self, PI):
        if PI is None:
            return
        self.pendingEmployees.append(PI)
        fullName = PI['firstname'] + ' ' + PI['lastname']
        PILabel = Label(self.onNowListFrame, text=fullName, bg=self.pendingBG, font=(
            "Helvetica", self.onNowEntryFontSize))
        PILabel.pack(side=TOP, pady=1, fill=BOTH)

        self.updateRootWindowNow()

    def PIisInOnNowDisplay(self, PI):
        if PI is None:
            return False

        id = PI['id']
        for e in self.onNowEmployees + self.pendingEmployees:
            print(e)
            if e['employee_id'] == id:
                return True
        return False

    def removePIFromOnNow(self, PI):
        id = PI['id']

        print("removing employee " + str(id) + " from onNow")

        # Remove from onNow with filter
        newOnNow = []
        for e in self.onNowEmployees:
            if e['employee_id'] != id:
                newOnNow.append(e)

        self.onNowEmployees = newOnNow

        self.updateOnNowFrame()

    def updateRootWindowNow(self):
        self.root.update_idletasks()
        self.root.update()
