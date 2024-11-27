from pushbullet import Pushbullet

API_KEY = "o.9QimAOJozQVEwyRHUhT64O8o2svKiHob"
pb = Pushbullet(API_KEY)
push = pb.push_note('Alpha Diary',"We have Recieved your complaint it will be processed soon")
from urllib.parse import urlencode
from urllib.request import urlopen,Request
user="BRIJESH"
key="066c862acdXX"
senderid="UPDSMS"
accusage="1"
entityid="1201159543060917386"
tempid="1207169476099469445"
message="We have Recieved your complaint it will be processed soon"
def sendsms(mobile):
    values={
'user':user,
'key':key,
'mobile':mobile,
'message':message,
'senderid':senderid,
'accusage':accusage,
'entityid':entityid,
'tempid':tempid
        }
    url="http://sms.bulkssms.com/submitsms.jsp"
    postdata=urlencode(values).encode("utf-8")
    req=Request(url,postdata)
    response=urlopen(req)
    response.read()
    push = pb.push_note('Alpha Diary',"We have Recieved your complaint it will be processed soon")
if __name__ == "__main__":

	sendsms(7307783941)
