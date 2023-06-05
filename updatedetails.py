from flask import Blueprint, Flask, request, jsonify, render_template,session,send_from_directory,redirect,url_for
from flask_cors import CORS
import requests
import json
import random
import string
import sqlite3
import datetime
conn_Emkay_digilocker = sqlite3.connect('Emkay_digilocker.db',check_same_thread=False)
from pdfOperationsBeforeESIGN import *

import os
from wand.image import Image as wi

from PIL import Image
from PyPDF2 import PdfFileWriter, PdfFileReader
import base64


updatedetailsapi = Blueprint('updatedetailsapi', __name__)

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders
def mailsending(from_,pass_,subject,body,toadd,cc,sendgrid):
    def login(sendgrid):
        s = smtplib.SMTP('emkaytransact.icewarpcloud.in', 587)
        s.starttls()
        s.login('rekyc_support@emkayglobal.in','aIbrw:lq2')
        return s
    def mail(toaadr,fromaddr,subject,body):
        

        msg = MIMEMultipart()
        msg['From'] = fromaddr
        add=toaadr
        msg['To'] = toaadr
        msg['cc'] =','.join(cc)

        qw=[]
        qw.append(toaadr)
        for i in range(0,len(cc)):
            qw.append(cc[i])

        body = body
        msg['Subject']=subject
        msg.attach(MIMEText(body,'html'))
        text = msg.as_string()
        s =login(sendgrid)
        
        s.sendmail(fromaddr, qw, text)
            
        print("new login")
        
    try :
        mail(toadd,from_,subject,body)
    except Exception as e:
        pass
        print(e)








def random_char(y):
        return ''.join(random.choice(string.digits) for x in range(y))




@updatedetailsapi.route('/updateEmail', methods=['POST'])
def updateEmail():
        data=request.get_json()
        clientcode=data['clientcode']
        clientcode=clientcode.lower()

        email=data['email']

        otp=random_char(4)
        body="Your OTP is "+ otp
        print(body)
        print(clientcode)
        chk=conn_Emkay_digilocker.execute('SELECT email,name FROM userdetails WHERE clientcode = "'+clientcode+'"').fetchall()

        if chk[0][0].lower()==email.lower():
            return jsonify({'msg':"You can't update the same email."})

        conn_Emkay_digilocker.execute("UPDATE userdetails SET otp='"+otp+"' where clientcode = '"+clientcode+"'")
        conn_Emkay_digilocker.commit()


        text='Your OTP for email Verify is: '+otp
        body='''<html>
                <head>
                  <title></title>
                </head>
                <body>
                <div style="background-color:#f0f1f3;font-family:'Poppins',sans-serif;font-size:18px;line-height:28px;margin:0;color:#1F346D;">
                    <div class="m_2513597272243517713gutter" style="padding:5px 0;">&nbsp;</div>
                    <div class="m_2513597272243517713root" style="margin:0 20px;">
                      <table class="m_2513597272243517713header" style="max-width:600px;margin:0 auto 5px auto;width:100%;">
                        <tbody>
                            <tr>
                              <td align="center" colspan="2">
                                <a href="" style="color:#387ed1;" target="_blank">
                                  <img alt="LOGO" src='https://www.emkayglobal.com/images/logo.png' style="width: 45%;">
                                </a>
                              </td>
                            </tr>
                        </tbody>
                      </table>
                      <p>Dear '''+chk[0][1]+''',<br/><br/>Welcome to Emkay Global Financial Services Ltd. <br/>Thank you for choosing us as your preferred Investment Partner. <br/>You can proceed further by filling  the online Re-KYC application form.<br/></p>
                      <p class="m_2513597272243517713wrap" > '''+text+'''<br/><br/> If you have any queries/concerns, you can call us at 022-66299299 or mail us at rekyc_support@emkayglobal.in</p><br/>
                      <p>Warm Regards,<br/>Team RE-KYC<br/>Emkay Global Financial Services Ltd.</p>
                      <div class="m_2513597272243517713footer" style="text-align:center;color:#1F346D;font-size:11px;">
                        
                </body>
                </html>'''

        #body= textile.textile(sendBody)
        #email='sandeepkumarpushp@gmail.com'
        mailsending("rekyc_support@emkayglobal.in",'',"Emkay Global Financial Services Ltd. ReKYC - Email Verify OTP",body,email,['',''],"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")

        return jsonify({'msg':'OTP has been sent sucessfully'})



@updatedetailsapi.route('/updateEmailverify', methods=['POST'])
def updateEmailverify():
        data=request.get_json()
        email=data['email']
        otp=data['emailotp']
        email_dependency = data['email_dependency']
        email_dependency_name = data['email_dependency_name']
        clientcode=data['clientcode'].lower()
        
        print(email)
        chk=conn_Emkay_digilocker.execute('SELECT otp,email,name FROM userdetails WHERE clientcode = "'+clientcode+'"').fetchall()
        print(chk)
        name=chk[0][2]
        if chk[0][0]!=otp:
                return jsonify({'data':'Invalid OTP'})

          
        conn_Emkay_digilocker.execute("UPDATE userdetails SET new_email='"+email+"', email_dependency_name='"+email_dependency_name+"', email_dependency='"+email_dependency+"', emailchangeyesno='yes' where clientcode = '"+clientcode+"'")
        conn_Emkay_digilocker.commit()


        #body='clientcode: '+clientcode+' email'+email

        text='Your Email has been verified Sucessfully. Please continue if you want to do further changes. And click on Next button to see further changes options.'
        body='''<html>
                <head>
                  <title></title>
                </head>
                <body>
                <div style="background-color:#f0f1f3;font-family:'Poppins',sans-serif;font-size:18px;line-height:28px;margin:0;color:#1F346D;">
                    <div class="m_2513597272243517713gutter" style="padding:5px 0;">&nbsp;</div>
                    <div class="m_2513597272243517713root" style="margin:0 20px;">
                      <table class="m_2513597272243517713header" style="max-width:600px;margin:0 auto 5px auto;width:100%;">
                        <tbody>
                            <tr>
                              <td align="center" colspan="2">
                                <a href="" style="color:#387ed1;" target="_blank">
                                  <img alt="LOGO" src='https://www.emkayglobal.com/images/logo.png' style="width: 45%;">
                                </a>
                              </td>
                            </tr>
                        </tbody>
                      </table>
                      <p>Dear '''+name+''',<br/></p>
                      <p class="m_2513597272243517713wrap" > '''+text+'''<br/><br/> If you have any queries/concerns, you can call us at 022-66299299 or mail us at rekyc_support@emkayglobal.in</p><br/>
                      <p>Warm Regards,<br/>Team RE-KYC<br/>Emkay Global Financial Services Ltd.</p>
                      <div class="m_2513597272243517713footer" style="text-align:center;color:#1F346D;font-size:11px;">
                        
                </body>
                </html>'''

        #body= textile.textile(sendBody)
        #email='sandeepkumarpushp@gmail.com'
        mailsending("rekyc_support@emkayglobal.in",'',"Emkay Global Financial Services Ltd. ReKYC Email Updated Sucessfully",body,email,['',''],"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")

        return jsonify({'msg':'Email has been verified sucessfully. Please continue if you want to do further changes. And click on Next button to see further changes options.'})



@updatedetailsapi.route('/updatePhone', methods=['POST'])
def updatePhone():
        data=request.get_json()

        phone=data['phone']
        clientcode=data['clientcode'].lower()

        otp=random_char(4)
        print(otp)

        chk=conn_Emkay_digilocker.execute('SELECT mobile FROM userdetails WHERE clientcode = "'+clientcode+'"').fetchall()[0][0]
        if chk==phone:
                return jsonify({'msg':"You can't update the same mobile."})

        conn_Emkay_digilocker.execute("UPDATE userdetails SET otp='"+otp+"' where clientcode = '"+clientcode+"'")
        conn_Emkay_digilocker.commit()

        try:
            url='http://sms.cell24x7.com:1111/mspProducerM/sendSMS?user=EMKAYIPO&pwd=apiemkayipo&sender=EMKAYG&mobile=91'+phone+'&msg='+otp+' is Your OTP for RE-KYC Registration with Emkay Global Financial Services Ltd. Do not Disclose this with anyone for your security&mt=0'
            response=requests.get(url,timeout=15)
            print(response.text)
        except Exception as e:
            print (e)
        return jsonify({'msg':'OTP has been sent sucessfully'})





@updatedetailsapi.route('/updatePhonelverify', methods=['POST'])
def updatePhonelverify():
        data=request.get_json()
        phone=data['phone']
        otp=data['phoneotp']
        mobile_dependency = data['mobile_dependency']
        mobile_dependency_name = data['mobile_dependency_name']
        clientcode=data['clientcode'].lower()

        chk=conn_Emkay_digilocker.execute('SELECT otp,email,new_email,name FROM userdetails WHERE clientcode = "'+clientcode+'"').fetchall()
        print(chk)
        if chk[0][0]!=otp:
                return jsonify({'data':'Invalid OTP'})
        name=chk[0][3]
        if chk[0][2]!='' and chk[0][2]!=None:
            email=chk[0][2]
        else:
            email=chk[0][1]

        #conn_Emkay_digilocker.execute("UPDATE userdetails SET mobile='"+phone+"', mobilechangeyesno='yes' where clientcode = '"+clientcode+"'")
        conn_Emkay_digilocker.execute("UPDATE userdetails SET new_mobile='"+phone+"', mobile_dependency_name='"+mobile_dependency_name+"', mobile_dependency='"+mobile_dependency+"', mobilechangeyesno='yes' where clientcode = '"+clientcode+"'")
        conn_Emkay_digilocker.commit()
        text='Your Mobile number has been verified Sucessfully. Please continue if you want to do further changes. And click on Next button to see further changes options.'
        body='''<html>
                <head>
                  <title></title>
                </head>
                <body>
                <div style="background-color:#f0f1f3;font-family:'Poppins',sans-serif;font-size:18px;line-height:28px;margin:0;color:#1F346D;">
                    <div class="m_2513597272243517713gutter" style="padding:5px 0;">&nbsp;</div>
                    <div class="m_2513597272243517713root" style="margin:0 20px;">
                      <table class="m_2513597272243517713header" style="max-width:600px;margin:0 auto 5px auto;width:100%;">
                        <tbody>
                            <tr>
                              <td align="center" colspan="2">
                                <a href="" style="color:#387ed1;" target="_blank">
                                  <img alt="LOGO" src='https://www.emkayglobal.com/images/logo.png' style="width: 45%;">
                                </a>
                              </td>
                            </tr>
                        </tbody>
                      </table>
                      <p>Dear '''+name+''',<br/></p>
                      <p class="m_2513597272243517713wrap" > '''+text+'''<br/><br/> If you have any queries/concerns, you can call us at 022-66299299 or mail us at rekyc_support@emkayglobal.in</p><br/>
                      <p>Warm Regards,<br/>Team RE-KYC<br/>Emkay Global Financial Services Ltd.</p>
                      <div class="m_2513597272243517713footer" style="text-align:center;color:#1F346D;font-size:11px;">
                        
                </body>
                </html>'''


        mailsending("rekyc_support@emkayglobal.in",'',"Emkay Global Financial Services Ltd. ReKYC Mobile Updated sucessfully",body,email,['',''],"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")

        #Update into main Table
        return jsonify({'message':'Phone has been verified sucessfully. Please continue if you want to do further changes. And click on Next button to see further changes options.'})


@updatedetailsapi.route('/other', methods=['POST'])
def other():
    
    
    data=request.get_json()
    segment=data['segment'].split(',')
    print(segment)
    nominee_check=data['nominee_check']
    annual_income=data['annual_income']
    clientcode=data['clientcode'].lower()

    newSegment=''
    chk = conn_Emkay_digilocker.execute('SELECT segment from userdetails WHERE clientcode="'+str(clientcode)+'" ').fetchall()
    if chk[0][0][0]=='Y' and segment[0]=='true':
        newSegment=newSegment+'false'
    else:
        newSegment=newSegment+segment[0]

    if chk[0][0][1]=='Y' and segment[1]=='true':
        newSegment=newSegment+","+'false'
    else:
        newSegment=newSegment+","+segment[1]

    if chk[0][0][2]=='Y' and segment[2]=='true':
        newSegment=newSegment+","+'false'
    else:
        newSegment=newSegment+","+segment[2]

    if chk[0][0][3]=='Y' and segment[3]=='true':
        newSegment=newSegment+","+'false'
    else:
        newSegment=newSegment+","+segment[3]

    if chk[0][0][4]=='Y' and segment[4]=='true':
        newSegment=newSegment+","+'false'
    else:
        newSegment=newSegment+","+segment[4]

    if chk[0][0][5]=='Y' and segment[5]=='true':
        newSegment=newSegment+","+'false'
    else:
        newSegment=newSegment+","+segment[5]

    if chk[0][0][6]=='Y' and segment[6]=='true':
        newSegment=newSegment+","+'false'
    else:
        newSegment=newSegment+","+segment[6]

    if chk[0][0][7]=='Y' and segment[7]=='true':
        newSegment=newSegment+","+'false'
    else:
        newSegment=newSegment+","+segment[7]

    if chk[0][0][8]=='Y' and segment[8]=='true':
        newSegment=newSegment+","+'false'
    else:
        newSegment=newSegment+","+segment[8]

    if chk[0][0][9]=='Y' and segment[9]=='true':
        newSegment=newSegment+","+'false'
    else:
        newSegment=newSegment+","+segment[9]

    if chk[0][0][10]=='Y' and segment[10]=='true':
        newSegment=newSegment+","+'false'
    else:
        newSegment=newSegment+","+segment[10]
        
    if chk[0][0][11]=='Y' and segment[11]=='true':
        newSegment=newSegment+","+'false'
    else:
        newSegment=newSegment+","+segment[11]
        
    if chk[0][0][12]=='Y' and segment[12]=='true':
        newSegment=newSegment+","+'false'
    else:
        newSegment=newSegment+","+segment[12]

    if 'true' in newSegment:
        conn_Emkay_digilocker.execute("UPDATE userdetails SET nominee_check='"+nominee_check+"', newSegment='"+newSegment+"', new_annual_income='"+annual_income+"', segmentactivationyesno='yes' where clientcode = '"+clientcode+"'")
        conn_Emkay_digilocker.commit()
    else:
        conn_Emkay_digilocker.execute("UPDATE userdetails SET nominee_check='"+nominee_check+"', newSegment='"+newSegment+"', new_annual_income='"+annual_income+"', segmentactivationyesno='no' where clientcode = '"+clientcode+"'")
        conn_Emkay_digilocker.commit()
        #Update into main Table
    return jsonify({'message':'Others has been verified sucessfully'})




@updatedetailsapi.route('/rekycGetNomineeDetails', methods=['POST'])
def rekycGetNomineeDetails():
    data = request.get_json()

    clientcode=data['clientcode'].lower()
    Nominee1_name=str(data['Nominee1_name'])
    Nominee1_PAN=str(data['Nominee1_PAN'])
    Nominee1_DOB=str(data['Nominee1_DOB'])
    Nominee1_relation=str(data['Nominee1_relation'])
    Nominee1_address1=str(data['Nominee1_address1'])
    Nominee1_address2=str(data['Nominee1_address2'])
    Nominee1_city=str(data['Nominee1_city'])
    Nominee1_state=str(data['Nominee1_state'])
    Nominee1_country=str(data['Nominee1_country'])
    Nominee1_pincode=str(data['Nominee1_pincode'])
    Nominee1_mobile=str(data['Nominee1_mobile'])
    Nominee1_email=str(data['Nominee1_email'])
    Nominee1_percentage=str(data['Nominee1_percentage'])
    nominee1_doc_type = str(data['Nominee1_Select_id'])

    Nominee2_name=str(data['Nominee2_name'])
    Nominee2_PAN=str(data['Nominee2_PAN'])
    Nominee2_DOB=str(data['Nominee2_DOB'])
    Nominee2_relation=str(data['Nominee2_relation'])
    Nominee2_address1=str(data['Nominee2_address1'])
    Nominee2_address2=str(data['Nominee2_address2'])
    Nominee2_city=str(data['Nominee2_city'])
    Nominee2_state=str(data['Nominee2_state'])
    Nominee2_country=str(data['Nominee2_country'])
    Nominee2_pincode=str(data['Nominee2_pincode'])
    Nominee2_mobile=str(data['Nominee2_mobile'])
    Nominee2_email=str(data['Nominee2_email'])
    Nominee2_percentage=str(data['Nominee2_percentage'])
    nominee2_doc_type = str(data['Nominee2_Select_id'])

    Nominee3_name=str(data['Nominee3_name'])
    Nominee3_PAN=str(data['Nominee3_PAN'])
    Nominee3_DOB=str(data['Nominee3_DOB'])
    Nominee3_relation=str(data['Nominee3_relation'])
    Nominee3_address1=str(data['Nominee3_address1'])
    Nominee3_address2=str(data['Nominee3_address2'])
    Nominee3_city=str(data['Nominee3_city'])
    Nominee3_state=str(data['Nominee3_state'])
    Nominee3_country=str(data['Nominee3_country'])
    Nominee3_pincode=str(data['Nominee3_pincode'])
    Nominee3_mobile=str(data['Nominee3_mobile'])
    Nominee3_email=str(data['Nominee3_email'])
    Nominee3_percentage=str(data['Nominee3_percentage'])
    nominee3_doc_type = str(data['Nominee3_Select_id'])

    ##########################################################   Guardian        #####################################################################
    Guardian_name=str(data['Guardian_name'])
    Guardian_dob=str(data['Guardian_dob'])
    Guardian_address=str(data['Guardian_address'])
    Guardian_city=str(data['Guardian_city'])
    Guardian_state=str(data['Guardian_state'])
    Guardian_country=str(data['Guardian_country'])
    Guardian_mobile=str(data['Guardian_mobile'])
    Guardian_email=str(data['Guardian_email'])
    Guardian_relation=str(data['Guardian_relation'])
    Guardian_doc_type=str(data['Guardian_doc_type'])
    Guardian_pincode=str(data['Guardian_pincode'])
    ################################Guardian2 #########################
    Guardian_name2=str(data['Guardian_name2'])
    Guardian_dob2=str(data['Guardian_dob2'])
    Guardian_address2=str(data['Guardian_address2'])
    Guardian_city2=str(data['Guardian_city2'])
    Guardian_state2=str(data['Guardian_state2'])
    Guardian_country2=str(data['Guardian_country2'])
    Guardian_mobile2=str(data['Guardian_mobile2'])
    Guardian_email2=str(data['Guardian_email2'])
    Guardian_relation2=str(data['Guardian_relation2'])
    Guardian_doc_type2=str(data['Guardian_doc_type2'])
    Guardian_pincode2=str(data['Guardian_pincode2'])
    ##########################################Guardian3 #######################################
    Guardian_name3=str(data['Guardian_name3'])
    Guardian_dob3=str(data['Guardian_dob3'])
    Guardian_address3=str(data['Guardian_address3'])
    Guardian_city3=str(data['Guardian_city3'])
    Guardian_state3=str(data['Guardian_state3'])
    Guardian_country3=str(data['Guardian_country3'])
    Guardian_mobile3=str(data['Guardian_mobile3'])
    Guardian_email3=str(data['Guardian_email3'])
    Guardian_relation3=str(data['Guardian_relation3'])
    Guardian_doc_type3=str(data['Guardian_doc_type3'])
    Guardian_pincode3=str(data['Guardian_pincode3'])

    

    conn_Emkay_digilocker.execute("UPDATE userdetails SET Nominee1_name='"+Nominee1_name+"', nominee1_doc_type='"+nominee1_doc_type+"', Nominee1_PAN='"+Nominee1_PAN+"', Nominee1_DOB='"+Nominee1_DOB+"', Nominee1_relation='"+Nominee1_relation+"', Nominee1_address1='"+Nominee1_address1+"', Nominee1_address2='"+Nominee1_address2+"', Nominee1_city='"+Nominee1_city+"', Nominee1_state='"+Nominee1_state+"', Nominee1_country='"+Nominee1_country+"', Nominee1_pincode='"+Nominee1_pincode+"', Nominee1_mobile='"+Nominee1_mobile+"', Nominee1_email='"+Nominee1_email+"', Nominee1_percentage='"+Nominee1_percentage+"' WHERE clientcode='"+clientcode+"'")
    conn_Emkay_digilocker.commit()

    conn_Emkay_digilocker.execute("UPDATE userdetails SET Nominee2_name='"+Nominee2_name+"', nominee2_doc_type='"+nominee2_doc_type+"', Nominee2_PAN='"+Nominee2_PAN+"', Nominee2_DOB='"+Nominee2_DOB+"', Nominee2_relation='"+Nominee2_relation+"', Nominee2_address1='"+Nominee2_address1+"', Nominee2_address2='"+Nominee2_address2+"', Nominee2_city='"+Nominee2_city+"', Nominee2_state='"+Nominee2_state+"', Nominee2_country='"+Nominee2_country+"', Nominee2_pincode='"+Nominee2_pincode+"', Nominee2_mobile='"+Nominee2_mobile+"', Nominee2_email='"+Nominee2_email+"', Nominee2_percentage='"+Nominee2_percentage+"' WHERE clientcode='"+clientcode+"'")
    conn_Emkay_digilocker.commit()

    conn_Emkay_digilocker.execute("UPDATE userdetails SET Nominee3_name='"+Nominee3_name+"', nominee3_doc_type='"+nominee3_doc_type+"', Nominee3_name='"+Nominee3_name+"', Nominee3_PAN='"+Nominee3_PAN+"', Nominee3_DOB='"+Nominee3_DOB+"', Nominee3_relation='"+Nominee3_relation+"', Nominee3_address1='"+Nominee3_address1+"', Nominee3_address2='"+Nominee3_address2+"', Nominee3_city='"+Nominee3_city+"', Nominee3_state='"+Nominee3_state+"', Nominee3_country='"+Nominee3_country+"', Nominee3_pincode='"+Nominee3_pincode+"', Nominee3_mobile='"+Nominee3_mobile+"', Nominee3_email='"+Nominee3_email+"', Nominee3_percentage='"+Nominee3_percentage+"' WHERE clientcode='"+clientcode+"'")
    conn_Emkay_digilocker.commit()

    conn_Emkay_digilocker.execute("UPDATE userdetails SET  Guardian_name='"+Guardian_name+"', Guardian_dob='"+Guardian_dob+"', Guardian_address='"+Guardian_address+"', Guardian_city='"+Guardian_city+"', Guardian_state='"+Guardian_state+"', Guardian_country='"+Guardian_country+"', Guardian_mobile='"+Guardian_mobile+"', Guardian_email='"+Guardian_email+"', Guardian_relation='"+Guardian_relation+"', Guardian_doc_type='"+Guardian_doc_type+"', Guardian_pincode='"+Guardian_pincode+"' where clientcode = '"+clientcode+"'")
    conn_Emkay_digilocker.commit()

    conn_Emkay_digilocker.execute("UPDATE userdetails SET Guardian_name2='"+Guardian_name2+"', Guardian_dob2='"+Guardian_dob2+"', Guardian_address2='"+Guardian_address2+"', Guardian_city2='"+Guardian_city2+"', Guardian_state2='"+Guardian_state2+"', Guardian_country2='"+Guardian_country2+"', Guardian_mobile2='"+Guardian_mobile2+"', Guardian_email2='"+Guardian_email2+"', Guardian_relation2='"+Guardian_relation2+"', Guardian_doc_type2='"+Guardian_doc_type2+"', Guardian_pincode2='"+Guardian_pincode+"' where clientcode = '"+clientcode+"'")
    conn_Emkay_digilocker.commit()

    conn_Emkay_digilocker.execute("UPDATE userdetails SET Guardian_name3='"+Guardian_name3+"', Guardian_dob3='"+Guardian_dob3+"', Guardian_address3='"+Guardian_address3+"', Guardian_city3='"+Guardian_city3+"', Guardian_state3='"+Guardian_state3+"', Guardian_country3='"+Guardian_country3+"', Guardian_mobile3='"+Guardian_mobile3+"', Guardian_email3='"+Guardian_email3+"', Guardian_relation3='"+Guardian_relation3+"', Guardian_doc_type3='"+Guardian_doc_type3+"', Guardian_pincode3='"+Guardian_pincode3+"' where clientcode = '"+clientcode+"'")
    conn_Emkay_digilocker.commit()

    conn_Emkay_digilocker.execute("UPDATE userdetails SET changes='Nominee',nominee_check='yes' WHERE clientcode='"+clientcode+"'")
    conn_Emkay_digilocker.commit()

    return jsonify({"data": "All Nominee details updated."})

@updatedetailsapi.route('/rekycUploadNomineeDetails/<clientcode>', methods=['POST'])
def rekycUploadNomineeDetails(clientcode):
    clientcode=clientcode.lower()
    chk=(os.path.isdir("static/userUpload/"+str(clientcode)))
    print(chk)
    path = "static/userUpload/"+str(clientcode)+"/"
    if chk==False:
        try:
            os.mkdir("static/joindre/userUpload")
        except:
            pass
        try:
            os.mkdir("static/userUpload/"+str(clientcode))
                                 
            
        except:
            pass


    path = "static/userUpload/"+str(clientcode)+"/"
    if "Nominee1" in request.files:
            nom1_file=request.files['Nominee1']
            nom1FileName=nom1_file.filename
            nom1_file.save(path+nom1FileName)
            print(nom1FileName)
            if 'png' in nom1FileName.split('.')[-1] or 'PNG' in nom1FileName.split('.')[-1] or 'jpg' in nom1FileName.split('.')[-1] or 'JPG' in nom1FileName.split('.')[-1] or 'jpeg' in nom1FileName.split('.')[-1] or 'JPEG' in nom1FileName.split('.')[-1]:
                im = Image.open(path+nom1FileName)
                rgb_im = im.convert('RGB')
                imageSizeBytes=os.path.getsize(path+nom1FileName)
                nom1FileName=nom1FileName.split('.')[-2]
                print(nom1FileName)
                quality=getImageQuality(imageSizeBytes)

                rgb_im.save(path+nom1FileName+'.jpg',quality=quality,optimize=True)
                nom1FileName=nom1FileName+'.jpg'
                print(nom1FileName)
            if str(path+nom1FileName).split('.')[-1]=='pdf' or str(path+nom1FileName).split('.')[-1]=='PDF':
                    PDFfile = wi(filename=path+nom1FileName+'[0]',resolution=150)
                    PDFfile.save(filename=path+'nom1.jpg')
                    nom1FileName='nom1.jpg'
            conn_Emkay_digilocker.execute("UPDATE userdetails SET uploadnom1='"+path+nom1FileName+"' where clientcode = '"+clientcode+"'")
            conn_Emkay_digilocker.commit()
    if "Nominee2" in request.files:
            # path = "static/userupload/"
            nom2_file=request.files['Nominee2']
            nom2FileName=nom2_file.filename
            nom2_file.save(path+nom2FileName)
            print(nom2FileName)
            if 'png' in nom2FileName.split('.')[-1] or 'PNG' in nom2FileName.split('.')[-1] or 'jpg' in nom2FileName.split('.')[-1] or 'JPG' in nom2FileName.split('.')[-1] or 'jpeg' in nom2FileName.split('.')[-1] or 'JPEG' in nom2FileName.split('.')[-1]:
                im = Image.open(path+nom2FileName)
                rgb_im = im.convert('RGB')
                imageSizeBytes=os.path.getsize(path+nom2FileName)
                nom2FileName=nom2FileName.split('.')[-2]
                print(nom2FileName)
                quality=getImageQuality(imageSizeBytes)

                rgb_im.save(path+nom2FileName+'.jpg',quality=quality,optimize=True)
                nom2FileName=nom2FileName+'.jpg'
                print(nom2FileName)
            if str(path+nom2FileName).split('.')[-1]=='pdf' or str(path+nom2FileName).split('.')[-1]=='PDF':
                    PDFfile = wi(filename=path+nom2FileName+'[0]',resolution=150)
                    PDFfile.save(filename=path+'nom2.jpg')
                    nom2FileName='nom2.jpg'
            conn_Emkay_digilocker.execute("UPDATE userdetails SET uploadnom2='"+path+nom2FileName+"' where clientcode = '"+clientcode+"'")
            conn_Emkay_digilocker.commit()
    if "Nominee3" in request.files:
            # path = "static/userupload/"
            nom3_file=request.files['Nominee3']
            nom3FileName=nom3_file.filename
            nom3_file.save(path+nom3FileName)
            print(nom3FileName)
            if 'png' in nom3FileName.split('.')[-1] or 'PNG' in nom3FileName.split('.')[-1] or 'jpg' in nom3FileName.split('.')[-1] or 'JPG' in nom3FileName.split('.')[-1] or 'jpeg' in nom3FileName.split('.')[-1] or 'JPEG' in nom3FileName.split('.')[-1]:
                im = Image.open(path+nom3FileName)
                rgb_im = im.convert('RGB')
                imageSizeBytes=os.path.getsize(path+nom3FileName)
                nom3FileName=nom3FileName.split('.')[-2]
                print(nom3FileName)
                quality=getImageQuality(imageSizeBytes)

                rgb_im.save(path+nom3FileName+'.jpg',quality=quality,optimize=True)
                nom3FileName=nom3FileName+'.jpg'
                print(nom3FileName)
            if str(path+nom3FileName).split('.')[-1]=='pdf' or str(path+nom3FileName).split('.')[-1]=='PDF':
                    PDFfile = wi(filename=path+nom3FileName+'[0]',resolution=150)
                    PDFfile.save(filename=path+'nom3.jpg')
                    nom3FileName='nom3.jpg'
            conn_Emkay_digilocker.execute("UPDATE userdetails SET uploadnom3='"+path+nom3FileName+"' where clientcode = '"+clientcode+"'")
            conn_Emkay_digilocker.commit()

    if "Guardian_doc_name" in request.files:
            #path = "static/userupload/"
            Guardian_doc_file=request.files['Guardian_doc_name']
            Guardian_doc_FileName=Guardian_doc_file.filename
            # Guardian_doc_FileName='Guardian1_'+Guardian_doc_type+'_'+str(datetime.datetime.now()).replace("-","_").replace(" ","_").replace(":","_").replace(".","_")+'.'+Guardian_doc_FileName.split('.')[-1]
            Guardian_doc_file.save(path+Guardian_doc_FileName)
            print(Guardian_doc_FileName)
            if 'png' in Guardian_doc_FileName.split('.')[-1] or 'PNG' in Guardian_doc_FileName.split('.')[-1] or 'jpg' in Guardian_doc_FileName.split('.')[-1] or 'JPG' in Guardian_doc_FileName.split('.')[-1] or 'jpeg' in Guardian_doc_FileName.split('.')[-1] or 'JPEG' in Guardian_doc_FileName.split('.')[-1]:
                im = Image.open(path+Guardian_doc_FileName)
                rgb_im = im.convert('RGB')
                imageSizeBytes=os.path.getsize(path+Guardian_doc_FileName)
                Guardian_doc_FileName=Guardian_doc_FileName.split('.')[-2]
                print(Guardian_doc_FileName)
                quality=getImageQuality(imageSizeBytes)

                rgb_im.save(path+Guardian_doc_FileName+'.jpg',quality=quality,optimize=True)
                Guardian_doc_FileName=Guardian_doc_FileName+'.jpg'
                print(Guardian_doc_FileName)
            if str(path+Guardian_doc_FileName).split('.')[-1]=='pdf' or str(path+Guardian_doc_FileName).split('.')[-1]=='PDF':
                    PDFfile = wi(filename=path+Guardian_doc_FileName+'[0]',resolution=150)
                    PDFfile.save(filename=path+'nom3.jpg')
                    Guardian_doc_FileName='nom3.jpg'
            conn_Emkay_digilocker.execute("UPDATE userdetails SET Guardian_doc_name='"+path+Guardian_doc_FileName+"' where clientcode = '"+clientcode+"'")
            conn_Emkay_digilocker.commit()

    if "Guardian_doc_name2" in request.files:
            #path = "static/userupload/"
            Guardian_doc_file2=request.files['Guardian_doc_name2']
            Guardian_doc_FileName2=Guardian_doc_file2.filename
            # Guardian_doc_FileName2='Guardian2_'+Guardian_doc_type+'_'+str(datetime.datetime.now()).replace("-","_").replace(" ","_").replace(":","_").replace(".","_")+'.'+Guardian_doc_FileName2.split('.')[-1]
            Guardian_doc_file2.save(path+Guardian_doc_FileName2)
            print(Guardian_doc_FileName2)
            if 'png' in Guardian_doc_FileName2.split('.')[-1] or 'PNG' in Guardian_doc_FileName2.split('.')[-1] or 'jpg' in Guardian_doc_FileName2.split('.')[-1] or 'JPG' in Guardian_doc_FileName2.split('.')[-1] or 'jpeg' in Guardian_doc_FileName2.split('.')[-1] or 'JPEG' in Guardian_doc_FileName2.split('.')[-1]:
                im = Image.open(path+Guardian_doc_FileName2)
                rgb_im = im.convert('RGB')
                imageSizeBytes=os.path.getsize(path+Guardian_doc_FileName2)
                Guardian_doc_FileName2=Guardian_doc_FileName2.split('.')[-2]
                print(Guardian_doc_FileName2)
                quality=getImageQuality(imageSizeBytes)

                rgb_im.save(path+Guardian_doc_FileName2+'.jpg',quality=quality,optimize=True)
                Guardian_doc_FileName2=Guardian_doc_FileName2+'.jpg'
                print(Guardian_doc_FileName2)
            if str(path+Guardian_doc_FileName2).split('.')[-1]=='pdf' or str(path+Guardian_doc_FileName2).split('.')[-1]=='PDF':
                    PDFfile = wi(filename=path+Guardian_doc_FileName2+'[0]',resolution=150)
                    PDFfile.save(filename=path+'nom3.jpg')
                    Guardian_doc_FileName2='nom3.jpg'
            conn_Emkay_digilocker.execute("UPDATE userdetails SET Guardian_doc_name2='"+path+Guardian_doc_FileName2+"' where clientcode = '"+clientcode+"'")
            conn_Emkay_digilocker.commit()

    if "Guardian_doc_name3" in request.files:
            #path = "static/userupload/"
            Guardian_doc_file3=request.files['Guardian_doc_name3']
            Guardian_doc_FileName3=Guardian_doc_file3.filename
            # Guardian_doc_FileName3='Guardian3_'+Guardian_doc_type+'_'+str(datetime.datetime.now()).replace("-","_").replace(" ","_").replace(":","_").replace(".","_")+'.'+Guardian_doc_FileName3.split('.')[-1]
            Guardian_doc_file3.save(path+Guardian_doc_FileName3)
            print(Guardian_doc_FileName3)
            if 'png' in Guardian_doc_FileName3.split('.')[-1] or 'PNG' in Guardian_doc_FileName3.split('.')[-1] or 'jpg' in Guardian_doc_FileName3.split('.')[-1] or 'JPG' in Guardian_doc_FileName3.split('.')[-1] or 'jpeg' in Guardian_doc_FileName3.split('.')[-1] or 'JPEG' in Guardian_doc_FileName3.split('.')[-1]:
                im = Image.open(path+Guardian_doc_FileName3)
                rgb_im = im.convert('RGB')
                imageSizeBytes=os.path.getsize(path+Guardian_doc_FileName3)
                Guardian_doc_FileName3=Guardian_doc_FileName3.split('.')[-2]
                print(Guardian_doc_FileName3)
                quality=getImageQuality(imageSizeBytes)

                rgb_im.save(path+Guardian_doc_FileName3+'.jpg',quality=quality,optimize=True)
                Guardian_doc_FileName3=Guardian_doc_FileName3+'.jpg'
                print(Guardian_doc_FileName3)
            if str(path+Guardian_doc_FileName3).split('.')[-1]=='pdf' or str(path+Guardian_doc_FileName3).split('.')[-1]=='PDF':
                    PDFfile = wi(filename=path+Guardian_doc_FileName3+'[0]',resolution=150)
                    PDFfile.save(filename=path+'nom3.jpg')
                    Guardian_doc_FileName3='nom3.jpg'
            conn_Emkay_digilocker.execute("UPDATE userdetails SET Guardian_doc_name3='"+path+Guardian_doc_FileName3+"' where clientcode = '"+clientcode+"'")
            conn_Emkay_digilocker.commit()
    return jsonify({"data":"Uplaoded"})




def getImageQuality(size):
        if size<999999:
                return 50
        elif size<1999999:
                return 40
        elif size<2999999:
                return 30
        elif size<5999999:
                return 25
        else:
                return 10




@updatedetailsapi.route('/uploadUserFiles/<clientcode>', methods=['POST'])
def uploadUserFiles(clientcode):
    clientcode=clientcode.lower()


    chk=(os.path.isdir("static/userUpload/"+str(clientcode)))
    #print(chk)
    path = "static/userUpload/"+str(clientcode)+"/"
    if chk==False:
        try:
            os.mkdir("static/userUpload")
        except:
            pass
        try:
            os.mkdir("static/userUpload/"+str(clientcode))
                                 
            
        except:
            pass

    name1=str(datetime.datetime.now()).replace("-","_").replace(" ","_").replace(":","_").replace(".","_")
    
    if len(request.files)<9:
        if "financialPassword" in request.form:
            financialPassword=request.form['financialPassword']
            try:
                financial_file = request.files['financial']
                financialFileName=financial_file.filename
                financial_proof_data='yes'
            except:
                financial_proof_data='no'


            if financial_proof_data=='yes':
                financial_file.save(path+financialFileName)
                if str(path+financialFileName).split('.')[-1]=='pdf' or str(path+financialFileName).split('.')[-1]=='PDF':
                        reader = PdfFileReader(path+financialFileName)
                        if reader.isEncrypted:
                            with open(path+financialFileName, 'wb') as output_file:
                                reader.decrypt(financialPassword)
                                writer=PdfFileWriter()
                                for i in range(reader.getNumPages()):
                                    writer.addPage(reader.getPage(i))
                                writer.write(output_file)
                        # PDFfile = wi(filename=path+financialFileName+'[0]',resolution=60)
                        # PDFfile.save(filename=path+'financial.jpg')
                        # financialFileName='financial.jpg'
            else:
                financialFileName=''
            conn_Emkay_digilocker.execute("UPDATE userdetails SET uploadFinancialproof='"+path+financialFileName+"' where clientcode = '"+clientcode+"'")
            conn_Emkay_digilocker.commit()


        if "bankproofPassword" in request.form:
            bankproofPassword=request.form['bankproofPassword']
            bankproof_file = request.files['bankproof']
            bankproofFileName=bankproof_file.filename
            bankproof_file.save(path+bankproofFileName)
            if 'png' in bankproofFileName.split('.')[-1] or 'PNG' in bankproofFileName.split('.')[-1] or 'jpg' in bankproofFileName.split('.')[-1] or 'JPG' in bankproofFileName.split('.')[-1] or 'jpeg' in bankproofFileName.split('.')[-1] or 'JPEG' in bankproofFileName.split('.')[-1]:
                im = Image.open(path+bankproofFileName)
                rgb_im = im.convert('RGB')
                imageSizeBytes=os.path.getsize(path+bankproofFileName)
                # bankproofFileName=bankproofFileName.split('.')[0]
                quality=getImageQuality(imageSizeBytes)

                bankproofFileName='bankproof_'+name1
                rgb_im.save(path+bankproofFileName+'.jpg',quality=quality,optimize=True)
                bankproofFileName=bankproofFileName+'.jpg'
            if str(path+bankproofFileName).split('.')[-1]=='pdf' or str(path+bankproofFileName).split('.')[-1]=='PDF':
                    reader = PdfFileReader(path+bankproofFileName)
                    if reader.isEncrypted:
                        with open(path+bankproofFileName, 'wb') as output_file:
                            reader.decrypt(bankproofPassword)
                            writer=PdfFileWriter()
                            for i in range(reader.getNumPages()):
                                writer.addPage(reader.getPage(i))
                            writer.write(output_file)
                    PDFfile = wi(filename=path+bankproofFileName+'[0]',resolution=150)
                    print(path+'bankproof_'+name1+'.jpg')
                    PDFfile.save(filename=path+'bankproof_'+name1+'.jpg')
                    bankproofFileName='bankproof_'+name1+'.jpg'
            conn_Emkay_digilocker.execute("UPDATE userdetails SET  uploadBankproof='"+path+bankproofFileName+"' where clientcode = '"+clientcode+"'")
            conn_Emkay_digilocker.commit()


        if "pancard" in request.files:
            pan_file=request.files['pancard']
            panFileName=pan_file.filename
            pan_file.save(path+panFileName)
            print(panFileName)
            if 'png' in panFileName.split('.')[-1] or 'PNG' in panFileName.split('.')[-1] or 'jpg' in panFileName.split('.')[-1] or 'JPG' in panFileName.split('.')[-1] or 'jpeg' in panFileName.split('.')[-1] or 'JPEG' in panFileName.split('.')[-1]:
                im = Image.open(path+panFileName)
                rgb_im = im.convert('RGB')
                imageSizeBytes=os.path.getsize(path+panFileName)
                # panFileName=panFileName.split('.')[0]
                print(panFileName)
                quality=getImageQuality(imageSizeBytes)

                panFileName='pancard_'+name1
                rgb_im.save(path+panFileName+'.jpg',quality=quality,optimize=True)
                panFileName=panFileName+'.jpg'
                print(panFileName)
            if str(path+panFileName).split('.')[-1]=='pdf' or str(path+panFileName).split('.')[-1]=='PDF':
                    PDFfile = wi(filename=path+panFileName+'[0]',resolution=150)
                    PDFfile.save(filename=path+'pancard_'+name1+'.jpg')
                    panFileName='pancard_'+name1+'.jpg'
            conn_Emkay_digilocker.execute("UPDATE userdetails SET uploadPAN='"+path+panFileName+"' where clientcode = '"+clientcode+"'")
            conn_Emkay_digilocker.commit()


        if "signature" in request.files:
            signature_file=request.files['signature']
            signatureFileName=signature_file.filename
            signature_file.save(path+signatureFileName)
            if 'png' in signatureFileName.split('.')[-1] or 'PNG' in signatureFileName.split('.')[-1] or 'jpg' in signatureFileName.split('.')[-1] or 'JPG' in signatureFileName.split('.')[-1] or 'jpeg' in signatureFileName.split('.')[-1] or 'JPEG' in signatureFileName.split('.')[-1]:
                im = Image.open(path+signatureFileName)
                rgb_im = im.convert('RGB')
                imageSizeBytes=os.path.getsize(path+signatureFileName)
                # signatureFileName=signatureFileName.split('.')[0]
                quality=getImageQuality(imageSizeBytes)

                signatureFileName='signature_'+name1
                rgb_im.save(path+signatureFileName+'.jpg',quality=quality,optimize=True)
                signatureFileName=signatureFileName+'.jpg'
            if str(path+signatureFileName).split('.')[-1]=='pdf' or str(path+signatureFileName).split('.')[-1]=='PDF':
                    PDFfile = wi(filename=path+signatureFileName+'[0]',resolution=60)
                    PDFfile.save(filename=path+'signature_'+name1+'.jpg')
                    signatureFileName='signature_'+name1+'.jpg'

            conn_Emkay_digilocker.execute("UPDATE userdetails SET  uploadSignature='"+path+signatureFileName+"' where clientcode = '"+clientcode+"'")
            conn_Emkay_digilocker.commit()
        

        conn_Emkay_digilocker.execute("UPDATE userdetails SET documentUploadVerify=?, documentUploadVerifyTime=?, freeze=? where clientcode =?" ,("yes",datetime.datetime.now(),'no',clientcode))
        conn_Emkay_digilocker.commit()


    data=conn_Emkay_digilocker.execute('SELECT emailchangeyesno,mobilechangeyesno,addresschangeyesno,segmentactivationyesno,bankchangeyesno,email,reject,rejectLIST,clientimage,new_email,name,pan FROM userdetails WHERE clientcode = "'+str(clientcode).lower()+'"').fetchall()
    print(clientcode)
    name=data[0][10]
    pan=data[0][11]
    if data[0][9]=="" or data[0][9]==None:
        emails=data[0][5]
    else:
        emails=data[0][9]
    rejectLIST=data[0][7]
    try:
        rejectLIST = list(filter(None, list(set(rejectLIST.split(' ')))))
    except:
        pass
    print(rejectLIST)
    if data[0][6]=='yes':
        for i in rejectLIST:
            if i!='image':
                rejectLIST.remove(i)
        if 'image' in rejectLIST:
            conn_Emkay_digilocker.execute("UPDATE userdetails SET rejectLIST='image', freeze='no' WHERE clientcode='"+clientcode+"'")
            conn_Emkay_digilocker.commit()
        else:
            conn_Emkay_digilocker.execute("UPDATE userdetails SET changes='review_pending', rejectLIST='', reject='', freeze='yes' WHERE clientcode='"+clientcode+"'")
            conn_Emkay_digilocker.commit()
    else:
        if "clientimage" in request.form:
            if request.form['clientimage']=='yes':
                conn_Emkay_digilocker.execute("UPDATE userdetails SET changes='document', freeze='no' where clientcode = '"+clientcode+"'")
                conn_Emkay_digilocker.commit()
            else:
                print('Rekycpdf called')
                try:
                    accountmodification(clientcode)
                except Exception as e:
                    print(e)
                    pass
                try:
                    kraAPI(clientcode)
                except:
                    pass
                conn_Emkay_digilocker.execute("UPDATE userdetails SET changes='requested', freeze='yes' WHERE clientcode='"+clientcode+"'")
                conn_Emkay_digilocker.commit()
                        
                email=''    
                mobile=''
                address=''
                segment=''
                bank=''
                count=0

                if data[0][0]=='yes':
                    email='Email' if count!=1 else ', Email'
                    count=1
                if data[0][1]=='yes':
                    mobile='Mobile' if count!=1 else ', Mobile'
                    count=1
                if data[0][2]=='yes':
                    address='Address' if count!=1 else ', Address'
                    count=1
                if data[0][3]=='yes':
                    segment='Segment' if count!=1 else ', Segment'
                    count=1
                if data[0][4]=='yes':
                    bank='Bank Details' if count!=1 else ', Bank Details'
                    count=1



                text='Your '+email+mobile+address+segment+bank+' has been updated.<br><br>Your ReKYC registration is completed, Our KYC admin will review your application and will send you the notification for esign process.'
                body='''<html>
                        <head>
                          <title></title>
                        </head>
                        <body>
                        <div style="background-color:#f0f1f3;font-family:'Poppins',sans-serif;font-size:18px;line-height:28px;margin:0;color:#1F346D;">
                            <div class="m_2513597272243517713gutter" style="padding:5px 0;">&nbsp;</div>
                            <div class="m_2513597272243517713root" style="margin:0 20px;">
                              <table class="m_2513597272243517713header" style="max-width:600px;margin:0 auto 5px auto;width:100%;">
                                <tbody>
                                    <tr>
                                      <td align="center" colspan="2">
                                        <a href="" style="color:#387ed1;" target="_blank">
                                          <img alt="LOGO" src='https://www.emkayglobal.com/images/logo.png' style="width: 45%;">
                                        </a>
                                      </td>
                                    </tr>
                                </tbody>
                              </table>
                              <p>Dear '''+name+''',<br/><br/>Welcome to Emkay Global Financial Services Ltd.<br/></p>
                              <p class="m_2513597272243517713wrap" > '''+text+'''<br/><br/> If you have any queries/concerns, you can call us at 022-66299299 or mail us at rekyc_support@emkayglobal.in</p><br/>
                              <p>Warm Regards,<br/>Team RE-KYC<br/>Emkay Global Financial Services Ltd.</p>
                              <div class="m_2513597272243517713footer" style="text-align:center;color:#1F346D;font-size:11px;">
                                
                        </body>
                        </html>'''

                mailsending("rekyc_support@emkayglobal.in",'',"Emkay Global Financial Services Ltd. ReKYC Registration Completed",body,emails,['',''],"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")
                
                try:
                    os.mkdir("static/rekycPDF/"+clientcode+"/finalrekycpdf")
                except:
                    pass
                try:
                    os.remove("static/rekycPDF/"+clientcode+"/finalrekycpdf/""Re_"+str(pan)+".pdf")
                except:
                    pass

                try:
                    shutil.copy("static/rekycPDF/"+clientcode+"/rekycam.pdf","static/rekycPDF/"+clientcode+"/finalrekycpdf")
                    os.rename("static/rekycPDF/"+clientcode+"/finalrekycpdf/rekycam.pdf", "static/rekycPDF/"+clientcode+"/finalrekycpdf/""Re_"+str(pan)+".pdf")
                except:
                    pass
                return jsonify({'msg':'All Files Upload sucessfully'})
    return jsonify({'msg':'All Files Upload sucessfully'})





 
@updatedetailsapi.route('/makeDefault/<clientcode>', methods=['POST'])
def makeDefault(clientcode):
    data=request.get_json()
    accountnumber = data['accountnumber'].strip()
    ifsc=data['ifsc'].strip()
    if conn_Emkay_digilocker.execute('SELECT BankAccountNumber, IFSC FROM userdetails WHERE clientcode = "'+clientcode+'"').fetchall()[0] == (accountnumber,ifsc):
        conn_Emkay_digilocker.execute("UPDATE userdetails SET isDefault = 1, isDefaultnew = 0 where clientcode = '"+clientcode+"'")
        conn_Emkay_digilocker.commit()
    
    elif conn_Emkay_digilocker.execute('SELECT newBankAccountNumber, newIFSC FROM userdetails WHERE clientcode = "'+clientcode+'"').fetchall()[0] == (accountnumber,ifsc):
        conn_Emkay_digilocker.execute("UPDATE userdetails SET isDefault = 0, isDefaultnew = 1 where clientcode = '"+clientcode+"'")
        conn_Emkay_digilocker.commit()
    
    else:
        return jsonify({'data':'Bank Not Found', 'success':False})        
    return jsonify({'data':'Default Bank is Set', 'success':True})
  


@updatedetailsapi.route('/addcolumn/<colname>', methods=['POST','GET'])
def addcolumn(colname):
     conn_Emkay_digilocker.execute("ALTER Table userdetails ADD COLUMN '"+colname+"'")
     conn_Emkay_digilocker.commit()

     return "Column Added"





@updatedetailsapi.route('/uploadUserImage/<clientcode>', methods=['POST'])
def uploadUserImage(clientcode):
    clientcode=clientcode.lower()
    

   
    path = "static/userUpload/"+str(clientcode)+"/"


    if "clientimage" in request.form:
        clientImageData=request.form['clientimage']
        clientImageData=clientImageData.split(',')[1]
        clientImageDataDecoded=base64.b64decode(clientImageData)
        clientimageFileName='clientimage.jpg'
        f=open(path+clientimageFileName,'wb')
        f.write(clientImageDataDecoded)
        f.close()
        conn_Emkay_digilocker.execute("UPDATE userdetails SET clientimage='"+path+clientimageFileName+"',changes='requested' where clientcode = '"+clientcode+"'")
        conn_Emkay_digilocker.commit()

    data=conn_Emkay_digilocker.execute('SELECT emailchangeyesno,mobilechangeyesno,addresschangeyesno,segmentactivationyesno,bankchangeyesno,email,reject,new_email,name,pan FROM userdetails WHERE clientcode = "'+clientcode+'"').fetchall()
    name=data[0][8]
    pan=data[0][9]
    if data[0][7]=="" or data[0][7]==None:
        emails=data[0][5]
    else:
        emails=data[0][7]
    if data[0][6]=='yes':
        conn_Emkay_digilocker.execute("UPDATE userdetails SET changes='review_pending', reject='', rejectLIST='', freeze='yes' WHERE clientcode='"+clientcode+"'")
        conn_Emkay_digilocker.commit()
    else:
        # print('Rekycpdf called')
        # accountmodification(clientcode)

        # print('RekycpdfKRA called')
        # kraAPI(clientcode)                     
        conn_Emkay_digilocker.execute("UPDATE userdetails SET changes='requested', freeze='yes' WHERE clientcode='"+clientcode+"'")
        conn_Emkay_digilocker.commit()

        email=''
        mobile=''
        address=''
        segment=''
        bank=''
        count=0

        if data[0][0]=='yes':
            email='Email' if count!=1 else ', Email'
            count=1
        if data[0][1]=='yes':
            mobile='Mobile' if count!=1 else ', Mobile'
            count=1
        if data[0][2]=='yes':
            address='Address' if count!=1 else ', Address'
            count=1
        if data[0][3]=='yes':
            segment='Segment' if count!=1 else ', Segment'
            count=1
        if data[0][4]=='yes':
            bank='Bank Details' if count!=1 else ', Bank Details'
            count=1


        text='Your '+email+mobile+address+segment+bank+' has been updated.<br><br>Your ReKYC registration is completed, Our KYC admin will review your application and will send you the notification for esign process.'
        body='''<html>
                <head>
                  <title></title>
                </head>
                <body>
                <div style="background-color:#f0f1f3;font-family:'Poppins',sans-serif;font-size:18px;line-height:28px;margin:0;color:#1F346D;">
                    <div class="m_2513597272243517713gutter" style="padding:5px 0;">&nbsp;</div>
                    <div class="m_2513597272243517713root" style="margin:0 20px;">
                      <table class="m_2513597272243517713header" style="max-width:600px;margin:0 auto 5px auto;width:100%;">
                        <tbody>
                            <tr>
                              <td align="center" colspan="2">
                                <a href="" style="color:#387ed1;" target="_blank">
                                  <img alt="LOGO" src='https://www.emkayglobal.com/images/logo.png' style="width: 45%;">
                                </a>
                              </td>
                            </tr>
                        </tbody>
                      </table>
                      <p>Dear '''+name+''',<br/><br/>Welcome to Emkay Global Financial Services Ltd.<br/></p>
                      <p class="m_2513597272243517713wrap" > '''+text+'''<br/><br/> If you have any queries/concerns, you can call us at 022-66299299 or mail us at rekyc_support@emkayglobal.in</p><br/>
                      <p>Warm Regards,<br/>Team RE-KYC<br/>Emkay Global Financial Services Ltd.</p>
                      <div class="m_2513597272243517713footer" style="text-align:center;color:#1F346D;font-size:11px;">
                        
                </body>
                </html>'''

        mailsending("rekyc_support@emkayglobal.in",'',"Emkay Global Financial Services Ltd. ReKYC Registration Completed",body,emails,['',''],"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")
        
        try:
            os.mkdir("static/rekycPDF/"+clientcode+"/finalrekycpdf")
        except:
            pass
        try:
            os.remove("static/rekycPDF/"+clientcode+"/finalrekycpdf/""Re_"+str(pan)+".pdf")
            os.remove("static/rekycPDF/"+clientcode+"/finalrekycpdf/""Rekra_"+str(pan)+".pdf")
        except:
            pass

        try:

            shutil.copy("static/rekycPDF/"+clientcode+"/rekycam.pdf","static/rekycPDF/"+clientcode+"/finalrekycpdf")
            os.rename("static/rekycPDF/"+clientcode+"/finalrekycpdf/rekycam.pdf", "static/rekycPDF/"+clientcode+"/finalrekycpdf/""Re_"+str(pan)+".pdf")
            
            shutil.copy("static/rekycPDF/"+clientcode+"/rekykra.pdf","static/rekycPDF/"+clientcode+"/finalrekycpdf")
            os.rename("static/rekycPDF/"+clientcode+"/finalrekycpdf/rekykra.pdf", "static/rekycPDF/"+clientcode+"/finalrekycpdf/""Rekra_"+str(pan)+".pdf")

        except:
            pass
    return jsonify({'msg':'Image Upload sucessfully'})








@updatedetailsapi.route('/userLocationTrackREKYC/<clientcode>', methods=['POST'])
def userLocationTrack(clientcode):
    data=request.get_json()
    print(data,clientcode)
    try:
        
        conn_Emkay_digilocker.execute("UPDATE userdetails SET userLocationData=? where clientcode =?",(str(data),clientcode.lower()))
        conn_Emkay_digilocker.commit()
    except Exception as e:
        print(e)
        
    return jsonify({'data':'Location Captured'})










cors = CORS(updatedetailsapi)


