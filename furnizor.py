from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from functii import on_enter,on_leave
import pymysql

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

    name_label=Label(left_frame,text='Nume furnizor',font=('times new roman',14,'bold'),bg='white')
    name_label.grid(row=1,column=0,padx=(20,40),pady=25,sticky='w')
    name_entry=Entry(left_frame,font=('times new roman',14,'bold'),bg='lightyellow')
    name_entry.grid(row=1,column=1)

    contact_label=Label(left_frame,text='Contact furnizor',font=('times new roman',14,'bold'),bg='white')
    contact_label.grid(row=2,column=0,padx=(20,40),sticky='w')
    contact_entry=Entry(left_frame,font=('times new roman',14,'bold'),bg='lightyellow')
    contact_entry.grid(row=2,column=1)

    description_label=Label(left_frame,text='Descriere',font=('times new roman',14,'bold'),bg='white')
    description_label.grid(row=3,column=0,padx=(20,40),sticky='nw',pady=25)
    description_text=Text(left_frame,width=25,height=6,bd=2,bg='lightyellow')
    description_text.grid(row=3,column=1,pady=25)

    button_frame=Frame(left_frame,bg='white')
    button_frame.grid(row=4,columnspan=2,pady=20)

    add_button = Button(button_frame, text='Adauga', font=('times new roman', 12), bg='white', width=8,
                        cursor='hand2')
    add_button.grid(row=0, column=0, padx=20)
    add_button.bind("<Enter>", on_enter)
    add_button.bind("<Leave>", on_leave)

    update_button = Button(button_frame, text='Actualizeaza', font=('times new roman', 12), bg='white', width=8,
                        cursor='hand2')
    update_button.grid(row=0, column=1)
    update_button.bind("<Enter>", on_enter)
    update_button.bind("<Leave>", on_leave)

    delete_button = Button(button_frame, text='Sterge', font=('times new roman', 12), bg='white', width=8,
                        cursor='hand2')
    delete_button.grid(row=0, column=3, padx=20)
    delete_button.bind("<Enter>", on_enter)
    delete_button.bind("<Leave>", on_leave)

    clear_button = Button(button_frame, text='Clear', font=('times new roman', 12), bg='white', width=8,
                        cursor='hand2')
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

    search_button = Button(search_frame, text='Cauta', font=('times new roman', 12), bg='white', width=8,
                           cursor='hand2')
    search_button.grid(row=0, column=2,padx=15)
    search_button.bind("<Enter>", on_enter)
    search_button.bind("<Leave>", on_leave)

    show_button = Button(search_frame, text='Toate', font=('times new roman', 12), bg='white', width=8,
                       cursor='hand2')
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




