import sys                                   #Dosya gönderme için
from time import gmtime, strftime, localtime #Zaman hesabı için
import time
import os.path
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
COMMASPACE = ','
from datetime import datetime, timedelta

config = open('config.txt','r')

line = config.readline()

reports = []

while line!='':
    if "[" in line:
        print ("Config Okunuyor..")
        report_name = line.split("[")[1].split("]")[0].strip()
        path = config.readline().split("=")[1].strip()
        dist_list = config.readline().split("=")[1].strip()
        dist_time = config.readline().split("=")[1].strip()
        sender_name = config.readline().split("=")[1].strip()
        smtp_adress = config.readline().split("=")[1].strip()
        smtp_port = config.readline().split("=")[1].strip()
        mail_adress = config.readline().split("=")[1].strip()
        mail_pass = config.readline().split("=")[1].strip()
        file_name= config.readline().split("=")[1].strip()
        body= config.readline().split("=")[1].strip()
        reports.append([report_name, path, dist_list, dist_time])
        print(smtp_port)
    line = config.readline()

#print reports

print ("Suanki zaman:", strftime("%a, %d %b %Y %H:%M:%S", localtime()))
now = strftime("%d %b %Y %H:%M:%S", localtime())
start_time = dist_time
now_min = int(now.split(" ")[3].split(":")[1])
now_sec = int(now.split(" ")[3].split(":")[2])
print ("Bu zamanda baslayacak:", str(start_time))
print ("Basliyor..")



# Gmail email sunucusuna bağlanıyoruz
while True:
    for report in reports:
        try:
            t = datetime.today()
            future = datetime(t.year,t.month,t.day,int(dist_time.split(":")[0]),int(dist_time.split(":")[1]))
            if t.hour >= int(dist_time.split(":")[0]):
                future += timedelta(days=1)
            print (report[2].split(","))
            print ("Beklemedeyim ", (future-t).seconds, "Saniye")
            time.sleep((future-t).seconds)


            alici = report[2].split(",")
            dongu= len(alici)
            print (dongu)
            mail = smtplib.SMTP(smtp_adress,smtp_port)
            print(mail)
            mail.ehlo()
            mail.starttls()
            mail.login(mail_adress, mail_pass)
            mesaj = MIMEMultipart()
            mesaj["From"] = sender_name + '<'+ mail_adress +'>'             # Gönderen
            mesaj["To"] = COMMASPACE.join(alici)                       # Alıcı

                            
            timestamp = datetime.strftime(datetime.now() - timedelta(1), '%Y%m%d')
            timestamp_sub = datetime.strftime(datetime.now() - timedelta(1), '%d.%m.%Y')
            mesaj["Subject"] = timestamp_sub+ " " + report[0]
            filename = path + file_name + "_" + timestamp + ".zip"
            sent_filename = file_name + "_" + timestamp + ".zip"
            body =timestamp_sub + body
            print ("Mail gonderiliyor...")
           
            mesaj.attach(MIMEText(body))
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(filename, "rb").read())
            print (filename)
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename=%s' % sent_filename)
            mesaj.attach(part)
            j=0
            while j<dongu:
                mail.sendmail(mesaj["From"], alici[j], mesaj.as_string())
                j+=1
                print("Mail başarılı bir şekilde gönderildi.")
            mail.close()
        except:
             pass
             



