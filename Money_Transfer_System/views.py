from django.http import HttpResponse
from django.shortcuts import render,redirect
from databases.models import Users, Payments, MESSAGES, Queries
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
import random
import datetime
import secrets
from django.contrib import messages
from django.contrib.sessions.models import Session

def First_Page(request):
    return render(request, "MoneyTransferSystem.html")

def UserLogin_Page(request):
    message=""
    problem="none"

    try:
        if request.method=="POST":
            # get the user-id and password from the login form:
            user_id=str(request.POST.get('user_id'))
            passwd=str(request.POST.get('passwd'))

            # check if user_id exist or not:
            data=Users.objects.filter(User_ID=user_id).values()
            if len(data)==0:
                # display -> user_id doesnot exists
                problem="user_id"
                message="Invalid User-ID/Password"
            else:
                # check f the password is correct or not
                if data[0]['Password']==passwd:
                    # check the status of user - pending/verified/invalid
                    if data[0]['Status']=='verified':
                        # login successfully then display page
                        problem="done"
                        message="login successfully"
                        session_id=secrets.token_urlsafe(10)
                        details=Users.objects.get(User_ID=user_id)
                        unique_key=details.Unique_Key
                        details.Active_Status=True
                        details.save()
                        url='/user-homepage/'+user_id+"/"+unique_key+'/'+session_id
                        return redirect(url)
                    elif data[0]['Status']=='pending':
                        # display -> pending message
                        problem="pending_status"
                        message="Your account details are still under validation process"
                    elif data[0]['Status']=='invalid':
                        # display -> invalid message
                        problem="invalid_status"
                        message="Your account details were invalid so you cannot login using this account"
                else:
                    problem="password"
                    message="Invalid User-ID/Password"
    except:
        # write except query here
        probelm='no_data'
        message="Please enter your User-ID & Password"

    data={
        'problem':problem,
        'message':message
    }

    return render(request, "user_login.html", data)

def NewUser_Registration(request):
    message=""
    problem="none"

    try:
        if request.method=="POST":
            # get all the form data:
            name=str(request.POST.get('name'))
            aadhar_no=str(request.POST.get('aadhar_no'))
            mobile_no=str(request.POST.get('mobile_no'))
            email=str(request.POST.get('email'))
            dob=str(request.POST.get('dob'))
            acc_no=str(request.POST.get('acc_no'))
            re_acc_no=str(request.POST.get('re_acc_no'))
            ifsc=str(request.POST.get('ifsc'))
            bank_name=str(request.POST.get('bank_name'))
            user_id=str(request.POST.get('user_id'))
            passwd=str(request.POST.get('passwd'))
            re_passwd=str(request.POST.get('re_passwd'))
            # set default values:
            mpin='000000'
            status='pending'
            balance=0

            # check if the acc_no and re_acc_no are same or not
            if (acc_no==re_acc_no):
                # if same then check if the account no entered already exists or not
                data=Users.objects.filter(Account_Number=acc_no).values()
                if len(data)==0:
                    # if not then check if the passwd and re_passwd are same or not
                    if passwd==re_passwd:
                        # if same then check if the user-id entered already exist or not
                        data=Users.objects.filter(User_ID=user_id).values()
                        if len(data)==0:
                            # if not then insert all the form data into the database
                            unique_key=secrets.token_urlsafe(9)
                            insert_user=Users(Name=name,Aadhar=aadhar_no,Mobile=mobile_no,Email=email,Date_Of_Birth=dob,Account_Number=acc_no,IFSC=ifsc,Bank_Name=bank_name,User_ID=user_id,Password=passwd,MPIN=mpin,Status=status,Balance=balance,Unique_Key=unique_key)
                            insert_user.save()
                            problem="done"
                            message="You details are submitted successfully.\nOnce your details are validated then you can easily login via your used-id and password"
                        else:
                            # if exists then:
                            # display -> user with user-id: user_id already exists please enter different user-id
                            problem="user-id"
                            message="user with user-id: "+user_id+" already exists please enter different user-id"
                    else:
                        # if not same then:
                        # display -> password and confirm password doesnot match
                        problem="password"
                        message="password and confirm password doesnot match"
                else:
                    # if exists then:
                    # display -> account number you entered already exists
                    problem="account no"
                    message="account number you entered already exists"
            else:
                # if not same then:
                # display -> account number and confirm account number doesnot match
                problem="account no"
                message="account number and confirm account number doesnot match"
    except:
        # except statement write here
        problem="no_data"
        message="Please enter data in all the fields required"

    data={
        'problem':problem,
        'message':message
    }

    return render(request, "user_register.html", data)

def User_HomePage(request,user_id,unique_key,session_id):
    details=Users.objects.filter(User_ID=user_id).values()
    if details[0]['Active_Status']==False or details[0]['Unique_Key']!=unique_key:
        return HttpResponse("Invalid session")
    
    name=details[0]['Name']

    profile_url='/user-profile/'+user_id+"/"+unique_key+'/'+session_id
    home_url='/user-homepage/'+user_id+"/"+unique_key+'/'+session_id
    help_url='/user-query/'+user_id+"/"+unique_key+'/'+session_id
    transfer_url='/user-transfer-funds/'+user_id+"/"+unique_key+'/'+session_id
    message_url='/user-messages/'+user_id+"/"+unique_key+'/'+session_id
    balance_url='/user-balance/'+user_id+"/"+unique_key+'/'+session_id
    history_url='/user-payment-history/'+user_id+"/"+unique_key+'/'+session_id
    logout_url='/user-logout/'+user_id+"/"+unique_key+'/'+session_id

    data={
        'logout_url':logout_url,
        'name':name,
        'user_id':user_id,
        'session_id':session_id,
        'profile_url':profile_url,
        'home_url':home_url,
        'help_url':help_url,
        'transfer_url':transfer_url,
        'message_url':message_url,
        'balance_url':balance_url,
        'history_url':history_url,
    }

    return render(request, "user_page.html", data)
    

def User_Profile(request,user_id,unique_key,session_id):
    details=Users.objects.filter(User_ID=user_id).values()
    if details[0]['Active_Status']==False or details[0]['Unique_Key']!=unique_key:
        return HttpResponse("Invalid session")

    name=""
    aadhar=""
    mobile=""
    email=""
    dob=""
    acc_no=""
    ifsc=""
    bank=""
    name=details[0]['Name']
    aadhar=details[0]['Aadhar']
    mobile=details[0]['Mobile']
    email=details[0]['Email']
    dob=details[0]['Date_Of_Birth']
    acc_no=details[0]['Account_Number']
    ifsc=details[0]['IFSC']
    bank=details[0]['Bank_Name']

    profile_url='/user-profile/'+user_id+"/"+unique_key+'/'+session_id
    home_url='/user-homepage/'+user_id+"/"+unique_key+'/'+session_id
    help_url='/user-query/'+user_id+"/"+unique_key+'/'+session_id
    transfer_url='/user-transfer-funds/'+user_id+"/"+unique_key+'/'+session_id
    message_url='/user-messages/'+user_id+"/"+unique_key+'/'+session_id
    balance_url='/user-balance/'+user_id+"/"+unique_key+'/'+session_id
    history_url='/user-payment-history/'+user_id+"/"+unique_key+'/'+session_id
    logout_url='/user-logout/'+user_id+"/"+unique_key+'/'+session_id

    data={
        'logout_url':logout_url,
        'name':name,
        'mobile':mobile,
        'email':email,
        'dob':dob,
        'acc_no':acc_no,
        'ifsc':ifsc,
        'bank':bank,
        'user_id':user_id,

        'profile_url':profile_url,
        'home_url':home_url,
        'help_url':help_url,
        'transfer_url':transfer_url,
        'message_url':message_url,
        'balance_url':balance_url,
        'history_url':history_url,
    }

    return render(request, 'user_profile.html', data)

def User_TransferFunds(request,user_id,unique_key,session_id):
    details=Users.objects.filter(User_ID=user_id).values()
    if details[0]['Active_Status']==False or details[0]['Unique_Key']!=unique_key:
        return HttpResponse("Invalid session")

    problem="none"
    message=""
    sender=user_id
    name=Users.objects.filter(User_ID=sender).values_list('Name',flat=True)
    amount=0

    try:
        if request.method=="POST":
            # get details for payment:
            amount=int(request.POST.get('amount'))
            reciever=str(request.POST.get('reciever'))
            remarks=str(request.POST.get('remarks'))
            request.session['reciever']=reciever
            request.session['amount']=amount
            request.session['remarks']=remarks
            # check balance:
            sender_details=Users.objects.filter(User_ID=sender).values()
            if sender_details[0]['Balance']>=amount:
                # check if reciever's user-id exists or not
                reciever_details=Users.objects.filter(User_ID=reciever).values()
                if len(reciever_details)==0 or reciever_details[0]['Status']!='verified':
                    problem="reciever"
                    message="The reciever's user-id you entered doesn't exists!"
                else:
                    problem="done"
            else:
                problem="balance"
                message="Insufficient Balance"
    except:
        try:
            if request.method=="POST":
                mpin=str(request.POST.get('mpin'))
                sender_details=Users.objects.filter(User_ID=sender).values()
                if sender_details[0]['MPIN']==mpin:
                    reciever=request.session['reciever']
                    amount=request.session['amount']
                    remarks=request.session['remarks']
                    reciever_details=Users.objects.filter(User_ID=reciever).values()
                    increase=reciever_details[0]['Balance']+amount
                    sender_details=Users.objects.filter(User_ID=sender).values()
                    decrease=sender_details[0]['Balance']-amount
                    ref_no=str(random.randint(0,10000000000))
                    data=Payments.objects.filter(Reference_Number=ref_no)
                    while len(data)!=0:
                        ref_no=str(random.randint(0,10000000000))
                        data=Payments.objects.filter(Reference_Number=ref_no)
                    date_time=datetime.datetime.now()
                    sender_details.update(Balance=decrease)
                    reciever_details.update(Balance=increase)
                    insert_payment=Payments(Sender=sender,Reciever=reciever,Amount=amount,Date_time=date_time,Reference_Number=ref_no,Payment_Status="completed",Remarks=remarks)
                    insert_payment.save()
                    message="₹"+str(amount)+" successfully sent to User-ID: "+reciever
                    problem="done"
                    sender_message="Your account is being debited by amount: ₹"+str(amount)
                    reciever_message="Your account is being credited by amount: ₹"+str(amount)

                    insert_message=MESSAGES(From='server',To=sender,Message=sender_message,Date_time=date_time)
                    insert_message.save()
                    insert_message=MESSAGES(From='server',To=reciever,Message=reciever_message,Date_time=date_time)
                    insert_message.save()
                    messages.success(request,message)
                    del request.session['amount']
                    del request.session['reciever']
                    del request.session['remarks']
                else:
                    message="Incorrect Mpin"
                    problem="invalid_mpin"
                redirect_url='/user-homepage/'+user_id+'/'+unique_key+'/'+session_id
                return redirect(redirect_url)
        except:
            problem="wrong_data"
            message="Please enter valid data"

    profile_url='/user-profile/'+user_id+"/"+unique_key+'/'+session_id
    home_url='/user-homepage/'+user_id+"/"+unique_key+'/'+session_id
    help_url='/user-query/'+user_id+"/"+unique_key+'/'+session_id
    transfer_url='/user-transfer-funds/'+user_id+"/"+unique_key+'/'+session_id
    message_url='/user-messages/'+user_id+"/"+unique_key+'/'+session_id
    balance_url='/user-balance/'+user_id+"/"+unique_key+'/'+session_id
    history_url='/user-payment-history/'+user_id+"/"+unique_key+'/'+session_id
    logout_url='/user-logout/'+user_id+"/"+unique_key+'/'+session_id

    data={
        'logout_url':logout_url,
        'problem':problem,
        'message':message,
        'name':name,
        'profile_url':profile_url,
        'home_url':home_url,
        'help_url':help_url,
        'transfer_url':transfer_url,
        'message_url':message_url,
        'balance_url':balance_url,
        'history_url':history_url,
    }

    return render(request, 'user_transfer_funds.html', data)

def User_Messages(request,user_id,unique_key,session_id):
    details=Users.objects.filter(User_ID=user_id).values()
    if details[0]['Active_Status']==False or details[0]['Unique_Key']!=unique_key:
        return HttpResponse("Invalid session")

    name=Users.objects.filter(User_ID=user_id).values_list('Name',flat=True)
    content=MESSAGES.objects.filter(From=user_id).values() | MESSAGES.objects.filter(To=user_id).values()
    size=len(content)
    content=reversed(content)

    profile_url='/user-profile/'+user_id+"/"+unique_key+'/'+session_id
    home_url='/user-homepage/'+user_id+"/"+unique_key+'/'+session_id
    help_url='/user-query/'+user_id+"/"+unique_key+'/'+session_id
    transfer_url='/user-transfer-funds/'+user_id+"/"+unique_key+'/'+session_id
    message_url='/user-messages/'+user_id+"/"+unique_key+'/'+session_id
    balance_url='/user-balance/'+user_id+"/"+unique_key+'/'+session_id
    history_url='/user-payment-history/'+user_id+"/"+unique_key+'/'+session_id
    logout_url='/user-logout/'+user_id+"/"+unique_key+'/'+session_id
    
    data={
        'logout_url':logout_url,
        'content':content,
        'size':size,
        'name':name,
        'profile_url':profile_url,
        'home_url':home_url,
        'help_url':help_url,
        'transfer_url':transfer_url,
        'message_url':message_url,
        'balance_url':balance_url,
        'history_url':history_url,
    }

    return render(request, 'user_messages.html', data)

def User_Balance(request,user_id,unique_key,session_id):
    details=Users.objects.filter(User_ID=user_id).values()
    if details[0]['Active_Status']==False or details[0]['Unique_Key']!=unique_key:
        return HttpResponse("Invalid session")

    name=Users.objects.filter(User_ID=user_id).values_list('Name',flat=True)
    balance=""
    
    try:
        if request.method=="POST":
            mpin=str(request.POST.get('mpin'))
            correct_mpin=Users.objects.filter(User_ID=user_id).values()
            if (correct_mpin[0]['MPIN']==mpin):
                balance=Users.objects.filter(User_ID=user_id).values_list('Balance', flat=True)
            else:
                balance="none"
    except:
        balance="wrong_data"

    profile_url='/user-profile/'+user_id+"/"+unique_key+'/'+session_id
    home_url='/user-homepage/'+user_id+"/"+unique_key+'/'+session_id
    help_url='/user-query/'+user_id+"/"+unique_key+'/'+session_id
    transfer_url='/user-transfer-funds/'+user_id+"/"+unique_key+'/'+session_id
    message_url='/user-messages/'+user_id+"/"+unique_key+'/'+session_id
    balance_url='/user-balance/'+user_id+"/"+unique_key+'/'+session_id
    history_url='/user-payment-history/'+user_id+"/"+unique_key+'/'+session_id
    logout_url='/user-logout/'+user_id+"/"+unique_key+'/'+session_id
    
    data={
        'logout_url':logout_url,
        'balance':balance,
        'name':name,
        'profile_url':profile_url,
        'home_url':home_url,
        'help_url':help_url,
        'transfer_url':transfer_url,
        'message_url':message_url,
        'balance_url':balance_url,
        'history_url':history_url,
    }

    return render(request, 'users_check_balance.html', data)

def User_PaymentHistory(request,user_id,unique_key,session_id):
    details=Users.objects.filter(User_ID=user_id).values()
    if details[0]['Active_Status']==False or details[0]['Unique_Key']!=unique_key:
        return HttpResponse("Invalid session")

    name=Users.objects.filter(User_ID=user_id).values_list('Name',flat=True)
    par=""
    history={}
    if 'search' in request.POST:
        search_item=request.POST.get('search')
        history=Payments.objects.filter(Reference_Number__icontains=search_item,Sender=user_id).values() | Payments.objects.filter(Reference_Number__icontains=search_item,Reciever=user_id).values() | Payments.objects.filter(Sender__icontains=search_item,Reciever=user_id).values() | Payments.objects.filter(Reciever__icontains=search_item,Sender=user_id).values()
    else:
        history=Payments.objects.filter(Sender=user_id).values() | Payments.objects.filter(Reciever=user_id).values()
    size=len(history)
    history=reversed(history)

    profile_url='/user-profile/'+user_id+"/"+unique_key+'/'+session_id
    home_url='/user-homepage/'+user_id+"/"+unique_key+'/'+session_id
    help_url='/user-query/'+user_id+"/"+unique_key+'/'+session_id
    transfer_url='/user-transfer-funds/'+user_id+"/"+unique_key+'/'+session_id
    message_url='/user-messages/'+user_id+"/"+unique_key+'/'+session_id
    balance_url='/user-balance/'+user_id+"/"+unique_key+'/'+session_id
    history_url='/user-payment-history/'+user_id+"/"+unique_key+'/'+session_id
    logout_url='/user-logout/'+user_id+"/"+unique_key+'/'+session_id
    
    data={
        'logout_url':logout_url,
        'name':name,
        'history':history,
        'user_id':user_id,
        'size':size,
        'profile_url':profile_url,
        'home_url':home_url,
        'help_url':help_url,
        'transfer_url':transfer_url,
        'message_url':message_url,
        'balance_url':balance_url,
        'history_url':history_url,
    }

    return render(request, 'user_transaction_history.html', data)

def User_Query(request,user_id,unique_key,session_id):
    details=Users.objects.filter(User_ID=user_id).values()
    if details[0]['Active_Status']==False or details[0]['Unique_Key']!=unique_key:
        return HttpResponse("Invalid session")

    problem="none"
    message=""

    name=Users.objects.filter(User_ID=user_id).values_list('Name',flat=True)
    query=""
    queries=Queries.objects.filter(From=user_id).values()
    size=len(queries)
    queries=reversed(queries)

    profile_url='/user-profile/'+user_id+"/"+unique_key+'/'+session_id
    home_url='/user-homepage/'+user_id+"/"+unique_key+'/'+session_id
    help_url='/user-query/'+user_id+"/"+unique_key+'/'+session_id
    transfer_url='/user-transfer-funds/'+user_id+"/"+unique_key+'/'+session_id
    message_url='/user-messages/'+user_id+"/"+unique_key+'/'+session_id
    balance_url='/user-balance/'+user_id+"/"+unique_key+'/'+session_id
    history_url='/user-payment-history/'+user_id+"/"+unique_key+'/'+session_id
    logout_url='/user-logout/'+user_id+"/"+unique_key+'/'+session_id

    try:
        query=request.GET.get('query')
        if query!=None:
            query=str(query)
            if query!='':
                date_time=datetime.datetime.now()
                insert_query=Queries(From=user_id,Query=query,Date_time=date_time,Query_Status='pending')
                insert_query.save()
                problem="done"
                message="Your query is recieved we will reach to you shortly"
    except:
        problem="no_data"
        message="Please enter query"
    
    data={
        'logout_url':logout_url,
        'name':name,
        'problem':problem,
        'message':message,
        'queries':queries,
        'size':size,
        'profile_url':profile_url,
        'home_url':home_url,
        'help_url':help_url,
        'transfer_url':transfer_url,
        'message_url':message_url,
        'balance_url':balance_url,
        'history_url':history_url,
    }

    return render(request, 'user_query.html', data)

def User_Logout(request,user_id,unique_key,session_id):
    details=Users.objects.get(User_ID=user_id)
    unique_key=details.Unique_Key
    details.Active_Status=False
    details.save()

    print(request.session)

    print(Session.objects.all()) #you see all sessions
    Session.objects.all().delete() 

    del session_id

    return render(request, 'user_logout.html')


# def Send_Mobile_OTP(mobile_no):
#     otp="123456"
#     return otp
# def Send_Email_OTP(email_id):
#     otp="123456"
#     return otp
# # NOT WORKING
# def ForgotUserIDPasswordMPIN(request):
#     got_data=False
#     problem="none"
#     message=""
#     otp_verified=False
#     try:
#         print("1st try block")
#         if request.method=="POST":
#             # get mobile email
#             mobile_no=str(request.POST.get('mobile_no'))
#             email=str(request.POST.get('email'))

#             # check if the data exist or not
#             data=Users.objects.filter(Mobile=mobile_no,Email=email).values()
#             if (len(data)==0):
#                 problem="not_exists"
#                 message="Invalid mobile/email entered"
#             else:
#                 sent_mobile_otp=Send_Mobile_OTP(mobile_no)
#                 sent_email_otp=Send_Email_OTP(email)
#                 request.session['sent_mobile_otp']=sent_mobile_otp
#                 request.session['sent_email_otp']=sent_mobile_otp
#                 problem="exists"
#                 got_data=True
#                 print("valid mobile email")

#     except:
#         print("wrong details")
    
#     data={
#         'problem':problem,
#         'message':message,
#         'otp_verified':otp_verified,
#         'got_data':got_data,
#     }

#     render(request, 'forgot_userid_password_mpin.html', data)

# def GetOTP(request):
#     problem="none"
#     message=""
#     try:
#         sent_mobile_otp=request.session['sent_mobile_otp']
#         sent_email_otp=request.session['sent_email_otp']
#         print(sent_email_otp,sent_mobile_otp)
#         if request.method=="POST":
#             # get both otps
#             mobile_otp=str(request.POST.get('otp1'))
#             email_otp=str(request.POST.get('otp2'))

#             print(mobile_otp,email_otp)
#             if sent_email_otp==email_otp and sent_mobile_otp==mobile_otp:
#                 problem="valid_otps"
#                 otp_verified=True
#                 print('valid otps')
#             else:
#                 problem="invalid_otps"
#                 message="Incorrect OTPs entered"
#                 print(message)
#     except:
#         print("wrong otps")

#     data={
#         'problem':problem,
#         'message':message,
#         'otp_verified':otp_verified,
#         'got_data':got_data,
#     }

#     return render(request, 'forgot_userid_password_mpin.html', data)

# def Create_New_Password(request):
#     problem="none"
#     message=""
#     try:
#         if request.method=="POST":
#             # get form details:
#             new_passwd=str(request.POST.get('new_passwd'))
#             re_new_passwd=str(request.POST.get('re-new_passwd'))
            
#             # check if new and confirm new password matches or not
#             if new_passwd==re_new_passwd:
#                 # update password
#                 user_id=request.session['user_id']
#                 data=Users.objects.get(User_ID=user_id)
#                 data.Password=new_passwd
#                 data.save()
#                 problem="done"
#                 message="New password updated successfully"
#                 return redirect('/user-login')
#             else:
#                 # display -> new and confirm new doesnot match
#                 problem="passwd"
#                 message="New password and confirm new password doesnot match"
#     except:
#         problem="no_data"
#         message="Please enter password"
#     data={
#         'problem':problem,
#         'message':message,
#     }
#     return render(request, 'create_new_passwd.html', data)

# def Create_New_MPIN(request):
#     problem="none"
#     message=""
#     try:
#         if request.method=="POST":
#             # get form details:
#             new_mpin=str(request.POST.get('new_mpin'))
#             re_new_mpin=str(request.POST.get('re-new_mpin'))
            
#             # check if new and confirm new mpin matches or not
#             if new_mpin==re_new_mpin:
#                 # update password
#                 user_id=request.session['user_id']
#                 data=Users.objects.get(User_ID=user_id)
#                 data.MPIN=new_mpin
#                 data.save()
#                 problem="done"
#                 message="New MPIN updated successfully"
#                 return redirect('/user-login')
#             else:
#                 # display -> new and confirm new doesnot match
#                 problem="mpin"
#                 message="New MPIN and confirm new MPIN doesnot match"
#     except:
#         problem="no_data"
#         message="Please enter MPIN"

#     data={
#         'problem':problem,
#         'message':message,
#     }

#     return render(request, "create_new_mpin.html", data)
