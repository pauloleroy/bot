import customtkinter as ctk
import tkinter
import tkinter.messagebox
from tkinter import CENTER, END, NO, RIGHT, VERTICAL, W, Y, YES, ttk

username=''
login_id = ''

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
        self.related_list.grid(row=2,column=1,ipadx=30, ipady=150,pady=2)
        self.remove_button = ctk.CTkButton(master=self.left_frame, text="Remove", command=self.delete_account)
        self.remove_button.grid(row=3, column=1,pady=2)
        self.since_label = ctk.CTkLabel(master=self.left_frame, text="Check since")
        self.since_label.grid(row=4,column=0,pady=2)
        self.since_entry = ctk.CTkEntry(master=self.left_frame)
        self.since_entry.grid(row=4,column=1,pady=10)
        self.search_button = ctk.CTkButton(master=self.left_frame, text="Search", command=self.check_likes)
        self.search_button.grid(row=5, column=1,pady=2)
        self.num_users_label = ctk.CTkLabel(master=self.left_frame, text="Number of Users")
        self.num_users_label.grid(row=0,column=2,padx=10)
        self.num_users_entry = ctk.CTkEntry(master=self.left_frame)
        self.num_users_entry.grid(row=0, column=3,padx=5)
        self.runbot_button = ctk.CTkButton(master=self.left_frame, text="Run BOT", command=self.auto_follow)
        self.runbot_button.grid(row=0,column=4,padx=5)
        self.list_frame = ctk.CTkFrame(master=self.left_frame)
        self.list_frame.grid(row=2, column=2,columnspan=2,rowspan=4,ipady=250, sticky='nsew')
        self.list_frame.grid_rowconfigure(0, weight=1)
        self.list_frame.grid_columnconfigure(0, weight=1)
        columns = ('Account', 'N Pages', 'N Likes')
        self.main_users_list = ttk.Treeview(master=self.list_frame, columns=columns, show='headings')
        self.main_users_list.column("#0", width=0, stretch=NO)
        self.main_users_list.column('Account',anchor=W,stretch=YES)
        self.main_users_list.column('N Pages',width=80,stretch=NO,anchor=CENTER)
        self.main_users_list.column('N Likes',width=80,stretch=NO,anchor=CENTER)
        self.main_users_list.heading("#0", text="",anchor=W)
        self.main_users_list.heading('Account',text="Account",anchor=CENTER)
        self.main_users_list.heading('N Pages',text="N Pages",anchor=CENTER)
        self.main_users_list.heading('N Likes',text="N Likes",anchor=CENTER)
        self.main_users_list.grid(row=0, column=0,sticky="nswe")
        self.main_users_scroll = ttk.Scrollbar(self.list_frame,orient=VERTICAL,command=self.main_users_list.yview)
        self.main_users_scroll.grid(column=1,row=0,sticky="ns")
        self.main_users_list.configure(yscrollcommand=self.main_users_scroll.set)

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
        '''open login pop-up'''
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
        '''close the whole app if login window is closed'''
        self.login.destroy()
        self.destroy()

    def login_app(self):
        '''login to instagram and send user data to DB'''
        #Check if there is a better way then using global variable
        global username
        global login_id
        self.bot.login(self.login.username.get(),self.login.password.get())
        check_login = self.bot.check_login()
        if check_login:
            self.username.set(self.login.username.get().lower())
            username = self.login.username.get().lower()
            self.database.insert_user(username)
            self.user_id = self.database.select_user_id_by_account(username)[0][0]
            login_id = self.database.insert_login_track(self.user_id)
            self.login.destroy()
            self.uptade_screen()
        else:
            #messagebox awarning login fail
            pass
        

    def uptade_screen(self):
        '''uptade main screen after login and uptade follower list on DB'''
        
        """
        #insert login_track
        """
        #loading related list
        self.related_list.delete(0,tkinter.END)
        related_list = self.database.select_related_page(username)
        for item in related_list:
            self.related_list.insert(tkinter.END, item[0])
        #clear and loading followers and following to database       
        self.database.delete_following()
        self.database.delete_follower()
        following_list = self.bot.get_following(username)
        for following in following_list:
            self.database.insert_following(following)
        follower_list = self.bot.get_followers(username)
        for follower in follower_list:
            self.database.insert_follower(follower)
        self.load_like_list()
        
    def add_related_page(self):
        '''add related pages to DB and list box'''
        to_insert = self.database.check_related_id_exists(username,self.user_entry.get().lower())
        if to_insert and self.user_entry.get() != '':
            self.database.insert_related_page(username,self.user_entry.get().lower())
            self.related_list.insert(tkinter.END, self.user_entry.get())
            self.user_entry.delete(0,tkinter.END)
            #insert msgbox
        else:
            #insert msgbox
            pass
        self.load_like_list()
    
    def delete_account(self):
        '''delete related page from DB and listbox'''
        if self.related_list.curselection():
            self.database.delete_related_page(username,self.related_list.get(tkinter.ANCHOR).lower())
            self.related_list.delete(tkinter.ANCHOR)
            #insert msgbox
        self.load_like_list()

    def check_likes(self):
        try:
            int(self.since_entry.get())
        except ValueError:
            #message box
            is_validated =  False
            print("pick valid number")
        else:
            is_validated = True
        if is_validated:
            related_pages = self.database.select_related_page_by_user(username)        
            for page in related_pages:
                url_likes = self.bot.check_likes(page[0], int(self.since_entry.get()))
                related_page_id = self.database.select_instagram_id_by_account(page[0])[0][0]
                for key, values in url_likes.items():
                    photo_id = self.database.insert_photo(related_page_id,key)
                    for account in values:
                        self.database.insert_like_track(photo_id,account)
        self.load_like_list()
    
    def load_like_list(self):
        for item in self.main_users_list.get_children():
            self.main_users_list.delete(item)
        like_list = self.get_like_list()
        for like in like_list:
            self.main_users_list.insert('', END, values=like)
    
    def auto_follow(self):
        try:
            int(self.num_users_entry.get())
        except ValueError:
            #message box
            is_validated =  False
            print("pick valid number")
        else:
            is_validated = True
        if is_validated:
            like_list = self.get_like_list()
            users_followed = 0
            #validate if it was a number inserted on text box
            n_accounts = int(self.num_users_entry.get())
            for account in like_list:
                account = account[0]
                instagram_id = self.database.select_instagram_id_by_account(account)[0][0]
                if users_followed >= n_accounts: break
                it_followed = self.bot.auto_follow(account)
                users_followed += 1
                if it_followed:
                    self.database.insert_bot_follow(login_id,instagram_id)
    
    def get_like_list(self):
        id_list = []
        related_list = self.database.select_related_page(username)
        for user in related_list:
            user = user [0]
            id_list.append(self.database.select_instagram_id_by_account(user)[0][0])
        if len(id_list) > 0:
            like_list = self.database.select_like_list(id_list)
        return like_list