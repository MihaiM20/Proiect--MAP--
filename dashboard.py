from tkinter import *
from PIL import Image, ImageTk
from angajati import angajati_tab
from functii import on_enter,on_leave
from furnizor import furnizor_tab

#trebuie sa descriu fiecare etapa in parte in dezvoltarea aplicatiei!

# Interfață grafică principală (GUI)
window = Tk()
window.title('Dashboard')
window.geometry('1270x671+0+0')
window.resizable(False, False)
window.configure(bg="turquoise")

# Load și setare imagine fundal
bgImage = PhotoImage(file='C:/Users/munte/Desktop/proiect/imagini/logo.png')
titleLabel = Label(window, image=bgImage, compound=LEFT, text='Sistem de management al inventarului',
                   font=('times new roman', 40, 'bold'), bg="blue", fg='white', anchor='w', padx=20)
titleLabel.place(x=0, y=0, relwidth=1)

logoutButton = Button(window, text='Logout', font=('times new roman', 20, 'bold'), bg='gray', fg='black')
logoutButton.place(x=1100, y=20)

# Hover pentru butonul logout
logoutButton.bind("<Enter>", lambda e: logoutButton.config(bg="dark gray"))
logoutButton.bind("<Leave>", lambda e: logoutButton.config(bg="gray"))

# Subtitlu
subtitleLabel = Label(window, text='Bine ai venit!\t\t Data: zz-ll-aaaa\t\t Ora: HH:MM:SS',
                      font=('times new roman', 15), bg='light blue', fg='black')
subtitleLabel.place(x=0, y=93, relwidth=1)

# Setare cadru stânga și imagine meniu
leftFrame = Frame(window, bg="light gray")
leftFrame.place(x=0, y=122, width=200, height=550)
menuImage = Image.open('C:/Users/munte/Desktop/proiect/imagini/meniu.png')
menuImage = menuImage.resize((100, 100), Image.LANCZOS)
menuPhoto = ImageTk.PhotoImage(menuImage)
imageLabel = Label(leftFrame, image=menuPhoto, bg="light gray")
imageLabel.pack()

menuLabel = Label(leftFrame, text='Meniu', font=('times new roman', 20), bg='gray', fg='white')
menuLabel.pack(fill=X)

# Load și resize pentru imaginea sageata
arrowImage = Image.open('C:/Users/munte/Desktop/proiect/imagini/sageata.png').resize((25, 25), Image.LANCZOS)
arrowPhoto = ImageTk.PhotoImage(arrowImage)

# Butoane din meniu
buttons = [
    {"text": " Angajati", "command": lambda:angajati_tab(window)},
    {"text": " Furnizor", "command": lambda:furnizor_tab(window)},
    {"text": " Categorie", "command": None},
    {"text": " Produse", "command": None},
    {"text": " Vanzari", "command": None},
    {"text": " Exit", "command": window.quit}
]

# Crează și aplică hover pentru fiecare buton
for button in buttons:
    btn = Button(leftFrame, image=arrowPhoto, compound=LEFT, text=button["text"],
                 font=('times new roman', 20, 'bold'), command=button["command"],
                 anchor='w', padx=10, bg="white",cursor='hand2')
    btn.pack(fill=X, ipady=8)

    # Adaugă efect de hover pe fiecare buton
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

emp_frame = Frame(window, bg='orange', bd='3', relief=RIDGE)
emp_frame.place(x=350, y=125, height=170, width=280)
total_emp_label = Label(emp_frame, text='\n\nTotal Angajati', bg='orange', fg='black',
                        font=('times new roman', 15, 'bold'))
total_emp_label.pack()
total_emp_count_label = Label(emp_frame, text='[0]', bg='orange', fg='black', font=('times new roman', 20, 'bold'))
total_emp_count_label.pack()

emp_frame = Frame(window, bg='#4db42f', bd='3', relief=RIDGE)
emp_frame.place(x=850, y=125, height=170, width=280)
total_emp_label = Label(emp_frame, text='\n\nTotal Furnizori', bg='#4db42f', fg='black',
                        font=('times new roman', 15, 'bold'))
total_emp_label.pack()
total_emp_count_label = Label(emp_frame, text='[0]', bg='#4db42f', fg='black', font=('times new roman', 20, 'bold'))
total_emp_count_label.pack()

emp_frame = Frame(window, bg='#a25c0e', bd='3', relief=RIDGE)
emp_frame.place(x=350, y=303, height=170, width=280)
total_emp_label = Label(emp_frame, text='\n\nTotal Categorii', bg='#a25c0e', fg='black',
                        font=('times new roman', 15, 'bold'))
total_emp_label.pack()
total_emp_count_label = Label(emp_frame, text='[0]', bg='#a25c0e', fg='black', font=('times new roman', 20, 'bold'))
total_emp_count_label.pack()

emp_frame = Frame(window, bg='#46c0dc', bd='3', relief=RIDGE)
emp_frame.place(x=850, y=303, height=170, width=280)
total_emp_label = Label(emp_frame, text='\n\nTotal Produse', bg='#46c0dc', fg='black',
                        font=('times new roman', 15, 'bold'))
total_emp_label.pack()
total_emp_count_label = Label(emp_frame, text='[0]', bg='#46c0dc', fg='black', font=('times new roman', 20, 'bold'))
total_emp_count_label.pack()

emp_frame = Frame(window, bg='#50f0e4', bd='3', relief=RIDGE)
emp_frame.place(x=600, y=480, height=170, width=280)
total_emp_label = Label(emp_frame, text='\n\nTotal Vanzari', bg='#50f0e4', fg='black',
                        font=('times new roman', 15, 'bold'))
total_emp_label.pack()
total_emp_count_label = Label(emp_frame, text='[0]', bg='#50f0e4', fg='black', font=('times new roman', 20, 'bold'))
total_emp_count_label.pack()

# Configurare mainloop pentru ferestre
window.mainloop()