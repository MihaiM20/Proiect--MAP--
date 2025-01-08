import sqlite3
import random

def adauga():
    conn = sqlite3.connect('scuze.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS scuze(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        scuze_text TEXT NOT NULL
     )             
                   
                   
                   ''')
    scuza_noua = input("Introdu scuza ta:")
    cursor.execute('INSERT INTO scuze (scuze_text) VALUES (?)',(scuza_noua,))
    conn.commit()
    print("Ai introdus cu succes scuza in DB")
    conn.close()

def afisare():
    conn = sqlite3.connect('scuze.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM scuze')
    scuze = cursor.fetchall()
    print("Scuzele existente in DB sunt: ")
    for i in scuze:
        print(f"{i[0]}:{i[1]}")
    conn.close()
    
def stergere():
    conn = sqlite3.connect('scuze.db')
    cursor = conn.cursor()
    afisare()
    id_de_sters = input("Introdu id-ul pe care vrei sa il stergi: ")
    cursor.execute('DELETE FROM scuze WHERE id = ?', (id_de_sters))
    conn.commit()
    print("Elementul tau a fost sters cu succes din DB")
    conn.commit()
    
def afisare_random():
    conn = sqlite3.connect('scuze.db')
    cursor = conn.cursor()
    cursor.execute('SELECT scuze_text FROM scuze')
    scuze = cursor.fetchall()
    if scuze:
        scuza_random = random.choice(scuze)
        print(f"Scuza ta este: {scuza_random}")
    conn.close()

def update():
    conn = sqlite3.connect('scuze.db')
    cursor = conn.cursor()
    afisare()
    id_modificat=input("Introdu id-ul pe care vrei sa il modifici: ")
    scuza_noua=input(f"Introdu o noua scuza pentru {id_modificat}: ")
    cursor.execute('UPDATE scuze SET scuze_text=? WHERE id = ?', (scuza_noua, id_modificat))
    conn.commit()
    print(f"Am modificat elementul cu id-ul {id_modificat}")
    conn.close()
    
#afisare()   
#adauga()
#stergere()
#afisare_random()
update() 