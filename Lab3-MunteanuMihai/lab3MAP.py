import requests
from bs4 import BeautifulSoup

# from hashlib import new
import smtplib
# from apscheduler.schedulers.blocking import BlockingScheduler
#   myaccount.google.com/apppasswords
with open('/Users/munte/Desktop/parola_google.txt', 'r') as fisier:
    parola_google = fisier.read()
 
to_addr_list = ['munteanu.mihai3416@gmail.com'] 
cc_addr_list= ['']
sender='munteanu.mihai3416@gmail.com'    
subject='A SCAZUT PRETUL LA PRODUSUL TAU'  
def sendemail(sender,message, subject,to_addr_list, cc_addr_list=[]):
    try:
        smtpserver='smtp.gmail.com:587'
        header  = 'From: %s\n' % sender
        header += 'To: %s\n' % ','.join(to_addr_list)
        header += 'Cc: %s\n' % ','.join(cc_addr_list)
        header += 'Subject: %s\n\n' % subject
        message = header + message
        server = smtplib.SMTP(smtpserver)
        server.starttls()
#Parola este de pe myaccount.google.com/apppasswords
        server.login(sender,parola_google)
        server.quit()
        return True
    except:
        print("Error: unable to send email")
        return False
def verificare_pret():
    req=requests.get("https://www.emag.ro/telefon-mobil-apple-iphone-16-pro-max-256gb-5g-desert-titanium-mywx3zd-a/pd/DW367LYBM/")
    soup=BeautifulSoup(req.text,"html.parser")
    pret=soup.find('p',attrs={'class':'product-new-price'}).text
    pret=pret[0:5]
    pret=pret.replace(".","")
    pret=int(pret)
    pret_de_referinta=7200
    nume_produs=data_nume().strip()
    recenzie_produse=data_recenzie()
    if(pret<pret_de_referinta):
        print("Pretul este mai mic decat pretul de referinta")
        print(pret)
        print(nume_produs)
        print(recenzie_produse)
        # message= "A scazut pretul la: " + nume_produs + "\n" + "Ratingul produsului este de: " + recenzie_produse
        # sendmail(sender,message,subject,to_addr_list,cc_addr_list=[])
    else:
        print("Pretul este mai mare decat pretul de referinta")
        print(pret)


def data_nume():
    req=requests.get("https://www.emag.ro/telefon-mobil-apple-iphone-16-pro-max-256gb-5g-desert-titanium-mywx3zd-a/pd/DW367LYBM/")
    soup=BeautifulSoup(req.text,"html.parser")
    titlu=soup.find('h1',attrs={'class':'page-title'}).text
    return titlu

def data_recenzie():
    req=requests.get("https://www.emag.ro/telefon-mobil-apple-iphone-16-pro-max-256gb-5g-desert-titanium-mywx3zd-a/pd/DW367LYBM/")
    soup=BeautifulSoup(req.text,"html.parser")
    recenzie=soup.find('p',attrs={'class':'review-rating-data'}).text
    return recenzie


verificare_pret()
# #from apscheduler.schedulers.blocking import BlockingScheduler
# scheduler = BlockingScheduler()
# scheduler.add_job(verificare_pret, 'interval', seconds=10)
# scheduler.start()