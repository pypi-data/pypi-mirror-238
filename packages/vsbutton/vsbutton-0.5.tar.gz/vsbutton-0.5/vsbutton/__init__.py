from tkinter import *


class VSButton:

    def __init__(self, master, heading="The Default Heading", desc="This is the default description (First Line)", secdesc = "and this is the second desc", icon=None, color="lightblue", theme='light'):
        # light: bg=#f5f5f5, border = #f1f1f1

        self.vsButton = Frame(master=master, width=450, height=150)
        self.border1 = Frame(master=self.vsButton, width=500, height=1)
        self.border2 = Frame(master=self.vsButton, width=500, height=1)
        self.border3 = Frame(master=self.vsButton, width=1, height=150)
        self.border4 = Frame(master=self.vsButton, width=1, height=150)

        self.border1.place(x=0, y=0)
        self.border2.place(x=0, y=149)
        self.border3.place(x=0, y=0)
        self.border4.place(x=449, y=0)

        self._heading_ = Label(master=self.vsButton, text=heading, font=("Segoe UI", 17))
        self._heading_.place(x=70, y=25)

        self._descp_ = Label(master=self.vsButton, text=desc, font=("Segoe UI", 10),
                     bg="#f5f5f5")
        self._descp_.place(x=70, y=65)

        self.optional_desc = Label(master=self.vsButton, text=secdesc, font=("Segoe UI", 10),
                              bg="#f5f5f5")
        self.optional_desc.place(x=70, y=87)

        if icon == None:
            self.icon = Label(master=self.vsButton, bg='black')
        else:
            self.iconPhoto = PhotoImage(file=icon)
            self.icon = Label(master=self.vsButton, image=self.iconPhoto)
        self.icon.place(x=20, y=35)


        if theme == 'light':
            self.vsButton.config(background="#f5f5f5")
            self.border1.config(bg="#f1f1f1")
            self.border2.config(bg="#f1f1f1")
            self.border3.config(bg="#f1f1f1")
            self.border4.config(bg="#f1f1f1")
            self._heading_.config(bg="#f5f5f5")
            self._descp_.config(bg="#f5f5f5")
            self.optional_desc.config(bg="#f5f5f5")
            self.icon.config(bg="#f5f5f5")

        elif theme == 'dark':
            self.vsButton.config(background="#333337")
            self.border1.config(bg="#333337")
            self.border2.config(bg="#333337")
            self.border3.config(bg="#333337")
            self.border4.config(bg="#333337")
            self._heading_.config(bg="#333337",fg='white')
            self._descp_.config(bg="#333337",fg='white')
            self.optional_desc.config(bg="#333337",fg='white')
            self.icon.config(bg="#333337")


        self.vsButton.bind("<Enter>", lambda event, h=heading, d=desc, sd=secdesc, ico=icon, th=theme, colr=color: self.hover(event, h, d, sd, ico, th, colr))
        self.vsButton.bind("<Leave>", lambda event, h=heading, d=desc, sd=secdesc, ico=icon, th=theme, colr=color: self.NotHover(event, h, d, sd, ico, th, colr))

    def command(self, commandName):
        self.vsButton.bind("<Button-1>", commandName)
        self._heading_.bind("<Button-1>", commandName)
        self._descp_.bind("<Button-1>", commandName)
        self.optional_desc.bind("<Button-1>", commandName)
        self.icon.bind("<Button-1>", commandName)

    def hover(self, event, heading, desc, secdesc, icon, theme, color):
        # Handle hover event using the provided parameters
        if theme == 'light':
            self.vsButton.config(background="#d2d2d2")
            self._heading_.config(background="#d2d2d2")
            self._descp_.config(background="#d2d2d2")
            self.optional_desc.config(background="#d2d2d2")
            self.icon.config(bg='#d2d2d2')
            self.border1.config(bg='#5f8fa7')
            self.border2.config(bg='#5f8fa7')
            self.border3.config(bg='#5f8fa7')
            self.border4.config(bg='#5f8fa7')

        elif theme == 'dark':
            self.vsButton.config(background="#4a4a4e")
            self._heading_.config(background="#4a4a4e")
            self._descp_.config(background="#4a4a4e")
            self.optional_desc.config(background="#4a4a4e")
            self.icon.config(bg="#4a4a4e")
            self.border1.config(bg="#d2d2d2")
            self.border2.config(bg="#d2d2d2")
            self.border3.config(bg="#d2d2d2")
            self.border4.config(bg="#d2d2d2")


    def NotHover(self, event, heading, desc, secdesc, icon, theme, color):
        # Handle mouse leave event using the provided parameters
        if theme == 'light':
            self.vsButton.config(background="#f5f5f5")
            self._heading_.config(background="#f5f5f5")
            self._descp_.config(background="#f5f5f5")
            self.optional_desc.config(background="#f5f5f5")
            self.icon.config(bg="#f5f5f5")
            self.border1.config(bg="#f1f1f1")
            self.border2.config(bg="#f1f1f1")
            self.border3.config(bg="#f1f1f1")
            self.border4.config(bg="#f1f1f1")

        if theme == 'dark':
            self.vsButton.config(background="#333337")
            self.border1.config(bg="#333337")
            self.border2.config(bg="#333337")
            self.border3.config(bg="#333337")
            self.border4.config(bg="#333337")
            self._heading_.config(bg="#333337", fg='white')
            self._descp_.config(bg="#333337", fg='white')
            self.optional_desc.config(bg="#333337", fg='white')
            self.icon.config(bg="#333337")

    def place(self, xAxis, yAxis):
        self.vsButton.place(x=xAxis, y=yAxis)