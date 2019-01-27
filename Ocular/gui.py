from tkinter import *
from time import sleep
from log import logger
from model import model

name_entry = ''
age_entry = ''
sex_entry = ''
email_entry = ''
pass1_entry = ''

def reg_open():

    def register():
        name_entry = name.get()
        age_entry = age.get()
        sex_entry = sex.get()
        email_entry = email.get()
        pass1_entry = pass1.get()

        registerData = [name_entry, age_entry, sex_entry, email_entry, pass1_entry]

        logger(registerData)
        
        login_open()
    
    Label (window, text = "Name", width=50, bg = "grey", fg="white", font="none 14 bold") .grid(row = 3, column = 0, sticky = '')
    name = Entry(window, width=20, bg="white", fg = "black")
    name.grid(row=3, column=1, sticky='')

    Label (window, text = "Age", width=50, bg = "grey", fg="white", font="none 14 bold") .grid(row = 4, column = 0, sticky = '')
    age = Entry(window, width=20, bg="white", fg = "black")
    age.grid(row=4, column=1, sticky='')

    Label (window, text = "Sex", width=50, bg = "grey", fg="white", font="none 14 bold") .grid(row = 5, column = 0, sticky = '')
    sex = Entry(window, width=20, bg="white", fg = "black")
    sex.grid(row=5, column=1, sticky='')

    Label (window, text = "Username", width=50, bg = "grey", fg="white", font="none 14 bold") .grid(row = 6, column = 0, sticky = '')
    email = Entry(window, width=20, bg="white", fg = "black")
    email.grid(row=6, column=1, sticky='')

    Label (window, text = "Set password", width=50, bg = "grey", fg="white", font="none 14 bold") .grid(row = 7, column = 0, sticky = '')
    pass1 = Entry(window, width=20, bg="white", fg = "black")
    pass1.grid(row=7, column=1, sticky='')

    Button(window, text='Register', width=10, command=register).grid(row=8, column=0, sticky='')
            
def login_open():

    def bilLevels():
        model.bilLevels()

    def cholLevels():
        model.cholLevels()

    def catLevels():
        model.catLevels()

    def login():

        log = ['a'] #csv file data

        loginUserID = email_login.get()
        loginPass = pass_login.get()


        if loginUserID in log and loginPass in log:

            window2.destroy()
            
            window4 = Tk()
            window4.title("OCULAR")
            window4.resizable(0, 0)
            window4.configure(background = "white")

            Label(window4, text = "Select what type of analysis you want.", bg = "white", fg="black", font="none 16 bold") .grid(row = 4, column = 0, sticky = '')

            Button(window4, text='Bilirubin levels', width=20, command=bilLevels).grid(row=5, column=0, sticky='')
            Button(window4, text='Cholesterol levels', width=20, command=cholLevels).grid(row=6, column=0, sticky='')
            Button(window4, text='Catarct levels', width=20, command=catLevels).grid(row=7, column=0, sticky='')

            
        else:
            window3 = Tk()
            window3.title("ERROR")
            window3.resizable(0, 0)
            window3.configure(background = "white")

            Label(window3, text = "Either Username or \nPassword is incorrect!", bg = "white", fg="black", font="none 16 bold") .grid(row = 1, column = 0, sticky = '')

    window.destroy()
    
    window2 = Tk()
    window2.title("OCULAR")
    window2.resizable(0, 0)
    window2.configure(background = "white")    
    
    Label (window2, text = "OCULAR | LOGIN", bg = "white", fg="black", font="none 18 bold") .grid(row = 3, column = 0, sticky = '')

    Label (window2, text = "Username", width=50, bg = "grey", fg="white", font="none 14 bold") .grid(row = 4, column = 0, sticky = '')
    email_login = Entry(window2, width=20, bg="white", fg = "black")
    email_login.grid(row=4, column=1, sticky='')

    Label (window2, text = "Set password", width=50, bg = "grey", fg="white", font="none 14 bold") .grid(row = 5, column = 0, sticky = '')
    pass_login = Entry(window2, width=20, bg="white", fg = "black")
    pass_login.grid(row=5, column=1, sticky='')

    Button(window2, text='Login', width=10, command=login).grid(row=6, column=0, sticky='')
    
window = Tk()
window.title("OCULAR")
window.resizable(0, 0)
window.configure(background = "white")

background_img = PhotoImage(file = "logo.gif")


Label (window, image = background_img, bg = "white") .grid(row = 0, column = 0, sticky = '')

Label (window, text = "Welcome to OCULAR! Your one step diagnostic tool.", bg = "white", fg="black", font="none 18 bold") .grid(row = 1, column = 0, sticky = '')

Button(window, text="REGISTER", width = 10, command=reg_open). grid(row=2, column=0,columnspan=1, sticky='W')
Button(window, text="LOGIN", width = 10, command=login_open). grid(row=2, column=1,columnspan=1, sticky='W')

window.mainloop()
