from flask import Blueprint, Flask, request, jsonify, render_template,session,send_from_directory,redirect,url_for
from flask_cors import CORS
import requests
import json
import random
import string
import sqlite3
import datetime
conn_Emkay_digilocker = sqlite3.connect('Emkay_digilocker.db',check_same_thread=False)
import base64

import os
import os
import sqlite3
import pdfkit

from fpdf import FPDF
url=open("static/server.txt","r").read()
from PyPDF4 import PdfFileMerger, PdfFileReader,PdfFileWriter
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image


from reportlab.lib.units import inch

import os
check_logo = os.getcwd()+"/static/images/check.jpg"

logo = "https://www.emkayglobal.com/images/logo.png"
LOGO = logo
from wand.image import Image as wi



pdfOperationsapi = Blueprint('pdfOperationsapi', __name__)

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders

import textile
import datetime
import os.path as op


def mailsending(from_,pass_,subject,body,toadd,cc,sendgrid,files):
    def login(sendgrid):
        s = smtplib.SMTP('emkaytransact.icewarpcloud.in', 587)
        s.starttls()
        s.login('rekyc_support@emkayglobal.in','aIbrw:lq2')
        return s
    def mail(toaadr,fromaddr,subject,body,files):
        

        msg = MIMEMultipart()
        msg['From'] = fromaddr
        add=toaadr
        msg['To'] = toaadr
        msg['cc'] =cc

        qw=[toaadr,cc]

        #for f in files or []:
        for path in files:
            part = MIMEBase('application', "octet-stream")
            with open(path, 'rb') as file:
                part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment; filename="{}"'.format(op.basename(path)))
            msg.attach(part)

        #smtp = smtplib.SMTP(server, port)
        
        body = body
        msg['Subject']=subject
        msg.attach(MIMEText(body,'html'))
        text = msg.as_string()
        s =login(sendgrid)
        
        s.sendmail(fromaddr, qw, text)
            
        print("new login")

        
    try :
        mail(toadd,from_,subject,body,files)
    except Exception as e:
        pass
        print(e)




def mailsendingSingleFile(from_,pass_,subject,body,toadd,cc,sendgrid,files):
    def login(sendgrid):
        s = smtplib.SMTP('emkaytransact.icewarpcloud.in', 587)
        s.starttls()
        s.login('rekyc_support@emkayglobal.in','aIbrw:lq2')
        return s
    def mail(toaadr,fromaddr,subject,body,files):
        

        msg = MIMEMultipart()
        msg['From'] = fromaddr
        add=toaadr
        msg['To'] = toaadr
        msg['cc'] =cc

        qw=[toaadr,cc]

        #for f in files or []:
        #for path in files:
        part = MIMEBase('application', "octet-stream")
        with open(files, 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachment; filename="{}"'.format(op.basename(files)))
        msg.attach(part)

        #smtp = smtplib.SMTP(server, port)
        
        body = body
        msg['Subject']=subject
        msg.attach(MIMEText(body,'html'))
        text = msg.as_string()
        s =login(sendgrid)
        
        s.sendmail(fromaddr, qw, text)
            
        print("new login")

        
    try :
        mail(toadd,from_,subject,body,files)
    except Exception as e:
        pass
        print(e)






@pdfOperationsapi.route("/test_pdf/<clientcode>")
def Consent_pdf(clientcode):
    data=conn_Emkay_digilocker.execute('SELECT * FROM userdetails WHERE clientcode = "'+clientcode+'"').fetchall()
       
    # stampimgpath=path

    name             =str(data[0][2]).upper()
    dpid=str(data[0][23])
    esign1="E-signed by:"+name
    esign2="Date:"+str(datetime.datetime.now())
    esign3="Reason: Rekyc/Modification"

    packet = io.BytesIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFontSize(10)
    can.drawString(90,695,name)
    can.drawString(280,670,dpid[-8:])
    can.drawString(150,655,clientcode)
    can.setFontSize(7)
    can.drawString(450,70,esign1)
    can.drawString(450,60,esign2)
    can.drawString(450,50,esign3)
    can.setFontSize(10)
    can.save()
    #move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(open("Consent for Digital Statement.pdf", "rb"))
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    # finally, write "output" to a real file
    outputStream = open("static/rekycPDF/"+str(clientcode)+"/Consent for Digital Statement.pdf", "wb")
    output.write(outputStream)
    outputStream.close()
    return "static/rekycPDF/"+str(clientcode)+"/Consent for Digital Statement.pdf"


def nomineePdf(clientcode):
    data=conn_Emkay_digilocker.execute('SELECT * FROM userdetails WHERE clientcode = "'+clientcode+'"').fetchall()

    clientcode=data[0][1]
    name             = str(data[0][2])
    pan=str(data[0][3])
    #nominee details 
    dp_id=str(data[0][23])
    permanent_add_1   = str(data[0][13])
    permanent_add_2   = str(data[0][14])
    print(dp_id)
    # 1st NOMINEE FORM FOR TRANDING ACCOUNT 

    name_of_nom1    = str(data[0][123])
    pan_of_nom1     = str(data[0][128])
    dob_nom1        = str(data[0][126])
    rel_with_bo1    = str(data[0][135])
    nom1_gender = str(data[0][127])

    # ADDRESS OF NOMINEE1

    nom1_add_1     = str(data[0][129])
    nom1_add_2     = str(data[0][130])
    nom1_add_3     = ''
    nom1_city_town = str(data[0][134])
    nom1_country   = str(data[0][132])
    nom1_state     = str(data[0][133])
    nom1_phone     = str(data[0][125])
    nom1_pin_code  = str(data[0][131])
    nom1_email     = str(data[0][124])
    percent_feild1 = str(data[0][137])
    # 2nd NOMINEE FORM FOR TRANDING ACCOUNT 

    name_of_nom2    = str(data[0][138])
    pan_of_nom2     = str(data[0][143])
    dob_nom2        = str(data[0][141])
    rel_with_bo2    = str(data[0][150])
    nom2_gender = str(data[0][142])
    # ADDRESS OF NOMINEE2

    nom2_add_1     = str(data[0][144])
    nom2_add_2     = str(data[0][145])
    nom2_add_3     = ''
    nom2_city_town = str(data[0][149])
    nom2_country   = str(data[0][147])
    nom2_state     = str(data[0][148])
    nom2_phone     = str(data[0][140])
    nom2_pin_code  = str(data[0][146])
    nom2_email     = str(data[0][139])
    percent_feild2 = str(data[0][152])
    # 3rd NOMINEE FORM FOR TRANDING ACCOUNT 

    name_of_nom3    =  str(data[0][153])
    pan_of_nom3     =  str(data[0][158])
    dob_nom3        =  str(data[0][156])
    rel_with_bo3    =  str(data[0][165])
    nom3_gender = str(data[0][157])
    # ADDRESS OF NOMINEE2

    nom3_add_1     =  str(data[0][159])
    nom3_add_2     =  str(data[0][160])
    nom3_add_3     = ''
    nom3_city_town =  str(data[0][164])
    nom3_country   =  str(data[0][162])
    nom3_state     =  str(data[0][163])
    nom3_phone     =  str(data[0][155])
    nom3_pin_code  =  str(data[0][161])
    nom3_email     =  str(data[0][154])
    percent_feild3 = str(data[0][167])
    #documnet_type
    nom_doc_type = str(data[0][136])
    #esign
    esign1=""
    esign2=""
    esign3=""
    #upload document
    nom1_upload_documnet=data[0][202]
    nom2_upload_documnnet=data[0][203]
    nom3_upload_documnnet=data[0][204]

    segment         = data[0][8]

    ##########################################################   Guardian        #####################################################################
    Guardian_name=str(data[0][169])
    Guardian_dob=str(data[0][170])
    Guardian_address=str(data[0][171])
    Guardian_city=str(data[0][172])
    Guardian_state=str(data[0][173])
    Guardian_country=str(data[0][174])
    Guardian_mobile=str(data[0][175])
    Guardian_email=str(data[0][176])
    Guardian_relation=str(data[0][177])
    Guardian_doc_type=str(data[0][178])
    Guardian_pincode=str(data[0][179])
    ################################Guardian2 #########################
    Guardian_name2=str(data[0][180])
    Guardian_dob2=str(data[0][181])
    Guardian_address2=str(data[0][182])
    Guardian_city2=str(data[0][183])
    Guardian_state2=str(data[0][184])
    Guardian_country2=str(data[0][185])
    Guardian_mobile2=str(data[0][186])
    Guardian_email2=str(data[0][187])
    Guardian_relation2=str(data[0][188])
    Guardian_doc_type2=str(data[0][189])
    Guardian_pincode2=str(data[0][190])
    ##########################################Guardian3 #######################################
    Guardian_name3=str(data[0][191])
    Guardian_dob3=str(data[0][192])
    Guardian_address3=str(data[0][193])
    Guardian_city3=str(data[0][194])
    Guardian_state3=str(data[0][195])
    Guardian_country3=str(data[0][196])
    Guardian_mobile3=str(data[0][197])
    Guardian_email3=str(data[0][198])
    Guardian_relation3=str(data[0][199])
    Guardian_doc_type3=str(data[0][200])
    Guardian_pincode3=str(data[0][201])

    mergedObject = PdfFileMerger()
    current_date = datetime.datetime.now().strftime("%d-%m-%Y")
    current_date_d = datetime.datetime.now().strftime("%d%m %Y")

    for i in range(2):
        # if i != 1:
        #   continue
        print(i)
        packet = io.BytesIO()
        # create a new PDF with Reportlab
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFontSize(10) 

        if i==0:
            can.drawString(240,647,name)
            can.drawString(230,630,permanent_add_1)
            can.drawString(230,620,permanent_add_2)
            can.drawString(143,577,current_date.replace('-',''),charSpace=9)
            can.drawString(460,577,dp_id[8:],charSpace=6)
            #nominee 1
            can.setFontSize(8)
            can.drawString(227,440,name_of_nom1)
            can.setFontSize(10)
            can.drawString(250,410,percent_feild1)
            can.drawString(227,360,rel_with_bo1)
            can.setFontSize(7)
            can.drawString(227,340,nom1_add_1[:26])
            can.drawString(227,332,nom1_add_1[26:])
            can.drawString(227,323,nom1_add_2[:26])
            can.drawString(227,314,nom1_add_2[26:])
            can.setFontSize(8)
            can.drawString(227,304,nom1_city_town)
            can.drawString(227,295,nom1_state+' & '+nom1_country)
            can.setFontSize(10)
            can.drawString(280,280,nom1_pin_code)
            can.drawString(227,260,nom1_phone)
            can.setFontSize(6)
            can.drawString(227,240,nom1_email)
            can.setFontSize(10)
            #nominee doc
            if 'Pan' in nom_doc_type:
                can.drawString(195,175,"✓")
            elif 'Aadhaar' in nom_doc_type:
                can.drawString(97,160,"✓")
                #can.drawString(145,210,"✓")
            elif 'Bank_proof' in nom_doc_type:
                can.drawString(140,160,"✓")
            else:
                can.drawString(143,245," ") 
            #nominee 2
            can.setFontSize(8)
            can.drawString(350,440,name_of_nom2)
            can.setFontSize(10)
            can.drawString(380,410,percent_feild2)
            can.drawString(367,360,rel_with_bo2)
            can.setFontSize(7)
            can.drawString(350,340,nom2_add_1[:26])
            can.drawString(350,332,nom2_add_1[26:])
            can.drawString(350,323,nom2_add_2[:26])
            can.drawString(350,314,nom2_add_2[26:])
            can.setFontSize(8)
            can.drawString(350,304,nom2_city_town)
            can.drawString(350,295,nom2_state+' & '+nom2_country)
            can.setFontSize(10)
            can.drawString(410,280,nom2_pin_code)
            can.drawString(350,260,nom2_phone)
            can.setFontSize(6)
            can.drawString(350,240,nom2_email)
            can.setFontSize(10)
            #nominee 3
            can.setFontSize(8)
            can.drawString(460,440,name_of_nom3)
            can.setFontSize(10)
            can.drawString(480,410,percent_feild3)
            can.drawString(460,360,rel_with_bo3)
            can.setFontSize(7)
            can.drawString(460,340,nom3_add_1[:26])
            can.drawString(460,332,nom3_add_1[26:])
            can.drawString(460,323,nom3_add_2[:26])
            can.drawString(460,314,nom3_add_2[26:])
            can.setFontSize(8)
            can.drawString(460,304,nom3_city_town)
            can.drawString(460,295,nom3_state+' & '+nom2_country)
            can.setFontSize(10)
            can.drawString(510,280,nom3_pin_code)
            can.drawString(460,260,nom3_phone)
            can.setFontSize(6)
            can.drawString(460,240,nom3_email)
            can.setFontSize(10)
            #gaudian1
            can.setFontSize(10)
            can.drawString(227,93,Guardian_dob)
            can.setFontSize(10)
            can.drawString(227,74,Guardian_name)
            #gaudian2
            can.setFontSize(10)
            can.drawString(350,93,Guardian_dob2)
            can.setFontSize(10)
            can.drawString(350,74,Guardian_name2)
            ##gaudian2
            can.setFontSize(10)
            can.drawString(460,93,Guardian_dob3)
            can.setFontSize(10)
            can.drawString(460,74,Guardian_name3)

        if i==1:    
            can.setFontSize(7)
            can.drawString(227,760,Guardian_address[:26])
            can.drawString(227,752,Guardian_address[26:])
            can.setFontSize(8)
            can.drawString(227,730,Guardian_city)
            can.drawString(227,720,Guardian_state+' & '+Guardian_country)
            can.setFontSize(10)
            can.drawString(284,696,Guardian_pincode)
            can.drawString(227,660,Guardian_mobile)
            can.setFontSize(6)
            can.drawString(227,640,Guardian_email)
            can.setFontSize(10)
            can.drawString(227,610,Guardian_relation)
            if 'pan' in Guardian_doc_type:
                can.drawString(100,510,"✓")
                #can.drawString(130,510,"✓")
            elif 'Aadhaar' in Guardian_doc_type:
                can.drawString(130,510,"✓")
            #2gaurdian
            can.setFontSize(7)
            can.drawString(350,760,Guardian_address2[:26])
            can.drawString(350,752,Guardian_address2[26:])
            can.setFontSize(8)
            can.drawString(350,730,Guardian_city2)
            can.drawString(350,720,Guardian_state2+' & '+Guardian_country2)
            can.setFontSize(10)
            can.drawString(404,696,Guardian_pincode2)
            can.drawString(350,660,Guardian_mobile2)
            can.setFontSize(6)
            can.drawString(350,640,Guardian_email2)
            can.setFontSize(10)
            can.drawString(350,610,Guardian_relation2)
            #3gaurdian
            can.setFontSize(7)
            can.drawString(460,760,Guardian_address3[:26])
            can.drawString(460,752,Guardian_address3[26:])
            can.setFontSize(8)
            can.drawString(460,730,Guardian_city3)
            can.drawString(460,720,Guardian_state3+' & '+Guardian_country3)
            can.setFontSize(10)
            can.drawString(510,696,Guardian_pincode3)
            can.drawString(460,660,Guardian_mobile3)
            can.setFontSize(6)
            can.drawString(460,640,Guardian_email3)
            can.setFontSize(10)
            can.drawString(460,610,Guardian_relation3)
            ######################
            can.setFontSize(7)
            can.drawString(227,440,name)
            can.drawString(456,440,esign1)
            can.drawString(456,430,esign2)
            can.drawString(456,422,esign3) 

            

        can.save()
        #move to the beginning of the StringIO buffer
        packet.seek(0)
        new_pdf = PdfFileReader(packet)
        # read your existing PDF
        existing_pdf = PdfFileReader(open("NOMINATION FORM (1).pdf", "rb"))
        output = PdfFileWriter()
        # add the "watermark" (which is the new pdf) on the existing page
        page = existing_pdf.getPage(i)
        page.mergePage(new_pdf.getPage(0))
        output.addPage(page)
        # finally, write "output" to a real file
        outputStream = open("static/rekycPDF/"+str(clientcode)+"/destination"+str(i)+".pdf", "wb")
        output.write(outputStream)
        outputStream.close()
        mergedObject.append(PdfFileReader("static/rekycPDF/"+str(clientcode)+"/destination"+str(i)+".pdf", "rb"), import_bookmarks=False)


    try:
        os.remove("static/rekycPDF/"+str(clientcode)+"/nomineePdf.pdf")
    except:
        pass
        #pdf_FILE_name=get_random_string(6)  
    mergedObject.write("static/rekycPDF/"+clientcode+"/nomineePdf.pdf")
    return "static/rekycPDF/"+clientcode+"/nomineePdf.pdf"



def DeclarationPdf(clientcode):
    data=conn_Emkay_digilocker.execute('SELECT * FROM userdetails WHERE clientcode = "'+clientcode+'"').fetchall()

    clientcode=data[0][1]
    name             = data[0][2]
    if "W/O" in name or "S/O" in name or "F/O" in name:
        name=name.split(" ")
        try:
            name=name[1]+" "+name[2]+" "+name[3]
        except:
            name=name[1]+" "+name[2]
    # father_name      = str(data[0][51]
    # mother_name      =str(data[0][5])
    # dob              = str(data[0][49])
    # pan             = str(data[0][3])
    # gender           = str(data[0][50])
    # print(gender)
    # country           = str(data[0][55])
    # city            = data[0][53]
    # state         = data[0][54]
    # country           = data[0][55]
    # pin_code      = data[0][63]
    # permanent_add_1 = data[0][52]
    # permanent_add_2 = data[0][62]
    # email         = data[0][7]
    # marital_status   = data[0][61]
    # print(marital_status)
    # date_d       = data[0][32]
    # date_time = datetime.datetime.fromisoformat(str(date_d))
    # date_d=date_time.strftime("%d-%m-%Y")

    # gross_anu_income   = data[0][37]
    # occupation    = data[0][39]
    # print(occupation)
    # bank_name     = data[0][40]
    # bank_acc_no   = data[0][45]
    # branch        = data[0][43]
    # ifsc          = data[0][41]
    # micr          = data[0][42]
    # bank_address  = data[0][44]
    # account_type  = data[0][13]

    # segment         = data[0][8]
    # #dp_id
    dp_id=str(data[0][23])
    esign1="E-signed by:"+name
    esign2="Date:"+str(datetime.datetime.now())
    esign3="Reason: Re-KYC"

    mergedObject = PdfFileMerger()
    current_date = datetime.datetime.now().strftime("%d-%m-%Y")
    current_date_d = datetime.datetime.now().strftime("%d%m %Y")

    for i in range(1):
        if i != 0:
            continue
        print(i)
        packet = io.BytesIO()
        # create a new PDF with Reportlab
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFontSize(10) 

        if i==0:
            can.drawString(320,610,current_date.replace('-',''),charSpace=25)
            can.drawString(320,480,dp_id[8:],charSpace=25)
            can.drawString(280,450,name)
            can.setFontSize(7)
            can.drawString(450,280,esign1)
            can.drawString(450,270,esign2)
            can.drawString(450,260,esign3)
            can.setFontSize(10)
            can.drawString(190,270,name)
            

        can.save()
        #move to the beginning of the StringIO buffer
        packet.seek(0)
        new_pdf = PdfFileReader(packet)
        # read your existing PDF
        existing_pdf = PdfFileReader(open("Opt_out.pdf", "rb"))
        output = PdfFileWriter()
        # add the "watermark" (which is the new pdf) on the existing page
        page = existing_pdf.getPage(i)
        page.mergePage(new_pdf.getPage(0))
        output.addPage(page)
        # finally, write "output" to a real file
        outputStream = open("static/rekycPDF/"+str(clientcode)+"/destination"+str(i)+".pdf", "wb")
        output.write(outputStream)
        outputStream.close()
        mergedObject.append(PdfFileReader("static/rekycPDF/"+str(clientcode)+"/destination"+str(i)+".pdf", "rb"), import_bookmarks=False)



    try:
        os.remove("static/rekycPDF/"+str(clientcode)+"/DeclarationPdf.pdf")
    except:
        pass
        #pdf_FILE_name=get_random_string(6)  
    mergedObject.write("static/rekycPDF/"+clientcode+"/DeclarationPdf.pdf")
    return "static/rekycPDF/"+clientcode+"/DeclarationPdf.pdf"


#@pdfOperationsapi.route('/rekycPDFmail/<clientcode>', methods=['POST'])
def rekycPDFmail(clientcode):
    clientcode=clientcode.lower()

    
    emails=conn_Emkay_digilocker.execute('SELECT email,clientimage FROM userdetails WHERE clientcode = "'+clientcode+'"').fetchall()
    email=emails[0][0]
    
    text='please click on this link to esign <a href="'+url+'requestesignemail/rekycPDF/rekycam/'+clientcode+'" style="background: #0067ab; outline: none; color: #fff; font-size: 13px; border: 1px solid #0067ab; padding: .50rem .75rem; letter-spacing: 1px; text-transform: uppercase;">Esign</a>'
    body='''<html>
                <head>
                  <title></title>
                </head>
                <body>
                  <div style="background-color:#f0f1f3;font-family:'Helvetica Neue','Segoe UI',sans-serif;font-size:16px;line-height:28px;margin:0;color:#444;">
                    <div class="m_2513597272243517713gutter" style="padding:5px 0;">&nbsp;</div>
                    <div class="m_2513597272243517713root" style="margin:0 20px;">
                      <table class="m_2513597272243517713header" style="max-width:600px;margin:0 auto 5px auto;width:100%;">
                        <tbody>
                            <tr>
                              <td align="center" colspan="2">
                                <a href="" style="color:#387ed1;" target="_blank">
                                  <img alt="LOGO" src="https://www.emkayglobal.com/images/logo.png" style="width: 30%;">
                                </a>
                              </td>
                            </tr>
                        </tbody>
                      </table>
                      <div class="m_2513597272243517713wrap" style="background-color:#fff;padding:30px;max-width:600px;margin:0 auto;border-radius:5px;">
                      '''+text+'''
                       
                            
                        </div>
                        <p>In case of any issue please raise a ticket at rekyc_support@emkayglobal.in</p>
                      <div class="m_2513597272243517713footer" style="text-align:center;color:#888;font-size:11px;">
                        
                </body>
                </html>'''

    #chk=conn_trustline_digilocker.execute('SELECT addresschangeyesno FROM userdetails WHERE clientcode = "'+clientcode+'"').fetchall()
    # if chk[0][0]=='no':
    #   print('nooooooo',"static/rekycPDF/"+clientcode+"/rekycam.pdf",email)
    #   mailsendingSingleFile("rekyc_support@emkayglobal.in",'',"ReKyc E-sign Process",body,email,'shyam@meon.co.in',"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","static/rekycPDF/"+clientcode+"/rekycam.pdf")
    #   return jsonify({'msg':'Single PDF Sent'})


    conn_Emkay_digilocker.execute("UPDATE userdetails SET email_time_after_esign='"+str(datetime.datetime.now())+"' where clientcode = '"+clientcode+"'")
    conn_Emkay_digilocker.commit()
    print(emails)
    if emails[0][1] == None or emails[0][1] =="":
        mailsending("rekyc_support@emkayglobal.in",'',"ReKyc E-sign Process",body,email,'',"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",["static/rekycPDF/"+clientcode+"/rekycam.pdf"])

    else:
        mailsending("rekyc_support@emkayglobal.in",'',"ReKyc E-sign Process",body,email,'',"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",["static/rekycPDF/"+clientcode+"/rekycam.pdf","static/rekycPDF/"+clientcode+"/rekykra.pdf"])

    return jsonify({'msg':'Mail Sent'})





@pdfOperationsapi.route('/rekycpdf_signed/<clientcode>', methods=['GET','POST'])
def accountmodification(clientcode):
    clientcode=clientcode.lower()
    original_clientcode=clientcode
    data=conn_Emkay_digilocker.execute('SELECT * FROM userdetails WHERE clientcode = "'+clientcode+'"').fetchall()
    clientcode=clientcode.split('-')[0]

    emailchangeyesno =    str(data[0][75]).lower()
    mobilechangeyesno=    str(data[0][76]).lower()
    if data[0][102]=="Active":
        acctype = 'Annual Income Updation'
    else:
        acctype = 'Account Reactivation'

    if emailchangeyesno.lower()=='yes' or mobilechangeyesno.lower()=='yes':
        em,acctype = '<img src="https://ipout.emkayglobal.com/static/images/check.jpg" alt="" style="width: 18px;height: 18px">','Account Modification' 
    else: 
        em =''
    if str(data[0][77]).lower()=='yes':
        addresschangeyesno,acctype =   '<img src="https://ipout.emkayglobal.com/static/images/check.jpg" alt="" style="width: 18px;height: 18px">','Account Modification' 
    else: 
        addresschangeyesno = ''
    if str(data[0][79]).lower()=='yes':
        bankchangeyesno,acctype  =    '<img src="https://ipout.emkayglobal.com/static/images/check.jpg" alt="" style="width: 18px;height: 18px">','Account Modification' 
    else:
        bankchangeyesno  =  ''
    if str(data[0][78]).lower()=='yes':
        segmentactivationyesno,acctype = '<img src="https://ipout.emkayglobal.com/static/images/check.jpg" alt="" style="width: 18px;height: 18px">','Account Modification'
    else:
        segmentactivationyesno =''

    segment_selected = str(data[0][89])if str(data[0][89]).split(',') !='None' else''
    bse_cash, bse_fo, bse_curr, bse_comm, bse_slb, nse_cash, nse_fo, nse_curr, nse_comm, nse_slb, bse_mf,mcx,ncdex = '','','','','','','','','','','','',''
    # for i in segment_selected:
    if 'true' in segment_selected[0]:
        bse_cash = '<img src="https://i.ibb.co/NpRRQvx/check.png" alt="" style="width: 18px;height: 18px">'
    if 'true' in segment_selected[1]:
        bse_fo = '<img src="https://i.ibb.co/NpRRQvx/check.png" alt="" style="width: 18px;height: 18px">'
    if 'true' in segment_selected[2]:
        bse_curr = '<img src="https://i.ibb.co/NpRRQvx/check.png" alt="" style="width: 18px;height: 18px">'
    if 'true' in segment_selected[3]:
        bse_comm = '<img src="https://i.ibb.co/NpRRQvx/check.png" alt="" style="width: 18px;height: 18px">'
    if 'true' in segment_selected[4]:
        bse_slb = '<img src="https://i.ibb.co/NpRRQvx/check.png" alt="" style="width: 18px;height: 18px">'
    if 'true' in segment_selected[5]:
        bse_mf = '<img src="https://i.ibb.co/NpRRQvx/check.png" alt="" style="width: 18px;height: 18px">'
    if 'true' in segment_selected[6]:
        nse_cash = '<img src="https://i.ibb.co/NpRRQvx/check.png" alt="" style="width: 18px;height: 18px">'
    if 'true' in segment_selected[7]:
        nse_fo = '<img src="https://i.ibb.co/NpRRQvx/check.png" alt="" style="width: 18px;height: 18px">'
    if 'true' in segment_selected[8]:
        nse_curr = '<img src="https://i.ibb.co/NpRRQvx/check.png" alt="" style="width: 18px;height: 18px">'
    if 'true' in segment_selected[9]:
        nse_comm = '<img src="https://i.ibb.co/NpRRQvx/check.png" alt="" style="width: 18px;height: 18px">'
    if 'true' in segment_selected[10]:
        nse_slb = '<img src="https://i.ibb.co/NpRRQvx/check.png" alt="" style="width: 18px;height: 18px">'
    if 'true' in segment_selected[11]:
        mcx = '<img src="https://i.ibb.co/NpRRQvx/check.png" alt="" style="width: 18px;height: 18px">'
    if 'true' in segment_selected[12]:
        ncdex = '<img src="https://i.ibb.co/NpRRQvx/check.png" alt="" style="width: 18px;height: 18px">'

    new_bank_type= str(data[0][85])
    new_bank_saving=''
    new_bank_current=''
    
    if 'Saving' in new_bank_type:
        new_bank_saving = '<img src="https://ipout.emkayglobal.com/static/images/check.jpg" alt="" style="width: 18px;height: 18px">'
    else:
        pass
    if 'Current' in new_bank_type:
        new_bank_current = '<img src="https://ipout.emkayglobal.com/static/images/check.jpg" alt="" style="width: 18px;height: 18px">'
    else:
        pass

    if len(data[0][8])==8:
        com = '<img src="https://ipout.emkayglobal.com/static/images/check.jpg" alt="" style="width: 18px;height: 18px">'
    else:
        com=""
    updation_annual_income='<img src="https://ipout.emkayglobal.com/static/images/check.jpg" alt="" style="width: 18px;height: 18px">' if str(data[0][90]) !='' else ''
    #commodity_clients='<img src="https://ipout.emkayglobal.com/static/images/check.jpg" alt="" style="width: 18px;height: 18px">' if str(data[0][8][5])=='Y' else ''
    #old_cash='<img src="https://ipout.emkayglobal.com/static/images/check.jpg" alt="" style="width: 18px;height: 18px">' + 'CASH' if str(data[0][8][1])=='Y' else ''
    #old_currency='<img src="https://ipout.emkayglobal.com/static/images/check.jpg" alt="" style="width: 18px;height: 18px">' + 'CURRENCY' if str(data[0][8][3])=='Y' else ''
    #old_fo='<img src="https://ipout.emkayglobal.com/static/images/check.jpg" alt="" style="width: 18px;height: 18px">' + 'F&O' if str(data[0][8][5])=='Y' else ''

    dp_id          =       str(data[0][23])
    client_id      =       str(data[0][1])
    name_first_ho  =       str(data[0][2])
    sign_of_holder =       "E-signed by:"+data[0][2]+" <br>Date: "+str(datetime.datetime.now())+"<br> Reason: Rekyc/Modification "
    sign =       "E-signed by:"+data[0][2]+" <br>Date: "+str(datetime.datetime.now())+"<br> Reason: Rekyc/Modification "

    name_sec_ho    =       ''
    sign_sec       =       ''
    name_third_ho  =       ''
    sign_third     =       ''
    # old_add_line1  =       str(data[0][13])
    # old_add_line2  =       str(data[0][14])
    # old_city       =       str(data[0][18])
    # old_state      =       str(data[0][17])
    # old_pincode    =       str(data[0][19])
    # na1  =                 str(data[0][52]) if str(data[0][52]) !='None' else ''
    # na2  =                 str(data[0][64]) if str(data[0][64]) !='None' else ''
    # new_city       =       str(data[0][53]) if str(data[0][53]) !='None' else ''
    new_annual_income=       str(data[0][90]) if str(data[0][90]) !='None' else ''
    # new_pincode    =       str(data[0][65]) if str(data[0][65]) !='None' else ''
    # new_state = str(data[0][54]) if str(data[0][54]) !='None' else ''
    #print(new_state)
    bank_name_old  =       str(data[0][40])
    account_no_old =       str(data[0][45])
    ifsc_code_old  =       str(data[0][41])
    micr_old       =       ""
    branch_name_old =      ""
    pincode_old_bank =     ''#str(data[0][85])
    city_old_bank    =     ""
    bank_name_new    =     str(data[0][70]) if str(data[0][70]) !='None' else ''
    account_no_new   =     data[0][74] if str(data[0][74]) !='None' else ''
    ifsc_code_new    =     data[0][71] if str(data[0][71]) !='None' else ''
    micr_new         =     str(data[0][82]) if str(data[0][82]) !='None' else ''
    branch_name_new  =     str(data[0][72]) if str(data[0][71]) !='None' else ''
    #pincode_new_bank =     str(data[0][86]) if str(data[0][87]) !=None else ''
    #city_new_bank    =     str(data[0][84])
    old_mob_no       =     str(data[0][6])
    #old_landline_no  =     str(data[0][91])
    old_email        =     str(data[0][7])
    new_mob_no       =     str(data[0][34]) if str(data[0][34]) !='None' else ''
    #new_landline_no  =     str(data[0][92])
    new_email        =     str(data[0][33]) if str(data[0][33]) !='None' else ''
    #aadhaar_first_ho =     str(data[0][93])
    aadhaar_sec_ho   =     ''
    aadhaar_third_ho =     ''
    #old_gross_income =     str(data[0][94])
    #old_net_worth    =     str(data[0][98])
    #old_date         =     str(data[0][96])
    #new_gross_income =     str(data[0][95])
    old_annual_income    =     str(data[0][20]) if str(data[0][20]) !='None' else ''
    old_date         =      str(datetime.datetime.now()).split(" ")[0]
    print(old_date)
    datetimeobject = datetime.datetime.strptime(old_date,'%Y-%m-%d')
    new_date = datetimeobject.strftime('%d-%m-%Y')

    new_add_line1    =     ''
    new_add_line2    =     ''
    mobile_dependency = data[0][112]
    email_dependency = data[0][209]
    if str(data[0][77]).lower()=='yes':
        old_add_line1  =       str(data[0][13])
        old_add_line2  =       str(data[0][14])
        old_city       =       str(data[0][18])
        old_state      =       str(data[0][17])
        old_pincode    =       str(data[0][19])
        na1  =                 str(data[0][52]) if str(data[0][52]) !='None' else ''
        na2  =                 str(data[0][64]) if str(data[0][64]) !='None' else ''
        new_city       =       str(data[0][53]) if str(data[0][53]) !='None' else ''
        new_pincode    =       str(data[0][65]) if str(data[0][65]) !='None' else ''
        new_state = str(data[0][54]) if str(data[0][54]) !='None' else ''
    else:
        old_add_line1  =''
        old_add_line2  = ''
        old_city       =  ''
        old_state      = ''
        old_pincode    =''
        na1  = ''
        na2  =''
        new_city       =''
        new_pincode    = ''
        new_state = ''



    html = ''' <!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
    <style>
        .input {
            padding: 6px 12px;
            outline: none;
            line-height: 1.5;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.075);
            margin: 5px 10px 5px 0px;
            width: 90%
        }

        .page-break {

        page-break-before: always;

        }

        .holder {
            margin-left: 50%;
            width: 150%;
        }

        
    </style>
</head>

<body>
    <div style="width:90%;border:20px solid #b3e7f2;margin:auto;">
        <div style="padding: 15px;">
            <img src='''+LOGO+''' alt="Emkay-logo" style="width:50%" />
        </div>
        <div style="padding: 15px;">
            <p style="text-align: center; font-size: 30px; margin: 0px;"> '''+acctype+''' </p><hr>
            <b>To,</b><br />
            <b style="margin-right:50px;">Emkay Global Financial Services Ltd.</b><br />
            <p>
               C-06 Ground Floor, Paragon Centre, Pandurang Bhudhkar Marg, Worli, Mumbai- 400 013.
            </p>
            <b style="line-height: 1.5rem;">Account Detail (s) Addition/Modification Request Form</b>
            <label
                style="display: inline-flex;position: relative;padding-left: 35px;margin: 0 0 12px 12px;cursor:pointer;font-size: 14px;text-align: justify;">DP
                <img src="'''+str(check_logo)+'''" alt="" style="width: 18px;height: 18px">

                <label
                    style="display: inline-flex;position: relative;padding-left: 35px;margin: 0 0 12px 12px;cursor:pointer;font-size: 14px;text-align: justify;">TRADING
                    <img src="'''+str(check_logo)+'''" alt="" style="width: 18px;height: 18px">
                </label>
        </div>
        <div style="padding: 15px">

            <tr>
                <td><b>BO ID</b></td>
                <td style="width: 50%"> <input type="text" name="" class="input" value=" '''+str(dp_id)+''' "
                        style="width: 30%" /> </td>
            </tr>
            <tr>
                <td> <b>UCC CODE</b></td>
                <td style="width: 50%"> <input type="text" name="" class="input"
                        value=" '''+str(clientcode).upper()+''' " style="width: 30%" /></td>
            </tr>
        </div>
        <div style="padding: 15px;">
            <tr>
                <td>
                    <b>Account Type:-</b></td>
                <td><label><img src="'''+str(check_logo)+'''" alt="" style="width: 18px;height: 18px">
                        Individual</label></td>
                <td><label><input type="checkbox" id="corpo_check" /> Corporate</label></td>
                <td><label><input type="checkbox" id="nri_check" /> NRI</label></td>
                <td><label><input type="checkbox" id="nro_check" /> NRO</label></td>
            </tr>
        </div>
        <div style="padding: 15px;">
            <table>
                <th>Account Holder's Details</th>
                <tr>
                    <td>Name of First/ Sole Holder</td>
                    <td><input type="text" name="" class="input holder" value=" '''+str(name_first_ho)+''' " /></td>
                </tr>
                <tr>
                    <td>Name of Second Holder</td>
                    <td><input type="text" name="" class="input holder" value=" '''+str(name_sec_ho)+''' " /></td>
                </tr>
                <tr>
                    <td>Name of Third Holder</td>
                    <td><input type="text" name="" class="input holder" value=" '''+str(name_third_ho)+''' " /></td>
                </tr>
            </table>
        </div>

        <div style="width: 98%;height: 1px;margin: auto;background: #ccc;margin-bottom: 12px;"></div>
        <div style="padding: 15px;">
            <div style="line-height: 0.5rem;">
                <b>Dear Sir/ Madam,</b>
                <p style="line-height: 15px;">
                    I/we hereby request you to make the following details Addition
                    /Modification to my/our Account in your record.
                </p>
            </div>
        </div>
        <!--Permanent Address-->
        <div style="margin-bottom:12px;text-align: center;background-color:#b3e7f2;padding: 10px 0;margin:0 15px;">
            <tr>
                '''+str(addresschangeyesno)+'''
                <b>Change of Permanent Address</b>
            </tr>
        </div>

        <div style="padding:15px">
            <table style="margin: 0;margin-left: 20px;width: 100%">
                <tr>
                    <th>Old Address Details</th>
                    <th>New Address Details</th>
                </tr>

                <tr>
                    <td> <input style="margin:0;" type="text" id="oldcor_address1" placeholder="Address Line 1" class="input"
                            value=" '''+str(old_add_line1)+''' "  /></td>
                    <td><input style="margin:0;" type="text" d="newcor_address2" placeholder="Address Line 2" class="input"
                            value=" '''+str(na1)+''' " /></td>
                </tr>
                <tr>
                    <td><input style="margin:0;" type="text" d="oldcor_address2" placeholder="Address Line 2" class="input"
                            value=" '''+str(old_add_line2)+''' "  /></td>
                    <td><input style="margin:0;" type="text" d="newcor_address2" placeholder="Address Line 2" class="input"
                            value=" '''+str(na2)+''' " /></td>
                </tr>
                <tr>
                    <td><input style="margin:0;"  type="text" id="oldcor_inputCity" placeholder="City" class="input"
                            value=" '''+str(old_city)+''' "  /></td>
                    <td><input style="margin:0;" type="text" id="newcor_inputCity" placeholder="City" class="input"
                            value=" '''+str(new_city)+''' " /></td>
                </tr>
                <tr>
                    <td><input style="margin:0;" type="text" id="oldcor_inputState" placeholder="State" class="input"
                            value="'''+str(old_state)+'''"  /></td>
                    <td><input style="margin:0;" type="text" id="newcor_inputState" placeholder="State" class="input"
                            value="'''+str(new_state)+'''" /></td>
                </tr>
                <tr>
                    <td><input style="margin:0;" type="text" id="oldcor_inputPincode" placeholder="Pincode" class="input"
                            value="'''+str(old_pincode)+'''" /> </td>
                    <td><input style="margin:0;" type="text" id="oldcor_inputPincode" placeholder="Pincode" class="input"
                            value="'''+str(new_pincode)+'''" /> </td>
                </tr>
            </table>
        </div>
        
    </div>
    <div style="width:90%;border:20px solid #b3e7f2;margin:12px auto;"  class="page-break">
        <!--correspondence Address-->
        <div style="margin-bottom:12px;text-align: center;background-color:#b3e7f2;padding: 10px 0;margin:15px 15px;">
            <tr>
                '''+str(addresschangeyesno)+'''
                <b>Change of Correspondence Address</b>
            </tr>
        </div>
        <div style="padding:15px">
            <table style="margin: 0;margin-left: 20px;width: 100%">
                <tr>
                    <th>Old Address Details</th>
                    <th>New Address Details</th>
                </tr>

                <tr>
                    <td> <input type="text" id="oldcor_address1" placeholder="Address Line 1" class="input"
                            value=" '''+str(old_add_line1)+''' " /></td>
                    <td><input type="text" d="newcor_address2" placeholder="Address Line 2" class="input"
                            value=" '''+str(na1)+''' " /></td>
                </tr>
                <tr>
                    <td><input type="text" d="oldcor_address2" placeholder="Address Line 2" class="input"
                            value=" '''+str(old_add_line2)+''' "  /></td>
                    <td><input type="text" d="newcor_address2" placeholder="Address Line 2" class="input"
                            value=" '''+str(na2)+''' " ></td>
                </tr>
                <tr>
                    <td><input type="text" id="oldcor_inputCity" placeholder="City" class="input"
                            value=" '''+str(old_city)+''' " /></td>
                    <td><input type="text" id="newcor_inputCity" placeholder="City" class="input"
                            value=" '''+str(new_city)+''' " /></td>
                </tr>
                <tr>
                    <td><input type="text" id="oldcor_inputState" placeholder="State" class="input"
                            value="'''+str(old_state)+'''" /></td>
                    <td><input type="text" id="newcor_inputState" placeholder="State" class="input"
                            value="'''+str(new_state)+'''" /></td>
                </tr>
                <tr>
                    <td><input type="text" id="oldcor_inputPincode" placeholder="Pincode" class="input"
                            value="'''+str(old_pincode)+'''" /> </td>
                    <td><input type="text" id="oldcor_inputPincode" placeholder="Pincode" class="input"
                            value="'''+str(new_pincode)+'''" /> </td>
                </tr>
            </table>
        </div>
<br>
<br>
<br>
<br>
        <!--Bank Details-->
        <div style="margin-bottom:12px;text-align: center;background-color:#b3e7f2;padding: 10px 0;margin:0 15px;">
            <tr>
                '''+str(bankchangeyesno)+'''
                <b>Change of Bank Details</b>
            </tr>
        </div>
        <div style="padding:15px">
            <table style="margin: 0;margin-left: 20px;width: 100%">
                <tr>
                    <th style="float:left;">Old Bank Details
                        <label> <input type="checkbox" id="oldbank_sb_check" />SB</label>
                        <label> <input type="checkbox" id="oldbank_ca_check" />CA</label>
                    </th>
                    <th>New Bank Details
                        <label> '''+str(new_bank_saving)+'''SB</label>
                        <label> '''+str(new_bank_current)+'''CA</label>
                    </th>
                </tr>

                <tr>
                    <td> <input type="text" id="oldbank_name" placeholder="Bank Name" class="input"
                            value=" '''+str(bank_name_old)+''' " /></td>
                    <td><input type="text" id="newbank_acc" placeholder="Bank Name" class="input"
                            value=" '''+str(bank_name_new)+''' " /></td>
                </tr>
                <tr>
                    <td><input type="text" id="oldbank_acc" placeholder="Account No" class="input"
                            value=" '''+str(account_no_old)+''' " /></td>
                    <td><input type="text" id="newbank_acc" placeholder="Account No" class="input"
                            value=" '''+str(account_no_new)+''' " /></td>
                </tr>
                <tr>
                    <td><input type="text" id="oldbank_ifsc" placeholder="IFSC Code" class="input"
                            value=" '''+str(ifsc_code_old)+''' " /></td>
                    <td><input type="text" id="newbank_ifsc" placeholder="IFSC Code" class="input"
                            value=" '''+str(ifsc_code_new)+''' " /></td>
                </tr>
                <tr>
                    <td> <input type="text" id="oldbank_micr" placeholder="MICR" class="input"
                            value=" '''+str(micr_old)+''' " /></td>
                    <td><input type="text" id="newbank_micr" placeholder="MICR" class="input"
                            value=" '''+str(micr_new)+''' " /></td>
                </tr>
                <tr>
                    <td><input type="text" id="oldbank_zip" placeholder="Branch Name" class="input"
                            value=" '''+str(branch_name_old)+''' " /></td>
                    <td> <input type="text" id="newbank_zip" placeholder="Branch Name" class="input"
                            value=" '''+str(branch_name_new)+''' " /></td>
                </tr>
            </table>
        </div>
        <!---->
        <div style="margin-bottom:12px;text-align: center;background-color:#b3e7f2;padding: 10px 0;margin:0 15px;">
            <tr>
                '''+str(em)+'''
                <b>Change of Email And Mobile No.</b>
            </tr>
        </div>
        <div style="padding:15px">
            <table style="margin: 0;margin-left: 30px;width: 90%">
                <tr>
                    <th style="text-align: center;">Old Mobile/ Landline No./ E-mail id</th>
                    <th style="text-align: center;">New Mobile/ Landline No./ E-mail id </th>
                    <th style="text-align: center;">Relation </th>
                </tr>
                <tr>
                    <td>
                        <input type="text" id="old_mob" placeholder="Mobile" class="input"
                            value=" '''+str(old_mob_no)+''' " />
                    </td>
                    <td>
                        <input type="text" id="new_mob" placeholder="mobile" class="input"
                            value=" '''+str(new_mob_no)+''' " />
                    </td>
                    <td>
                        <input type="text" id="new_mob" placeholder="mobile dependency" class="input"
                            value=" '''+str(mobile_dependency)+''' " />
                    </td>
                </tr>
                <tr>
                    <td>
                        <input type="text" id="old_email" placeholder="Email" class="input"
                            value=" '''+str(old_email)+''' " />
                    </td>
                    <td>
                        <input type="text" id="new_email" placeholder="Email" class="input"
                            value=" '''+str(new_email)+''' " />
                    </td>
                    <td>
                        <input type="text" id="new_email" placeholder="email dependency" class="input"
                            value=" '''+str(email_dependency)+''' " />
                    </td>
                </tr>
            </table>
        </div>

        <!--details-->

        <!---->

        <!--change div-->

        <div style="margin-bottom:12px;text-align: center;background-color:#b3e7f2;padding: 10px 0;margin:0 15px;">
            <tr>
                '''+str(updation_annual_income)+'''
                <b>Updation in Annual Income Details</b>
            </tr>
        </div>
        <div style="padding:15px">
            <table style="margin: 0;margin-left: 20px;width: 100%">
                <tr>
                    <th style="text-align: center;">Old Annual Income details</th>
                    <th style="text-align: center;">New Annual Income As on '''+str(new_date)+'''details </th>
                </tr>
                <tr>
                    <td><input type="text" id="old_grossincome" placeholder="Annual Income Rs.**  Lac per annum"
                            class="input" value=" '''+str(old_annual_income)+''' " /></td>
                    <td><input type="text" id="new_grossincome" placeholder="Annual Income Rs.**  Lac per annum"
                            class="input" value=" '''+str(new_annual_income)+''' " /></td>
                </tr>
            </table>
        </div>
        
    </div>
    <div style="width:90%;border:20px solid #b3e7f2;margin:12px auto;"  class="page-break">
        <!---->
        <div style="margin-bottom:12px;text-align: center;background-color:#b3e7f2;padding: 10px 0;margin:15px 15px;">
            <tr>
                '''+str(segmentactivationyesno)+'''
                <b>Reactivation of Inactive Client / Activate Segment</b>
            </tr>
        </div>
        <table style="padding: 20px;width: 100%">

            <tr>
                <td><label>
                        '''+str(bse_cash)+''' BSE CASH 
                         
                        
                    </label></td>
                <td><label style="margin-left: 80px">
                        '''+str(bse_curr)+''' BSE CURRENCY
                        
                </label>
                </td>
                <td><label style="margin-left: 80px">
                        '''+str(bse_fo)+''' BSE F&O
                       
                    </label></td>

            </tr>
            <tr>
                <td><label>
                        '''+str(bse_comm)+''' BSE Commodity
                        
                    </label></td>
                
                <td>
                    <label style="margin-left: 80px">
                        '''+str(bse_slb)+''' BSE SLB
                         
                    </label>
                </td>
                <td>
                    <label style="margin-left: 80px">
                        '''+str(bse_mf)+''' BSE MF
                         
                    </label>
                </td>
            </tr>
            <tr>
                <td><label>
                        '''+str(nse_cash)+''' NSE CASH 
                         
                        
                    </label></td>
                <td><label style="margin-left: 80px">
                        '''+str(nse_curr)+''' NSE CURRENCY
                        
                </label>
                </td>
                <td><label style="margin-left: 80px">
                        '''+str(nse_fo)+''' NSE F&O
                       
                    </label></td>

            </tr>
            <tr>
                <td><label>
                        '''+str(nse_comm)+''' NSE Commodity
                        
                    </label></td>
                
                <td>
                    <label style="margin-left: 80px">
                        '''+str(nse_slb)+''' NSE SLB
                         
                    </label>
                </td>
                
            </tr>
            <tr>
                <td><label>
                        '''+str(mcx)+''' NSE Commodity
                        
                    </label></td>
                
                <td>
                    <label style="margin-left: 80px">
                        '''+str(ncdex)+''' NSE SLB
                         
                    </label>
                </td>
                
            </tr>
        </table>

        <div align="left">
            <div style="padding:30px 15px ;width: 90%">
                <p>
                    Note : Please share the filled and duly signed KRA, CKYC & FATCA forms
                    separately in case details are not updated
                </p>
                <p>
                    In case address proof update, KRA and CKYC forms are mandatory
                    with the supporting documents along with this form.
                </p>
            </div>
        </div>
      
        <div style="padding: 10px">
            <table style="width: 100%;border-collapse: collapse;">

                <tr
                    style="text-align:center;background:#b3e7f2;padding-top:10px;margin:0 15px;margin-bottom:12px;padding-bottom: 8px">
                    <th></th>
                    <th>First/Sole Holder</th>
                    <th>Second Holder</th>
                    <th>Third Holder</th>
                </tr>
                <tr style="height: 60px;">
                    <th>Name</th>
                    <td> <input type="text" name="" id="first_holder" class="input"
                            value=" '''+str(name_first_ho)+''' " /></td>
                    <td><input type="text" name="" id="second_holder" class="input"
                            value=" '''+str(name_sec_ho)+''' " /></td>
                    <td><input type="text" name="" id="third_holder" class="input"
                            value=" '''+str(name_third_ho)+''' " /></td>
                </tr>
                <tr>
                    <th>Signature</th>
                    <td>'''+str(sign)+''' </td>
                    <td></td>
                    <td></td>
                </tr>
            </table>
            <div align="left">
            <div style="padding:30px 15px ;width: 90%;">
            <p>Emkay Global Financial Services Ltd. CIN : L67120MH1995PLC084899, SEBI REGN No. INZ000203933, Bombay Stock Exchange Ltd (BSE) : 185, National Stock Exchange of India Ltd (NSE) : 9018, Multi Commodity Exchange of India Ltd (MCX): 56270, Metropolitan Stock Exchange of India Ltd (MSEI): 1089, National Commodity & Derivatives Exchange Limited (NCDEX): 1263, Registered CDSL DP (23000): IN-DP-CDSL-60-2015, Registered Research Analyst : INH000000354, Registered Merchant Banker : INM000011229, AMFI Registration Number (ARN No.): 1563. <br><br>
             [  C-06 Ground Floor, Paragon Centre, Pandurang Bhudhkar Marg, Worli, Mumbai- 400 013, Phones: +91 22 66121212 • Fax: 91 22 22650575 <br>E-mail: rekyc_support@emkayglobal.in Website: www.emkayglobal.com]</p></br>

        </div>
        </div>
        </div>



    </div>

    </div>
<br><br><br><br><br><br><br>
        <h3>Geo Tagging Details of Photo:'''+str(data[0][86])+'''</h3>
</body>

</html>'''


    
    chk=(os.path.isdir("static/rekycPDF/"+original_clientcode))
    if chk==False:
        try:
            os.mkdir("static/rekycPDF")
        except:
            pass
        try:
            os.mkdir("static/rekycPDF/"+str(original_clientcode))
        except:
            pass


    options = {'enable-local-file-access': None,'--page-size' :'A4'}
    try:
        pdfkit.from_string(html,"static/rekycPDF/"+str(original_clientcode)+"/rekycamtest_signed.pdf",options=options )
    except:
        pass
    
    pdf = FPDF()


    if data[0][28]!="":
        
        pdf.add_page()
        pdf.image(data[0][28], x=10, y=10, w=150, h=150)
        pdf.set_font('Arial', 'B', 8)
        pdf.y = 200
        pdf.x = 10
        pdf.cell(40, 20,"E-signed by:"+data[0][2])
        pdf.y = 205
        pdf.x = 10
        pdf.cell(50, 20,"Date: "+str(datetime.datetime.now()))
        pdf.y = 210
        pdf.x = 10
        pdf.cell(60, 20,"Reason: Re-KYC")
        
    
            
    # if data[0][29]!="":
    #     pdf.add_page()
    #     pdf.image(data[0][29], x=10, y=10, w=150, h=150)
    #     pdf.set_font('Arial', 'B', 8)
    #     pdf.y = 200
    #     pdf.x = 10
    #     pdf.cell(40, 20,"E-signed by:"+data[0][2])
    #     pdf.y = 205
    #     pdf.x = 10
    #     pdf.cell(50, 20,"Date: "+data[0][32])
    #     pdf.y = 210
    #     pdf.x = 10
    #     pdf.cell(60, 20,"Reason: Re-KYC")
    #     pdf.y = 215
    #     pdf.x = 10
    #     pdf.cell(70, 20,"Location: India" )

    if data[0][29].split('/')[-1]!='':
        pdfWand = wi(filename=data[0][29], resolution=100)
        pdfimage = pdfWand.convert("jpeg")
        i=1
        uploadFinancialproof=[]
        for img in pdfimage.sequence:
            page = wi(image=img)
            page.save(filename='uploadFinancialproof'+str(i)+".jpg")
            uploadFinancialproof.append('uploadFinancialproof'+str(i)+".jpg")
            i +=1

        for i in uploadFinancialproof:
            pdf.add_page()
            pdf.image(i, x=10, y=10, w=150, h=150)
            pdf.set_font('Arial', 'B', 8)
            pdf.y = 200
            pdf.x = 10
            pdf.cell(40, 20,"E-signed by:"+data[0][2])
            pdf.y = 205
            pdf.x = 10
            pdf.cell(50, 20,"Date: "+str(datetime.datetime.now()))
            pdf.y = 210
            pdf.x = 10
            pdf.cell(60, 20,"Reason: Re-KYC")
            
            
            
    if data[0][30]!="":
        
        pdf.add_page()
        pdf.image(data[0][30], x=10, y=10, w=150, h=150)
        pdf.set_font('Arial', 'B', 8)
        pdf.y = 200
        pdf.x = 10
        pdf.cell(40, 20,"E-signed by:"+data[0][2])
        pdf.y = 205
        pdf.x = 10
        pdf.cell(50, 20,"Date: "+str(datetime.datetime.now()))
        pdf.y = 210
        pdf.x = 10
        pdf.cell(60, 20,"Reason: Re-KYC")
        
            
            
    if data[0][31]!="":
        pdf.add_page()
        pdf.image(data[0][31], x=10, y=10, w=150, h=150)
        pdf.set_font('Arial', 'B', 8)
        pdf.y = 200
        pdf.x = 10
        pdf.cell(40, 20,"E-signed by:"+data[0][2])
        pdf.y = 205
        pdf.x = 10
        pdf.cell(50, 20,"Date: "+str(datetime.datetime.now()))
        pdf.y = 210
        pdf.x = 10
        pdf.cell(60, 20,"Reason: Re-KYC")
        
            
            
    if data[0][66]!="" :
        
        if data[0][66]!=None:
            pdf.add_page()
            pdf.image(data[0][66], x=10, y=10, w=150, h=150)
            pdf.set_font('Arial', 'B', 8)
            pdf.y = 200
            pdf.x = 10
            pdf.cell(40, 20,"E-signed by:"+data[0][2])
            pdf.y = 205
            pdf.x = 10
            pdf.cell(50, 20,"Date: "+str(datetime.datetime.now()))
            pdf.y = 210
            pdf.x = 10
            pdf.cell(60, 20,"Reason: Re-KYC")
        
                
        
        
        
        
    pdf.output("static/rekycPDF/"+str(original_clientcode)+"/pdf2.pdf")

    mergedObject = PdfFileMerger()
    mergedObject.append(PdfFileReader("static/rekycPDF/"+str(original_clientcode)+"/rekycamtest_signed.pdf", "rb"), import_bookmarks=False)
    if data[0][168] == 'yes':
        path = nomineePdf(clientcode)
    elif data[0][168] == 'not_required':
        path = 'NOMINATION FORM (1).pdf'
    else:
        path = DeclarationPdf(clientcode)
    
    account_status=str(data[0][102])if str(data[0][102]) !='None' else ''
    if account_status =='Dormant':
        path=Reactivation(clientcode)
        #mergedObject.append(PdfFileReader("static/rekycPDF/"+str(original_clientcode)+"/reactivationPDF.pdf", "rb"), import_bookmarks=False)
    else:
        pass
    mergedObject.append(PdfFileReader(path, "rb"), import_bookmarks=False)
    mergedObject.append(PdfFileReader("static/rekycPDF/"+str(original_clientcode)+"/pdf2.pdf", "rb"), import_bookmarks=False)
    mergedObject.write("static/rekycPDF/"+str(original_clientcode)+"/rekycam_signed.pdf")
    os.remove("static/rekycPDF/"+str(original_clientcode)+"/pdf2.pdf")



    return jsonify({'msg':'PDF File Generated'})

	


#@pdfOperationsapi.route('/secondpdfAPI/<clientcode>', methods=['POST'])
# def kraAPI(clientcode):
#     clientcode=clientcode.lower()
#     original_clientcode=clientcode
#     print("inside signkra")
#     # chk=conn_Emkay_digilocker.execute('SELECT addresschangeyesno FROM userdetails WHERE clientcode = "'+clientcode+'"').fetchall()
#     # if chk[0][0]=='no':
#     #     return jsonify({'msg':'Cannot Generate KRA PDF'})


#     data=conn_Emkay_digilocker.execute('SELECT * FROM userdetails WHERE clientcode = "'+clientcode+'"').fetchall()
#     clientcode=clientcode.split('-')[0]

#     if (data[0][80] != None and data[0][80] !="") or data[0][75] == 'yes' or data[0][76] == 'yes':
        
#         name             = str(data[0][2])
#         maiden_name      = ' '
#         father_name      = str(data[0][4])
#         mother_name      = str(data[0][5]) if str(data[0][5]) !='None' else ''
#         dob              = str(data[0][60])
#         gender           = str(data[0][61])
#         marital_status   = str(data[0][63])
#         citizenship      = 'INDIAN'
#         signature        = "E-signed by:"+data[0][2]+" <br>Date: "+str(datetime.datetime.now())+"<br> Reason: Re-KYC "
#         residentional_s  = "INDIVIDUAL"
#         occupation_type  = str(data[0][39])
#         res_for_tax      = 'No'
#         country_of_juris =  "India" #str(data[0][16])
#         tax_iden_num     = 'N/A'
#         place_of_birth   = data[0][53] # str(data[0][16])
#         country_of_birth = "India" #str(data[0][16])

#         pan             = data[0][3]
#         aadhaar         = data[0][100]
#         SIGNATURE       = "E-signed by:"+data[0][2]+" <br>Date: "+str(datetime.datetime.now())+"<br> Reason: Re-KYC "




#         # PROFF OF ADDRESS

#         adderess_type  = 'RESIDENTIAL/BUSINESS'
#         proff_of_add   = 'AADHAAR CARD'

#         # CORRESPONDENCE ADD
        
#         add_line_1    = str(data[0][52])
#         add_line_2    = str(data[0][64])
#         add_line_3    = ''
#         city_town_vill= str(data[0][53])
#         state         = str(data[0][54])
#         country       = str(data[0][55])
#         pin_code      = str(data[0][65])

       


#         # PERMANENT ADD

#         permanent_add_1 = str(data[0][52])
#         permanent_add_2 = str(data[0][64])
#         permanent_add_3 = ''
#         p_city_town_vill= str(data[0][53])
#         p_state         = str(data[0][54])
#         P_country       = str(data[0][55])
#         p_pin_code      = str(data[0][65])


#         # CONTANCT DETAILS

#         tel            = ''
#         tel_res        = ""
#         mob_no         = str(data[0][34]) if str(data[0][34]) !='' else str(data[0][6])
#         fax            = ''
#         email_id       =  str(data[0][33]) if str(data[0][33]) !='' else str(data[0][7])


#         # DETAILS OF RELATED PERSON

#         r_name         = 'NA'
#         r_person_type  = 'NA'
#         r_pan          = 'NA'

#         digi_trans_id =  str(datetime.datetime.now())#data[0][81]


#         # APPLICANT DECLARTION

#         date_d       = str(data[0][32])
#         palce_d      = str(data[0][86])
#         sign_d       = "E-signed by:"+data[0][2]+" <br>Date: "+str(datetime.datetime.now())+"<br> Reason: Re-KYC "
#         date_off     = str(data[0][32])


#         # ATTESTATION/FOR OFFICE

#         doc_received  = ''
#         employee_name = 'Digilocker'
#         sebi_no       = ''
#         employee_id   = ''
#         designation   = 'Sales'
#         data_off      = str(data[0][32])
#         doc_upload_img = ''
#         if data[0][80] !=None and data[0][80]!= '':
#             with open(data[0][80], "rb") as img_file:
#               my_stringss = base64.b64encode(img_file.read())
#             imgenc64    =my_stringss.decode('utf-8')
#         else:
#             imgenc64=''
#         #logo        =''


#         html =  '''<!DOCTYPE html>
# <html lang="en">
# <head>
# <meta charset="UTF-8" />
# <title>PDF</title>
# <style>
# @page {
# margin: 0.1in 0.1in 0.1in 0.1in;
# }body {
# font-family: calibri;
# font-size: 14px;
# max-width: 800px;
# width: 100%;
# margin: 0;
# margin-left: 10px
# letter-spacing: 1px;
# }@media print {
# body {
# margin-top: 10mm;
# margin-bottom: 10mm;
# margin-left: 0mm;
# margin-right: 0mm;
# }}label {
# text-transform: uppercase;
# }.bold {
# font-weight: bold;
# }.justify {
# text-align: justify;
# }.center {
# text-align: center;
# }.borderthick {
# border-width: 3px;
# }.displayn {
# display: none;
# }.margincorrect {
# margin-top: -1px;
# margin-bottom: -1px;
# }.marginupdown {
# margin-top: 5px;
# margin-bottom: 5px;
# }.font13 {
# font-size: 14px;
# }.font12 {
# font-size: 14px;
# }.font11 {
# font-size: 14px;
# }.center {
# text-align: center;
# }.head {
# background: #d7d8d8;
# font-weight: 600;
# padding: 3px;
# padding-left: 30px;
# margin-top: 10px;
# margin-bottom: 10px;
# width: 100%;
# }.subhead {
# background: #bfc1c1;
# font-weight: 600;
# padding: 3px;
# padding-left: 30px;
# margin: 10px 0 10px 0;
# width: 100%;
# }table {
# font-family: calibri, sans-serif;
# border-collapse: collapse;
# width: 100%;
# margin: auto 15px;
# font-size: 11px;
# letter-spacing: 1px;
# }td, th {
# border: 1px solid #ccc;
# text-align: left;
# padding: 5px 5px 0 5px;
# vertical-align:middle;
# font-size: 14px;
# }.fieldlabel {
# width: 50px;
# }tr:nth-child(even) {
# background-color: #eee;
# }.page-break {
# page-break-before: always;
# }.signhere {
# color: #727a81;
# height: 90px;
# }</style>
# </head>
# <body>
# <div><div class="center bold"><img src='''+LOGO+''' width="120px" alt="" /></div><div class="center bold">Emkay Global Financial Services Ltd.</div><div class="center">Central KYC Registry | Know Your Customer(KYC) Application | Individual</div><!--    Index   -->
#    <div class="bold" style="float: right" ><h3>'''+str(clientcode).upper()+'''</h3></div>
#     <div class="alldetails ">
#             <div class="head marginupdown"> Registered Office Address </div>
#             <div class="marginupdown justify">  C-06 Ground Floor, Paragon Centre, Pandurang Bhudhkar Marg, Worli, Mumbai- 400 013 | Phones: +91 22 66121212 | Fax: 91 22 22650575<br /> Email : rekyc_support@emkayglobal.in |  Web Site : www.emkayglobal.com<br /> </div>
#             <br /> 
#             <div class="head marginupdown"> Corporate Office </div>
#             <div class="marginupdown justify">  C-06 Ground Floor, Paragon Centre, Pandurang Bhudhkar Marg, Worli, Mumbai- 400 013 | Phones: +91 22 66121212 | Fax: 91 22 22650575<br /> Email : rekyc_support@emkayglobal.in |  Web Site : www.emkayglobal.com<br /> </div>
#             <!-- personal details --> 
#             <div class="alldetails">
#                <div class="head"> 1. Personal Details </div>
#                <div>
#                   <table style="margin-bottom: 5px;">
#                      <tbody>
#                         <tr>
#                            <td style="width: 20%" class="bold"><span> Name*</span> </td>
#                            <td style="width: 60%"><label>'''+str(name)+'''</label></td>
#                            <td style="width: 20%" rowspan="6"><img src="data:image/png;base64,'''+imgenc64+'''"  width="180" height="200" alt="Base64 encoded image"  /></td>
#                         </tr>
#                         <tr>
#                            <td class="bold">Maiden Name <span style="font-size: 12px">(If any*)</span></td>
#                            <td><label>'''+str(maiden_name)+'''</label></td>
#                         </tr>
#                         <tr>
#                            <td><span class="bold">Father/Spouse Name* </span></td>
#                            <td><label>'''+str(father_name)+'''</label></td>
#                         </tr>
#                         <tr>
#                            <td><span class="bold">Mother Name* </span></td>
#                            <td><label>'''+str(mother_name)+'''</label></td>
#                         </tr>
#                         <tr>
#                            <td><span class="bold">Date of Birth* </span></td>
#                            <td><label>'''+str(dob)+'''</label></td>
#                         </tr>
#                         <tr>
#                            <td><span class="bold">Gender* </span></td>
#                            <td><label>'''+str(gender)+'''</label></td>
#                         </tr>
#                         <tr>
#                            <td><span class="bold">Marital Status* </span></td>
#                            <td><label>'''+str(marital_status)+'''</label></td>
#                            <td>'''+str(signature)+'''</td>
#                         </tr>
#                         <tr>
#                            <td class="bold"><span> Citizenship*</span></td>
#                            <td colspan="2"><label>'''+str(citizenship)+'''</label></td>
#                         </tr>
#                         <tr>
#                            <td class="bold">Residential Status* </td>
#                            <td colspan="2"><label>'''+str(residentional_s)+'''</label></td>
#                         </tr>
#                         <tr>
#                            <td class="bold">Occupation Type* </td>
#                            <td colspan="2"><label>'''+str(occupation_type)+'''</label></td>
#                         </tr>
#                         <tr>
#                            <td class="bold">Residence for Tax Purposes In Jurisdiction(s) Outside India* </td>
#                            <td colspan="2"><label>'''+str(res_for_tax)+'''</label></td>
#                         </tr>
#                         <tr>
#                            <td class="bold">Country of Jurisdiction of Residence* </td>
#                            <td colspan="2"><label>'''+str(country_of_juris)+'''</label></td>
#                         </tr>
#                         <tr>
#                            <td class="bold">Tax Identification Number or Equivalent<span style="font-size: 12px">(If issued by jurisdiction)</span>* </td>
#                            <td colspan="2"><label>'''+str(tax_iden_num)+'''</label></td>
#                         </tr>
#                         <tr>
#                            <td class="bold">Place/City of Birth* </td>
#                            <td colspan="2"><label>'''+str(place_of_birth)+'''</label></td>
#                         </tr>
#                         <tr>
#                            <td class="bold">Country of Birth* </td>
#                            <td colspan="2"><label>'''+str(country_of_birth)+'''</label></td>
#                         </tr>
#                      </tbody>
#                   </table>
#                </div>
#             </div>
#             <!-- proof of identity--> 
#             <div class="alldetails marginupdown">
#                <div class="head"> 2. Proof of Identity </div>
#                <div>
#                   <table style="margin-bottom: 5px;">
#                      <tbody>
#                         <tr>
#                            <td style="width: 20%"><span class="bold"> PAN*</span></td>
#                            <td style="width: 80%"><label>'''+str(pan)+'''</label></td>
#                         </tr>
#                         <tr>
#                            <td style="width: 20%"><span class="bold"> AADHAAR*</span></td>
#                            <td style="width: 80%"><label>'''+str(aadhaar)+'''</label></td>
#                         </tr>
#                      </tbody>
#                   </table>
#                </div>
#             </div>
#             <!-- proof of address--> 
#             <div class="alldetails marginupdown">
#                <div class="head"> 3. Proof of Address </div>
#                <div>
#                   <table style="margin-bottom: 5px;">
#                      <tbody>
#                         <tr>
#                            <td style="width: 20%"><span class="bold"> Address Type*</span></td>
#                            <td style="width: 80%" colspan="3"><label>'''+str(adderess_type)+'''</label></td>
#                         </tr>
#                         <tr>
#                            <td style="width: 20%"><span class="bold"> Proof of Address*</span></td>
#                            <td style="width: 80%" colspan="3"><label>'''+str(proff_of_add)+'''</label></td>
#                         </tr>
#                         <tr>
#                            <td colspan="4"><span class="bold">Correspondence Address</span></td>
#                         </tr>
#                         <tr>
#                            <td style="width: 20%"><span class="bold"> Address Line 1*</span></td>
#                            <td style="width: 80%" colspan="3"><label>'''+str(add_line_1)+'''</label></td>
#                         </tr>
#                         <tr>
#                            <td style="width: 20%"><span class="bold"> Address Line 2</span></td>
#                            <td style="width: 80%" colspan="3"><label>'''+str(add_line_2)+'''</label></td>
#                         </tr>
#                         <tr>
#                            <td style="width: 20%" colspan="3"><span class="bold"> Address Line 3</span></td>
#                            <td style="width: 80%" colspan="3"><label></label></td>
#                         </tr>
#                         <tr>
#                            <td style="width: 20%"><span class="bold">City/Town/Village* </span></td>
#                            <td style="width: 30%"><label>'''+str(city_town_vill)+'''</label></td>
#                            <td style="width: 20%"><span class="bold">State* </span></td>
#                            <td style="width: 30%"><label>'''+str(state)+'''</label></td>
#                         </tr>
#                         <tr>
#                            <td style="width: 20%"><span class="bold">Country* </span></td>
#                            <td style="width: 30%"><label>'''+str(country)+'''</label></td>
#                            <td style="width: 20%"><span class="bold">PIN Code* </span></td>
#                            <td style="width: 30%"><label>'''+str(pin_code)+'''</label></td>
#                         </tr>
#                      </tbody>
#                   </table>
#                   <table class="page-break" style="margin-bottom: 5px;">
#                      <tbody>
#                         <tr>
#                            <td colspan="4"><span class="bold">Permanent Address</span></td>
#                         </tr>
#                         <tr>
#                            <td style="width: 20%"><span class="bold"> Address Line 1*</span></td>
#                            <td style="width: 80%" colspan="3"><label>'''+str(permanent_add_1)+'''</label></td>
#                         </tr>
#                         <tr>
#                            <td style="width: 20%"><span class="bold"> Address Line 2</span></td>
#                            <td style="width: 80%" colspan="3"><label>'''+str(permanent_add_2)+'''</label></td>
#                         </tr>
#                         <tr>
#                            <td style="width: 20%"><span class="bold"> Address Line 3</span></td>
#                            <td style="width: 80%" colspan="3"><label>'''+str(permanent_add_3)+'''</label></td>
#                         </tr>
#                         <tr>
#                            <td style="width: 20%"><span class="bold">City/Town/Village* </span></td>
#                            <td style="width: 30%"><label>'''+str(p_city_town_vill)+'''</label></td>
#                            <td style="width: 20%"><span class="bold">State* </span></td>
#                            <td style="width: 30%"><label>'''+str(p_state)+'''</label></td>
#                         </tr>
#                         <tr>
#                            <td style="width: 20%"><span class="bold">Country* </span></td>
#                            <td style="width: 30%"><label>'''+str(P_country)+'''</label></td>
#                            <td style="width: 20%"><span class="bold">PIN Code* </span></td>
#                            <td style="width: 30%"><label>'''+str(p_pin_code)+'''</label></td>
#                         </tr>
#                      </tbody>
#                   </table>
#                </div>
#             </div>
#             <!-- Contact--> 
#             <div class="alldetails marginupdown">
#                <div class="head"> 4. Contact Details </div>
#                <table style="margin-bottom: 5px;">
#                   <tbody>
#                      <tr>
#                         <td style="width: 20%"><span class="bold">Tel.(Off.) </span></td>
#                         <td style="width: 30%"><label>'''+str(tel)+'''</label></td>
#                         <td style="width: 20%"><span class="bold">Tel.(Res.) </span></td>
#                         <td style="width: 30%"><label>'''+str(tel_res)+'''</label></td>
#                      </tr>
#                      <tr>
#                         <td style="width: 20%"><span class="bold">Mobile No.*</span></td>
#                         <td style="width: 30%"><label>'''+str(mob_no)+'''</label></td>
#                         <td style="width: 20%"><span class="bold">Fax </span></td>
#                         <td style="width: 30%"><label>'''+str(fax)+'''</label></td>
#                      </tr>
#                      <tr>
#                         <td style="width: 20%"><span class="bold"> Email ID*</span></td>
#                         <td style="width: 80%" colspan="3"><label>'''+str(email_id)+'''</label></td>
#                      </tr>
#                   </tbody>
#                </table>
#             </div>
#             <!-- Details of Related Person--> 
#             <div class="alldetails">
#                <div class="head"> 5. Details of Related Person </div>
#                <table style="margin-bottom: 5px;">
#                   <tbody>
#                      <tr>
#                         <td style="width: 20%" class="bold">Name</td>
#                         <td style="width: 80%"><label>'''+str(r_name)+'''</label></td>
#                      </tr>
#                      <tr>
#                         <td style="width: 20%" class="bold"> Related Person Type</td>
#                         <td style="width: 80%"><label>'''+str(r_person_type)+'''</label></td>
#                      </tr>
#                      <tr>
#                         <td style="width: 20%" class="bold"> PAN </td>
#                         <td style="width: 80%"><label>'''+str(r_pan)+'''</label></td>
#                      </tr>
#                   </tbody>
#                </table>
#             </div>
#             <!-- Applicant Declaration--> 
#             <div class="alldetails">
#                <div class="head"> 6. Applicant Declaration </div>
#                <table style="margin-bottom: 5px;">
#                   <tbody>
#                      <tr>
#                         <td class="fieldlabel font12 justify" style="width: 70%" colspan="2"> *I hereby declare that the details furnished above are true and correct to the best of my knowledge and belief and I undertake to inform you of any changes therein, immediately. In case any of the above information is found to be false or untrue or misleading or misrepresenting. I am aware that I may be held liable for it. <br /> *I hereby consent to receiving information from Central KYC Registry through SMS/Email on the above registered number/email address. <br /> </td>
#                         <td class="signhere" style="width: 30%" rowspan="2">'''+str(sign_d)+'''</td>
#                      </tr>
#                      <tr>
#                         <td>Date: '''+str(date_d)+'''</td>
#                         <td>Place: '''+str(palce_d)+'''</td>
#                      </tr>
#                   </tbody>
#                </table>
#             </div>
#             <!-- Attestation/For Office use only--> 
#             <div class="alldetails ">
#                <div class="head"> 7. Attestation/For Office use only </div>
#                <table style="margin-bottom: 5px;">
#                   <tbody>
#                      <tr>
#                         <td style="width: 20%" class="fieldlabel"><span class="bold"> Document Received</span></td>
#                         <td style="width: 80%" colspan="5"><label>'''+str(doc_received)+'''</label></td>
#                      </tr>
#                      <tr class="bold">
#                         <td class="center" colspan="2">Intermediary/Institution Details</td>
#                         <td class="center" colspan="4">Kyc Details</td>
#                      </tr>
#                      <tr>
#                         <td class="bold" style="width: 20%" rowspan="3">Name</td>
#                         <td style="width: 21%;" rowspan="3">Emkay Global Financial Services Ltd.</td>
#                         <td class="bold" colspan="2"><h1>Mode Of Kyc</h1></td>
#                         <td colspan="2"><h1>'''+str(employee_name)+'''</h1></td>
#                      </tr>
#                      <tr>
#                         <td colspan="2" class="bold">Digilocker Transaction Id</td>
#                         <td colspan="2">'''+str(digi_trans_id)+'''</td>
#                      </tr>
#                      <tr>
#                         <td class="bold" style="width: 12%"></td>
#                         <td style="width: 12%"></td>
#                         <td class="bold" style="width: 12%"></td>
#                         <td style="width: 12%"></td>
#                      </tr>
#                      <tr>
#                         <td style="width: 20%" class="bold" rowspan="2">CKYC Institution Code</td>
#                         <td style="width: 21%;" rowspan="2"></td>
#                         <td class="bold">Signature</td>
#                         <td style="width: 12%">'''+str(sign_d)+'''</td>
#                         <td colspan="3"></td>
#                      </tr>
#                      <tr>
#                         <td class="bold">Date</td>
#                         <td colspan="3">'''+str(date_d)+'''</td>
#                      </tr>
#                   </tbody>
#                </table>
#             </div>
#             <div> '''+str(doc_upload_img)+''' </div>
#             <br><br>
#             <h3>Geo Tagging Details of Photo:'''+str(data[0][86])+'''</h3><br><br>
#             <img src="'''+check_logo+'''" alt="" style="width: 25px;height: 25px"> 
#             I/We hereby declare that the KYC details furnished by me are true and correct to the best 
#             of my/our knowledge and belief and I/we under-take to inform you of any changes 
#             therein, immediately. In case any of the above information is found to be false or untrue 
#             or misleading or misrepresenting, I am/We are aware that I/We may be held liable for it.<br>
#             <img src="'''+check_logo+'''" alt="" style="width: 25px;height: 25px"> 
#             I/We hereby consent to receiving information from CVL KRA through SMS/Email on 
#             the above registered number/Email address.<br>
#             <img src="'''+check_logo+'''" alt="" style="width: 25px;height: 25px"> 
#             I am/We are also aware that for Aadhaar OVD based KYC, my KYC request shall be 
#             validated against Aadhaar details. I/We hereby consent to sharing my/our masked 
#             Aadhaar card with readable QR code or my Aadhaar XML/Digilocker XML file, along 
#             with passcode and as applicable, with KRA and other Intermediaries with whom I have a 
#             business relationship for KYC purposes only.
#             <br>
#             <div>
#             <h4>Name: '''+str(name)+'''</h4>
#             <h4>Date: '''+str(digi_trans_id)+'''</h4>
#          </body>
#         </html>'''

#         chk=(os.path.isdir("static/rekycPDF/"+original_clientcode))
#         if chk==False:
#             try:
#                 os.mkdir("static/rekycPDF")
#             except:
#                 pass
#             try:
#                 os.mkdir("static/rekycPDF/"+str(original_clientcode))
#             except:
#                 pass

                  
#         options = {'enable-local-file-access': None,'--page-size' :'A4'}
#         try:
#             pdfkit.from_string(html,"static/rekycPDF/"+str(original_clientcode)+"/rekykratest_signed.pdf",options=options )
#         except:
#             pass



#         pdf = FPDF()


#         if data[0][28]!="":
            
#             pdf.add_page()
#             pdf.image(data[0][28], x=10, y=10, w=150, h=150)
#             pdf.set_font('Arial', 'B', 8)
#             pdf.y = 200
#             pdf.x = 10
#             pdf.cell(40, 20,"E-signed by:"+data[0][2])
#             pdf.y = 205
#             pdf.x = 10
#             pdf.cell(50, 20,"Date: "+str(datetime.datetime.now()))
#             pdf.y = 210
#             pdf.x = 10
#             pdf.cell(60, 20,"Reason: Re-KYC")
            
        
#         if str(data[0][29]).split('/')[-1]!='' and str(data[0][29]).split('/')[-1]!='None':
#             pdfWand = wi(filename=data[0][29], resolution=100)
#             pdfimage = pdfWand.convert("jpeg")
#             i=1
#             uploadFinancialproof=[]
#             for img in pdfimage.sequence:
#                 page = wi(image=img)
#                 page.save(filename='uploadFinancialproof'+str(i)+".jpg")
#                 uploadFinancialproof.append('uploadFinancialproof'+str(i)+".jpg")
#                 i +=1

#             for i in uploadFinancialproof:
#                 pdf.add_page()
#                 pdf.image(i, x=10, y=10, w=150, h=150)
#                 pdf.set_font('Arial', 'B', 8)
#                 pdf.y = 200
#                 pdf.x = 10
#                 pdf.cell(40, 20,"E-signed by:"+data[0][2])
#                 pdf.y = 205
#                 pdf.x = 10
#                 pdf.cell(50, 20,"Date: "+str(datetime.datetime.now()))
#                 pdf.y = 210
#                 pdf.x = 10
#                 pdf.cell(60, 20,"Reason: Re-KYC")
#                 pdf.y = 215
#                 pdf.x = 10
#                 pdf.cell(70, 20,"Location: India" )
        
                
        
                
#         if data[0][30]!="":
            
#             pdf.add_page()
#             pdf.image(data[0][30], x=10, y=10, w=150, h=150)
#             pdf.set_font('Arial', 'B', 8)
#             pdf.y = 200
#             pdf.x = 10
#             pdf.cell(40, 20,"E-signed by:"+data[0][2])
#             pdf.y = 205
#             pdf.x = 10
#             pdf.cell(50, 20,"Date: "+str(datetime.datetime.now()))
#             pdf.y = 210
#             pdf.x = 10
#             pdf.cell(60, 20,"Reason: Re-KYC")
            
                
                
            
                
                

#         if data[0][66]!="" :
            
#             if data[0][66]!=None:
#                 pdf.add_page()
#                 pdf.image(data[0][66], x=10, y=10, w=150, h=150)
#                 pdf.set_font('Arial', 'B', 8)
#                 pdf.y = 200
#                 pdf.x = 10
#                 pdf.cell(40, 20,"E-signed by:"+data[0][2])
#                 pdf.y = 205
#                 pdf.x = 10
#                 pdf.cell(50, 20,"Date: "+str(datetime.datetime.now()))
#                 pdf.y = 210
#                 pdf.x = 10
#                 pdf.cell(60, 20,"Reason: Re-KYC")
                
            
            
            
#         pdf.output("static/rekycPDF/"+str(original_clientcode)+"/pdf2.pdf")
#         mergedObject = PdfFileMerger()
#         mergedObject.append(PdfFileReader("static/rekycPDF/"+str(original_clientcode)+"/rekykratest_signed.pdf", "rb"), import_bookmarks=False)
#         mergedObject.append(PdfFileReader("static/rekycPDF/"+str(original_clientcode)+"/pdf2.pdf", "rb"), import_bookmarks=False)
#         mergedObject.write("static/rekycPDF/"+str(original_clientcode)+"/rekykra_signed.pdf")
#         os.remove("static/rekycPDF/"+str(original_clientcode)+"/pdf2.pdf")


#     return jsonify({'msg':'Second PDF Created'})

def Dec_Terms(clientcode):
    data=conn_Emkay_digilocker.execute('SELECT * FROM userdetails WHERE clientcode = "'+clientcode+'"').fetchall()
    aadhar=str(data[0][104])

    dp_id=str(data[0][23])
    name     = str(data[0][2])

    esign1=''
    esign2=''
    esign3=" "
  

    mergedObject = PdfFileMerger()
    current_date = datetime.datetime.now().strftime("%d/%m/%Y") 
    chk=(os.path.isdir("static/rekycPDF/"+str(clientcode)))
    if chk==False:
      try:
          os.mkdir("static/rekycPDF")
      except:
          pass
      try:
          os.mkdir("static/rekycPDF/"+str(clientcode))
      except:
          pass
     
    for i in range(1):
        print(i)
        packet = io.BytesIO()
        # create a new PDF with Reportlab
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFontSize(10)

        if i==0:
            can.drawString(60,600,"Name:-  "+name)
            can.drawString(60,585,"Date  :-  "+current_date)


        can.save()
        #move to the beginning of the StringIO buffer
        packet.seek(0)
        new_pdf = PdfFileReader(packet)
        # read your existing PDF
        existing_pdf = PdfFileReader(open("terms.pdf", "rb"))
        output = PdfFileWriter()
        # add the "watermark" (which is the new pdf) on the existing page
        page = existing_pdf.getPage(i)
        page.mergePage(new_pdf.getPage(0))
        output.addPage(page)
        # finally, write "output" to a real file
        outputStream = open("static/rekycPDF/"+str(clientcode)+"/destination"+str(i)+".pdf", "wb")
        output.write(outputStream)
        outputStream.close()
        mergedObject.append(PdfFileReader("static/rekycPDF/"+str(clientcode)+"/destination"+str(i)+".pdf", "rb"), import_bookmarks=False)
        # if i == 0:
        #   break


    try:
        os.remove("static/rekycPDF/"+str(clientcode)+"/termsdec.pdf")
    except:
        pass
        #pdf_FILE_name=get_random_string(6)  
    mergedObject.write("static/rekycPDF/"+clientcode+"/termsdec.pdf")  

@pdfOperationsapi.route('/secondpdfAPI_signed/<clientcode>', methods=['GET','POST'])
def kraAPI(clientcode):
    data=conn_Emkay_digilocker.execute('SELECT * FROM userdetails WHERE clientcode = "'+clientcode+'"').fetchall()
    name             = str(data[0][2])
   
    if data[0][34]=="":
        mobile=data[0][6]
    else:
        mobile=data[0][34]

    father_name      = str(data[0][4])
    #father_names      =father_name.split(' ')
    mother_name           =data[0][5]
    Education     = data[0][38]
    #mother_name      =mother.split(' ')
    dob              = str(data[0][60])
    pan             = data[0][3]
    dp_id           =str(data[0][23])if str(data[0][23]) !='None' else ''
    dp_type         = str(data[0][24])
    gender           = str(data[0][61])

    country           = data[0][55]
    city            = str(data[0][53])
    state         = data[0][54]
    country           = str(data[0][55])
    pin_code      = data[0][65]
    permanent_add_1 = str(data[0][52])
    permanent_add_2 =str( data[0][64])
    
    if data[0][33]=="":
        email=data[0][7]
    else:
        email=data[0][33]
    bo_id         =str(data[0][23])if str(data[0][23]) !='None' else ''
    mobile_dependency=str(data[0][99])
    email_dependency=str(data[0][100])


    marital_status   = str(data[0][63])

    date_d       = data[0][32]
    # date_time = datetime.datetime.fromisoformat(str(date_d))
    # date_d=date_time.strftime("%d-%m-%Y")

    gross_anu_income   = data[0][37]
    print(gross_anu_income)
    networth          = str(data[0][20])if str(data[0][20])!='None' else ''
    politically_exposes= str(data[0][58])
    trading_ex=data[0][59]
    print(trading_ex)
    education    = data[0][38]
    occupation    = data[0][39]
    bank_name     = data[0][40]
    bank_acc_no   = data[0][45]
    branch        = data[0][43]
    ifsc          = data[0][41]
    micr          = str(data[0][42])if str(data[0][42]) !='None' else ''
    print(micr)
    bank_address  = data[0][44]
    account_type  = data[0][13]
    print(account_type)
    aadhaar         = str(data[0][100])
    name_of_nom1    = data[0][107]
    pan_of_nom1     = data[0][108]
    dob_nom1        = data[0][109]
    rel_with_bo1    = data[0][110]
    net_date='31/03/2021'
    geolocation=str(data[0][86])
    esign1="E-signed by: "+name
    esign2="Date: "+str(datetime.datetime.now())
    esign3="Reason: Rekyc/Modification"
    dp_addrees='Office No 1,2,3,4, Flower Valley, Khadakpada Chowk, Kalyan West ( 421301 )'
    dpid='12087500'
    dipositort_name='CDSL'
    dip_particiapnt='Kedia capital services Pvt. Ltd.'
    stateToCode = {"andaman and nicobar islands" :"", "andhra pradesh":"28", "arunachal pradesh" :"12", "assam" :"18", "bihar":"10", "chhattisgarh":"22", "dadra and nagar haveli":"", "daman and diu":"", "delhi":"07", "goa":"30", "gujarat":"24", "haryana":"06", "himachal pradesh" :"02", "jammu and kashmir":"01", "karnataka":"29", "kerala":"32", "lakhswadeep":"", "madhya pradesh":"23", "maharashtra":"27", "manipur":"14", "meghalaya":"17", "mizoram":"15", "nagaland":"13", "odisha":"21", "puducherry":"", "punjab":"03", "rajasthan":"08", "sikkim":"11", "tamil nadu":"33", "tripura":"16", "uttar pradesh":"09", "west bengal":"19", "chandigarh":"04", "uttarakhand":"05", "jharkhand":"20", "telangana":"", "ladakh":"", "apo":""}
    state=data[0][54]
    try:
        state_code = stateToCode[state.lower()]
        print(state_code)
    except:
        state_code = ""

    mergedObject = PdfFileMerger()
    current_date = datetime.datetime.now().strftime("%d-%m-%Y")
    current_date_d = datetime.datetime.now().strftime("%d%m %Y")
       


    chk=(os.path.isdir("static/rekycPDF/"+str(clientcode)))
    if chk==False:
      try:
          os.mkdir("static/rekycPDF")
      except:
          pass
      try:
          os.mkdir("static/rekycPDF/"+str(clientcode))
      except:
          pass
    for i in range(1):
        # if i !=1:
        #   continue
        print(i)
        packet = io.BytesIO()
        # create a new PDF with Reportlab
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFontSize(10)     

        if i==0:
            can.setFontSize(7)
            can.drawString(343,770,"✓")#modification
            can.drawString(120,620,"✓")#Nationality
            can.drawString(150,607,"✓")#Resident_Indivusual
            # can.drawString(340,716,"✓")#KYC
            can.drawString(335,746,"✓")#digiloker
            can.drawString(154,576,"✓")#PAN
            can.setFontSize(9)
            can.drawString(290,576,pan)
            can.drawString(100,593,pan)#aadhar
            can.drawString(297,593,aadhaar)#aadhar
            #if data[0][72] != None and data[0][72] != '':
            can.drawImage(data[0][80], 476,630,width=68,height=90)
            # dob= datetime.datetime.now().strftime("%d/%y/%m")
            can.drawString(140,635,dob)
            if gender=="male":
                can.drawString(155,693,"Mr.",charSpace=4)
            elif gender=="Female" and marital_status.lower()=="single":
                can.drawString(155,693,"Miss",charSpace=1)
            elif gender== "Female":
                can.drawString(155,693,"Mrs",charSpace=5)
            ncount=name.count(' ')
            if ncount==0: 
                can.drawString(180,706,name.split(' ')[0]) 
            elif ncount==1:
                can.drawString(180,706,name.split(' ')[0])
                can.drawString(400,706,name.split(' ')[1])
            else:
                can.drawString(180,706,name.split(' ')[0])
                can.drawString(280,706,name.split(' ')[1])
                can.drawString(380,706,' '.join(name.split(' ')[2:]))
            if "D/O" in father_name or 'W/O' in father_name or "S/O" in father_name:
                fcount=father_name.count(' ') 
                if fcount==1:
                    can.drawString(200,693,father_name.split(' ')[0]) 
                    can.drawString(452,693,father_name.split(' ')[1]) 
                elif fcount==2:
                    can.drawString(200,693,father_name.split(' ')[0])
                    can.drawString(312,693,father_name.split(' ')[1])
                    can.drawString(452,693,father_name.split(' ')[2])
                elif fcount>=2:
                    can.drawString(200,693,father_name.split(' ')[0],charSpace=5)
                    can.drawString(220,693,father_name.split(' ')[1])
                    can.drawString(315,693,father_name.split(' ')[2])
                    can.drawString(452,693,' '.join(father_name.split(' ')[3:]))        
            else:
                can.drawString(150,693,"Mr",charSpace=5)    
                fcount=father_name.count(' ') 
                if fcount==0:
                    can.drawString(180,693,father_name.split(' ')[0]) 
                elif fcount==1:
                    can.drawString(180,693,father_name.split(' ')[0])
                    can.drawString(280,693,father_name.split(' ')[1])
                else:
                    can.drawString(180,693,father_name.split(' ')[0])
                    can.drawString(280,693,father_name.split(' ')[1])
                    can.drawString(380,693,' '.join(father_name.split(' ')[2:])) 
            can.setFontSize(8)
            if gender=="male":
                can.drawString(110,648,"✓")#male
            elif gender=="Female":
                can.drawString(144,648,"✓")#female
            if marital_status=="married":
                can.drawString(300,648,"✓")#Single
            else:
                can.drawString(331,648,"✓")#Married
                

            can.setFontSize(8)
            #can.drawString(80,553,"✓")#aadhar
            can.drawString(176,553,aadhaar[-4:],charSpace=4)
            can.setFontSize(8)
            address=permanent_add_1+" "+permanent_add_2
            can.drawString(105,495,address[:85])
            can.drawString(105,480,address[85:170])
            can.drawString(105,190,address[170:230])
            can.drawString(135,455,city)
            can.drawString(470,455,pin_code)
            can.drawString(105,443,state)
            can.drawString(330,443,country)
            
            can.drawString(140,258,email)
            can.drawString(118,245,"+91")
            can.drawString(160,245,mobile[:10])
            
            can.setFontSize(5)
            can.drawString(350,180,esign1)
            can.drawString(350,175,esign2)
            can.drawString(350,170,esign3)
            if data[0][30] != None and data[0][30] != '':
                can.drawImage(data[0][30],450,160,width=90,height=30)
            can.setFontSize(8)
            can.drawString(100,138,city)
            can.drawString(280,138,current_date)
                
            can.drawString(35,25,"Geolocation:- "+geolocation[:105])
            can.drawString(35,15,geolocation[105:200])

        can.save()
        #move to the beginning of the StringIO buffer
        packet.seek(0)
        new_pdf = PdfFileReader(packet)
        # read your existing PDF
        existing_pdf = PdfFileReader(open("KRA_NEW.pdf", "rb"))
        output = PdfFileWriter()
        # add the "watermark" (which is the new pdf) on the existing page
        page = existing_pdf.getPage(i)
        page.mergePage(new_pdf.getPage(0))
        output.addPage(page)
        # finally, write "output" to a real file
        outputStream = open("static/rekycPDF/"+str(clientcode)+"/destination"+str(i)+".pdf", "wb")
        output.write(outputStream)
        outputStream.close()
        mergedObject.append(PdfFileReader("static/rekycPDF/"+str(clientcode)+"/destination"+str(i)+".pdf", "rb"), import_bookmarks=False)
        # if i == 33:
        #   break


    try:
        os.remove("static/rekycPDF/"+str(clientcode)+"/rekykratest.pdf")
    except:
        pass
        #pdf_FILE_name=get_random_string(6)  
    mergedObject.write("static/rekycPDF/"+clientcode+"/rekykratest.pdf")       

  

   

    


    pdf = FPDF()
    if data[0][28] != None and data[0][28] != '':
        pdf.add_page()
        pdf.image(data[0][28], x=10, y=10, w=150, h=150)
    

    
    #pdfWand = wi(filename=data[0][29], resolution=100)
    #pdfimage = pdfWand.convert("jpeg")
    #i=1
    #uploadFinancialproof=[]
    #for img in pdfimage.sequence:
        #page = wi(image=img)
        #page.save(filename='uploadFinancialproof'+str(i)+".jpg")
        #uploadFinancialproof.append('uploadFinancialproof'+str(i)+".jpg")
        #i +=1

    #for i in uploadFinancialproof:
        #pdf.add_page()
        #pdf.image(i, x=10, y=10, w=150, h=150)


    # AADHAR IMG
    try:
        pdf.add_page()
        pdf.image(data[0][66], x=10, y=10, w=150, h=150)
    except:
        pass    
      
    if data[0][30] != None and data[0][30] != '':
        pdf.add_page()
        pdf.image(data[0][30], x=10, y=10, w=150, h=150)
    
    
    #pdf.add_page()
    #pdf.image(data[0][31], x=10, y=10, w=150, h=150)
    
    
    
    
    
    
    
    pdf.output("static/rekycPDF/"+str(clientcode)+"/pdf2.pdf")

    mergedObject = PdfFileMerger()
    mergedObject.append(PdfFileReader("static/rekycPDF/"+str(clientcode)+"/rekykratest.pdf", "rb"), import_bookmarks=False)
    # mergedObject.append(PdfFileReader("static/terms.pdf", "rb"), import_bookmarks=False)
    # path=Dec_Terms(clientcode)
    # mergedObject.append(PdfFileReader("static/rekycPDF/"+str(clientcode)+"/termsdec.pdf", "rb"), import_bookmarks=False)
    mergedObject.append(PdfFileReader("static/rekycPDF/"+str(clientcode)+"/pdf2.pdf", "rb"), import_bookmarks=False)
    mergedObject.write("static/rekycPDF/"+str(clientcode)+"/rekykra_signed.pdf")
    # compress("static/rekycPDF/"+str(clientcode)+"/rekykrapre.pdf","static/rekycPDF/"+str(clientcode)+"/rekykra.pdf")
    # os.remove("static/rekycPDF/"+str(clientcode)+"/rekykrapre.pdf")
    os.remove("static/rekycPDF/"+str(clientcode)+"/pdf2.pdf")
    return jsonify({'msg': 'EquityKRA PDF Generated'})


@pdfOperationsapi.route('/freeze/<clientcode>', methods=['POST', 'GET'])
def freeze(clientcode):
    clientcode=clientcode.lower()

    cmd = 'update userdetails set freeze="yes" WHERE clientcode = "'+clientcode+'"'
    conn_Emkay_digilocker.execute(cmd)
    conn_Emkay_digilocker.commit()

    return jsonify({'msg':'Successfull'})

@pdfOperationsapi.route('/unfreeze/<clientcode>', methods=['POST', 'GET'])
def unfreeze(clientcode):
    clientcode=clientcode.lower()

    cmd = 'update userdetails set freeze="no" WHERE clientcode = "'+clientcode+'"'
    conn_Emkay_digilocker.execute(cmd)
    conn_Emkay_digilocker.commit()

    return jsonify({'msg':'Successfull'})


def Reactivation(clientcode):
    data=conn_Emkay_digilocker.execute('SELECT * FROM userdetails WHERE clientcode = "'+clientcode+'"').fetchall()

    clientcode=str(data[0][1])
    name        =str(data[0][2])if str(data[0][2]) !='None' else ''
    myname      =name.split(' ')
    dp_type     =data[0][24]if str(data[0][24]) !='None' else ''
    dp_id       =str(data[0][23])if str(data[0][23]) !='None' else ''
    pan          =str(data[0][3])if str(data[0][3]) !='None' else ''
    bsda          =str(data[0][202])if str(data[0][202]) !='None' else ''
    father_name=str(data[0][4])if str(data[0][4]) !='None' else ''
    mother_name=str(data[0][5])if str(data[0][5]) !='None' else ''
    gender=str(data[0][61])if str(data[0][61]) !='None' else ''
    marital_status=str(data[0][63])if str(data[0][63]) !='None' else ''
    dob=str(data[0][60])if str(data[0][60]) !='None' else ''
    new_anu_income=str(data[0][90])if str(data[0][90]) !='None' else ''
    Occupation=str(data[0][39])if str(data[0][39]) !='None' else ''
    account_type=str(data[0][13])if str(data[0][13]) !='None' else ''
    account_status=str(data[0][102])if str(data[0][102]) !='None' else ''


    city_town_vill            = str(data[0][53])
    city            = str(data[0][18])
    state         = str(data[0][54])
    country           = str(data[0][55])
    pin_code      = data[0][19]
    permanent_add_1 = str(data[0][52])
    permanent_add_2 = str(data[0][62])
    email         = data[0][7]
    segment         = str(data[0][8])
    marital_status   = str(data[0][61])
    date_d       = data[0][32]
    date_time = datetime.datetime.fromisoformat(str(date_d))
    date_d=date_time.strftime("%d-%m-%Y")
    gross_anu_income   = str(data[0][37])
    dp_id=str(data[0][23])if str(data[0][23])!='None'else ''
    dp_type=str(data[0][24])
    email_dependency=str(data[0][100])
    adhar_number=str(data[0][104])
    occupation    = str(data[0][39])
    bank_name     = str(data[0][40])
    bank_acc_no   = str(data[0][45])
    # branch        = str(data[0][43])
    branch        = 'Noida'
    ifsc          = str(data[0][41])
    micr          = str(data[0][42])
    bank_address  = str(data[0][44])
    account_type  = str(data[0][13])
    trading_ex=str(data[0][59])
    addhar_addres=str(data[0][60])
    if data[0][34]=="":
        mobile=data[0][6]
    else:
        mobile=data[0][34]

    #transposed = signature.rotate(90)
    date_d       = data[0][32]
    date_time = datetime.datetime.fromisoformat(str(date_d))
    date_d=date_time.strftime("%d- %m- %Y")
    segment         = data[0][8]
    esign1="E-signed by: "+data[0][2]
    esign2="Date: "+str(datetime.datetime.now())
    current_date = datetime.datetime.now().strftime("%d/%m/%Y")
    esign3="Reason: ACCOUNT OPENING"
    adhar_number=str(data[0][104])
    mergedObject = PdfFileMerger()
    current_date = datetime.datetime.now().strftime("%d/%m/%Y")

    for i in range(2):
        # if i != 1:
        #   continue
        print(i)
        packet = io.BytesIO()
        # create a new PDF with Reportlab
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFontSize(10) 

        if i==0:
            # can.drawString(26,680,"✓")#Regular DematAccount
            # can.drawString(26,670,"✓")#BSDA Account
            can.setFontSize(8)
            can.drawString(79,436,"✓")#I/We wish to modify
            can.drawString(79,399,"✓")#There are no changes in respect of my/our Name
            can.drawString(79,348,"✓")#I do not wish to nominate
            can.drawString(79,335,"✓")#I do wish to nominate
            can.drawString(156,588,clientcode,charSpace=5)#1
            # can.drawString(245,182,clientcode,charSpace=8)#2
            can.drawString(75,718,current_date,charSpace=1)#1
            # can.drawString(490,182,current_date,charSpace=1)#2
            can.drawString(453,588,branch,charSpace=1)#2
            can.drawString(80,600,name) 
            #can.drawImage(data[0][30],80,195,width=80,height=30)#wetsignture
            # can.setFontSize(6)
            # can.drawString(100,136,esign1)
            # can.drawString(100,130,esign2)
            # can.drawString(100,123,esign3)  
                
        if i==1:
            can.drawString(100,730,name) 
            can.drawString(150,715,father_name) 
            can.drawString(150,700,mother_name) 
            can.drawString(108,622,pan,charSpace=6) 
            can.drawString(300,622,adhar_number,charSpace=6) 
            can.drawString(375,665,dob,charSpace=5) 
            if gender =="male":
                can.drawString(108,670,"✓")
            else:
                can.drawString(137,670,"✓")
                
            if marital_status == "single":
                can.drawString(240,670,"✓")#Single
            else:
                can.drawString(272,670,"✓")#Married

            can.drawString(120,655,"✓")#Nationality
            can.drawString(156,642,"✓")#Resident Individual 
            
            
            can.setFontSize(8)
            can.drawString(222,412,adhar_number[8:],charSpace=4)#aadhaar
            can.drawString(80,560,permanent_add_1)
            can.drawString(80,550,permanent_add_2)
            can.setFontSize(10)
            can.drawString(136,535,city_town_vill)
            # can.drawString(320,535,city)
            can.drawString(479,523,pin_code,charSpace=7)
            can.drawString(125,523,state)

            can.drawString(330,523,country)#residential
            can.drawString(250,427,mobile,charSpace=7.5)
            can.drawString(400,427,email)

            #Declaration
            can.drawString(85,363,city)
            # can.drawString(330,363,current_date)
            #can.drawImage(data[0][30], 430,368,width=80,height=30)#wetsignture
            
            #annual_Income
            if new_anu_income == "below 1 lac":
                can.drawString(150,260,"✓")#up 1
            elif new_anu_income == "1-5 lac":
                can.drawString(220,260,"✓")#1-5
            elif new_anu_income == "5-10 lac":
                can.drawString(320,260,"✓")#5-10
            elif new_anu_income == "10-25 lac":
                can.drawString(151,250,"✓")#10-25
            elif new_anu_income == ">1Cr lac":
                can.drawString(260,250,"✓")#25-1core
            elif new_anu_income == ">1Cr lac":
                can.drawString(370,250,"✓")#>1core
            #Occupation
            if 'Private' in Occupation.lower():
                can.drawString(150,220,"✓")#private
            elif 'Public Sector' in Occupation.lower():
                can.drawString(150,220,"✓")#private
            elif 'Government Service' in Occupation.lower() :
                can.drawString(225,220,"✓")#govt
            elif 'Business' in Occupation.lower():
                can.drawString(297,220,"✓")#B
            elif 'Professional' in Occupation.lower():
                can.drawString(335,220,"✓")#Pro
            elif 'Agriculturist' in Occupation.lower():
                can.drawString(382,220,"✓")#Ag
            elif 'Retired' in Occupation.lower():
                can.drawString(150,208,"✓")#Re
            elif 'House Wife' in Occupation.lower():
                can.drawString(185,208,"✓")#house
            elif 'Student' in Occupation.lower():
                can.drawString(227,208,"✓")#student
            elif 'Other' in Occupation.lower():
                can.drawString(260,208,"✓")#other
            #bank details
            can.setFontSize(8)
            can.drawString(118,138,bank_name)#bank
            can.drawString(118,125,bank_address)#bankaddress
            can.drawString(116,109,bank_acc_no.replace('-',''),charSpace=6.5)#account no
            
            if account_type.lower()== 'Saving':
                can.drawString(334,111,"✓")#saving
            else:
                can.drawString(362,111,"✓")#current
            # can.drawString(393,111,"✓")#NRI
            # can.drawString(446,111,"✓")#other
            can.drawString(124,90,micr,charSpace=15)#micr
            can.drawString(350,90,ifsc,charSpace=13)#ifsc
        if i==2:
            pass

            

        can.save()
        #move to the beginning of the StringIO buffer
        packet.seek(0)
        new_pdf = PdfFileReader(packet)
        # read your existing PDF
        existing_pdf = PdfFileReader(open("Reactivation_form.pdf", "rb"))
        output = PdfFileWriter()
        # add the "watermark" (which is the new pdf) on the existing page
        page = existing_pdf.getPage(i)
        page.mergePage(new_pdf.getPage(0))
        output.addPage(page)
        # finally, write "output" to a real file
        outputStream = open("static/rekycPDF/"+str(clientcode)+"/destination"+str(i)+".pdf", "wb")
        output.write(outputStream)
        outputStream.close()
        mergedObject.append(PdfFileReader("static/rekycPDF/"+str(clientcode)+"/destination"+str(i)+".pdf", "rb"), import_bookmarks=False)


    try:
        os.remove("static/rekycPDF/"+str(clientcode)+"/reactivationPDF.pdf")
    except:
        pass
        #pdf_FILE_name=get_random_string(6)  
    mergedObject.write("static/rekycPDF/"+clientcode+"/reactivationPDF.pdf")
    return "static/rekycPDF/"+clientcode+"/reactivationPDF.pdf"
    
cors = CORS(pdfOperationsapi)


