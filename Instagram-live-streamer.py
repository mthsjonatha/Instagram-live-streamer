import subprocess,os,shutil,ctypes,sys,json,time,random,base64,hmac,hashlib
import urllib.request
from datetime import datetime
from tkinter import Tk
from tkinter.filedialog import askopenfilename
if not(ctypes.windll.shell32.IsUserAnAdmin()) : ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)



def microtime(get_as_float = False) :
    d = datetime.now()
    t = time.mktime(d.timetuple())
    if get_as_float:
        return t
    else:
        ms = d.microsecond / 1000000.
        return '%f %d' % (ms, t)

def getUserId(username):
    resp = urllib.request.urlopen("http://instagram.com/{}/".format(username))
    resp = resp.read().decode()
    resp = resp.split(',"id":"')[1]
    resp = resp.split('"')[0]
    return resp

def createBroadcast(api):
    data = json.dumps({'_uuid': api.uuid,
                           '_uid': api.username_id,
                           'preview_height': 1920,
                           'preview_width': 1080,
                           'broadcast_message': '',
                           'broadcast_type': 'RTMP',
                           'internal_only': 0,
                           '_csrftoken': api.token})
    return api.SendRequest('live/create/', api.generateSignature(data))

def startBroadcast(api,broadcastId):
    data = json.dumps({'_uuid': api.uuid,
                           '_uid': api.username_id,
                           'should_send_notifications': int(True),
                           '_csrftoken': api.token})
    return api.SendRequest('live/' + str(broadcastId) + '/start', api.generateSignature(data))

def stopBroadcast(api, broadcastId):
        data = json.dumps({'_uuid': api.uuid,
                           '_uid': api.username_id,
                           '_csrftoken': api.token})
        return api.SendRequest('live/' + str(broadcastId) + '/end_broadcast/', api.generateSignature(data))

def addBroadcastToLive(api, broadcastId):
        data = json.dumps({'_uuid': api.uuid,
                           '_uid': api.username_id,
                           '_csrftoken': api.token})
        return api.SendRequest('live/' + str(broadcastId) + '/add_to_post_live/', api.generateSignature(data))


def postCommentBroadcast(api,broadcastId,message):
    data = json.dumps({'user_breadcrumb': UserBreadcrumb(len(message)).decode(),
                           'idempotence_token': generateUUID(True),
                           'comment_text': message,
                           'live_or_vod' : 1,
                           'offset_to_video_start' : 0})
    return api.SendRequest('live/' + str(broadcastId) + '/comment/', api.generateSignature(data))


def pinComment(api,broadcastId,commentId):
    data = json.dumps({ 'offset_to_video_start': 0,
                            'comment_id' : commentId,
                            '_uuid': api.uuid,
                            '_uid': api.username_id,
                            '_csrftoken': api.token})
    return api.SendRequest('live/' + str(broadcastId) + '/pin_comment/', api.generateSignature(data))

def muteComments(api,broadcastId):
    data = json.dumps({'_uuid': api.uuid,
                           '_uid': api.username_id,
                           '_csrftoken': api.token})
    return api.SendRequest('live/' + str(broadcastId) + '/mute_comment/', api.generateSignature(data))

def unmuteComments(api,broadcastId):
    data = json.dumps({'_uuid': api.uuid,
                           '_uid': api.username_id,
                           '_csrftoken': api.token})
    return api.SendRequest('live/' + str(broadcastId) + '/unmute_comment/', api.generateSignature(data))
    

def addBroadcastToFeed(api,broadcastId):
    data = json.dumps({ '_uuid': api.uuid,
                            '_uid': api.username_id,
                            '_csrftoken': api.token})
    return api.SendRequest('live/' + str(broadcastId) + '/add_to_post_live/', api.generateSignature(data))

def getComments(api,broadcastId,lastCommentTs=0,commentsRequested=3):
    data = json.dumps({ 'last_comment_ts': lastCommentTs,
                            'num_comments_requested': commentsRequested})
    return api.SendRequest('live/' + str(broadcastId) + '/get_comment/', api.generateSignature(data))



def UserBreadcrumb(length):
    key = 'iN4$aGr0m'
    date = microtime(True)*1000
    term = random.randrange(2,3)*1000 + length * random.randrange(15,20) * 100
    text_change_event_count = round(length/random.randrange(2,3))
    if text_change_event_count==0:
        text_change_event_count=1
    data = str(length)+" "+str(term)+" "+str(text_change_event_count)+" "+str(date)
    return base64.standard_b64encode(hmac.new(key.encode(),data.encode(),hashlib.sha256).digest())+b"\n"+base64.standard_b64encode(data.encode())+b"\n"

def generateUUID(dashes=True):
    if dashes:
        return "1c9bd518-002e-421b-8d38-5705a95c5a05"
    else:
        return "1c9bd518-002e-421b-8d38-5705a95c5a05".replace("-","")



os.system("copy .\ffmpeg.exe C:\\windows\\system32\\")







try:
    from InstagramAPI import InstagramAPI
except ImportError:
    os.system("pip install InstagramAPI")
    from InstagramAPI import InstagramAPI

USERNAME = input("Your username?\t")
PASSWORD = input("Your password?\t")
TYPE = input("Direct streaming or streaming from file?(d\\f)\t").lower()
if TYPE not in ("f","d"):
    print("Only f or d\nTerminating...")
    sys.exit()
if TYPE== "f":
    Tk().withdraw()
    FILE_PATH = askopenfilename()
PUBLISH_TO_LIVE_FEED = False
SEND_NOTIFICATIONS = False

api = InstagramAPI(USERNAME, PASSWORD, debug=False)
assert api.login()


assert createBroadcast(api)
broadcast_id = api.LastJson['broadcast_id']
upload_url = api.LastJson['upload_url']


assert startBroadcast(api,broadcast_id)
if TYPE== "f":
    comment = input("Your Comment? ")
    #Commented By Torabi
	#ffmpeg_cmd = "ffmpeg.exe -rtbufsize 256M -re -i \"{file}\" -acodec libmp3lame -ar 44100 -b:a 128k -pix_fmt yuv420p -profile:v baseline -s 720x1280 -bufsize 6000k -vb 400k -maxrate 1500k -deinterlace -vcodec libx264 -preset veryfast -g 30 -r 30 -f flv \"{stream_url}\"".format(
    ffmpeg_cmd = "ffmpeg.exe -rtbufsize 256M -re -i \"{file}\" -acodec libmp3lame -ar 44100 -b:a 128k -pix_fmt yuv420p -profile:v baseline -s 720x1280 -vf transpose=1 -bufsize 6000k -vb 400k -maxrate 1500k -deinterlace -vcodec libx264 -preset veryfast -g 30 -r 30 -f flv \"{stream_url}\"".format(
    file=FILE_PATH,
    stream_url=upload_url.replace(':443', ':80', ).replace('rtmps://', 'rtmp://'),
    )
    postCommentBroadcast(api,broadcast_id,comment)
    comment_id = api.LastResponse.json()['comment']['pk']
    pinComment(api,broadcast_id,comment_id)
if TYPE=="d":
    print(upload_url.replace(':443', ':80', ).replace('rtmps://', 'rtmp://'))
print("Hit Ctrl+C to stop broadcast")
try:
    if TYPE=="f":
        output = subprocess.check_output(ffmpeg_cmd,shell = True)
        #os.system(ffmpeg_cmd)
        #for i in output.stdout:
            #print(i)
        while True:
            act = input("1.send comment\n2.block user\n3.get comments\n4.mute comments\n5.unmute comments\n")

            if   act=="1":
                postCommentBroadcast(api,broadcast_id,input("Comment: "))
                comment_id = api.LastResponse.json()['comment']['pk']
                pinComment(api,broadcast_id,comment_id)
            elif act=="2":
                user_id = getUserId(input("Username: "))
                api.block(user_id)
            elif act=="3":
                try:
                    num = int(input("how many? "))
                except:
                    print("thats not a valid number\ntry again")
                    continue
                getComments(api,broadcast_id,commentsRequested=num)
                raw_comments = api.LastResponse.json()['comments']
                comments = list()
                for comment in raw_comments:
                    comments.append((comment['text'] , comment['user']['username'], comment['pk']))
                for comment in comments:
                    print("{}:{}\t<{}>".format( comment[1] , comment[0] , comment[2] ))
            elif act=="4":
                muteComments(api,broadcast_id)
            elif act=="5":
                unmuteComments(api,broadcast_id)
            else:
                continue
            #print(getComments(api,broadcast_id))
            

            #print(api.LastResponse.json())
    else:
        while True:
            act = input("1.send comment\n2.block user\n3.get comments\n4.mute comments\n5.unmute comments\n")

            if   act=="1":
                postCommentBroadcast(api,broadcast_id,input("Comment: "))
                comment_id = api.LastResponse.json()['comment']['pk']
                pinComment(api,broadcast_id,comment_id)
            elif act=="2":
                user_id = getUserId(input("Username: "))
                api.block(user_id)
            elif act=="3":
                try:
                    num = int(input("how many? "))
                except:
                    print("thats not a valid number\ntry again")
                    continue
                getComments(api,broadcast_id,commentsRequested=num)
                raw_comments = api.LastResponse.json()['comments']
                comments = list()
                for comment in raw_comments:
                    comments.append((comment['text'] , comment['user']['username'], comment['pk']))
                for comment in comments:
                    print("{}:{}\t<{}>".format( comment[1] , comment[0] , comment[2] ))
            elif act=="4":
                muteComments(api,broadcast_id)
            elif act=="5":
                unmuteComments(api,broadcast_id)
            else:
                continue
except KeyboardInterrupt:
    print('Stop Broadcasting')

assert stopBroadcast(api,broadcast_id)

print('Finished Broadcast')

if PUBLISH_TO_LIVE_FEED:
    a = addBroadcastToFeed(api,broadcast_id)
    print(a)
print('Added Broadcast to LiveFeed')
input()
