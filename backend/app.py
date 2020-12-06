from flask import Flask
from flask import request
import uuid, json

import time
from threading import Lock
import os
import sys
try:
    sys.path.append("./ocr")
    from ocr import run_ocr
    # text_ocr.ocr_init('test')
except Exception as e:
    print('Exception-----'
          '', e)
useDB = 0
if useDB:
    import pymysql
basedir = os.path.abspath(os.path.dirname(__file__))

if useDB:
    conn = pymysql.connect(
        host="127.0.0.1",
        # host="172.17.169.235",
        user="root",
        password="123456",
        database="ocrs",
        charset="utf8")
    lock = Lock()
    cursor = conn.cursor()  # 获取一个连接对象

# 新开一个进程，运行OCR算法
# run_ocr.run_ocr('mobile')
run_ocr.run_ocr('server')

# 开启Flask
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


all_result = {}


# 获取结果
@app.route('/api/getResult', methods=['POST'])
def get_result():
    print(request, 'request')
    uid = request.get_json()['uuid']


    result = {}
    try:
        #  把所有处理好的数据放到字典all_result中，极端情况下是否会很耗时？
        while not run_ocr.output_queue.empty():
            one = run_ocr.output_queue.get()
            all_result[one['uid']] = one['ocr_data']

        print(all_result)
        # id在字典中，说明已经处理完毕，则返回识别结果
        if uid in all_result:
            result['status'] = 1
            result['result'] = all_result[uid]
            # del all_result[uid]
        else:
            result['status'] = 0
            result['remain'] = 3
        return json.dumps(result)
        # sql = "select status,result,createTime from ocrs where uuid=%s"
        # args = (fileId)
        # cursor.execute(sql, args)
        # conn.commit()
        # res = cursor.fetchone()
        # print('res:', res)
        # status = int(res[0])
        #
        # result['status'] = status
        # # 状态为0说明还未完成，返回前置队列数，否则返回识别结果
        # if status == 0:
        #     sql2 = "select COUNT(*) from ocrs where status=0 and createTime < %s"
        #     args=(res[2])
        #     cursor.execute(sql2, args)
        #     conn.commit()
        #     res = cursor.fetchone()[0]
        #     result['remain'] = res
        #     return json.dumps(result)
        # else:
        #     result['result'] = res[1]
        #     return json.dumps(result)

    except Exception as e:
        print(e, 'ERROR WHILE GETTING RESULTS')
        return '0'


# 处理跨域问题
@app.after_request
def cors(environ):
    environ.headers['Access-Control-Allow-Origin']='*'
    environ.headers['Access-Control-Allow-Method']='*'
    environ.headers['Access-Control-Allow-Headers']='x-requested-with,content-type'
    return environ


# 上传图片
@app.route('/api/post/picture', methods=['GET', 'POST'])
def upload_file():
    print('posting picture')
    if request.method == 'POST':
        # event.set()
        uid = -1
        try:
            f = request.files['pic']

            # 用uuid生成一个新的文件名并保存
            file_name = str(f.filename)
            file_type = file_name.split('.')[-1]
            uid = str(uuid.uuid1())
            new_file_name = uid + '.' + file_type

            # 读取图片文件
            f.seek(0)
            blob = f.read()

            # 数据放入队列中，交给后置进程处理
            inq = {
                "img_blob": blob,
                "uuid": uid,
                "new_file_name": new_file_name
            }
            # print(run_ocr.input_queue)
            run_ocr.input_queue.put(inq)

            if useDB:
                # 获取时间戳
                create_time = time.time_ns()
                # 插入数据库
                sql = "insert into ocrs(uuid,fileName,status,createTime) values (%s,%s,%s,%s)"
                args = (uid, new_file_name, 0, create_time)

                # 加锁插入表,不加锁会报错
                lock.acquire()
                cursor.execute(sql, args)
                lock.release()

                conn.commit()

        except Exception as e:
            print(e, 'ERROR WHILE UPLOADING')
        finally:
            print('uid=',uid)
            return uid


@app.route('/api/post/pic', methods=['GET', 'POST'])
def upload_file1():
    if request.method == 'POST':
        # event.set()
        uid = -1
        try:
            f = request.data
            print(f)
            return "aaa"

        except Exception as e:
            print(e, 'ERROR WHILE UPLOADING')
        finally:
            return uid


@app.route('/api/test', methods=['GET', 'POST'])
def test():
    print('-------------------testj----')

    return 'hello world\r\n'

