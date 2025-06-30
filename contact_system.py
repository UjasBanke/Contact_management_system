from tkinter import *
import os
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, 'contact.db')
import sqlite3
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox

root = Tk()
root.title("Contact Management System")
width = 900
height = 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)
root.config(bg="#6666ff")


NAME = StringVar()
GENDER = StringVar()
ADDRESS = StringVar()
CONTACT = StringVar()



def Database():
    tree.delete(*tree.get_children()) 
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, name TEXT, gender TEXT, address TEXT, contact TEXT)")
    cursor.execute("SELECT * FROM `member` ORDER BY `name` ASC")
    fetch = cursor.fetchall()
    
    count = 1
    for data in fetch:
        tree.insert('', 'end', values=(count, data[1], data[2], data[3], data[4]))
        count += 1

    cursor.close()
    conn.close()


def SubmitData():
    if NAME.get() == "" or GENDER.get() == "" or ADDRESS.get() == "" or CONTACT.get() == "":
        tkMessageBox.showwarning('', 'Please Complete The Required Field', icon="warning")
    else:
        conn = sqlite3.connect(db_path)

        cursor = conn.cursor()
        cursor.execute("INSERT INTO `member` (name, gender, address, contact) VALUES(?, ?, ?, ?)", (str(NAME.get()), str(GENDER.get()), str(ADDRESS.get()), str(CONTACT.get())))
        conn.commit()
        cursor.close()
        conn.close()
        Database() 
        NAME.set("")
        GENDER.set("")
        ADDRESS.set("")
        CONTACT.set("")

def UpdateData():
    if NAME.get() == "":
        tkMessageBox.showwarning('', 'Please Complete The Required Field', icon="warning")
    else:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE `member` SET `name` = ?, `gender` =?, `address` = ?, `contact` = ? WHERE `mem_id` = ?", (str(NAME.get()), str(GENDER.get()), str(ADDRESS.get()), str(CONTACT.get()), int(mem_id)))
        conn.commit()
        cursor.close()
        conn.close()
        Database()  
        NAME.set("")
        GENDER.set("")
        ADDRESS.set("")
        CONTACT.set("")


def OnSelected(event):
    global mem_id, UpdateWindow
    curItem = tree.focus()
    contents = (tree.item(curItem))
    selecteditem = contents['values']
    mem_id = selecteditem[0]
    NAME.set(selecteditem[1])
    GENDER.set(selecteditem[2])
    ADDRESS.set(selecteditem[3])
    CONTACT.set(selecteditem[4])

    UpdateWindow = Toplevel()
    UpdateWindow.title("Update Contact")
    width = 400
    height = 250
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = ((screen_width/2) + 450) - (width/2)
    y = ((screen_height/2) + 20) - (height/2)
    UpdateWindow.resizable(0, 0)
    UpdateWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))

    FormTitle = Frame(UpdateWindow)
    FormTitle.pack(side=TOP)
    ContactForm = Frame(UpdateWindow)
    ContactForm.pack(side=TOP, pady=10)
    RadioGroup = Frame(ContactForm)
    Radiobutton(RadioGroup, text="Male", variable=GENDER, value="Male", font=('arial', 14)).pack(side=LEFT)
    Radiobutton(RadioGroup, text="Female", variable=GENDER, value="Female", font=('arial', 14)).pack(side=LEFT)

    Label(FormTitle, text="Update Contact", font=('arial', 16), bg="orange", width=300).pack(fill=X)
    Label(ContactForm, text="Name", font=('arial', 14), bd=5).grid(row=0, sticky=W)
    Label(ContactForm, text="Gender", font=('arial', 14), bd=5).grid(row=1, sticky=W)
    Label(ContactForm, text="Address", font=('arial', 14), bd=5).grid(row=2, sticky=W)
    Label(ContactForm, text="Contact", font=('arial', 14), bd=5).grid(row=3, sticky=W)

    Entry(ContactForm, textvariable=NAME, font=('arial', 14)).grid(row=0, column=1)
    RadioGroup.grid(row=1, column=1)
    Entry(ContactForm, textvariable=ADDRESS, font=('arial', 14)).grid(row=2, column=1)
    Entry(ContactForm, textvariable=CONTACT, font=('arial', 14)).grid(row=3, column=1)

    Button(ContactForm, text="Update", width=50, command=UpdateData).grid(row=4, columnspan=2, pady=10)

def DeleteData():
    if not tree.selection():
        tkMessageBox.showwarning('', 'Please Select Something First!', icon="warning")
    else:
        result = tkMessageBox.askquestion('', 'Are you sure you want to delete this record?', icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            selecteditem = tree.item(curItem)['values']
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM `member` WHERE `mem_id` = ?", (selecteditem[0],))
            conn.commit()
            cursor.close()
            conn.close()
            Database()  

def AddNewWindow():
    global NewWindow
    NAME.set("")
    GENDER.set("")
    ADDRESS.set("")
    CONTACT.set("")

    NewWindow = Toplevel()
    NewWindow.title("Add New Contact")
    width = 400
    height = 250
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = ((screen_width/2) - 455) - (width/2)
    y = ((screen_height/2) + 20) - (height/2)
    NewWindow.resizable(0, 0)
    NewWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))

    FormTitle = Frame(NewWindow)
    FormTitle.pack(side=TOP)
    ContactForm = Frame(NewWindow)
    ContactForm.pack(side=TOP, pady=10)
    RadioGroup = Frame(ContactForm)
    Radiobutton(RadioGroup, text="Male", variable=GENDER, value="Male", font=('arial', 14)).pack(side=LEFT)
    Radiobutton(RadioGroup, text="Female", variable=GENDER, value="Female", font=('arial', 14)).pack(side=LEFT)

    Label(FormTitle, text="Add New Contact", font=('arial', 16), bg="#66ff66", width=300).pack(fill=X)
    Label(ContactForm, text="Name", font=('arial', 14), bd=5).grid(row=0, sticky=W)
    Label(ContactForm, text="Gender", font=('arial', 14), bd=5).grid(row=1, sticky=W)
    Label(ContactForm, text="Address", font=('arial', 14), bd=5).grid(row=2, sticky=W)
    Label(ContactForm, text="Contact", font=('arial', 14), bd=5).grid(row=3, sticky=W)

    Entry(ContactForm, textvariable=NAME, font=('arial', 14)).grid(row=0, column=1)
    RadioGroup.grid(row=1, column=1)
    Entry(ContactForm, textvariable=ADDRESS, font=('arial', 14)).grid(row=2, column=1)
    Entry(ContactForm, textvariable=CONTACT, font=('arial', 14)).grid(row=3, column=1)

    Button(ContactForm, text="Save", width=50, command=SubmitData).grid(row=4, columnspan=2, pady=10)


Top = Frame(root, width=500, bd=1, relief=SOLID)
Top.pack(side=TOP)
Mid = Frame(root, width=500, bg="#6666ff")
Mid.pack(side=TOP)
MidLeft = Frame(Mid, width=100)
MidLeft.pack(side=LEFT, pady=10)
MidRight = Frame(Mid, width=100)
MidRight.pack(side=RIGHT, pady=10)
TableMargin = Frame(root, width=500)
TableMargin.pack(side=TOP)

Label(Top, text="Contact Management System", font=('arial', 16), width=500).pack(fill=X)
Button(MidLeft, text="+ ADD NEW", bg="#66ff66", command=AddNewWindow).pack()
Button(MidRight, text="DELETE", bg="red", command=DeleteData).pack(side=RIGHT)

scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
tree = ttk.Treeview(TableMargin, columns=("S.No", "Name", "Gender", "Address", "Contact"), height=400, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill=X)

tree.heading('S.No', text="S.No", anchor=W)
tree.heading('Name', text="Name", anchor=W)
tree.heading('Gender', text="Gender", anchor=W)
tree.heading('Address', text="Address", anchor=W)
tree.heading('Contact', text="Contact", anchor=W)

tree.column('#0', stretch=NO, minwidth=0, width=0)
tree.column('#1', stretch=NO, minwidth=0, width=80)
tree.column('#2', stretch=NO, minwidth=0, width=120)
tree.column('#3', stretch=NO, minwidth=0, width=150)
tree.column('#4', stretch=NO, minwidth=0, width=320)
tree.pack()
tree.bind('<Double-Button-1>', OnSelected)

if __name__ == '__main__':
    Database()
    root.mainloop()
