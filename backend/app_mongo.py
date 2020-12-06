from flask import Flask
from flask import request
import uuid
import json
import time
from threading import  Lock
import  pymongo

client = pymongo.MongoClient('mongodb://root:123456@172.17.169.235:27017/')
db = client.ocrs
collection = db.ocrs

lock = Lock()
app = Flask(__name__)



@app.route('/')
def hello_world():
    return 'Hello World!'

# @app.route('/post/picture')
# def get_picture():
#     return 'h'
@app.route('/api/getResult',methods=['POST'])
def getStatus():
    print(request,'request')
    fileId = request.get_json()['uuid']
    print(fileId,'fileID')

    result = {}

    condition = {
        "uuid":fileId
    }
    # 查询图片识别结果
    queryRes = collection.find_one(condition)
    status = int(queryRes['status'])
    result['status'] = status
    # 状态为0说明还未完成，返回前置队列数，否则返回识别结果
    if status == 0:
        creTime = queryRes['createTime']
        condition = {
            "createTime":{
                "$lt":creTime
            }
        }
        # print(time.time(),time.time_ns())
        # 从数据库查询前置队列数
        remain = collection.count_documents(condition)
        # print(time.time_ns())
        result['remain'] = remain
        return json.dumps(result)
    else:
        # 识别完成，返回结果
        result['result'] = queryRes['result']
        return json.dumps(result)



@app.route('/api/post/picture', methods=['GET', 'POST'])
def uploadFile():
    if request.method == 'POST':

        try:
            f = request.files['pic']
            print('receiving file',f)

            # 用uuid生成一个新的文件名并保存
            fileName = str(f.filename)
            print(fileName)
            fileType = fileName.split('.')[-1]
            id = str(uuid.uuid1())
            newFileName = id + '.' + fileType
            #读取图片文件
            f.seek(0)
            blob = f.read()
            #获取时间戳
            createTime = time.time_ns()

            # 加锁插入表
            lock.acquire()

            #插入数据库，图片作为blob插入

            insertData = {
                "uuid":id,
                "fileName":newFileName,
                "fileBlob":blob,
                "result":"",
                "status":0,
                "createTime":createTime
            }

            # sql = "insert into ocrs(uuid,fileName,fileBlob,status,createTime) values (%s,%s,%s,%s,%s)"
            # args = (id,newFileName,blob,0,createTime)
            ins_id = collection.insert_one(insertData).inserted_id
            print('ins_id=',ins_id)
            lock.release()

        except Exception as e:
            print(e,'ERROR WHILE UPLOADING')
        finally:
            return id

@app.route('/api/test',methods=['GET','POST'])
def test():
    print('in test............')
    return 'helloy'

