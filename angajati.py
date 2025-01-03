from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
from functii import on_enter,on_leave
import pymysql

def conectare_bd():
    try:
        # Conectarea la serverul MySQL
        conectare = pymysql.connect(
            host='localhost',
            user='root',
            password='1234',
            port=3307
        )
        cursor = conectare.cursor()

        return cursor, conectare

    except pymysql.MySQLError as e:
        # Afișează detaliile erorii MySQL
        messagebox.showerror('Eroare MySQL', f'Problema cu conectarea bazei de date: {e}')
        return None, None

    except Exception as e:
        # Afișează detaliile altor erori
        messagebox.showerror('Eroare', f'A apărut o problemă: {e}')
        return None, None

def create_db_tabel():
    cursor,conectare=conectare_bd()
    # Crearea bazei de date dacă nu există
    cursor.execute('CREATE DATABASE IF NOT EXISTS sistem_inventar')

    # Utilizarea bazei de date 'sistem_inventar'
    cursor.execute('USE sistem_inventar')

    # Crearea tabelului 'date_angajati' dacă nu există
    cursor.execute('''
               CREATE TABLE IF NOT EXISTS date_angajati (
                   id INT PRIMARY KEY AUTO_INCREMENT,
                   nume VARCHAR(100),
                   email VARCHAR(100),
                   gen VARCHAR(50),
                   data_nastere VARCHAR(30),
                   contact VARCHAR(50),
                   tip_angajare VARCHAR(50),
                   educatie VARCHAR(100),
                   program_lucru VARCHAR(50),
                   adresa VARCHAR(100),
                   data_angajare VARCHAR(30),
                   salariu VARCHAR(50),
                   tip_utilizator VARCHAR(50),
                   parola VARCHAR(50)
               )
           ''')

def treeview_data():
    cursor, conectare = conectare_bd()
    if not cursor or not conectare:
        return
    cursor.execute('use sistem_inventar')
    try:
        cursor.execute('SELECT * FROM date_angajati')  # Executăm interogarea direct
        inregistrari_angajati = cursor.fetchall()      # Obținem toate înregistrările
        angajati_treeview.delete(*angajati_treeview.get_children())
        for inregistrare in inregistrari_angajati:
            angajati_treeview.insert('',END,values=inregistrare)

    except pymysql.MySQLError as e:
        messagebox.showerror('Eroare MySQL', f'A apărut o problemă cu interogarea datelor: {e}')
    finally:
        cursor.close()
        conectare.close()

def select_data(event,id_entry,nume_entry,email_entry,gen_combobox,data_nastere_entry,
                contact_entry,tip_angajare_combobox,educatie_combobox,program_lucru_combobox,
                adresa_text,data_angajare_entry,salariu_entry,tip_utilizator_combobox,parola_entry):
    index=angajati_treeview.selection()
    content=angajati_treeview.item(index)
    row=content['values']
    print(row)
    clear_fields(id_entry,nume_entry,email_entry,gen_combobox,data_nastere_entry,
                contact_entry,tip_angajare_combobox,educatie_combobox,program_lucru_combobox,
                adresa_text,data_angajare_entry,salariu_entry,tip_utilizator_combobox,parola_entry,False)
    id_entry.insert(0,row[0])
    nume_entry.insert(0,row[1])
    email_entry.insert(0,row[2])
    gen_combobox.set(row[3])
    data_nastere_entry.set_date(row[4])
    contact_entry.insert(0,row[5])
    tip_angajare_combobox.set(row[6])
    educatie_combobox.set(row[7])
    program_lucru_combobox.set(row[8])
    adresa_text.insert(1.0, row[9])
    data_angajare_entry.set_date(row[10])
    salariu_entry.insert(0,row[11])
    tip_utilizator_combobox.set(row[12])
    parola_entry.insert(0,row[13])

def clear_fields(id_entry,nume_entry,email_entry,gen_combobox,data_nastere_entry,
                contact_entry,tip_angajare_combobox,educatie_combobox,program_lucru_combobox,
                adresa_text,data_angajare_entry,salariu_entry,tip_utilizator_combobox,parola_entry,check):
    id_entry.delete(0,END)
    nume_entry.delete(0,END)
    email_entry.delete(0,END)
    from datetime import date
    gen_combobox.set('Selecteaza gen')
    data_nastere_entry.set_date(date.today())
    contact_entry.delete(0,END)
    tip_angajare_combobox.set('Selecteaza tip')
    educatie_combobox.set('Selecteaza educatie')
    program_lucru_combobox.set('Selecteaza program')
    adresa_text.delete(1.0,END)
    data_angajare_entry.set_date(date.today())
    salariu_entry.delete(0,END)
    tip_utilizator_combobox.set('Selecteaza utilizator')
    parola_entry.delete(0,END)
    if check:
        angajati_treeview.selection_remove(angajati_treeview.selection())

def adauga_angajat(id, nume, email, gen, data_nastere, contact, tip_angajare, educatie, program_lucru, adresa,
                   data_angajare, salariu, tip_utilizator, parola):
    if (
        id == '' or nume == '' or email == '' or gen == 'Selecteaza gen' or contact == '' or tip_angajare == 'Selecteaza tip' or
        educatie == 'Selecteaza educatie' or program_lucru == 'Selecteaza program' or adresa == '\n' or salariu == '' or
        tip_utilizator == '' or parola == ''
    ):
        messagebox.showerror('Error', 'Toate spatiile trebuiesc completate!')
    else:
        cursor, conectare = conectare_bd()
        if not cursor or not conectare:
            return
        cursor.execute('use sistem_inventar')
        try:
            cursor.execute('SELECT id FROM date_angajati WHERE id=%s',(id,))
            if cursor.fetchone():
                messagebox.showerror('Error','Id-ul deja exista!')
                return
            adresa=adresa.strip()
            cursor.execute('INSERT INTO date_angajati VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (
            id, nume, email, gen, data_nastere, contact, tip_angajare, educatie, program_lucru, adresa,
            data_angajare, salariu, tip_utilizator, parola
            ))
            conectare.commit()
            treeview_data()  # Reîmprospătăm datele în Treeview
            messagebox.showinfo('Succes', 'Datele au fost introduse cu succes')
        except pymysql.MySQLError as e:
            messagebox.showerror('Eroare MySQL', f'A apărut o problemă cu introducerea datelor: {e}')
        finally:
            cursor.close()
            conectare.close()


def adauga_angajat(id, nume, email, gen, data_nastere, contact, tip_angajare, educatie, program_lucru, adresa,
                   data_angajare, salariu, tip_utilizator, parola):
    if (
        id == '' or nume == '' or email == '' or gen == 'Selecteaza gen' or contact == '' or tip_angajare == 'Selecteaza tip' or
        educatie == 'Selecteaza educatie' or program_lucru == 'Selecteaza program' or adresa == '\n' or salariu == '' or
        tip_utilizator == '' or parola == ''
    ):
        messagebox.showerror('Error', 'Toate spatiile trebuiesc completate!')
    else:
        cursor, conectare = conectare_bd()
        if not cursor or not conectare:
            return
        cursor.execute('use sistem_inventar')
        try:
            cursor.execute('SELECT id FROM date_angajati WHERE id=%s',(id,))
            if cursor.fetchone():
                messagebox.showerror('Error','Id-ul deja exista!')
                return
            adresa=adresa.strip()
            cursor.execute('INSERT INTO date_angajati VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (
            id, nume, email, gen, data_nastere, contact, tip_angajare, educatie, program_lucru, adresa,
            data_angajare, salariu, tip_utilizator, parola
            ))
            conectare.commit()
            treeview_data()  # Reîmprospătăm datele în Treeview
            messagebox.showinfo('Succes', 'Datele au fost introduse cu succes')
        except pymysql.MySQLError as e:
            messagebox.showerror('Eroare MySQL', f'A apărut o problemă cu introducerea datelor: {e}')
        finally:
            cursor.close()
            conectare.close()


def update_angajati(id, nume, email, gen, data_nastere, contact, tip_angajare, educatie, program_lucru, adresa,
                    data_angajare, salariu, tip_utilizator, parola):
    selectat = angajati_treeview.selection()
    if not selectat:
        messagebox.showerror('Eroare', 'Nu ai selectat o linie!')
        return

    cursor, conectare = conectare_bd()
    if not cursor or not conectare:
        return

    try:
        cursor.execute('use sistem_inventar')
        cursor.execute('SELECT * from date_angajati WHERE id=%s', (id,))
        current_data = cursor.fetchone()

        if not current_data:
            messagebox.showerror('Eroare', 'Nu s-a găsit înregistrarea selectată!')
            return

        # Exclude primul câmp (id) din current_data
        current_data = current_data[1:]

        # Normalizează datele
        current_data = tuple(str(value).strip() for value in current_data)
        adresa = adresa.strip()
        new_data = (nume, email, gen, data_nastere, contact, tip_angajare, educatie, program_lucru, adresa,
                    data_angajare, salariu, tip_utilizator, parola)
        new_data = tuple(str(value).strip() for value in new_data)

        # Compară datele
        if current_data == new_data:
            messagebox.showinfo('Info', 'Nu s-au detectat schimbări!')
            return

        # Actualizare în baza de date
        cursor.execute(
            'UPDATE date_angajati SET nume=%s, email=%s, gen=%s, data_nastere=%s, contact=%s, tip_angajare=%s, '
            'educatie=%s, program_lucru=%s, adresa=%s, data_angajare=%s, salariu=%s, tip_utilizator=%s, parola=%s '
            'WHERE id=%s',
            (nume, email, gen, data_nastere, contact, tip_angajare, educatie, program_lucru, adresa, data_angajare,
             salariu, tip_utilizator, parola, id))
        conectare.commit()
        treeview_data()  # Reîmprospătăm datele în Treeview
        messagebox.showinfo('Succes!', 'Datele au fost actualizate!')

    except pymysql.MySQLError as e:
        messagebox.showerror('Eroare MySQL', f'A apărut o problemă cu actualizarea datelor: {e}')

    finally:
        cursor.close()
        conectare.close()

def delete_angajati(id):
    selectat = angajati_treeview.selection()
    if not selectat:
        messagebox.showerror('Eroare', 'Nu ai selectat o linie!')
        return
    else:
        result = messagebox.askyesno('Confirmare', 'Doresti sa stergi aceasta inregistrare?')
        if result:
            cursor, conectare = conectare_bd()
            if not cursor or not conectare:
                return
            try:
                cursor.execute('use sistem_inventar')

                # Ștergem înregistrarea specificată
                cursor.execute('DELETE FROM date_angajati WHERE id=%s', (id,))

                # Actualizăm ID-urile pentru a fi consecutive
                cursor.execute('SET @new_id = 0')
                cursor.execute('UPDATE date_angajati SET id = (@new_id := @new_id + 1) ORDER BY id')

                conectare.commit()
                treeview_data()
                messagebox.showinfo('Succes', 'Inregistrarea a fost stearsa si ID-urile au fost actualizate!')
            except pymysql.MySQLError as e:
                messagebox.showerror('Eroare MySQL', f'A apărut o problemă cu actualizarea datelor: {e}')
            finally:
                cursor.close()
                conectare.close()

def search_angajati(search_option, value):
    if search_option == 'Search By':
        messagebox.showerror('Eroare', 'Nici o optiune selectata')
    elif value == '':
        messagebox.showerror('Eroare', 'Introdu valoarea pentru a cauta')
    else:
        search_option=search_option.replace(' ','_')
        cursor, conectare = conectare_bd()
        if not cursor or not conectare:
            return
        try:
            cursor.execute('use sistem_inventar')
            query = f"SELECT * FROM date_angajati WHERE {search_option} LIKE %s"
            cursor.execute(query, (f"%{value}%",))  # Corect parametrizat
            inregistrari = cursor.fetchall()
            angajati_treeview.delete(*angajati_treeview.get_children())
            for inregistrare in inregistrari:
                angajati_treeview.insert('', END, values=inregistrare)
        except pymysql.MySQLError as e:
            messagebox.showerror('Eroare MySQL', f'A apărut o problemă cu actualizarea datelor: {e}')
        finally:
            cursor.close()
            conectare.close()

def show_all(search_entry,search_combobox):
    treeview_data()
    search_entry.delete(0,END)
    search_combobox.set('Search by')

def angajati_tab(window):
    global back_image,angajati_treeview
    angajati_frame = Frame(window, width=1070, height=600, bg='light gray')
    angajati_frame.place(x=200, y=94)
    headingLabel = Label(angajati_frame, text='Gestionarea detaliilor angajatilor',
                         font=('times new roman', 16, 'bold'), bg='light green', fg='black')
    headingLabel.place(x=0, y=0, relwidth=1)

    top_frame = Frame(angajati_frame, bg='white')
    top_frame.place(x=0, y=30, relwidth=1, height=235)

    back_img_path = 'C:/Users/munte/Desktop/proiect/imagini/back.png'
    back_img = Image.open(back_img_path)
    resized_back_img = back_img.resize((30, 30))
    back_image = ImageTk.PhotoImage(resized_back_img)
    back_button = Button(angajati_frame, image=back_image, bd=0, cursor='hand2', bg='white',
                         command=lambda: angajati_frame.place_forget())
    back_button.place(x=10, y=30)

    # Adaugă hover efect pe butonul back
    back_button.bind("<Enter>", on_enter)
    back_button.bind("<Leave>", on_leave)
    search_frame = Frame(top_frame, bg='white')
    search_frame.pack()
    search_combobox = ttk.Combobox(search_frame, values=('id', 'nume', 'email'), font=('times new roman', 12),
                                   state='readonly', justify=CENTER)
    search_combobox.set('Search by')
    search_combobox.grid(row=0, column=0, padx=20)
    search_entry = Entry(search_frame, font=('times new roman', 12), bg='lightyellow')
    search_entry.grid(row=0, column=1)
    search_button = Button(search_frame, text='Search', font=('times new roman', 12), bg='white', width=10,
                           cursor='hand2',command=lambda :search_angajati(search_combobox.get(),search_entry.get()))
    search_button.grid(row=0, column=2, padx=20)
    search_button.bind("<Enter>", on_enter)
    search_button.bind("<Leave>", on_leave)

    show_button = Button(search_frame, text='Show All', font=('times new roman', 12), bg='white', width=10,
                         cursor='hand2', command=lambda :show_all(search_entry,search_combobox))
    show_button.grid(row=0, column=3)
    show_button.bind("<Enter>", on_enter)
    show_button.bind("<Leave>", on_leave)

    horizontal_scrollbar = Scrollbar(top_frame, orient=HORIZONTAL)
    vertical_scrollbar = Scrollbar(top_frame, orient=VERTICAL)
    angajati_treeview = ttk.Treeview(top_frame, columns=(
    'id', 'nume', 'email', 'gen', 'data_nastere', 'contact', 'tip_angajare', 'educatie', 'program_lucru'
    , 'adresa', 'data_angajare', 'salariu', 'tip_utilizator', 'parola'), show='headings',
                                     yscrollcommand=vertical_scrollbar.set,
                                     xscrollcommand=horizontal_scrollbar.set)  # show="headings" ascunde titlul default si le lasa doar pe cele introduse
    horizontal_scrollbar.pack(side=BOTTOM, fill=X)
    vertical_scrollbar.pack(side=RIGHT, fill=Y, pady=(10, 0))
    horizontal_scrollbar.config(command=angajati_treeview.xview)
    vertical_scrollbar.config(command=angajati_treeview.yview)
    angajati_treeview.pack(pady=(10, 0))  # umplutura de sus e 10 si cea de jos 0
    angajati_treeview.heading('id', text='ID')
    angajati_treeview.heading('nume', text='Nume')
    angajati_treeview.heading('email', text='Email')
    angajati_treeview.heading('gen', text='Gen')
    angajati_treeview.heading('data_nastere', text='Data Naștere')
    angajati_treeview.heading('contact', text='Contact')
    angajati_treeview.heading('tip_angajare', text='Tip Angajare')
    angajati_treeview.heading('educatie', text='Educație')
    angajati_treeview.heading('program_lucru', text='Program Lucru')
    angajati_treeview.heading('adresa', text='Adresă')
    angajati_treeview.heading('data_angajare', text='Data Angajare')
    angajati_treeview.heading('salariu', text='Salariu')
    angajati_treeview.heading('tip_utilizator', text='Tip Utilizator')
    angajati_treeview.heading('parola', text='Parolă')

    angajati_treeview.column('id', width=60)
    angajati_treeview.column('nume', width=140)
    angajati_treeview.column('email', width=180)
    angajati_treeview.column('gen', width=80)
    angajati_treeview.column('data_nastere', width=80)
    angajati_treeview.column('contact', width=100)
    angajati_treeview.column('tip_angajare', width=120)
    angajati_treeview.column('educatie', width=120)
    angajati_treeview.column('program_lucru', width=100)
    angajati_treeview.column('adresa', width=200)
    angajati_treeview.column('data_angajare', width=100)
    angajati_treeview.column('salariu', width=140)
    angajati_treeview.column('tip_utilizator', width=80)
    angajati_treeview.column('parola', width=80)

    treeview_data()

    detail_frame = Frame(angajati_frame)
    detail_frame.place(x=0, y=270)

    id_label = Label(detail_frame, text='ID', font=('times new roman', 12))
    id_label.grid(row=0, column=0, padx=40, pady=10, sticky='w')
    id_entry = Entry(detail_frame, font=('times new roman', 12), bg='lightyellow')
    id_entry.grid(row=0, column=1, padx=10, pady=10)

    nume_label = Label(detail_frame, text='Nume', font=('times new roman', 12))
    nume_label.grid(row=0, column=2, padx=40, pady=10, sticky='w')
    nume_entry = Entry(detail_frame, font=('times new roman', 12), bg='lightyellow')
    nume_entry.grid(row=0, column=3, padx=10, pady=10)

    email_label = Label(detail_frame, text='Email', font=('times new roman', 12))
    email_label.grid(row=0, column=4, padx=40, pady=10, sticky='w')
    email_entry = Entry(detail_frame, font=('times new roman', 12), bg='lightyellow')
    email_entry.grid(row=0, column=5, padx=10, pady=10)

    gen_label = Label(detail_frame, text='Gen', font=('times new roman', 12))
    gen_label.grid(row=1, column=0, padx=40, pady=10, sticky='w')
    gen_combobox = ttk.Combobox(detail_frame, values=('Male', 'Female', 'Other'), font=('times new roman', 12),
                                width=18, state='readonly')
    gen_combobox.set('Selecteaza gen')
    gen_combobox.grid(row=1, column=1, padx=10, pady=10)

    data_nastere_label = Label(detail_frame, text='Data nastere', font=('times new roman', 12))
    data_nastere_label.grid(row=1, column=2, padx=40, pady=10, sticky='w')
    data_nastere_entry = DateEntry(detail_frame, width=18, font=('times new roman', 12), state='readonly',
                                   date_pattern='dd/mm/yyyy')
    data_nastere_entry.grid(row=1, column=3)

    contact_label = Label(detail_frame, text='Contact', font=('times new roman', 12))
    contact_label.grid(row=1, column=4, padx=40, pady=10, sticky='w')
    contact_entry = Entry(detail_frame, font=('times new roman', 12), bg='lightyellow')
    contact_entry.grid(row=1, column=5, padx=10, pady=10)

    tip_angajare_label = Label(detail_frame, text='Tip angajare', font=('times new roman', 12))
    tip_angajare_label.grid(row=3, column=0, padx=40, pady=10, sticky='w')
    tip_angajare_combobox = ttk.Combobox(detail_frame, values=('Full time', 'Part time', 'Internship'),
                                         font=('times new roman', 12), width=18, state='readonly')
    tip_angajare_combobox.set('Selecteaza tip')
    tip_angajare_combobox.grid(row=3, column=1, padx=10, pady=10)

    educatie_label = Label(detail_frame, text='Educatie', font=('times new roman', 12))
    educatie_label.grid(row=3, column=2, padx=40, pady=10, sticky='w')
    educatie_combobox = ttk.Combobox(detail_frame, values=('test'), font=('times new roman', 12), width=18,
                                     state='readonly')
    educatie_combobox.set('Selecteaza educatie')
    educatie_combobox.grid(row=3, column=3, padx=10, pady=10)

    program_lucru_label = Label(detail_frame, text='Program Lucru', font=('times new roman', 12))
    program_lucru_label.grid(row=3, column=4, padx=40, pady=10, sticky='w')
    program_lucru_combobox = ttk.Combobox(detail_frame, values=('Dimineata', 'Dupa-amiaza', 'Seara'),
                                          font=('times new roman', 12), width=18, state='readonly')
    program_lucru_combobox.set('Selecteaza program')
    program_lucru_combobox.grid(row=3, column=5, padx=10, pady=10)

    adresa_label = Label(detail_frame, text='Adresa', font=('times new roman', 12))
    adresa_label.grid(row=4, column=0, padx=40, pady=10, sticky='w')
    adresa_text = Text(detail_frame, width=20, height=3, font=('times new roman', 12), bg='lightyellow')
    adresa_text.grid(row=4, column=1)

    data_angajare_label = Label(detail_frame, text='Data angajare', font=('times new roman', 12))
    data_angajare_label.grid(row=4, column=2, padx=40, pady=10, sticky='w')
    data_angajare_entry = DateEntry(detail_frame, width=18, font=('times new roman', 12), state='readonly',
                                    date_pattern='dd/mm/yyyy')
    data_angajare_entry.grid(row=4, column=3)

    tip_utilizator_label = Label(detail_frame, text='Tip utilizator', font=('times new roman', 12))
    tip_utilizator_label.grid(row=5, column=2, padx=40, pady=10, sticky='w')
    tip_utilizator_combobox = ttk.Combobox(detail_frame, values=('Admin', 'Angajat'), font=('times new roman', 12),
                                           width=18, state='readonly')
    tip_utilizator_combobox.set('Selecteaza utilizator')
    tip_utilizator_combobox.grid(row=5, column=3, padx=10, pady=10)

    salariu_label = Label(detail_frame, text='Salariu', font=('times new roman', 12))
    salariu_label.grid(row=4, column=4, padx=40, pady=10, sticky='w')
    salariu_entry = Entry(detail_frame, font=('times new roman', 12), bg='lightyellow')
    salariu_entry.grid(row=4, column=5, padx=10, pady=10)

    parola_label = Label(detail_frame, text='Parola', font=('times new roman', 12))
    parola_label.grid(row=5, column=4, padx=40, pady=10, sticky='w')
    parola_entry = Entry(detail_frame, font=('times new roman', 12), bg='lightyellow')
    parola_entry.grid(row=5, column=5, padx=10, pady=10)

    button_frame = Frame(angajati_frame, bg='light gray')
    button_frame.place(x=200, y=525)

    add_button = Button(button_frame, text='Add', font=('times new roman', 12), bg='white', width=10,
                        cursor='hand2',
                        command=lambda :adauga_angajat(id_entry.get(),nume_entry.get(),email_entry.get(),
                                                              gen_combobox.get(),data_nastere_entry.get(),contact_entry.get(),
                                                              tip_angajare_combobox.get(),educatie_combobox.get(),program_lucru_combobox.get(),adresa_text.get(1.0,END),
                                                              data_angajare_entry.get(),salariu_entry.get(),tip_utilizator_combobox.get(),parola_entry.get()))
    add_button.grid(row=0, column=0, padx=20, pady=10)
    add_button.bind("<Enter>", on_enter)
    add_button.bind("<Leave>", on_leave)

    update_button = Button(button_frame, text='Update', font=('times new roman', 12), bg='white', width=10,
                           cursor='hand2',
                           command=lambda :update_angajati(id_entry.get(),nume_entry.get(),email_entry.get(),
                                                                  gen_combobox.get(),data_nastere_entry.get(),contact_entry.get(),
                                                                  tip_angajare_combobox.get(),educatie_combobox.get(),program_lucru_combobox.get(),adresa_text.get(1.0,END),
                                                                  data_angajare_entry.get(),salariu_entry.get(),tip_utilizator_combobox.get(),parola_entry.get()))
    update_button.grid(row=0, column=1, padx=20, pady=10)
    update_button.bind("<Enter>", on_enter)
    update_button.bind("<Leave>", on_leave)

    delete_button = Button(button_frame, text='Delete', font=('times new roman', 12), bg='white', width=10,
                           cursor='hand2',command=lambda :delete_angajati(id_entry.get(),))
    delete_button.grid(row=0, column=2, padx=20, pady=10)
    delete_button.bind("<Enter>", on_enter)
    delete_button.bind("<Leave>", on_leave)

    clear_button = Button(button_frame, text='Clear', font=('times new roman', 12), bg='white', width=10,
                          cursor='hand2',command=lambda :clear_fields(id_entry,nume_entry,email_entry,
                                                                      gen_combobox,data_nastere_entry,contact_entry,tip_angajare_combobox,educatie_combobox,
                                                                      program_lucru_combobox,adresa_text,data_angajare_entry,salariu_entry,tip_utilizator_combobox,parola_entry,True))
    clear_button.grid(row=0, column=3, padx=20, pady=10)
    angajati_treeview.bind('<ButtonRelease-1>',lambda event:select_data(event,id_entry,nume_entry,email_entry,gen_combobox,data_nastere_entry,
                                                                        contact_entry,tip_angajare_combobox,educatie_combobox,program_lucru_combobox,adresa_text,data_angajare_entry,
                                                                        salariu_entry,tip_utilizator_combobox,parola_entry))

    create_db_tabel()
    clear_button.bind("<Enter>", on_enter)
    clear_button.bind("<Leave>", on_leave)