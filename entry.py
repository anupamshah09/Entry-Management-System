#import PIL.ImageTk, PIL.Image
from tkinter.ttk import *
from tkinter import *
from tkinter import messagebox
import mysql.connector
import smtplib
import time
import phonenumbers
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type
from twilio.rest import Client
from validate_email import validate_email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from config import *
   # from message import *
#from py3DNS import *

def popup1():
    messagebox.showinfo("SAVED", "Your information has been stored!")

def popup2():
    messagebox.showerror("Error","Please enter valid details!")

def popup3():
    messagebox.showinfo("Checked-Out", "You have been successfully checked out!")

def popup4():
    messagebox.showerror("Error","You have already checked_out")

my_db= mysql.connector.connect(host='localhost',
                                         user=MYSQL,
                                         password=MYSQLPASSWORD)

def emailv(mail):

    cursor2=my_db.cursor()
    mail1 = mail.get()
    em = smtplib.SMTP('smtp.gmail.com', 587)
    em.starttls()
    em.login(EMAIL,PASSWORD)

    msg = "Details of the meeting is\n"

    sql = "UPDATE information SET check_out=NOW() WHERE vis_Email=%s and check_out is NULL"# simple queries of the MySQL
    cursor2.execute(sql,(mail1,))
    my_db.commit()

    sql1="select vis_name from information where vis_email=%s"
    cursor2.execute(sql1,(mail1,))
    vist_name=""
    for i in cursor2:
        vist_name=str(i[0])

    sql2 = "select vis_number from information where vis_email=%s"
    cursor2.execute(sql2, (mail1,))
    vist_number=""
    for i in cursor2:
        vist_number=str(i[0])

    sql3 = "select h_name from information where vis_email=%s"
    cursor2.execute(sql3, (mail1,))
    hst_name=""
    for i in cursor2:
        hst_name= str(i[0])

    sql4= "select check_in from information where vis_email=%s"
    cursor2.execute(sql4, (mail1,))
    chkin=""
    for i in cursor2:
        chkin = str(i[0])

    sql5 = "select check_out from information where vis_email=%s"
    cursor2.execute(sql5, (mail1,))
    chkout=""
    for i in cursor2:
        chkout = str(i[0])

    msg+="your name-->"+vist_name+"\n"+"your number-->"+vist_number+"\ncheck-in time-->"+chkin+"\ncheck out time"+chkout+"\nhost name-->"+hst_name+"\nAddress is 2nd and 9th Floor, Tower 3, Candor Techspace, Rajat Vihar, Block B, Industrial Area, Sector 62, Noida, Uttar Pradesh 201309"
    em.sendmail(EMAIL,mail1, msg) # Send An email to the visitor Which Contain message msg Which is the details of the meeting

    em.quit()
    popup3()

def sms(vis_name,vis_num,host_num):
    auth_token = TOKEN
    account_sid = ACCOUNT

    client = Client(account_sid, auth_token)
    message = client.messages.create(
        to= str(host_num),
        from_ = CONTACT,
        body=vis_name+ " is coming to meet you and visitor's Contact Number is " + vis_num)
    
def hemail(Name,host_email,NUMBER):
    em = smtplib.SMTP('smtp.gmail.com', 587)

    em.starttls()

    em.login(EMAIL,PASSWORD)

    msg = Name + " is coming to meet you and\nhis contact number is " + NUMBER
    em.sendmail(EMAIL, host_email, msg)

    em.quit()

def save_query(name,email,number,name1,email1,number1):
    cursor1=my_db.cursor()
    v_name= name.get()
    v_email=email.get()
    v_number = number.get()
    ho_name = name1.get()
    ho_email= email1.get()
    ho_number= number1.get()
    hemail(v_name, ho_email, v_number)
    sms(v_name, v_email, ho_number)
    sql2 = "INSERT INTO information(vis_name,vis_email,vis_number,h_name,h_email,h_number) VALUES(%s,%s,%s,%s,%s,%s)"
    var = (v_name, v_email, v_number, ho_name, ho_email, ho_number)
    cursor1.execute(sql2,var)
    my_db.commit()
    popup1()
def create_database():
    cursor = my_db.cursor()
    try:
        query1="create database contain_information"

        cursor.execute(query1)
        cursor.execute("use contain_information")
        query2= "CREATE TABLE information( vis_name varchar(255),vis_email varchar(255),vis_number varchar(255),h_name varchar(255),h_email varchar(255),h_number varchar(255),check_in TIMESTAMP DEFAULT CURRENT_TIMESTAMP,check_out TIMESTAMP)"
        cursor.execute( query2)
    except:
        cursor.execute("use contain_information")
def checkout():
    window2=Tk() 
    window2.geometry("500x500+500+500")
    heading1 = Label(window2, text="Enter Visitor email-id", fg='blue',bg='white',font=('Arial 14 bold'))
    heading1.place(x=120,y=15)
    det= Label(window2, text="Email-id",bg='white',font=('Arial 12'))
    det.place(x=115, y=50)
    ent_det=Entry(window2 ,bd=5,width=40)
    ent_det.place(x=200, y=50)
    window2.configure(background="white")
    b1=Button(window2, text="finally checkout",bg='white',height=3,command=lambda: emailv(ent_det))
    b1.place(x=200, y=100)
def checkin():
    window1=Tk() 
    window1.geometry("500x500+300+300")
    heading = Label(window1, text="Enter Visitor Details", fg='blue',bg='white',font=('Arial 14 bold'))
    heading.place(x=115,y=15)
    det= Label(window1, text="Name",bg='white',font=('Arial 12'))
    det.place(x=115, y=50)
    ent_det=Entry(window1, bd=5,width=40)
    ent_det.place(x=175, y=50)
    det1= Label(window1, text="Email",bg='white',font=('Arial 12'))
    det1.place(x=115, y=80)
    ent_det1= Entry(window1, bd=5,width=40)
    ent_det1.place(x=175, y=80)
    det2 = Label(window1, text="Number",bg='white',font=('Arial 12'))
    det2.place(x=104, y=110)
    ent_det2 = Entry(window1, bd=5,width=40)
    ent_det2.place(x=175, y=110)
    heading1 = Label(window1, text="Enter host details", fg='blue',bg='white', font=('Arial 15 bold'))
    heading1.place(x=115, y=145)

    det3 = Label(window1, text="Name",bg='white',font=('Arial 12'))
    det3.place(x=115, y=180)
    ent_det3 = Entry(window1, bd=5,width=40)
    ent_det3.place(x=175, y=180)
    det4 = Label(window1, text="Email",bg='white',font=('Arial 12'))
    det4.place(x=115, y=210)
    ent_det4 = Entry(window1, bd=5,width=40)
    ent_det4.place(x=175, y=210)
    det5 = Label(window1, text="Number",bg='white',font=('Arial 12'))
    det5.place(x=104, y=240)
    ent_det5 = Entry(window1, bd=5,width=40)
    ent_det5.place(x=175, y=240)
    window1.configure(background="white")
    window1.title('Enter details')
    b=Button(window1, text="save_query",height=3,command=lambda: save_query(ent_det,ent_det1,ent_det2,ent_det3,ent_det4,ent_det5))
    b.place(x=140, y=280)
    b1=Button(window1, text="Back",height=3,width=10,command=window1.destroy)
    b1.place(x=230, y=280)

    window1.mainloop()
    

    #save_query(ent_det,ent_det1,ent_det2,ent_det3,ent_det4,ent_det5)
create_database()
window=Tk()
window.geometry("350x350+500+300")
img= PhotoImage(file=r"E:\IDS\tick.png")
photoimg = img.subsample(7, 7)
b=Button(window, text="Check-In",image = photoimg,compound = LEFT,command=checkin)
b.place(x=70, y=140)
img1= PhotoImage(file=r"E:\IDS\cancel.png")
photoimg1 = img1.subsample(16, 16)
btn1 = Button(window, text="Check-Out",image = photoimg1,compound = LEFT,command=checkout)
btn1.place(x=180, y=140)
window.configure(background="white")
window.title('Entry Managment System')
window.mainloop()
