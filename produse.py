from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from functii import on_enter, on_leave
from angajati import conectare_bd
from tkinter import messagebox
from tkinter import Label, Spinbox
import pymysql

# Variabilă globală pentru a salva ID-ul selectat
selected_produs_id = None
def show_all(treeview):
    cursor, conectare = conectare_bd()
    if not cursor or not conectare:
        return

    try:
        cursor.execute('USE sistem_inventar')  # Selectează baza de date
        cursor.execute('SELECT * FROM date_produse')  # Interogare pentru a obține toate produsele
        records = cursor.fetchall()

        treeview.delete(*treeview.get_children())  # Șterge înregistrările anterioare din treeview
        if len(records) > 0:
            for record in records:
                treeview.insert('', 'end', values=record)  # Adaugă fiecare produs în treeview
        else:
            messagebox.showinfo('Info', 'Nu există produse în baza de date!')

    except pymysql.MySQLError as e:
        messagebox.showerror('Eroare MySQL', f'Eroare la interogarea datelor: {e}')
    finally:
        cursor.close()
        conectare.close()

def cauta_produs(search_combobox, search_entr, treeview):
    # Verifică dacă utilizatorul a selectat o opțiune din combobox
    if search_combobox.get() == "Search By":
        messagebox.showwarning('Atentie!', 'Trebuie să selectezi o opțiune!')
        return

    # Verifică dacă utilizatorul a introdus o valoare în entry
    elif search_entr.get() == '':
        messagebox.showwarning('Atentie', 'Trebuie să introduci o valoare!')
        return

    try:
        cursor, conectare = conectare_bd()
        if not cursor or not conectare:
            return

        cursor.execute('USE sistem_inventar')  # Selectează baza de date
        query = f'SELECT * FROM date_produse WHERE {search_combobox.get()}=%s'
        cursor.execute(query, (search_entr.get(),))  # Execută interogarea cu valoarea căutată

        records = cursor.fetchall()  # Obține toate rezultatele
        if len(records) == 0:
            messagebox.showerror('Error', 'No records found')
            return

        # Șterge înregistrările anterioare din treeview
        treeview.delete(*treeview.get_children())

        # Adaugă noile înregistrări în treeview
        for record in records:
            treeview.insert('', 'end', values=record)

    except pymysql.MySQLError as e:
        messagebox.showerror('Eroare MySQL', f'Eroare la interogarea datelor: {e}')
    finally:
        if cursor:
            cursor.close()  # Închide cursorul
        if conectare:
            conectare.close()  # Închide conexiunea

def select_produs(event, treeview, categorie_combobox, furnizor_combobox, nume_entry, pret_entry, discount_spinbox, cantitate_entry,
                  status_combobox):
    global selected_produs_id  # Folosim variabila globală
    # Obține elementul selectat
    index = treeview.selection()
    if not index:  # Verifică dacă un element este selectat
        return

    content = treeview.item(index)
    row = content['values']  # Obține valorile rândului selectat

    # Setează ID-ul produsului selectat
    selected_produs_id = row[0]  # ID-ul este prima coloană

    # Șterge câmpurile existente
    categorie_combobox.set('Empty')  # Resetează combobox-ul pentru categorie
    furnizor_combobox.set('Empty')  # Resetează combobox-ul pentru furnizor
    nume_entry.delete(0, END)  # Șterge textul din entry-ul pentru nume produs
    pret_entry.delete(0, END)  # Șterge textul din entry-ul pentru preț
    discount_spinbox.delete(0, 'end')  # Șterge valoarea din spinbox pentru discount
    cantitate_entry.delete(0, END)  # Șterge textul din entry-ul pentru cantitate
    status_combobox.set('Selecteaza status')  # Resetează combobox-ul pentru status

    # Populează câmpurile cu datele selectate
    categorie_combobox.set(row[1])  # Setează valoarea din col. 2 (categorie) în combobox
    furnizor_combobox.set(row[2])  # Setează valoarea din col. 3 (furnizor) în combobox
    nume_entry.insert(0, row[3])  # Setează valoarea din col. 4 (nume) în entry
    pret_entry.insert(0, row[4])  # Setează valoarea din col. 5 (pret) în entry
    discount_spinbox.insert(0, row[5])  # Setează valoarea din col. 6 (discount) în spinbox
    cantitate_entry.insert(0, row[7])  # Setează valoarea din col. 8 (cantitate) în entry
    status_combobox.set(row[8])  # Setează valoarea din col. 9 (status) în combobox

def clear_fields(categorie_combobox, furnizor_combobox, nume_entry, pret_entry, discount_spinbox, cantitate_entry, status_combobox):
    # Resetează toate câmpurile
    categorie_combobox.set('Selecteaza')  # Resetează combobox-ul pentru categorie
    furnizor_combobox.set('Selecteaza')  # Resetează combobox-ul pentru furnizor
    nume_entry.delete(0, END)  # Șterge textul din entry-ul pentru nume produs
    pret_entry.delete(0, END)  # Șterge textul din entry-ul pentru preț
    discount_spinbox.delete(0, 'end')
    cantitate_entry.delete(0, END)  # Șterge textul din entry-ul pentru cantitate
    status_combobox.set('Selecteaza status')  # Resetează combobox-ul pentru status


def delete_produs(treeview):
    global selected_produs_id  # Folosim variabila globală pentru ID-ul selectat

    if selected_produs_id is None:
        messagebox.showerror('Eroare', 'Nu a fost selectat niciun produs!')
        return

    # Confirmare înainte de ștergere
    confirm = messagebox.askyesno('Confirmare', 'Sigur doriți să ștergeți acest produs?')
    if not confirm:
        return

    # Conectare la baza de date
    cursor, conectare = conectare_bd()
    if not cursor or not conectare:
        return

    try:
        cursor.execute('USE sistem_inventar')

        # Ștergerea produsului din baza de date
        cursor.execute('DELETE FROM date_produse WHERE id = %s', (selected_produs_id,))
        conectare.commit()

        # Actualizare treeview pentru a reflecta ștergerea
        treeview_data(treeview)

        # Resetare variabilă globală
        selected_produs_id = None

        messagebox.showinfo('Succes', 'Produsul a fost șters cu succes!')

    except pymysql.MySQLError as e:
        messagebox.showerror('Eroare MySQL', f'Problema la ștergerea produsului: {e}')
    finally:
        cursor.close()
        conectare.close()

def actualizeaza_produs(categorie, furnizor, nume, pret, discount, cantitate, status, treeview):
    global selected_produs_id  # Folosim variabila globală pentru ID-ul selectat

    if selected_produs_id is None:
        messagebox.showerror('Eroare', 'Nu a fost selectat niciun produs!')
        return

    # Verificăm dacă câmpurile sunt completate corect
    if categorie in ('Empty', 'Select') or furnizor in ('Empty', 'Select') or status == 'Selecteaza status' or not nume or not pret or not cantitate:
        messagebox.showerror('Eroare', 'Toate câmpurile trebuie completate corect!')
        return

    # Validare valori pentru preț și cantitate
    try:
        pret = float(pret)
        cantitate = int(cantitate)
        discount = int(discount) if discount.isdigit() else 0  # Asigură-te că discount-ul este un număr întreg valid
        if pret < 0 or cantitate < 0 or discount < 0 or discount > 100:
            raise ValueError
    except ValueError:
        messagebox.showerror('Eroare', 'Pretul, cantitatea și discount-ul trebuie să fie valori valide!')
        return

    # Calcularea prețului cu discount
    pret_discount = round(pret - (pret * discount / 100), 2) if discount > 0 else pret  # Aplicăm discount-ul dacă este mai mare decât 0

    # Conectare la baza de date
    cursor, conectare = conectare_bd()
    if not cursor or not conectare:
        return

    try:
        cursor.execute('USE sistem_inventar')

        # Verificare dacă valorile curente din baza de date sunt deja aceleași
        cursor.execute('SELECT categorie, furnizor, nume, pret, cantitate, status, discount FROM date_produse WHERE id=%s',
                       (selected_produs_id,))
        produs = cursor.fetchone()

        if produs:
            # Comparăm valorile curente cu cele noi
            if (produs[0] == categorie and produs[1] == furnizor and produs[2] == nume and
                    produs[3] == pret and produs[4] == cantitate and produs[5] == status and produs[6] == discount):
                messagebox.showinfo('Info', 'Nu s-au făcut modificări, valorile sunt aceleași!')
                return

        # Actualizare produs
        cursor.execute(
            'UPDATE date_produse SET categorie=%s, furnizor=%s, nume=%s, pret=%s, discount=%s, pret_discount=%s, cantitate=%s, status=%s WHERE id=%s',
            (categorie, furnizor, nume, pret, discount, pret_discount, cantitate, status, selected_produs_id)  # Folosim ID-ul selectat
        )
        conectare.commit()

        # Actualizare treeview
        treeview_data(treeview)
        messagebox.showinfo('Succes', 'Produsul a fost actualizat cu succes!')

    except pymysql.MySQLError as e:
        messagebox.showerror('Eroare MySQL', f'Problema la actualizarea produsului: {e}')
    finally:
        cursor.close()
        conectare.close()

def treeview_data(treeview):
    cursor, conectare = conectare_bd()
    if not cursor or not conectare:
        return

    try:
        cursor.execute('USE sistem_inventar')
        cursor.execute('SELECT * FROM date_produse')  # Obține toate datele din tabel
        rows = cursor.fetchall()

        # Șterge datele existente din Treeview
        treeview.delete(*treeview.get_children())

        # Adaugă rândurile noi în Treeview
        for row in rows:
            treeview.insert('', 'end', values=row)

    except pymysql.MySQLError as e:
        messagebox.showerror('Eroare MySQL', f'Problema la afișarea datelor: {e}')
    finally:
        cursor.close()
        conectare.close()

def fetch_categorie_furnizor(categorie_combobox,furnizor_combobox):
    optiuni_categorie=[]
    optiuni_furnizor=[]
    cursor, conectare = conectare_bd()
    if not cursor or not conectare:
        return
    cursor.execute('USE sistem_inventar')
    cursor.execute('SELECT nume from date_categorie')
    names=cursor.fetchall()
    if len(names)>0:
        categorie_combobox.set('Selecteaza')
        for nume in names:
            optiuni_categorie.append(nume[0])
        categorie_combobox.config(values=optiuni_categorie)

    cursor.execute('SELECT nume from date_furnizori')
    names=cursor.fetchall()
    if len(names)>0:
        furnizor_combobox.set('Selecteaza')
        for nume in names:
            optiuni_furnizor.append(nume[0])
        furnizor_combobox.config(values=optiuni_furnizor)

def adauga_produs(categorie, furnizor, nume, pret, discount, cantitate, status, treeview, categorie_combobox, furnizor_combobox, nume_entry, pret_entry, discount_spinbox, cantitate_entry, status_combobox):
    if categorie in ('Empty', 'Selecteaza') or furnizor in ('Empty', 'Selecteaza') or status == 'Selecteaza status' or not nume or not pret or not cantitate:
        messagebox.showerror('Eroare', 'Toate câmpurile trebuie completate corect!')
        return

    try:
        pret = float(pret)
        cantitate = int(cantitate) if cantitate.isdigit() else 0  # Asigură-te că cantitatea este un număr întreg valid
        discount = int(discount) if discount.isdigit() else 0  # Asigură-te că discount-ul este un număr întreg valid

        if pret < 0 or cantitate < 0 or discount < 0 or discount > 100:
            raise ValueError
    except ValueError:
        messagebox.showerror('Eroare', 'Pretul, cantitatea și discount-ul trebuie să fie valori valide!')
        return

    pret_discount = round(pret - (pret * discount / 100), 2)

    cursor, conectare = conectare_bd()
    if not cursor or not conectare:
        return

    try:
        cursor.execute('USE sistem_inventar')

        # Creăm tabelul dacă nu există
        cursor.execute('''CREATE TABLE IF NOT EXISTS date_produse (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            categorie VARCHAR(100),
                            furnizor VARCHAR(100),
                            nume VARCHAR(100),
                            pret DECIMAL(10,2),
                            discount INT,
                            pret_discount DECIMAL(10,2),
                            cantitate INT,
                            status VARCHAR(50)
                        )''')

        # Verificăm dacă produsul există deja
        cursor.execute('SELECT * FROM date_produse WHERE categorie=%s AND furnizor=%s AND nume=%s',
                       (categorie, furnizor, nume))
        produs_existent = cursor.fetchone()
        if produs_existent:
            messagebox.showerror('Eroare', 'Produsul deja exista!')
            return

        # Adăugăm produsul în baza de date
        cursor.execute(
            'INSERT INTO date_produse (categorie, furnizor, nume, pret, discount, pret_discount, cantitate, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
            (categorie, furnizor, nume, pret, discount, pret_discount, cantitate, status)
        )
        conectare.commit()

        # Actualizăm Treeview
        treeview_data(treeview)

        # Resetare câmpuri
        categorie_combobox.set('Selecteaza')
        furnizor_combobox.set('Selecteaza')
        nume_entry.delete(0, END)
        pret_entry.delete(0, END)
        discount_spinbox.delete(0, END)
        cantitate_entry.delete(0, END)
        status_combobox.set('Selecteaza status')

        messagebox.showinfo('Succes', 'Produsul a fost adăugat cu succes!')

    except pymysql.MySQLError as e:
        messagebox.showerror('Eroare MySQL', f'Problema la adăugarea produsului: {e}')
    finally:
        cursor.close()
        conectare.close()

def produse_tab(window):
    global back_image
    produse_frame = Frame(window, width=1070, height=600, bg='white')
    produse_frame.place(x=200, y=93)

    # Imagine buton back
    back_img_path = 'C:/Users/munte/Desktop/proiect/imagini/back.png'
    back_img = Image.open(back_img_path)
    resized_back_img = back_img.resize((30, 30))
    back_image = ImageTk.PhotoImage(resized_back_img)
    back_button = Button(produse_frame, image=back_image, bd=0, cursor='hand2', bg='white',
                         command=lambda: produse_frame.place_forget())
    back_button.place(x=10, y=10)
    back_button.bind("<Enter>", on_enter)
    back_button.bind("<Leave>", on_leave)

    left_frame = Frame(produse_frame, bg='white',bd=2,relief=RIDGE)
    left_frame.place(x=20, y=45)  # Repozitionare secțiune detalii

    headingLabel = Label(left_frame, text='Gestionare produse',
                         font=('times new roman', 16, 'bold'), bg='light green', fg='black')
    headingLabel.grid(row=0,columnspan=2,sticky='we')

    categorie_label = Label(left_frame, text='Categorie', font=('times new roman', 14, 'bold'), bg='white')
    categorie_label.grid(row=1, column=0, padx=20, sticky='w')
    categorie_combobox=ttk.Combobox(left_frame,font=('times new roman', 14, 'bold'),width=18,state='readonly')
    categorie_combobox.grid(row=1,column=1,pady=20)
    categorie_combobox.set('Empty')

    furnizor_label = Label(left_frame, text='Furnizor', font=('times new roman', 14, 'bold'), bg='white')
    furnizor_label.grid(row=2, column=0, padx=20, sticky='w')
    furnizor_combobox=ttk.Combobox(left_frame,font=('times new roman', 14, 'bold'),width=18,state='readonly')
    furnizor_combobox.grid(row=2,column=1)
    furnizor_combobox.set('Empty')

    nume_label = Label(left_frame, text='Nume produs', font=('times new roman', 14, 'bold'), bg='white')
    nume_label.grid(row=3, column=0, padx=20, sticky='w')
    nume_entry = Entry(left_frame, font=('times new roman', 14), bg='light yellow',width=18)
    nume_entry.grid(row=3, column=1, padx=10, pady=20, sticky='w')

    pret_label = Label(left_frame, text='Pret', font=('times new roman', 14, 'bold'), bg='white')
    pret_label.grid(row=4, column=0, padx=20, sticky='w')
    pret_entry = Entry(left_frame, font=('times new roman', 14), bg='light yellow',width=18)
    pret_entry.grid(row=4, column=1, padx=10, pady=20, sticky='w')

    discount_label = Label(left_frame, text='Discount(%)', font=('times new roman', 14, 'bold'), bg='white')
    discount_label.grid(row=5, column=0, padx=20, sticky='w')
    discount_spinbox = Spinbox(left_frame, from_=0, to=100, font=('times new roman', 14),width=18)
    discount_spinbox.grid(row=5, column=1, padx=10, pady=20, sticky='w')

    cantitate_label = Label(left_frame, text='Cantitate', font=('times new roman', 14, 'bold'), bg='white')
    cantitate_label.grid(row=6, column=0, padx=20, sticky='w')
    cantitate_entry = Entry(left_frame, font=('times new roman', 14), bg='light yellow',width=18)
    cantitate_entry.grid(row=6, column=1, padx=10, pady=30, sticky='w')

    status_label = Label(left_frame, text='Status', font=('times new roman', 14, 'bold'), bg='white')
    status_label.grid(row=7, column=0, padx=20, sticky='w')
    status_combobox=ttk.Combobox(left_frame,values=('Activ','Inactiv'),font=('times new roman', 14, 'bold'),width=18,state='readonly')
    status_combobox.grid(row=7,column=1)
    status_combobox.set('Selecteaza status')

    button_frame=Frame(left_frame,bg='white')
    button_frame.grid(row=8,columnspan=2,pady=(30,10))

    add_button = Button(button_frame, text='Add', font=('times new roman', 12), bg='white', width=8, cursor='hand2',
                        command=lambda: adauga_produs(
                            categorie_combobox.get(),
                            furnizor_combobox.get(),
                            nume_entry.get(),
                            pret_entry.get(),
                            discount_spinbox.get(),
                            cantitate_entry.get(),
                            status_combobox.get(),
                            treeview,
                            categorie_combobox,
                            furnizor_combobox,
                            nume_entry,
                            pret_entry,
                            discount_spinbox,
                            cantitate_entry,
                            status_combobox
                        ))

    add_button.grid(row=0, column=0, padx=10)
    add_button.bind("<Enter>", on_enter)
    add_button.bind("<Leave>", on_leave)

    update_button = Button(button_frame, text='Update', font=('times new roman', 12), bg='white', width=8,
                           cursor='hand2', command=lambda: actualizeaza_produs(
            categorie_combobox.get(),  # Obține valoarea din combobox pentru categorie
            furnizor_combobox.get(),  # Obține valoarea din combobox pentru furnizor
            nume_entry.get(),  # Obține valoarea din entry-ul pentru nume produs
            pret_entry.get(),  # Obține valoarea din entry-ul pentru preț
            discount_spinbox.get(),
            cantitate_entry.get(),  # Obține valoarea din entry-ul pentru cantitate
            status_combobox.get(),  # Obține valoarea din combobox pentru status
            treeview  # Actualizează treeview-ul
        ))

    update_button.grid(row=0, column=1)
    update_button.bind("<Enter>", on_enter)
    update_button.bind("<Leave>", on_leave)

    delete_button = Button(button_frame, text='Delete', font=('times new roman', 12), bg='white', width=8,
                           cursor='hand2', command=lambda: delete_produs(treeview))
    delete_button.grid(row=0, column=2, padx=10)
    delete_button.bind("<Enter>", on_enter)
    delete_button.bind("<Leave>", on_leave)

    clear_button = Button(button_frame, text='Clear', font=('times new roman', 12), bg='white', width=8, cursor='hand2',
                          command=lambda: clear_fields(categorie_combobox, furnizor_combobox, nume_entry, pret_entry,
                                                       discount_spinbox, cantitate_entry, status_combobox))
    clear_button.grid(row=0, column=3, padx=10)
    clear_button.bind("<Enter>", on_enter)
    clear_button.bind("<Leave>", on_leave)

    search_frame=LabelFrame(produse_frame,text='Cauta Produs',font=('times new roman', 14,'bold'),bg='white')
    search_frame.place(x=480,y=30)

    search_combobox=ttk.Combobox(search_frame,font=('times new roman', 14),values=('Categorie','Furnizor','Nume','Status'),state='readonly',width=16)
    search_combobox.grid(row=0,column=0,padx=10)
    search_combobox.set('Search By')
    search_entry = Entry(search_frame, font=('times new roman', 14), bg='light yellow',width=16)
    search_entry.grid(row=0, column=1, padx=10, sticky='w')

    search_button = Button(search_frame, text='Search', font=('times new roman', 12), bg='white', width=8, cursor='hand2',
                           command= lambda:cauta_produs(search_combobox,search_entry,treeview))
    search_button.grid(row=0, column=2, padx=(10,0),pady=10)
    search_button.bind("<Enter>", on_enter)
    search_button.bind("<Leave>", on_leave)

    show_button = Button(search_frame, text='Show All', font=('times new roman', 12), bg='white', width=8,
                         cursor='hand2', command=lambda: show_all(treeview))
    show_button.grid(row=0, column=3, padx=10)
    show_button.bind("<Enter>", on_enter)
    show_button.bind("<Leave>", on_leave)

    treeview_frame=Frame(produse_frame)
    treeview_frame.place(x=480,y=125,width=570,height=430)


    scrolly = Scrollbar(treeview_frame, orient=VERTICAL)
    scrollx = Scrollbar(treeview_frame, orient=HORIZONTAL)
    treeview = ttk.Treeview(treeview_frame,
                            column=('id', 'categorie', 'furnizor', 'nume', 'pret','discount','pret_discount', 'cantitate', 'status'),
                            show='headings', yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

    scrolly.pack(side=RIGHT, fill=Y)
    scrollx.pack(side=BOTTOM, fill=X)
    scrollx.config(command=treeview.xview)
    scrolly.config(command=treeview.yview)
    treeview.pack(fill=BOTH, expand=1)

    treeview.heading('id', text='ID')
    treeview.heading('categorie', text='Categorie')
    treeview.heading('furnizor', text='Furnizor')
    treeview.heading('nume', text='Nume produs')
    treeview.heading('pret', text='Pret')
    treeview.heading('discount', text='Discount')
    treeview.heading('pret_discount', text='Pret Discount')
    treeview.heading('cantitate', text='Cantitate')
    treeview.heading('status', text='Status')

    treeview.column('id', width=50)
    treeview.column('categorie', width=100)
    treeview.column('furnizor', width=100)
    treeview.column('nume', width=140)
    treeview.column('pret', width=100)
    treeview.column('discount', width=100)
    treeview.column('pret_discount', width=100)
    treeview.column('cantitate', width=100)
    treeview.column('status', width=100)

    fetch_categorie_furnizor(categorie_combobox,furnizor_combobox)
    treeview_data(treeview)
    treeview.bind('<ButtonRelease-1>',
                   lambda e: select_produs(e, treeview, categorie_combobox, furnizor_combobox, nume_entry,
                                           pret_entry,discount_spinbox, cantitate_entry, status_combobox))
    return produse_frame