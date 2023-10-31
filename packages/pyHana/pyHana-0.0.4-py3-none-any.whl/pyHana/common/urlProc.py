import requests
import time
# import datetime as dt

def requests_url_call(urlStr, params=''):
    errInd = 'N'
    
    print('\r' + urlStr, params, end='')

    while(1):
        try:                       
            # 2023.10.24 post 방식 추가
            if len(params) == 0:      
                resp = requests.get(urlStr, timeout=(5, 60)) # connect timeout 5초, read timeout 30로 각각 설정             
            else:
                resp = requests.post(urlStr, timeout=(5, 60), params=params)    

            if errInd == 'Y':
                print('>> Requests retry success : ', flush=True)              
            return resp
        
        except Exception as e:
            print("\n", ':', type(e), ':',  e, flush=True)
            errInd = 'Y'
            time.sleep(5)

    print('\r', end='')            
    return resp