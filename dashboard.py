from tkinter import *
from PIL import Image, ImageTk
from angajati import angajati_tab
from functii import on_enter,on_leave
from furnizor import furnizor_tab
from categorie import categorie_tab
from produse import produse_tab
from angajati import conectare_bd
from tkinter import Toplevel, Label, Spinbox, Tk
from tkinter import messagebox
import time

def update():
    cursor, conectare = conectare_bd()
    if not cursor or not conectare:
        return
    cursor.execute('USE sistem_inventar')
    cursor.execute('SELECT * FROM date_angajati')
    records=cursor.fetchall()
    total_ang_count_label.config(text=len(records))

    cursor.execute('USE sistem_inventar')
    cursor.execute('SELECT * FROM date_categorie')
    records=cursor.fetchall()
    total_cat_count_label.config(text=len(records))

    cursor.execute('USE sistem_inventar')
    cursor.execute('SELECT * FROM date_furnizori')
    records=cursor.fetchall()
    total_fur_count_label.config(text=len(records))

    cursor.execute('USE sistem_inventar')
    cursor.execute('SELECT * FROM date_produse')
    records=cursor.fetchall()
    total_prd_count_label.config(text=len(records))

    date_time=time.strftime('%I:%M:%S %p   %A %d/%m/%Y')
    subtitleLabel.config(text=f'Bine ai venit!\t\t\t\t\t\t\t\t\t\t {date_time}')
    subtitleLabel.after(1000,update)

def tax_window():
    def save_tax():
        value = float(tax_count.get())  # Asigură-te că valoarea este numerică
        cursor, conectare = conectare_bd()

        if not cursor or not conectare:
            return

        # Crearea bazei de date dacă nu există
        cursor.execute('CREATE DATABASE IF NOT EXISTS sistem_inventar')
        # Utilizarea bazei de date 'sistem_inventar'
        cursor.execute('USE sistem_inventar')

        # Crearea tabelei dacă nu există
        cursor.execute('CREATE TABLE IF NOT EXISTS tax_table (id INT PRIMARY KEY, tax DECIMAL(5,2))')

        # Verificarea dacă există deja un rând cu id=1
        cursor.execute('SELECT id FROM tax_table WHERE id = 1')
        if cursor.fetchone():
            # Dacă există, actualizează valoarea taxei
            cursor.execute('UPDATE tax_table SET tax = %s WHERE id = 1', (value,))
        else:
            # Dacă nu există, inserează un nou rând
            cursor.execute('INSERT INTO tax_table (id, tax) VALUES (1, %s)', (value,))

        # Confirmarea modificărilor în baza de date
        conectare.commit()
        messagebox.showinfo('Succes!',f'Taxa este setata la {value}% si salvata cu succes!',parent=tax_root)

        # Închiderea conexiunii
        cursor.close()
        conectare.close()
    tax_root = Toplevel()
    tax_root.title('Tax window')
    tax_root.geometry('300x200')
    tax_root.grab_set()
    tax_percentage = Label(tax_root, text='Introdu procentajul de taxa(%)', font=('arial', 12))
    tax_percentage.pack(pady=10)
    tax_count = Spinbox(tax_root, from_=0, to=100, font=('arial', 12))
    tax_count.pack()
    save_button = Button(tax_root,text='Save',font=('arial',20,'bold'),bg="white",fg='black',width=10,cursor='hand2',command=save_tax)
    save_button.pack(pady=20)
    save_button.bind("<Enter>", on_enter)
    save_button.bind("<Leave>", on_leave)
    tax_root.mainloop()

current_frame=None
def show_form(form_function):
    global current_frame
    if current_frame:
        current_frame.place_forget()
    current_frame = form_function(window)

# Interfață grafică principală (GUI)
window = Tk()
window.title('Dashboard')
window.geometry('1270x675+0+0')
window.resizable(False, False)
window.configure(bg="turquoise")

# Load și setare imagine fundal
bgImage = PhotoImage(file='C:/Users/munte/Desktop/proiect/imagini/logo.png')
titleLabel = Label(window, image=bgImage, compound=LEFT, text='Sistem de management al inventarului',
                   font=('times new roman', 40, 'bold'), bg="blue", fg='white', anchor='w', padx=20)
titleLabel.place(x=0, y=0, relwidth=1)

#logoutButton = Button(window, text='Logout', font=('times new roman', 20, 'bold'), bg='gray', fg='black')
#logoutButton.place(x=1100, y=20)
#
## Hover pentru butonul logout
#logoutButton.bind("<Enter>", lambda e: logoutButton.config(bg="dark gray"))
#logoutButton.bind("<Leave>", lambda e: logoutButton.config(bg="gray"))

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

# Load și resize pentru imaginea sageata
arrowImage = Image.open('C:/Users/munte/Desktop/proiect/imagini/sageata.png').resize((25, 25), Image.LANCZOS)
arrowPhoto = ImageTk.PhotoImage(arrowImage)

# Butoane din meniu
buttons = [
    {"text": " Angajati", "command": lambda: show_form(angajati_tab)},
    {"text": " Furnizor", "command": lambda: show_form(furnizor_tab)},
    {"text": " Categorie", "command": lambda: show_form(categorie_tab)},
    {"text": " Produse", "command": lambda: show_form(produse_tab)},
    {"text": " Tax", "command": tax_window},
    {"text": " Exit", "command": window.quit}
]

# Crează și aplică hover pentru fiecare buton
for button in buttons:
    btn = Button(leftFrame, image=arrowPhoto, compound=LEFT, text=button["text"],
                 font=('times new roman', 20, 'bold'), command=button["command"],
                 anchor='w', padx=10, bg="white",cursor='hand2')
    btn.pack(fill=X, ipady=11)

    # Adaugă efect de hover pe fiecare buton
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

ang_frame = Frame(window, bg='orange', bd='3', relief=RIDGE)
ang_frame.place(x=350, y=180, height=170, width=280)
total_ang_label = Label(ang_frame, text='\n\nTotal Angajati', bg='orange', fg='black',
                     font=('times new roman', 15, 'bold'))
total_ang_label.pack()
total_ang_count_label = Label(ang_frame, text='[0]', bg='orange', fg='black', font=('times new roman', 20, 'bold'))
total_ang_count_label.pack()

fur_frame = Frame(window, bg='#4db42f', bd='3', relief=RIDGE)
fur_frame.place(x=850, y=180, height=170, width=280)
total_fur_label = Label(fur_frame, text='\n\nTotal Furnizori', bg='#4db42f', fg='black',
                        font=('times new roman', 15, 'bold'))
total_fur_label.pack()
total_fur_count_label = Label(fur_frame, text='[0]', bg='#4db42f', fg='black', font=('times new roman', 20, 'bold'))
total_fur_count_label.pack()

cat_frame = Frame(window, bg='#a25c0e', bd='3', relief=RIDGE)
cat_frame.place(x=350, y=430, height=170, width=280)
total_cat_label = Label(cat_frame, text='\n\nTotal Categorii', bg='#a25c0e', fg='black',
                        font=('times new roman', 15, 'bold'))
total_cat_label.pack()
total_cat_count_label = Label(cat_frame, text='[0]', bg='#a25c0e', fg='black', font=('times new roman', 20, 'bold'))
total_cat_count_label.pack()

prd_frame = Frame(window, bg='#46c0dc', bd='3', relief=RIDGE)
prd_frame.place(x=850, y=430, height=170, width=280)
total_prd_label = Label(prd_frame, text='\n\nTotal Produse', bg='#46c0dc', fg='black',
                        font=('times new roman', 15, 'bold'))
total_prd_label.pack()
total_prd_count_label = Label(prd_frame, text='[0]', bg='#46c0dc', fg='black', font=('times new roman', 20, 'bold'))
total_prd_count_label.pack()

#emp_frame = Frame(window, bg='#50f0e4', bd='3', relief=RIDGE)
#emp_frame.place(x=600, y=480, height=170, width=280)
#total_emp_label = Label(emp_frame, text='\n\nTotal Vanzari', bg='#50f0e4', fg='black',
#                        font=('times new roman', 15, 'bold'))

#total_emp_label.pack()
#total_emp_count_label = Label(emp_frame, text='[0]', bg='#50f0e4', fg='black', font=('times new roman', 20, 'bold'))
#total_emp_count_label.pack()
update()
# Configurare mainloop pentru ferestre
window.mainloop()