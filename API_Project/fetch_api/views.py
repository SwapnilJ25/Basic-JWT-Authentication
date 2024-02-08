import datetime
from django.shortcuts import redirect, render
import requests
import jwt
import socket
import time

def login_and_store_tokens(request):
    login_url = 'http://127.0.0.1:8000/token/'  
    payload = {'username': 'admin', 'password': 'admin'}  
    token = request.session.get('token')
    
    
    response = requests.post(login_url, data=payload)
    
    if response.status_code == 200:
        data = response.json()
        print("data",data)
        access_token = data.get('token')
        refresh_token = data.get('refresh_token')

        
        request.session['Token']= access_token
        request.session['Refresh Token']= refresh_token
        
        return render(request,'home.html')
    else:
        print('Login failed')
        
    print("ERRRRRRRORRRRR")    
        


def get_Authenticate(request,token,refresh_token):
    # print("token",token)

    # print("+++++>>>>>", token_value)

    token = token.replace("Bearer ","")
    token = token.lstrip().rstrip()
    # print("-------->>>>>", token)
    token_payload = jwt.decode(token, 'secret', algorithm=[
                    "HS256"], verify=False)
    # print("+++++++++++++++++++++")
    # print("Token Payload : ", token_payload)
    # print("+++++++++++++++++++++")
    curr_time= int(time.time())
    # print("curr_time",curr_time)
    if curr_time > token_payload["exp"]:
        
        refresh_token_payload = jwt.decode(refresh_token, 'secret', algorithm=[
                    "HS256"], verify=False)
        # print("+++++++++++++++++++++")
        # print("Token Payload : ", refresh_token_payload)
        # print("+++++++++++++++++++++")
        curr_time_ref= int(time.time())
        if curr_time_ref > refresh_token_payload["exp"]:
            print("333333333333333")
            return False
        
        else:
            refresh_url = 'http://127.0.0.1:8000/refreshtoken/' 
            payload = {'expired_token': token, 'refresh_token': refresh_token}  
            
            # headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
            
            response = requests.post(refresh_url , data=payload)
            
            if response.status_code == 200:
                data = response.json()
                # print("data",data)
                access_token = data.get('token')
                refresh_token = data.get('refresh_token')
                request.session['Token']= access_token
                request.session['Refresh Token']= refresh_token
                print("token",access_token)
                print("refresh_token",refresh_token)
                print("1111111111111111111111111111111111")
                return True
    else:
        print("222222222222222222222222")
        return True



def show(request):
    if get_Authenticate(request,request.session.get('Token'),request.session.get('Refresh Token')):
        return render(request,"show.html")
    else:
        return render(request,'login.html')

    
            
            
                


