import sqlite3
from tkinter import *
from tkinter import ttk, messagebox
class ContactManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='green')
        title = Label(self.root, text="Contact Book - Shalini's Project", font=(
            "Helvetica", 20, ), bd=8,  bg='black', fg='blue')
        title.pack(side=TOP, fill=X)
        self.firstname = StringVar()
        self.lastname = StringVar()
        self.mobile = StringVar()
        self.addr = StringVar()
        self.pin = StringVar()
        Detail_F = Frame(self.root, bd=4, relief=RIDGE, bg='blue')
        Detail_F.place(x=50, y=130, width=360, height=270)
        lbl_name = Label(Detail_F, text="First Name",
                         font=("Helvetica", 12, ))
        lbl_name.grid(row=1, column=0, pady=10, padx=20, sticky="w")
        txt_name = Entry(Detail_F, font=("Helvetica", 10, ),
                         bd=3,  textvariable=self.firstname)
        txt_name.grid(row=1, column=1, pady=10, sticky="w")

        
        lbl_mob = Label(Detail_F, text="Last Name",
                        font=("Helvetica", 12, ))
        lbl_mob.grid(row=2, column=0, pady=10, padx=20, sticky="w")
        txt_mob = Entry(Detail_F, font=("Helvetica", 10, ),
                        bd=3,  textvariable=self.lastname)
        txt_mob.grid(row=2, column=1, pady=10, sticky="w")

        
        lbl_aa = Label(Detail_F, text="Mobile No.",
                       font=("Helvetica", 12, ))
        lbl_aa.grid(row=3, column=0, pady=10, padx=20, sticky="w")
        txt_aa = Entry(Detail_F, font=("Helvetica", 10, ),
                       bd=3,  textvariable=self.mobile)
        txt_aa.grid(row=3, column=1, pady=10, sticky="w")

        
        lbl_add = Label(Detail_F, text="Address", font=("Helvetica", 12, ))
        lbl_add.grid(row=4, column=0, pady=10, padx=20, sticky="w")
        txt_add = Entry(Detail_F, font=("Helvetica", 10, ),
                        bd=3,  textvariable=self.addr)
        txt_add.grid(row=4, column=1, pady=10, sticky="w")

        
        lbl_pin = Label(Detail_F, text="Email", font=("Helvetica", 12, ))
        lbl_pin.grid(row=5, column=0, pady=10, padx=20, sticky="w")
        txt_pin = Entry(Detail_F, font=("Helvetica", 10, ),
                        bd=3,  textvariable=self.pin)
        txt_pin.grid(row=5, column=1, pady=10, sticky="w")

        recordFrame = Frame(self.root, bd=5, relief=RIDGE)
        recordFrame.place(x=410, y=130, width=560, height=270)

        yscroll = Scrollbar(recordFrame, orient=VERTICAL)
        
        self.contact_table = ttk.Treeview(recordFrame, columns=(
            "firstname", "lastname", "mobile", "address", "pin"), yscrollcommand=yscroll.set)
        yscroll.pack(side=RIGHT, fill=Y)
        yscroll.config(command=self.contact_table.yview)
        self.contact_table.heading("firstname", text="First Name")
        self.contact_table.heading("lastname", text="Last Name")
        self.contact_table.heading("mobile", text="Mobile No.")
        self.contact_table.heading("address", text="Address")
        self.contact_table.heading("pin", text="Email")

        self.contact_table['show'] = 'headings'

        self.contact_table.column("firstname", width=100)
        self.contact_table.column("lastname", width=100)
        self.contact_table.column("mobile", width=100)
        self.contact_table.column("address", width=100)
        self.contact_table.column("pin", width=110)
        self.contact_table.pack(fill=BOTH, expand=1)
        self.fetch_data()
        self.contact_table.bind("<ButtonRelease-1>", self.get_cursor)

        btnFrame = Frame(self.root, bd=5, relief=RIDGE)
        btnFrame.configure(bg="yellow")
        btnFrame.place(x=250, y=400, width=480, height=60)
        btn1 = Button(btnFrame, text='Add record', font='arial 12 bold',
                      bg='black', fg='blue', width=9, command=self.addrecord)
        btn1.grid(row=0, column=0, padx=10, pady=10)
        
        btn2 = Button(btnFrame, text='Update', font='arial 12 bold',
                      bg='black', fg='blue', width=9, command=self.update)
        btn2.grid(row=0, column=1, padx=8, pady=10)
        
        btn3 = Button(btnFrame, text='Delete', font='arial 12 bold',
                      bg='black', fg='blue', width=9, command=self.delete)
        btn3.grid(row=0, column=2, padx=8, pady=10)
        
        btn4 = Button(btnFrame, text='Reset', font='arial 12 bold',
                      bg='black', fg='blue', width=9, command=self.reset)
        btn4.grid(row=0, column=3, padx=8, pady=10)

    def addrecord(self):
        if self.firstname.get() == '' or self.lastname.get() == '' or self.mobile.get() == '' or self.addr.get() == '' or self.pin.get() == '':
            messagebox.showerror('Error', 'Please enter details ?')
        else:
            con = sqlite3.connect('contactbook.db')
            cur = con.cursor()
            cur.execute("Select * from contact")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == self.mobile.get():
                    messagebox.showerror(
                        'Error', 'Duplicates not allowed')
                    return
            cur.execute("insert into contact values(?,?,?,?,?)", (
                self.firstname.get(),
                self.lastname.get(),
                self.mobile.get(),
                self.addr.get(),
                self.pin.get(),
            ))
            con.commit()
            self.fetch_data()
            con.close()

    def fetch_data(self):
        con = sqlite3.connect('contactbook.db')
        cur = con.cursor()
        cur.execute(
            "select firstname , lastname , mobile , addr , pin  from contact")
        rows = cur.fetchall()
        if len(rows) != 0:
            self.contact_table.delete(*self.contact_table.get_children())
            for row in rows:
                self.contact_table.insert('', END, values=row)
        con.commit()
        con.close()

    def update(self):
        if self.mobile.get() == '':
            messagebox.showerror('Error', 'Select a record to update !')
        else:
            con = sqlite3.connect('contactbook.db')
            cur = con.cursor()
            cur.execute("update contact set firstname = ?, lastname = ?, mobile = ?, addr = ?, pin = ? where mobile = ?", (
                self.firstname.get(),
                self.lastname.get(),
                self.mobile.get(),
                self.addr.get(),
                self.pin.get(),
                self.mobile.get()
            ))
            messagebox.showinfo(
                'Info', f'Record {self.mobile.get()} Updated Successfully')
            con.commit()
            con.close()
            self.fetch_data()
            self.reset()
    def delete(self):
        if self.mobile.get() == '':
            messagebox.showerror(
                'Error', 'Enter contact ID to delete the records')
        else:
            con = sqlite3.connect('contactbook.db')
            cur = con.cursor()
            cur.execute("delete from contact where mobile = ?",
                        (self.mobile.get(),))
            con.commit()
            con.close()
            self.fetch_data()
            self.reset()
    def reset(self):
        self.firstname.set('')
        self.lastname.set('')
        self.mobile.set('')
        self.addr.set('')
        self.pin.set('')
    def get_cursor(self, ev):
        cursor_row = self.contact_table.focus()
        content = self.contact_table.item(cursor_row)
        row = content['values']
        if row:
            self.firstname.set(row[0])
        else:
            print("No results found")
        self.lastname.set(row[1])
        self.mobile.set(row[2])
        self.addr.set(row[3])
        self.pin.set(row[4])
class Login():
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book Login Window")
        self.root.geometry("300x180")
        self.root.configure(bg="red")
        self.username = StringVar()
        self.password = StringVar()
        Label(self.root, text="Username:").grid(
            row=0, column=0, padx=10, pady=10)
        Entry(self.root, textvariable=self.username).grid(
            row=0, column=1, padx=10, pady=10)
        Label(self.root, text="Password:").grid(
            row=1, column=0, padx=10, pady=10)
        Entry(self.root, textvariable=self.password,
              show="*").grid(row=1, column=1, padx=10, pady=10)
        Button(self.root, text="Login", command=self.login).grid(
            row=2, column=1, padx=10, pady=10)
    def login(self):
        if self.username.get() == "hello" and self.password.get() == "hello":
           
            root.destroy()
            nroot = Tk()
            ContactManager(nroot)
        else:
            
            messagebox.showerror("Error", "Invalid username or password")
con = sqlite3.connect('contactbook.db')
cur = con.cursor()
cur.execute('create table if not exists contact (firstname varchar(20),lastname varchar(20),mobile varchar(20) primary key , addr varchar(20) , pin varchar(20))')
root = Tk()
obj = Login(root)
root.mainloop()