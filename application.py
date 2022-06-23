import uuid
import random
import numpy as np

from tkinter import *
from tkinter import ttk
from tkinter import tix
from tkinter import messagebox

from PIL import ImageTk, Image

from dataframes import *
from recommenderSystem import PopularityBasedFiltering, ModelBasedCF, UserBasedFiltering

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

        # initialize option menu of recommender systems
        self.initOptionMenu()

        # initialize buttons
        self.selectButton = Button(self.root, text='Select', command=self.selectClicked, width=31, height=2)
        self.mainCanvas.create_window(511, 640, window=self.selectButton)
        self.exitButton = Button(self.root, text='Exit', command=self.exitClicked, width=31, height=2)
        self.mainCanvas.create_window(788, 640, window=self.exitButton)

        # call recommender engine in application
        self.RecommenderEngine = RecommenderEngine(self.root, self.mainCanvas)

    def setBackground(self):
        # fit background image to window size
        image = Image.open('./images/background.jpg')
        resizedImage = image.resize((self.width, self.height), Image.ANTIALIAS)
        self.backgroundImage = ImageTk.PhotoImage(resizedImage)
        self.mainCanvas.create_image(0, 0, image=self.backgroundImage, anchor=NW)
    
    def initOptionMenu(self):
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
    
    def exitClicked(self):
        self.root.destroy()

class RecommenderEngine:
    def __init__(self, root, canvas):

        self.root = root
        self.canvas = canvas

        self.ExistingUserWindow = ExistingUserWindow(self.root, self.canvas)
        self.NewUserWindow = NewUserWindow(self.root, self.canvas)
    
    def runEngine(self):
        self.canvas.delete('all')
 
        self.newUserButton = Button(
            self.root, text='New User', 
            command=self.newUserButtonClicked, 
            width=31, height=2)
        self.canvas.create_window(650, 390, window=self.newUserButton)

        self.existingUserButton = Button(
            self.root, text='Existing User', 
            command=self.existingUserButtonClicked, 
            width=31, height=2)
        self.canvas.create_window(650, 450, window=self.existingUserButton)

    def newUserButtonClicked(self):
        
        # delete all widgets from canvas
        self.canvas.delete("all")

        # load new user window
        self.NewUserWindow.load()
    
    def existingUserButtonClicked(self):

        # delete all widgets from canvas
        self.canvas.delete("all")

        # load existing user window
        self.ExistingUserWindow.load()

class NewUserWindow:
    def __init__(self, root, canvas):

        self.root = root
        self.canvas = canvas
    
    def load(self):

        # User Data Frame
        self.userDataFrame = LabelFrame(self.canvas, text='User Data')
        self.userDataFrame.place(height=400, width=600, x=0, y=0)

        # initialize text box labels
        font=("Helvetica", 12)
        f_name_label = Label(self.userDataFrame, text='First Name:', font=font)
        f_name_label.place(x=75, y=10)
        l_name_label = Label(self.userDataFrame, text='Last Name:', font=font)
        l_name_label.place(x=76, y=50)
        gender_label = Label(self.userDataFrame, text='Gender:', font=font)
        gender_label.place(x=105, y=90)
        age_label = Label(self.userDataFrame, text='Age:', font=font)
        age_label.place(x=136, y=130)
        origin_label = Label(self.userDataFrame, text='Origin:', font=font)
        origin_label.place(x=119, y=170)
        country_label = Label(self.userDataFrame, text='Country:', font=font)
        country_label.place(x=103, y=210)
        income_label = Label(self.userDataFrame, text='Income:', font=font)
        income_label.place(x=107, y=250)
        lot_label = Label(self.userDataFrame, text='Length of Trip:', font=font)
        lot_label.place(x=49, y=290)
        ss_label = Label(self.userDataFrame, text='Social State:', font=font)
        ss_label.place(x=65, y=330)
        
        # initialize text boxes and option menus
        self.f_name = Entry(self.userDataFrame, width=30)
        self.f_name.place(x=190, y=11)
        self.l_name = Entry(self.userDataFrame, width=30)
        self.l_name.place(x=190, y=51)

        self.genderOptionsVar = StringVar()
        self.genderOptions = ('Male', 'Female')
        self.genderOM = OptionMenu(self.userDataFrame, self.genderOptionsVar, *self.genderOptions)
        self.genderOM.config(width=24)
        self.genderOM.place(x=188, y=84)
        
        self.age = Entry(self.userDataFrame, width=30)
        self.age.place(x=190, y=130)

        self.originOptionsVar = StringVar()
        self.originOptions = (demographics_df['origin'].unique())
        self.originOM = OptionMenu(self.userDataFrame, self.originOptionsVar, *self.originOptions)
        self.originOM.config(width=24)
        self.originOM.place(x=188, y=163)

        self.countryOptionsVar = StringVar()
        self.countryOptions = (demographics_df['country'].unique())
        self.countryOM = OptionMenu(self.userDataFrame, self.countryOptionsVar, *self.countryOptions)
        self.countryOM.config(width=24)
        self.countryOM.place(x=188, y=203)
        
        self.incomeOptionsVar = StringVar()
        self.incomeOptions = ('Low', 'Average', 'High')
        self.incomeOM = OptionMenu(self.userDataFrame, self.incomeOptionsVar, *self.incomeOptions)
        self.incomeOM.config(width=24)
        self.incomeOM.place(x=188, y=243)

        self.lotOptionsVar = StringVar()
        self.lotOptions = ('short-term', 'long-term')
        self.lotOM = OptionMenu(self.userDataFrame, self.lotOptionsVar, *self.lotOptions)
        self.lotOM.config(width=24)
        self.lotOM.place(x=188, y=283)

        self.socialStateOptionsVar = StringVar()
        self.socialStateOptions = (demographics_df['social_state'].unique())
        socialStateOM = OptionMenu(self.userDataFrame, self.socialStateOptionsVar, *self.socialStateOptions)
        socialStateOM.config(width=24)
        socialStateOM.place(x=188, y=323)      

        # User Interests Frame
        self.interestsFrame = LabelFrame(self.canvas, text='User Interests')
        self.interestsFrame.place(height=400, width=700, x=600, y=0)

        # checklist of user interest
        self.createCheckList()

        self.recommendationFrame = LabelFrame(self.canvas, text='Recommendations')
        self.recommendationFrame.place(height=450, width=1300, x=0, y=400)

        # Option Menu for recommendations
        rec_label = Label(self.recommendationFrame, text='Type of Recommendations:', font=('Helvetica', '11'))
        rec_label.place(x=10, y=11)
        self.recOptionsVar = StringVar()
        self.recOptions = ('Basic Recommendations', 'Contextualized Recommendations')
        self.recOM = OptionMenu(self.recommendationFrame, self.recOptionsVar, *self.recOptions)
        self.recOM.config(width=30)
        self.recOM.place(x=235, y=0)

        # Buttons
        submitButton = Button(self.root, text='Submit', command=self.submitClicked, width=12)
        self.canvas.create_window(65, 875, window=submitButton)

        recommendButton = Button(self.root, text='Recommend POI', command=self.recommendClicked, width=14)
        self.canvas.create_window(183, 875, window=recommendButton)

        clearButton = Button(self.root, text='Clear', command=self.clearClicked, width=12)
        self.canvas.create_window(1125, 875, window=clearButton)

        goBackButton = Button(self.root, text='Back', command=self.goBackClikced, width=12)
        self.canvas.create_window(1235, 875, window=goBackButton)

    def createCheckList(self):
        self.checklist = tix.CheckList(self.interestsFrame)
        self.checklist.pack(expand=1, fill='both')
        self.checklist.hlist.config(bg='#EBEBEB', selectmode='none')

        # Food types
        self.checklist.hlist.add("A", text="Food")
        self.checklist.hlist.add("A.CL1", text="Restaurant")
        self.checklist.hlist.add("A.CL2", text="Cafe")
        self.checklist.hlist.add("A.CL3", text="Pub")
        self.checklist.hlist.add("A.CL4", text="Tea House")

        # Shopping types
        self.checklist.hlist.add("B", text="Shopping")
        self.checklist.hlist.add("B.CL1", text="Library")
        self.checklist.hlist.add("B.CL2", text="Store")

        # Night life types
        self.checklist.hlist.add("C", text="Night Life")
        self.checklist.hlist.add("C.CL1", text="Casino")
        self.checklist.hlist.add("C.CL2", text="Night Club")
        self.checklist.hlist.add("C.CL3", text="Bar")

        # Cultural types
        self.checklist.hlist.add("D", text="Cultural")
        self.checklist.hlist.add("D.CL1", text="Museum")
        self.checklist.hlist.add("D.CL2", text="Art Gallery")
        self.checklist.hlist.add("D.CL3", text="Tourist Attraction")
        self.checklist.hlist.add("D.CL4", text="Landmark and Historical Building")
        self.checklist.hlist.add("D.CL5", text="Church")
        self.checklist.hlist.add("D.CL6", text="Synagogue")
        self.checklist.hlist.add("D.CL7", text="Mosque")

        # Accommodation types
        self.checklist.hlist.add("E", text="Accommodation")
        self.checklist.hlist.add("E.CL1", text="Lodging")

        # Sport types
        self.checklist.hlist.add("F", text="Sport")
        self.checklist.hlist.add("F.CL1", text="SPA")
        self.checklist.hlist.add("F.CL2", text="Gym")
        self.checklist.hlist.add("F.CL3", text="Stadium")
        self.checklist.hlist.add("F.CL4", text="Bike Sharing")

        # Nature types
        self.checklist.hlist.add("G", text="Nature")
        self.checklist.hlist.add("G.CL1", text="Park")

        # Entertainment types
        self.checklist.hlist.add("H", text="Entertainment")
        self.checklist.hlist.add("H.CL1", text="Movie Theater")
        self.checklist.hlist.add("H.CL2", text="Bowling Alley")

        self.setChecklistmodeOff()    
        self.checklist.autosetmode()
    
    def setChecklistmodeOff(self):

         # self.checklist.setstatus("A", "off")
        self.checklist.setstatus("A.CL1", "off")
        self.checklist.setstatus("A.CL2", "off")
        self.checklist.setstatus("A.CL3", "off")
        self.checklist.setstatus("A.CL4", "off")

        # self.checklist.setstatus("B", "off")
        self.checklist.setstatus("B.CL1", "off")
        self.checklist.setstatus("B.CL2", "off")

        # self.checklist.setstatus("C", "off")
        self.checklist.setstatus("C.CL1", "off")
        self.checklist.setstatus("C.CL2", "off")
        self.checklist.setstatus("C.CL3", "off")

        # self.checklist.setstatus("D", "off")
        self.checklist.setstatus("D.CL1", "off")
        self.checklist.setstatus("D.CL2", "off")
        self.checklist.setstatus("D.CL3", "off")
        self.checklist.setstatus("D.CL4", "off")
        self.checklist.setstatus("D.CL5", "off")
        self.checklist.setstatus("D.CL6", "off")
        self.checklist.setstatus("D.CL7", "off")

        # self.checklist.setstatus("E", "off")
        self.checklist.setstatus("E.CL1", "off")

        # self.checklist.setstatus("F", "off")
        self.checklist.setstatus("F.CL1", "off")
        self.checklist.setstatus("F.CL2", "off")
        self.checklist.setstatus("F.CL3", "off")
        self.checklist.setstatus("F.CL4", "off")

        # self.checklist.setstatus("G", "off")
        self.checklist.setstatus("G.CL1", "off")

        # self.checklist.setstatus("H", "off")
        self.checklist.setstatus("H.CL1", "off")
        self.checklist.setstatus("H.CL2", "off")

    def submitClicked(self):
        # initialize user id
        s = True
        while s:
            self.user_id = str(uuid.uuid4())
            if self.user_id not in demographics_df['user_id'].tolist():
                s = False

        # retrieve user data
        gender = self.genderOptionsVar.get()
        username = ''.join([self.f_name.get().lower(), self.l_name.get().lower()])
        origin = ''.join(self.originOptionsVar.get().split())
        age = self.age.get()
        country = ''.join(self.countryOptionsVar.get().split())
        income = self.incomeOptionsVar.get()
        length_of_trip = self.lotOptionsVar.get()
        social_state = self.socialStateOptionsVar.get()

        # replace none value attributes with NaN value
        if username == '':
            username = np.NaN
        if gender == '':
            gender = np.NaN
        if origin == '':
            origin = np.NaN
        if age == '':
            age = np.NaN
        if country == '':
            country = np.NaN
        if income == '':
            income = np.NaN
        if length_of_trip == '':
            length_of_trip = np.NaN
        if social_state == '':
            social_state = np.NaN

        # create user profile
        user_profile = pd.DataFrame({
            'user_id': self.user_id,
            'gender': gender,
            'username': username,
            'origin': origin,
            'age': age,
            'country': country,
            'income': income,
            'length_of_trip': length_of_trip,
            'social_state': social_state,
            'agreeableness': round(random.choice(np.arange(0.1, 1, 0.1)), 2)
        }, index=[0])

        if user_profile.isnull().values.any():
            messagebox.showwarning('Warning Window', 'Please fill in all the required fields!')
        else:
            # add to user database
            self.demographics_df_new = demographics_df.append(user_profile, ignore_index=True)
            messagebox.showinfo('Information Window', 'Submitted Successfully!')
    
    def recommendClicked(self):

        selected_interests = []
        for selected in self.checklist.getselection():
            interest = self.checklist.hlist.item_cget(selected, 0, '-text').lower()
            if len(interest.split()) > 1:
                interest = '_'.join(interest.split())
            selected_interests.append(interest)

        if 'Basic' in self.recOptionsVar.get().split():
            self.demographics_df_new['origin'] = self.demographics_df_new['origin'].apply(clean_demographics)
            self.demographics_df_new['country'] = self.demographics_df_new['country'].apply(clean_demographics)
            self.demographics_df_new['age'] = self.demographics_df_new['age'].astype('str')
            # create user soup
            columns = ['age', 'gender', 'country', 'income', 'length_of_trip', 'social_state']
            self.demographics_df_new['user_profile'] = self.demographics_df_new[columns].T.agg(' '.join)
            model = UserBasedFiltering(self.user_id, self.demographics_df_new)
            recommendations_df = model.make_recommendation()
            recommendations_df = PopularityBasedFiltering(recommendations_df).generate_scores()

            for index, row in recommendations_df.iterrows():
                if row['type_2'] in selected_interests:
                    recommendations_df.loc[index, 'score'] = recommendations_df.loc[index, 'score']*1.5
            
            recommendations_df = recommendations_df.sort_values('score', ascending=False)
            
            self.recsTree = ttk.Treeview(self.recommendationFrame)
            self.recsTree.place(x=15, y=50, height=355, width=1260)

            recommendations_df = recommendations_df[['place_name', 'place_types', 'average_rating', 'user_ratings_total', 'score']]
            self.recsTree['columns'] = list(recommendations_df.columns)
            self.recsTree['show'] = 'headings'

            for column in self.recsTree['columns']:
                self.recsTree.heading(column, text=column)

            recommendations_df_rows = recommendations_df.to_numpy().tolist()
            for row in recommendations_df_rows:
                self.recsTree.insert('', 'end', values=row)
        else:
            messagebox.showwarning('Warning Window', 'Choose your recommendation type!')
    
    def clearClicked(self):
        
        self.setChecklistmodeOff() 
        self.recsTree.delete(*self.recsTree.get_children())
        

    def goBackClikced(self):
        self.canvas.delete('all')
        self.userDataFrame.place_forget()
        self.recommendationFrame.place_forget()
        self.interestsFrame.place_forget()
        RecommenderEngine(self.root, self.canvas).runEngine()

class ExistingUserWindow:
    def __init__(self, root, canvas):

        self.root = root
        self.canvas = canvas
    
    def load(self):
        self.userFrame = LabelFrame(self.canvas, text='User Data')
        self.userFrame.place(height=365, width=490, x=0, y=0)

        self.userCanvas = Canvas(self.userFrame, height=400, width=500)
        self.userCanvas.pack(fill=BOTH, expand=True)

        font = ('Helvetica', '11')
        self.userCanvas.create_text(75, 30, text='Username:', font=font)

        # create textbox
        self.inputTextBox = Text(self.userFrame, height=1, width=32)
        self.userCanvas.create_window(290, 30, window=self.inputTextBox)

        # User Columns
        data_font = ('Helvetica', '10', 'bold')
        self.userCanvas.create_text(90, 74, text='User ID:', font=data_font)
        self.userCanvas.create_text(90, 111, text='Gender:', font=data_font)
        self.userCanvas.create_text(105, 148, text='Age:', font=data_font)
        self.userCanvas.create_text(88, 185, text='Country:', font=data_font)
        self.userCanvas.create_text(91, 222, text='Income:', font=data_font)
        self.userCanvas.create_text(65, 259, text='Length of trip:', font=data_font)
        self.userCanvas.create_text(73, 296, text='Social state:', font=data_font)

        self.placesFrame = LabelFrame(self.canvas, text='Rated Places')
        self.placesFrame.place(height=365, width=810, x=490, y=0)

        self.placeCanvas = Canvas(self.placesFrame, height=400, width=800)
        self.placeCanvas.pack(fill=BOTH, expand=True)

        self.placeCanvas.create_text(120, 30, text='Number of Rated Places:', font=font)

        self.recommendationFrame = LabelFrame(self.canvas, text='Recommendations')
        self.recommendationFrame.place(height=485, width=1300, x=0, y=365)

        # Option Menu for recommendations
        rec_label = Label(self.recommendationFrame, text='Type of Recommendations:', font=font)
        rec_label.place(x=10, y=11)

        self.recOptionsVar = StringVar()
        self.recOptions = ('Basic Recommendations', 'Contextualized Recommendations')
        self.recOM = OptionMenu(self.recommendationFrame, self.recOptionsVar, *self.recOptions)
        self.recOM.config(width=30)
        self.recOM.place(x=235, y=0)

        # Buttons
        getButton = Button(self.root, text='Show Profile', command=self.showProfileClicked, width=12)
        self.canvas.create_window(65, 875, window=getButton)

        recommendButton = Button(self.root, text='Recommend POI', command=self.recommendClicked, width=14)
        self.canvas.create_window(183, 875, window=recommendButton)

        metricsButton = Button(self.root, text='Show Metrics', command=self.showMetricsClicked, width=14)
        self.canvas.create_window(310, 875, window=metricsButton)

        clearButton = Button(self.root, text='Clear', command=self.clearClicked, width=12)
        self.canvas.create_window(1125, 875, window=clearButton)

        goBackButton = Button(self.root, text='Back', command=self.goBackClikced, width=12)
        self.canvas.create_window(1235, 875, window=goBackButton)
    
    def showProfileClicked(self):

        user = demographics_df[demographics_df['username']==str(self.inputTextBox.get(1.0, "end-1c"))]

        # User Personal Information
        self.user_data = [
            str(user['user_id'].values[0]),
            str(user['gender'].values[0]),
            str(user['age'].values[0]),
            str(user['country'].values[0]),
            str(user['income'].values[0]),
            str(user['length_of_trip'].values[0]),
            str(user['social_state'].values[0])]

        y = 74
        self.labels = []
        for i in range(len(self.user_data)):
            self.user_label = Label(self.userCanvas, text=self.user_data[i], 
                                    font=('Helvetica', 10), bd=1, 
                                    relief='sunken', 
                                    width=36, height=1)
            self.userCanvas.create_window(290, y, window=self.user_label)
            y+=37
            self.labels.append(self.user_label)

        rated_places = merged_df[merged_df['user_id']==self.user_data[0]]
        self.no_places = Label(self.placeCanvas, text=str(len(rated_places)), font=('Helvetica', 12), bd=1, 
                               relief='sunken', justify='left', width=4, height=1)
        self.placeCanvas.create_window(255, 27, window=self.no_places)

        self.placesTree = ttk.Treeview(self.placesFrame)
        self.placesTree.place(x=20, y=60, height=250, width=750)

        df = rated_places[['place_name', 'type_1', 'type_2', 'rating']]
        self.placesTree['columns'] = list(df.columns)
        self.placesTree['show'] = 'headings'

        for column in self.placesTree['columns']:
            self.placesTree.heading(column, text=column)

        df_rows = df.to_numpy().tolist()
        for row in df_rows:
            self.placesTree.insert('', 'end', values=row)
    
    def recommendClicked(self):
        if 'Basic' in self.recOptionsVar.get().split():
            self.model = ModelBasedCF()
            recommendations_df = self.model.make_recommendations(self.user_data[0])
            recommendations_df = PopularityBasedFiltering(recommendations_df).generate_scores()

            self.recsTree = ttk.Treeview(self.recommendationFrame)
            self.recsTree.place(x=15, y=50, height=355, width=1260)

            recommendations_df = recommendations_df[['place_name', 'place_types', 'average_rating', 'user_ratings_total', 'score']]
            self.recsTree['columns'] = list(recommendations_df.columns)
            self.recsTree['show'] = 'headings'

            for column in self.recsTree['columns']:
                self.recsTree.heading(column, text=column)

            recommendations_df_rows = recommendations_df.to_numpy().tolist()
            for row in recommendations_df_rows:
                self.recsTree.insert('', 'end', values=row)

        elif 'Contextualized' in self.recOptionsVar.get().split():
            self.model = ModelBasedCF()
            recommendations_df = self.model.make_recommendations(self.user_data[0])
            recommendations_df = PopularityBasedFiltering(recommendations_df).generate_scores()

            self.recsTree = ttk.Treeview(self.recommendationFrame)
            self.recsTree.place(x=15, y=50, height=355, width=1260)

            recommendations_df = recommendations_df[['place_name', 'place_types', 'average_rating', 'user_ratings_total']]
            self.recsTree['columns'] = list(recommendations_df.columns)
            self.recsTree['show'] = 'headings'

            for column in self.recsTree['columns']:
                self.recsTree.heading(column, text=column)

            recommendations_df_rows = recommendations_df.to_numpy().tolist()
            for row in recommendations_df_rows:
                self.recsTree.insert('', 'end', values=row)

        else:
            messagebox.showwarning('Warning Window', 'Choose your recommendation type!')
        
    def showMetricsClicked(self):
        
        # show rmse of recommender model
        rmse_text = Label(self.recommendationFrame, text='RMSE:', font=('Helvetica', 11, 'bold'))
        rmse_text.place(x=15, y=422)

        rmse_label = Label(self.recommendationFrame, text=self.model.rmse,
                           font=('Helvetica', 12), relief='sunken',
                           width=5, height=1)
        rmse_label.place(x=82, y=419)

        # show mae of recommender model
        mae_text = Label(self.recommendationFrame, text='MAE:', font=('Helvetica', 11, 'bold'))
        mae_text.place(x=155, y=422)

        mae_label = Label(self.recommendationFrame, text=self.model.mae,
                           font=('Helvetica', 12), relief='sunken',
                           width=5, height=1)
        mae_label.place(x=212, y=419)
    
    def clearClicked(self):
        self.placesTree.delete(*self.placesTree.get_children())
        self.recsTree.delete(*self.recsTree.get_children())
        for label in self.labels:
            label.destroy()
        self.no_places.destroy()

    def goBackClikced(self):
        self.canvas.delete('all')
        self.userFrame.place_forget()
        self.recommendationFrame.place_forget()
        self.placesFrame.place_forget()
        RecommenderEngine(self.root, self.canvas).runEngine()

if __name__ == '__main__':
    root = tix.Tk()
    app = Application(root)
    root.resizable(False, False)
    root.mainloop()