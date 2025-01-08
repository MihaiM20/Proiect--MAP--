from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from functii import on_enter,on_leave
from angajati import conectare_bd
from tkinter import messagebox
import pymysql


def show_all(treeview, search_entry):
    # Reîncărcăm toate datele în treeview
    treeview_data(treeview)

    # Golește câmpul de căutare
    search_entry.delete(0, END)


def cauta_furnizor(search_value, treeview):
    if search_value == '':
        messagebox.showerror('Eroare', 'Introdu numărul facturii!')
        return

    cursor, conectare = conectare_bd()
    if not cursor or not conectare:
        return

    try:
        cursor.execute('USE sistem_inventar')
        cursor.execute('SELECT * FROM date_furnizori WHERE facturi=%s', (search_value,))
        inregistrare = cursor.fetchone()  # Folosește fetchone pentru un singur rezultat

        # Curăță toate rândurile anterioare
        treeview.delete(*treeview.get_children())

        if inregistrare:
            # Adaugă înregistrarea găsită în treeview
            treeview.insert('', END, values=inregistrare)
        else:
            # Dacă nu găsim nicio înregistrare, arată un mesaj de eroare și reîncarcă toate datele
            messagebox.showerror('Eroare', 'Nu au fost găsite rezultate!')
            treeview_data(treeview)  # Reîncarcă toate înregistrările

    except pymysql.MySQLError as e:
        # Capturăm erorile MySQL și afișăm un mesaj de eroare
        messagebox.showerror('Eroare MySQL', f'A apărut o problemă cu interogarea: {e}')
        treeview_data(treeview)  # În caz de eroare, reîncarcă toate datele
    finally:
        cursor.close()
        conectare.close()

def clear_campuri(entries, descriere_text):
    for entry in entries:
        entry.delete(0, END)
    descriere_text.delete(1.0, END)

def sterge_furnizor(facturi, treeview):
    if not facturi:
        messagebox.showerror('Eroare', 'Trebuie să selectați o factură pentru ștergere!')
        return

    cursor, conectare = conectare_bd()
    if not cursor or not conectare:
        return

    try:
        cursor.execute('USE sistem_inventar')
        cursor.execute('DELETE FROM date_furnizori WHERE facturi=%s', (facturi,))
        conectare.commit()
        treeview_data(treeview)
        messagebox.showinfo('Succes', 'Furnizorul a fost șters cu succes!')
    except pymysql.MySQLError as e:
        messagebox.showerror('Eroare MySQL', f'Problema la ștergerea furnizorului: {e}')
    finally:
        cursor.close()
        conectare.close()

def actualizeaza_furnizor(facturi, nume, contact, descriere, treeview):
    if not facturi or not nume or not contact or descriere.strip() == '':
        messagebox.showerror('Eroare', 'Toate câmpurile sunt necesare pentru actualizare!')
        return

    cursor, conectare = conectare_bd()
    if not cursor or not conectare:
        return

    try:
        cursor.execute('USE sistem_inventar')
        cursor.execute(
            'UPDATE date_furnizori SET nume=%s, contact=%s, descriere=%s WHERE facturi=%s',
            (nume, contact, descriere.strip(), facturi)
        )
        conectare.commit()
        treeview_data(treeview)
        messagebox.showinfo('Succes', 'Furnizorul a fost actualizat cu succes!')
    except pymysql.MySQLError as e:
        messagebox.showerror('Eroare MySQL', f'Problema la actualizarea furnizorului: {e}')
    finally:
        cursor.close()
        conectare.close()

def select_furnizor(event, treeview, facturi_entry, nume_entry, contact_entry, descriere_text):
    # Obține elementul selectat
    index = treeview.selection()
    if not index:  # Verifică dacă un element este selectat
        return

    content = treeview.item(index)
    row = content['values']  # Obține valorile rândului selectat

    # Șterge câmpurile existente
    facturi_entry.delete(0, END)
    nume_entry.delete(0, END)
    contact_entry.delete(0, END)
    descriere_text.delete(1.0, END)

    # Populează câmpurile cu datele selectate
    facturi_entry.insert(0, row[0])
    nume_entry.insert(0, row[1])
    contact_entry.insert(0, row[2])
    descriere_text.insert(1.0, row[3])

def treeview_data(treeview):
    cursor, conectare = conectare_bd()
    if not cursor or not conectare:
        return
    cursor.execute('use sistem_inventar')
    try:
        cursor.execute('SELECT * FROM date_furnizori')  # Executăm interogarea direct
        inregistrari_furnizori = cursor.fetchall()      # Obținem toate înregistrările
        treeview.delete(*treeview.get_children())
        for inregistrare in inregistrari_furnizori:
            treeview.insert('',END,values=inregistrare)

    except pymysql.MySQLError as e:
        messagebox.showerror('Eroare MySQL', f'A apărut o problemă cu interogarea datelor: {e}')
    finally:
        cursor.close()
        conectare.close()

def create_db_tabel_furnizori():
    cursor, conectare = conectare_bd()
    if not cursor or not conectare:
        return

    try:
        # Crearea bazei de date dacă nu există
        cursor.execute('CREATE DATABASE IF NOT EXISTS sistem_inventar')

        # Utilizarea bazei de date 'sistem_inventar'
        cursor.execute('USE sistem_inventar')

        # Crearea tabelului 'date_furnizori' dacă nu există
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS date_furnizori (
                facturi INT PRIMARY KEY,
                nume VARCHAR(100),
                contact VARCHAR(15),
                descriere TEXT
            )
        ''')
        conectare.commit()
    except pymysql.MySQLError as e:
        messagebox.showerror('Eroare MySQL', f'Problema cu crearea tabelului: {e}')
    finally:
        cursor.close()
        conectare.close()

def adauga_furnizor(facturi, nume, contact, descriere, treeview):
    if not facturi or not nume or not contact or descriere.strip() == '':
        messagebox.showerror('Eroare', 'Toate câmpurile sunt necesare!')
        return

    cursor, conectare = conectare_bd()
    if not cursor or not conectare:
        return

    try:
        # Utilizarea bazei de date 'sistem_inventar'
        cursor.execute('USE sistem_inventar')

        # Crearea tabelului dacă nu există (pentru siguranță)
        create_db_tabel_furnizori()

        # Inserarea datelor în tabelul 'date_furnizori'
        cursor.execute(
            'INSERT INTO date_furnizori (facturi, nume, contact, descriere) VALUES (%s, %s, %s, %s)',
            (facturi, nume, contact, descriere.strip())
        )
        conectare.commit()
        treeview_data(treeview)
        messagebox.showinfo('Succes', 'Furnizorul a fost adăugat cu succes!')
    except pymysql.MySQLError as e:
        messagebox.showerror('Eroare MySQL', f'Problema la adăugarea furnizorului: {e}')
    finally:
        cursor.close()
        conectare.close()

def furnizor_tab(window):
    global back_image
    furnizor_frame = Frame(window, width=1070, height=600, bg='white')
    furnizor_frame.place(x=200, y=94)

    headingLabel = Label(furnizor_frame, text='Gestionarea detaliilor furnizorilor',
                         font=('times new roman', 16, 'bold'), bg='light green', fg='black')
    headingLabel.place(x=0, y=0, relwidth=1)

    back_img_path = 'C:/Users/munte/Desktop/proiect/imagini/back.png'
    back_img = Image.open(back_img_path)
    resized_back_img = back_img.resize((30, 30))
    back_image = ImageTk.PhotoImage(resized_back_img)
    back_button = Button(furnizor_frame, image=back_image, bd=0, cursor='hand2', bg='white',
                         command=lambda: furnizor_frame.place_forget())
    back_button.place(x=10, y=30)

    # Adaugă hover efect pe butonul back
    back_button.bind("<Enter>", on_enter)
    back_button.bind("<Leave>", on_leave)

    left_frame=Frame(furnizor_frame,bg='white')
    left_frame.place(x=10,y=100)

    facturi_label=Label(left_frame,text='Factura nr.',font=('times new roman',14,'bold'),bg='white')
    facturi_label.grid(row=0,column=0,padx=(20,40),sticky='w')
    facturi_entry=Entry(left_frame,font=('times new roman',14,'bold'),bg='lightyellow')
    facturi_entry.grid(row=0,column=1)

    nume_label=Label(left_frame,text='Nume furnizor',font=('times new roman',14,'bold'),bg='white')
    nume_label.grid(row=1,column=0,padx=(20,40),pady=25,sticky='w')
    nume_entry=Entry(left_frame,font=('times new roman',14,'bold'),bg='lightyellow')
    nume_entry.grid(row=1,column=1)

    contact_label=Label(left_frame,text='Contact furnizor',font=('times new roman',14,'bold'),bg='white')
    contact_label.grid(row=2,column=0,padx=(20,40),sticky='w')
    contact_entry=Entry(left_frame,font=('times new roman',14,'bold'),bg='lightyellow')
    contact_entry.grid(row=2,column=1)

    descriere_label=Label(left_frame,text='Descriere',font=('times new roman',14,'bold'),bg='white')
    descriere_label.grid(row=3,column=0,padx=(20,40),sticky='nw',pady=25)
    descriere_text=Text(left_frame,width=25,height=6,bd=2,bg='lightyellow')
    descriere_text.grid(row=3,column=1,pady=25)

    button_frame=Frame(left_frame,bg='white')
    button_frame.grid(row=4,columnspan=2,pady=20)

    add_button = Button(button_frame, text='Add', font=('times new roman', 12), bg='white', width=8,
                        cursor='hand2', command=lambda :adauga_furnizor(
            facturi_entry.get(),nume_entry.get(),contact_entry.get(),descriere_text.get(1.0,END),treeview
        ))
    add_button.grid(row=0, column=0, padx=20)
    add_button.bind("<Enter>", on_enter)
    add_button.bind("<Leave>", on_leave)

    update_button = Button(button_frame, text='Update', font=('times new roman', 12), bg='white', width=8,
                           cursor='hand2', command=lambda: actualizeaza_furnizor(
            facturi_entry.get(), nume_entry.get(), contact_entry.get(), descriere_text.get(1.0, END), treeview
        ))
    update_button.grid(row=0, column=1)
    update_button.bind("<Enter>", on_enter)
    update_button.bind("<Leave>", on_leave)

    delete_button = Button(button_frame, text='Delete', font=('times new roman', 12), bg='white', width=8,
                        cursor='hand2', command=lambda: sterge_furnizor(
            facturi_entry.get(), treeview
        ))
    delete_button.grid(row=0, column=3, padx=20)
    delete_button.bind("<Enter>", on_enter)
    delete_button.bind("<Leave>", on_leave)

    clear_button = Button(button_frame, text='Clear', font=('times new roman', 12), bg='white', width=8,
                        cursor='hand2', command=lambda: clear_campuri(
            [facturi_entry, nume_entry, contact_entry], descriere_text
        ))
    clear_button.grid(row=0, column=4)
    clear_button.bind("<Enter>", on_enter)
    clear_button.bind("<Leave>", on_leave)

    right_frame=Frame(furnizor_frame,bg='white')
    right_frame.place(x=565,y=90,width=500,height=350)

    search_frame=Frame(right_frame,bg='white')
    search_frame.pack(pady=(0,20))

    num_label=Label(search_frame,text='Factura nr.',font=('times new roman',14,'bold'),bg='white')
    num_label.grid(row=0,column=0,padx=(0,15),sticky='w')
    search_entry=Entry(search_frame,font=('times new roman',14,'bold'),bg='lightyellow',width=10)
    search_entry.grid(row=0,column=1)

    search_button = Button(search_frame, text='Search', font=('times new roman', 12), bg='white', width=8,
                           cursor='hand2', command=lambda: cauta_furnizor(search_entry.get(), treeview))
    search_button.grid(row=0, column=2, padx=15)
    search_button.bind("<Enter>", on_enter)
    search_button.bind("<Leave>", on_leave)

    show_button = Button(search_frame, text='Show All', font=('times new roman', 12), bg='white', width=8,
                         cursor='hand2', command=lambda: show_all(treeview, search_entry))  # Apelează show_all
    show_button.grid(row=0, column=3)
    show_button.bind("<Enter>", on_enter)
    show_button.bind("<Leave>", on_leave)

    scrolly=Scrollbar(right_frame,orient=VERTICAL)
    scrollx=Scrollbar(right_frame,orient=HORIZONTAL)
    treeview=ttk.Treeview(right_frame,column=('factura','nume','contact','descriere'),
                          show='headings',yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
    scrolly.pack(side=RIGHT,fill=Y)
    scrollx.pack(side=BOTTOM,fill=X)
    scrollx.config(command=treeview.xview)
    scrolly.config(command=treeview.yview)
    treeview.pack(fill=BOTH,expand=1)
    treeview.heading('factura',text='Id factura')
    treeview.heading('nume',text='Nume furnizor')
    treeview.heading('contact',text='Contact furnizor')
    treeview.heading('descriere',text='Descriere')

    treeview.column('factura',width='80')
    treeview.column('nume',width='160')
    treeview.column('contact',width='120')
    treeview.column('descriere',width='300')

    treeview_data(treeview)
    treeview.bind('<ButtonRelease-1>',
                  lambda event: select_furnizor(event, treeview, facturi_entry, nume_entry, contact_entry,
                                                descriere_text))
    return furnizor_frame