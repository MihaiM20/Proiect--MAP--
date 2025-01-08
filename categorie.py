from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from functii import on_enter, on_leave
from angajati import conectare_bd
from tkinter import messagebox
import pymysql

def select_categorie(event, treeview, id_entry, nume_entry, descriere_text):
    # Obține elementul selectat
    index = treeview.selection()
    if not index:  # Verifică dacă un element este selectat
        return

    content = treeview.item(index)
    row = content['values']  # Obține valorile rândului selectat

    # Șterge câmpurile existente
    id_entry.delete(0, END)
    nume_entry.delete(0, END)
    descriere_text.delete(1.0, END)

    # Populează câmpurile cu datele selectate
    id_entry.insert(0, row[0])
    nume_entry.insert(0, row[1])
    descriere_text.insert(1.0, row[2])

def adauga_categorie(id_categorie, nume_categorie, descriere_categorie, treeview, id_entry, category_name_entry, descriere_text):
    if not id_categorie or not nume_categorie or descriere_categorie.strip() == '':
        messagebox.showerror('Eroare', 'Toate câmpurile sunt necesare!')
        return

    cursor, conectare = conectare_bd()
    if not cursor or not conectare:
        return

    try:
        # Utilizarea bazei de date 'sistem_inventar'
        cursor.execute('USE sistem_inventar')

        # Crearea tabelului dacă nu există (pentru siguranță)
        create_db_tabel_categorie()

        # Inserarea datelor în tabelul 'date_categorie'
        cursor.execute(
            'INSERT INTO date_categorie (id, nume, descriere) VALUES (%s, %s, %s)',
            (id_categorie, nume_categorie, descriere_categorie.strip())
        )
        conectare.commit()

        # Actualizare TreeView
        treeview_data(treeview)

        # Șterge automat câmpurile după adăugare
        id_entry.delete(0, END)
        category_name_entry.delete(0, END)
        descriere_text.delete("1.0", END)

        messagebox.showinfo('Succes', 'Categoria a fost adăugată cu succes!')
    except pymysql.MySQLError as e:
        messagebox.showerror('Eroare MySQL', f'Problema la adăugarea categoriei: {e}')
    finally:
        cursor.close()
        conectare.close()

def sterge_categorie(id, treeview):
    if not id:
        messagebox.showerror('Eroare', 'Trebuie să selectați un ID pentru ștergere!')
        return

    cursor, conectare = conectare_bd()
    if not cursor or not conectare:
        return

    try:
        cursor.execute('USE sistem_inventar')
        cursor.execute('DELETE FROM date_categorie WHERE id=%s', (id,))
        conectare.commit()
        treeview_data(treeview)
        messagebox.showinfo('Succes', 'Categoria a fost ștearsă cu succes!')
    except pymysql.MySQLError as e:
        messagebox.showerror('Eroare MySQL', f'Problema la ștergerea categoriei: {e}')
    finally:
        cursor.close()
        conectare.close()

def create_db_tabel_categorie():
    cursor, conectare = conectare_bd()
    if not cursor or not conectare:
        return

    try:
        # Crearea bazei de date dacă nu există
        cursor.execute('CREATE DATABASE IF NOT EXISTS sistem_inventar')

        # Utilizarea bazei de date 'sistem_inventar'
        cursor.execute('USE sistem_inventar')

        # Crearea tabelului 'date_categorie' dacă nu există
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS date_categorie (
                id INT PRIMARY KEY,
                nume VARCHAR(100),
                descriere TEXT
            )
        ''')
        conectare.commit()
    except pymysql.MySQLError as e:
        messagebox.showerror('Eroare MySQL', f'Problema cu crearea tabelului: {e}')
    finally:
        cursor.close()
        conectare.close()

def treeview_data(treeview):
    # Conectare la baza de date și populare Treeview
    cursor, conectare = conectare_bd()
    if not cursor or not conectare:
        return

    cursor.execute('USE sistem_inventar')
    try:
        cursor.execute('SELECT * FROM date_categorie')  # Interogare pentru toate înregistrările
        inregistrari_categorii = cursor.fetchall()  # Obținem toate înregistrările

        # Ștergem datele existente din Treeview
        treeview.delete(*treeview.get_children())

        # Adăugăm înregistrările în Treeview
        for inregistrare in inregistrari_categorii:
            treeview.insert('', END, values=inregistrare)

    except pymysql.MySQLError as e:
        messagebox.showerror('Eroare MySQL', f'A apărut o problemă cu interogarea datelor: {e}')
    finally:
        cursor.close()
        conectare.close()

def clear_campuri(entries, text_widget):
    for entry in entries:
        entry.delete(0, END)  # Șterge câmpurile de tip Entry
    text_widget.delete(1.0, END)  # Șterge câmpul de tip Text

def categorie_tab(window):
    global back_image, logo
    categorie_frame = Frame(window, width=1070, height=600, bg='white')
    categorie_frame.place(x=200, y=93)

    headingLabel = Label(categorie_frame, text='Gestionarea detaliilor categoriilor',
                         font=('times new roman', 16, 'bold'), bg='light green', fg='black')
    headingLabel.place(x=0, y=0, relwidth=1)

    # Imagine buton back
    back_img_path = 'C:/Users/munte/Desktop/proiect/imagini/back.png'
    back_img = Image.open(back_img_path)
    resized_back_img = back_img.resize((30, 30))
    back_image = ImageTk.PhotoImage(resized_back_img)
    back_button = Button(categorie_frame, image=back_image, bd=0, cursor='hand2', bg='white',
                         command=lambda: categorie_frame.place_forget())
    back_button.place(x=10, y=30)
    back_button.bind("<Enter>", on_enter)
    back_button.bind("<Leave>", on_leave)

    # Imagine categorie
    logo = Image.open('C:/Users/munte/Desktop/proiect/imagini/categorii.png')
    logo_resized = logo.resize((300, int(300 * logo.height / logo.width)))  # Păstrează proporțiile
    logo_resized = ImageTk.PhotoImage(logo_resized)
    label = Label(categorie_frame, image=logo_resized, bg='white')
    label.place(x=100, y=150)  # Repozitionare imagine mai centrală
    label.image = logo_resized

    # Detalii categorie
    details_frame = Frame(categorie_frame, bg='white')
    details_frame.place(x=500, y=60)  # Repozitionare secțiune detalii

    # ID categorie
    id_label = Label(details_frame, text='Id', font=('times new roman', 14, 'bold'), bg='white')
    id_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')
    id_entry = Entry(details_frame, font=('times new roman', 14), bg='light yellow')
    id_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')

    # Nume categorie
    category_name_label = Label(details_frame, text='Nume categorie', font=('times new roman', 14, 'bold'), bg='white')
    category_name_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')
    category_name_entry = Entry(details_frame, font=('times new roman', 14), bg='light yellow')
    category_name_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')

    # Descriere categorie
    descriere_label = Label(details_frame, text='Descriere', font=('times new roman', 14, 'bold'), bg='white')
    descriere_label.grid(row=2, column=0, padx=10, pady=10, sticky='nw')
    descriere_text = Text(details_frame, width=25, height=6, bd=2, bg='light yellow')
    descriere_text.grid(row=2, column=1, pady=15)

    # Butoane
    button_frame = Frame(categorie_frame, bg='white')
    button_frame.place(x=570, y=280)

    # Buton pentru adăugarea unei categorii
    add_button = Button(button_frame, text='Add', font=('times new roman', 12), bg='white', width=8, cursor='hand2',
                        command=lambda: adauga_categorie(
                            id_entry.get(),
                            category_name_entry.get(),
                            descriere_text.get("1.0", END),
                            treeview,
                            id_entry,
                            category_name_entry,
                            descriere_text
                        ))
    add_button.grid(row=0, column=0, padx=20)
    add_button.bind("<Enter>", on_enter)
    add_button.bind("<Leave>", on_leave)

    # Buton pentru ștergerea unei categorii
    delete_button = Button(button_frame, text='Delete', font=('times new roman', 12), bg='white', width=8,
                           cursor='hand2',
                           command=lambda: sterge_categorie(
                               id_entry.get(),  # Preluare valoare din câmpul ID
                               treeview  # TreeView-ul unde se vor afișa datele
                           ))
    delete_button.grid(row=0, column=1, padx=20)
    delete_button.bind("<Enter>", on_enter)
    delete_button.bind("<Leave>", on_leave)

    # Buton Clear pentru a șterge câmpurile
    clear_button = Button(button_frame, text='Clear', font=('times new roman', 12), bg='white', width=8,
                          cursor='hand2', command=lambda: clear_campuri([id_entry, category_name_entry], descriere_text))
    clear_button.grid(row=0, column=2, padx=20)
    clear_button.bind("<Enter>", on_enter)
    clear_button.bind("<Leave>", on_leave)

    # Treeview pentru categorii
    treeview_frame = Frame(categorie_frame, bg='yellow')
    treeview_frame.place(x=530, y=340, height=200, width=500)

    scrolly = Scrollbar(treeview_frame, orient=VERTICAL)
    scrollx = Scrollbar(treeview_frame, orient=HORIZONTAL)
    treeview = ttk.Treeview(treeview_frame, column=('id', 'nume', 'descriere'),
                            show='headings', yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
    scrolly.pack(side=RIGHT, fill=Y)
    scrollx.pack(side=BOTTOM, fill=X)
    scrollx.config(command=treeview.xview)
    scrolly.config(command=treeview.yview)
    treeview.pack(fill=BOTH, expand=1)
    treeview.heading('id', text='Id')
    treeview.heading('nume', text='Nume categorie')
    treeview.heading('descriere', text='Descriere')
    treeview.column('id', width='80')
    treeview.column('nume', width='140')
    treeview.column('descriere', width='140')

    # Creează tabelul dacă nu există și populează Treeview
    create_db_tabel_categorie()
    treeview_data(treeview)

    # Selectare element din Treeview
    treeview.bind('<ButtonRelease-1>', lambda event: select_categorie(event, treeview, id_entry, category_name_entry, descriere_text))
    return categorie_frame
