
from flask import Flask, request
from pywebcopy import save_webpage
import requests
import requests.packages.urllib3, requests, json, time, datetime, re, os, csv
from bs4 import BeautifulSoup as bs
from os import listdir, system
from os.path import isfile, join
from urllib.parse import urlparse
from urllib import parse
import re
import hashlib
from apscheduler.schedulers.background import BlockingScheduler
import threading
import datetime

def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")
        
botEmail = "bob8gook_kisa@webex.bot"
accessToken = "YzE4Y2ZhYjAtMDk5Yy00NTZlLWIwYjAtODYwNzQwNDExOWRmMDFjZmI1ODYtM2Rm_PF84_22cb7792-d880-4ec5-b6a6-649d9411bb5e"
headers = {"Authorization": "Bearer %s" % accessToken, "Content-Type": "application/json", 'Accept' : 'application/json'}
roomId_kisa_private = 'Y2lzY29zcGFyazovL3VzL1JPT00vNDkwNzIwMjAtMTBhNy0xMWVkLTk4ZDktNzU3YWU5MmY2MDFh' #kisa 개인방
roomId_soc = 'Y2lzY29zcGFyazovL3VzL1JPT00vZmIwY2M1YTAtMDYzZS0xMWVjLWExNzgtZDEzYjhjMjEwNzVk'
roomId_availability = 'Y2lzY29zcGFyazovL3VzL1JPT00vZTVmMmJiYTAtMTE2Ni0xMWVkLThmMjctZmQ4YjY5ODZmODc3'
roomId_use = roomId_soc

now = datetime.datetime.now()
now = now + datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=9, weeks=0)

try:
    with open('num_last.txt', 'r') as f:
        num_last = int(f.read())
except:
        num_last = 9999
print('num_last : ' + str(num_last))
now = datetime.datetime.now()
now = now + datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=9, weeks=0)
url = 'https://krcert.or.kr'
fPath_working = os.getcwd()
fPath_kisa =fPath_working + '/kisa'
createDirectory(fPath_kisa)
print('[*] path : ' + os.getcwd() + '/kisa')
enc = hashlib.md5()

def DownloadFullPage(url, fPath):  
    #kwargs = {'bypass_robots': True, 'project_name': 'recognisable-name', 'bypass_robots' : True, 'debug' : True,'open_in_browser' : True, 'delay':None,'threaded':False}
    kwargs = {'bypass_robots': True, 'project_name': 'recognisable-name', 'bypass_robots' : True, 'debug' : False,'open_in_browser' : True, 'delay':None,'threaded':False}
    save_webpage(url, fPath, **kwargs)

def SendMessage(payload, msg):
    payload["text"] = str(msg)
    response = requests.request("POST", "https://webexapis.com/v1/messages", data=json.dumps(payload),
                                    headers=headers)
    response = json.loads(response.text)
    return {'messageId' : response['id']}

def ModifyMessage(payload, msg, messageId):
    payload["text"] = str(msg)
    requests.request("PUT", "https://webexapis.com/v1/messages/{}".format(messageId),
                                                data=json.dumps(payload), headers=headers)
def GetFilePath(selected, url):
    parser_url = urlparse(url)
    if selected == 'url':
        return url.replace(os.path.basename(parser_url.path), '')
    elif selected == 'uri':
        return os.path.split(f'{parser_url.path}')[0]
    elif selected == 'file':
        return os.path.basename(parser_url.path)

def RetrieveFiles(rscPath, parent_file, cur_path, level=''):
    with open(f'{rscPath}/{parent_file}', 'r', encoding='utf8', errors='ignore') as f_r:
        content = f_r.read()
    if '요청하는 페이지를 찾을 수 없습니다.' in content:
        return False
    srcs =re.findall('((?:https*:\/\/[\w\_\-0-9]*?\.[\w\_\-0-9]+\.\w+(?:\:\d+)*)*\/*[a-zA-Z\-\_0-9\.\/]+?\.(?:css|js|png|swg|woff|woff2|gif|ico|svg))[\)\"\']',  content)
    for s in srcs:
        target_file = GetFilePath('file', s)
        if os.path.exists(f'{rscPath}/{target_file}'):
            down_fName = 'a' + target_file 
        else : 
            down_fName = target_file
        if s.startswith('http'):
            system(f'wget {s} -O {rscPath}/{target_file}')        
            print('1111')
            next_path = GetFilePath('url', s)
            downpath = s
        else:
            uri = GetFilePath('uri', s)
            print('22222')
            if not (uri=='/' or len(uri)==0):
                #next_path = cur_path + uri
                next_path = url + uri
                #아래도 추가
                cur_path = url + uri
            else:
                next_path = cur_path
                
            if not s.endswith('/') :
                system(f'wget {cur_path}/{target_file} -O {rscPath}/{down_fName}')
                downpath = f'{cur_path}/{target_file}'
            else:
                system(f'wget {cur_path}{target_file} -O {rscPath}/{down_fName}')
                downpath = f'{cur_path}{target_file}'
            '''
            if 'sprite.png' in target_file:
                with open(f'{rscPath}/{parent_file}', 'r', encoding='utf8', errors='ignore') as f_r:
                    content = f_r.read()
                    content = content.replace(f'{s}', target_file)
                with open(f'{rscPath}/{parent_file}_out', 'w', encoding='utf8', errors='ignore') as f_r:
                    f_r.write(content)
                print('\n\n\n[*] down path : ' + target_file)
                print('[*] level : ' + level)
                input(f's : {s}')
            ''' 
        with open(f'{rscPath}/{parent_file}', 'r', encoding='utf8', errors='ignore') as f_r:
            content = f_r.read()
            content = content.replace(f'{s}', target_file)
        with open(f'{rscPath}/{parent_file}', 'w', encoding='utf8', errors='ignore') as f_r:
            f_r.write(content)
        '''
        print('333')
        print('[*] downpath : ' + downpath)
        print('[*] level : ' + ' - '.join(level))
        print('[*] origin : ' + s)
        print('[*] file name : ' + target_file)
        '''
        #input('[*] next_path : ' + next_path)
        RetrieveFiles(rscPath, target_file, next_path, level=level + ' / ' + target_file)

def SendFile(fullPath, roomId, text=""):
    print('send the file')
    with open(fullPath, 'rb') as f:
        cmd = f"""curl --request POST\
         --header "Authorization: Bearer {accessToken}"\
         --form "files=@{fullPath};type=image/png"\
         --form "roomId={roomId}"\
         --form "text={text}"\
         https://webexapis.com/v1/messages"""
        os.system(cmd)

def CheckNotice():
    global num_last, roomId_kisa_private, roomId_use, fPath_kisa, fPath_working
    list_files = []
    for page in range(5,0,-1):
        response = requests.post(f"{url}/kr/bbs/list.do", data={'pageIndex' : page, 'bbsId' : 'B0000133', 'menuNo' : '205020', 'searchCnd' : '1'})
        soup = bs(response.text, "html.parser")
        elements = soup.select('#List > div.board > div > table > tbody > tr')
        for element in elements[::-1]:
            tds = element.select("td")
            num = tds[0].get_text().strip()
            title = tds[1].get_text().strip()
            title = title.replace('(', '__').replace(')', '__')
            link = url + tds[1].find('a')['href']
            fullDate = tds[4].get_text().strip()
            try:
                num = int(num)
            except ValueError:
                print(f'[*] 보안공지 다운로드 실패 - 아마 공지사항.. : {fullDate}_{title}_{num}')
                continue
            
            try:
                if num > int(num_last):
                    date=fullDate
                    title = '_'.join(title.split(' '))
                    htmlPath = f'{fPath_kisa}/{date}_{title}_{num}'
                    DownloadFullPage(link, htmlPath)
                    sourcePath = htmlPath + '/recognisable-name/krcert.or.kr/kr/bbs'
                    htmlName = [x for x in listdir(sourcePath) if '.html' in x][0]
                    source = ''
                    with open(f'{sourcePath}/{htmlName}', 'r') as f:
                        source = f.read()
                    soup = bs(source, "html.parser")

                    rscPath = htmlPath + '/recognisable-name/krcert.or.kr/kr/bbs/rsc'
                    system(f'mkdir {rscPath}')
                    #source=parse.unquote(source)
                    rsc_srcs = re.findall('(?:href|src)\=\"(\/(?:\w+\/)*[\w\-\.]+?\.(?:js|css|ico|png|gif|tif|jpg|bmp))\"', source)
                    rsc_srcs = rsc_srcs + re.findall('img src=\"(.+?)\"', source)
                    rsc_srcs = list(set(rsc_srcs))
                    for rsc in rsc_srcs:
                        new_src = GetFilePath('file', rsc)
                        #input('[*] Root fileName : ' + new_src)

                        cur_path = GetFilePath('url', rsc)
                        source = source.replace(rsc, './rsc/' + new_src )
                        system(f'wget {url}{rsc} -O {rscPath}/{new_src}')
                        RetrieveFiles(rscPath, new_src, url + cur_path, level=new_src)

                    with open(f'{sourcePath}/{htmlName}', 'w') as f:
                        f.write(source)
                    os.chdir(fPath_kisa + f'/{date}_{title}_{num}/recognisable-name/')
                    time.sleep(2)
                    system(f'zip -r {date}_{title}_{num}.zip *')
                    system(f'mv {date}_{title}_{num}.zip {fPath_kisa}')
                    list_files.append([f'{fPath_kisa}/{date}_{title}_{num}.zip', f'[*] 새로운 보안공지 확인\n[{num}] {title} ({fullDate})'])
                    time.sleep(2)
                    os.chdir(fPath_kisa)
                    system(f'rm -rf {date}_{title}_{num}')
                    ###
                    #SendFile(f'{fPath_kisa}/{date}_{title}_{num}.zip', roomId_use, f'[*] 새로운 보안공지 확인\n[{num}] {title} ({fullDate})')
                    system(f'{fPath_kisa}/{date}_{title}_{num}.zip')
                    #input(f'\n\n[*] file : {fPath_kisa}/{date}_{title}_{num}.zip')
                    num_last = int(num)
            except Exception as e:
                payload = {"roomId": roomId_use}
                num_last = int(num)
                print('### ' + str(e))
                #input(f'[*] 예외 발생!!! ==> {new_src}')
                os.chdir(fPath_working)
                with open('error.log', 'a') as f:
                    now = datetime.datetime.now()
                    now = now + datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=9, weeks=0)
                    f.write(f'[{now}] ' + str(e) + f'({num_last})\n')
                    print('@@@ num : ' + str(num_last))
    return list_files

                
app = Flask(__name__)

'''
@app.route('/', methods=['POST'])
def receive():
    #global roomId_kisa_private
    data = request.json.get('data')
    email, messageId = data['personEmail'], data['id']
    print('message : ' + str(data))
    if email == botEmail:
        return ("")
    #response = json.loads(requests.request("GET", "https://api.ciscospark.com/v1/messages/{}".format(messageId), headers=headers).text)
    #print(str(response))
    #msgs = response['text'].strip().split('\n')
    #payload = {"roomId": roomId_kisa_private}
    #SendMessage(payload, "Echo : Hi!!")
    return {'status' : 'success', 'num_last': num_last}
'''

@app.route('/', methods=['GET'])
def BotComu():
    return "123"
    global roomId_use, num_last
    temp = num_last
    print('num_last : ' + str(num_last) )
    GS25()
    try:
        num = request.args.to_dict()['num']
        print('@num : ' + str(num))
        num = int(num)
        num_last = num
    except:
        print('@num_last : ' + str(num_last))
    return {'status' : 'success', 'num_last': num_last}

def GS25():
    global roomId_kisa_private, roomId_soc, num_last, roomId_use, fPath_working
    print('Im GS25  - num last : ' + str(num_last))
    for fPath, title in CheckNotice():
    	SendFile(fPath, roomId_use, title)
    	system(f"rm {fPath}")
    os.chdir(fPath_working)
    with open('num_last.txt', 'w') as f:
        print('what is wrong? : '+ str(num_last))
        f.write(str(num_last))
    print('Bye Bye - num last : ' + str(num_last))
    
def CallerCheck():
    sched = BlockingScheduler(timezone='Asia/Seoul')
    sched.add_job(GS25,'interval', minutes=30, id='kisa')
    #sched.add_job(GS25,'interval', minutes=1, id='kisa')
    sched.start()
def CallerCheck2():
    sched = BlockingScheduler(timezone='Asia/Seoul')
    #sched.add_job(CheckAvailability,'interval', minutes=60*24, id='availability')
    sched.add_job(CheckAvailability,'date', hour='10', id='availability')
    #sched.add_job(CheckAvailability,'interval', minutes=1, id='availability')
    sched.start()
def CallerCheck3():
    sched = BlockingScheduler(timezone='Asia/Seoul')
    sched.add_job(CheckCallForwarding,'date', hour='8',minute='50', id='CheckCallForwarding')
    sched.add_job(SaveEletrics,'date', hour='17',minute='50', id='saveEletrics')
    sched.start()


def CheckAvailability():
    global roomId_availability, now, roomId_use
    payload = {"roomId": roomId_availability}
    now = datetime.datetime.now()
    now = now + datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=9, weeks=0)
    SendMessage(payload, "[{}] 상태 체크".format(now.strftime('%Y-%m-%d %H:%M:%S')))

    
def SaveEletrics(prefix=''):
    global roomId_availability, now, roomId_use
    payload = {"roomId": roomId_use}
    now = datetime.datetime.now()
    now = now + datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=9, weeks=0)
    SendMessage(payload, "[{}] 퇴근 시간입니다. 코드 전원 꺼주세요.".format(now.strftime('%Y-%m-%d %H:%M:%S')))


def CheckCallForwarding(prefix=''):
    global roomId_availability, now, roomId_use
    payload = {"roomId": roomId_use}
    now = datetime.datetime.now()
    now = now + datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=9, weeks=0)
    SendMessage(payload, "[{}] 퇴근 시간입니다. 전화 착신 확인해주세요.".format(now.strftime('%Y-%m-%d %H:%M:%S')))
    
def run():
    payload = {"roomId": roomId_availability}
    SendMessage(payload, "[{}] 상태 체크".format(now.strftime('%Y-%m-%d %H:%M:%S')))
    t = threading.Thread(target=CallerCheck)
    t.start()
    t2 = threading.Thread(target=CallerCheck2)
    t2.start()
    t3 = threading.Thread(target=CallerCheck3)
    t3.start()
    app.run(host="0.0.0.0", port=9099)

GS25()
run()