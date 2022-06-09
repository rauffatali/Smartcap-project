from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image

import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(2)

class Application:
    def __init__(self, root, width=1300, height=900):
        
        # init root window
        self.root = root

        # define height and width of window
        self.width = width
        self.height = height

        # set window title
        self.root.title('Rouen Tourism')

        # set window icon
        self.root.iconphoto(False, ImageTk.PhotoImage(Image.open('./images/icon.png')))

        # center window position
        self.positionRight = int(self.root.winfo_screenwidth()/2 - self.width/1.9)
        self.positionDown = int(self.root.winfo_screenheight()/2 - self.height/1.9)
        self.root.geometry("{}x{}+{}+{}".format(width, height, self.positionRight, self.positionDown))
        
        # initialize main canvas
        self.mainCanvas = Canvas(self.root, width=self.width, height=self.height)
        self.mainCanvas.pack(fill=BOTH, expand=True)

        # set background image
        self.setBackground()

        self.mainCanvas.create_text(
            650, 400, 
            fill='white', font=('Helvetica','30', 'bold'), 
            text='WELCOME ON BOARD'
        )

        # create option menu of recommender systems
        self.setOptionMenu()

        # initialize buttons
        self.selectButton = Button(self.root, text='Select', command=self.selectClicked, width=31, height=2)
        self.mainCanvas.create_window(511, 640, window=self.selectButton)
        self.exitButton = Button(self.root, text='Exit', command=self.root.destroy, width=31, height=2)
        self.mainCanvas.create_window(788, 640, window=self.exitButton)

    def setBackground(self):
        # fit background image to window size
        image = Image.open('./images/background.jpg')
        resizedImage = image.resize((self.width, self.height), Image.ANTIALIAS)
        self.backgroundImage = ImageTk.PhotoImage(resizedImage)
        self.mainCanvas.create_image(0, 0, image=self.backgroundImage, anchor=NW)
    
    def setOptionMenu(self):
        options = (
            (25*' ')+'Recommender System of FATALI Rauf'+(33*' '), 
            (22*' ')+'Recommender System of ALIZADA Nadir'+(31*' '),
            (17*' ')+'Recommender System of HAGVERDIYEV Ramiz'+(27*' ')
        )

        self.optionsVar = StringVar()
        self.optionsVar.set('Choose your recommender system:')
    
        optionMenu = OptionMenu(self.mainCanvas, self.optionsVar, *options)
        optionMenu.config(width=60)
        self.mainCanvas.create_window(650, 500, window=optionMenu)

    def selectClicked(self):
        if 'Rauf' in self.optionsVar.get().split():
            try:
                self.RecommenderEngine.runEngine()
            except:
                messagebox.showwarning('Warning Window', 'Oops, Something went wrong!')

        elif 'Nadir' in self.optionsVar.get().split():
            try: 
                # add your code here
                self.RecommenderEngineNadir.runEngine()
            except:
                messagebox.showwarning('Warning Window', 'Oops, Something went wrong!')

        else:
            try: 
                # add your code here
                self.RecommenderEngineRamiz.runEngine()
            except:
                messagebox.showwarning('Warning Window', 'Oops, Something went wrong!')

class RecommenderEngine:
    def __init__(self, root, canvas):

        self.root = root
        self.canvas = canvas
    
    def runEngine(self):
        self.canvas.delete('all')
 
        # create buttons
        self.newUserButton = Button(self.root, text='New User', command=self.newUserButtonClicked, width=31, height=2)
        self.canvas.create_window(650, 390, window=self.newUserButton)
        self.existingUserButton = Button(self.root, text='Existing User', command=self.existingUserButtonClicked, width=31, height=2)
        self.canvas.create_window(650, 450, window=self.existingUserButton)

if __name__ == '__main__':
    
    root = Tk()
    app = Application(root)
    root.resizable(False, False)
    root.mainloop()