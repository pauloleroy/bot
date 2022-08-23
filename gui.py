from cgitb import text
from turtle import width
import customtkinter as ctk
import tkinter
import tkinter.messagebox

username=''

ctk.set_appearance_mode("light")
class App(ctk.CTk):
    w = 1180 #get user computer resolution
    h = 620
    def __init__(self, bot, database):
        super().__init__()
        self.state("zoomed")
        self.title("Instagram BOT")
        self.geometry(f"{App.w}x{App.h}")
        self.bot = bot
        self.database = database

        self.username = ctk.StringVar()

        self.grid_rowconfigure(1, weight=1)
        self.top_frame = ctk.CTkFrame(master=self)
        self.top_frame.grid(row=0,column=0,columnspan=2,padx=5, pady=5, sticky="we")
        self.left_frame = ctk.CTkFrame (master=self, height=App.h-100)
        self.left_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nswe")
        self.right_frame = ctk.CTkFrame (master=self, height=App.h-100)
        self.right_frame.grid(row=1, column=1,pady=5,padx=5,ipadx=150, sticky="nswe")
        self.right_frame.propagate(False)
        self.left_frame.propagate(False)

        self.login_label = ctk.CTkLabel(master=self.top_frame, text='User:', anchor="e")
        self.login_label.grid(row=0,column=0, padx=15, pady=5)
        self.login_entry = ctk.CTkLabel(master=self.top_frame, textvariable=self.username,)
        self.login_entry.grid(row=0,column=1)

        self.user_label = ctk.CTkLabel(master=self.left_frame, text="Related Users")
        self.user_label.grid(row=0,column=0,pady=5)
        self.user_entry = ctk.CTkEntry(master=self.left_frame)
        self.user_entry.grid(row=0,column=1, ipadx=40)
        self.add_button = ctk.CTkButton(master=self.left_frame, text="Add", command=self.add_related_page)
        self.add_button.grid(row=1,column=1,pady=2)
        self.list_label = ctk.CTkLabel(master=self.left_frame, text="List")
        self.list_label.grid(row=2,column=0, padx=10, sticky="ne",pady=2)
        self.related_list = tkinter.Listbox(master=self.left_frame)
        self.related_list.grid(row=2,column=1,ipadx=40, ipady=150,pady=2)
        self.remove_button = ctk.CTkButton(master=self.left_frame, text="Remove", command=self.delete_account)
        self.remove_button.grid(row=3, column=1,pady=2)
        self.since_label = ctk.CTkLabel(master=self.left_frame, text="Check since")
        self.since_label.grid(row=4,column=0,pady=2)
        self.since_entry = ctk.CTkEntry(master=self.left_frame)
        self.since_entry.grid(row=4,column=1,pady=10)
        self.search_button = ctk.CTkButton(master=self.left_frame, text="Search")
        self.search_button.grid(row=5, column=1,pady=2)
        self.num_users_label = ctk.CTkLabel(master=self.left_frame, text="Number of Users")
        self.num_users_label.grid(row=0,column=2,padx=10)
        self.num_users_entry = ctk.CTkEntry(master=self.left_frame)
        self.num_users_entry.grid(row=0, column=3,padx=5)
        self.runbot_button = ctk.CTkButton(master=self.left_frame, text="Run BOT")
        self.runbot_button.grid(row=0,column=4,padx=5)
        self.main_users_list = tkinter.Listbox(master=self.left_frame)
        self.main_users_list.grid(row=1, column=3,columnspan=2,rowspan=4, ipadx=120,ipady=250)

        self.right_frame.grid_rowconfigure(1,weight=1)
        self.unfollow_since_label = ctk.CTkLabel(master=self.right_frame, text="Since")
        self.unfollow_since_label.grid(row=0,column=0,pady=5)
        self.unfollow_since_entry = ctk.CTkEntry(master=self.right_frame)
        self.unfollow_since_entry.grid(row=0,column=1)
        self.unfollow_button = ctk.CTkButton(master=self.right_frame, text='Unfollow All')
        self.unfollow_button.grid(row=0,column=2,padx=10)
        self.unfollow_list = tkinter.Listbox(master=self.right_frame)
        self.unfollow_list.grid(row=1,column=0,columnspan=3,sticky="ns", pady=20,ipadx=60)

        self.open_login_window()

    def open_login_window(self):
        self.login = ctk.CTkToplevel(self)
        self.login.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.login.grab_set()
        self.login.title("Login")
        self.login.geometry('300x140')
        self.login.username_label = ctk.CTkLabel (master=self.login, text='User')
        self.login.username_label.grid(row=0,column=0,pady=5,padx=5)
        self.login.username = ctk.CTkEntry(master=self.login)
        self.login.username.grid(row=0,column=1,pady=5,padx=5)
        self.login.password_label = ctk.CTkLabel (master=self.login, text='password')
        self.login.password_label.grid(row=1,column=0,pady=5,padx=5)
        self.login.password = ctk.CTkEntry(master=self.login)
        self.login.password.grid(row=1,column=1,pady=5,padx=5)
        self.login.confirm_button = ctk.CTkButton(master=self.login, text='Confirm', command=self.login_app)
        self.login.confirm_button.grid(row=2,pady=5,padx=5)
        

    def on_closing(self):
        self.login.destroy()
        self.destroy()

    def login_app(self):
        #Check if there is a better way then using global variable
        global username
        #check if login on instagram was successful instagram before open main gui
        if True:
            self.username.set(self.login.username.get().lower())
            username = self.login.username.get().lower()
            self.database.insert_user(username)
            self.login.destroy()
            self.uptade_screen()
        

    def uptade_screen(self):
        
        """
        #check if login was successful instagram before open main gui
        #insert user to database if doesnt exist
        #insert login_track
        """
        #loading related list
        self.related_list.delete(0,tkinter.END)
        related_list = self.database.load_related_page(username)
        for item in related_list:
            self.related_list.insert(tkinter.END, item[0])
        #clear and loading followers and following to database       
        '''
        self.database.delete_following()
        self.database.delete_follower()
        following_list = self.bot.get_following(username)
        follower_list = self.bot.get_followers(username)
        for following in following_list:
            self.database.insert_following(following)
        for follower in follower_list:
            self.database.insert_follower(follower)
        '''
        
    def add_related_page(self):
        to_insert = self.database.check_related_id_exists(username,self.user_entry.get().lower())
        if to_insert and self.user_entry.get() != '':
            self.database.insert_related_page(username,self.user_entry.get().lower())
            self.related_list.insert(tkinter.END, self.user_entry.get())
            self.user_entry.delete(0,tkinter.END)
            #insert msgbox
        else:
            #insert msgbox
            pass
        
    
    def delete_account(self):
        if self.related_list.curselection():
            self.database.delete_related_page(username,self.related_list.get(tkinter.ANCHOR).lower())
            self.related_list.delete(tkinter.ANCHOR)
            #insert msgbox