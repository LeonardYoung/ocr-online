from . import text_ocr
from multiprocessing import Process, Queue
import json
import os
import time


print('in module run_ocr')
MAX_SIZE = 1024

input_queue = Queue(MAX_SIZE)
output_queue = Queue(MAX_SIZE)

# import os


#执行检测文件
def run_detection(input_image_path):

    project_root = os.path.dirname(os.path.realpath("yolov5-master"))  # 获取项目根目录
    result_file = project_root + "\\yolov5-master\\runs\\detect\\result\\1.txt"
    rootpath=project_root + "\\yolov5-master\\"
    # rootpath=rootpath[:-4]
    # print(rootpath)
    Pyfile=rootpath+"detect.py"
    weight=rootpath+"runs/train/exp13/weights/best.pt"
    # data=rootpath+"test"
    ranlan="python "+Pyfile+" --source "+input_image_path+" --weights "+weight
    # print(ranlan)

    # 删除结果文件
    if os.path.exists(result_file):
        with open(result_file,'w') as f:
            f.truncate()
        # os.remove(result_file)

    # 运行程序
    os.system(ranlan)

    lines = []
    with open(result_file) as f:
        lines.append(f.readline())
        lines.append(f.readline())
    positions = []
    yy = []
    for line in lines:
        items = line.split(' ')
        if len(items) != 5 :
            break

        yy.append(float(items[2]))
        x = float(items[1])
        y = float(items[2])
        w = float(items[3])
        h = float(items[4])

        point0 = [x - w / 2, y - h /2]
        point1 = [x + w / 2, y - h /2]
        point2 = [x + w / 2, y + h / 2]
        point3 = [x - w/2, y + h/2]
        position = [point0, point1,point2,point3]
        positions.append(position)

    if lines[0][0] == '1':
        positions.reverse()

    result_data = [{"text": 'Ω', "text_box_position": positions[-1]}]
    # 有两行，说明识别到了 'm'
    if len(yy) ==2 and abs(yy[0] - yy[1]) > 3:
        result_data.append({"text": 'm', "text_box_position": positions[0]})

    return result_data



def target_ocr(t, inq, ouq):
    ocr = text_ocr.TextOcr(t)
    while True:
        one = inq.get()
        print('ocr start one :', one)
        file_path = 'input/' + one['new_file_name']
        f = open(file_path, mode='wb')
        f.write(one['img_blob'])
        f.close()

        # 调用识别算法
        # res, dtime = ocr.ocr_single(file_path)
        # 调用仪表数据识别算法
        res, dtime = ocr.get_feature(file_path)

        # 调用yolov5 识别mΩ
        ex_result = run_detection(file_path)

        # json.loads(res)[0]['data'],


        # 放入输出队列
        out_data = {
            'uid': one['uuid'],
            # 'data': res[0]
            'ocr_data': json.loads(res)[0]['data'] + ex_result,
            'dtime': dtime
        }
        ouq.put(out_data)


def run_ocr(t):
    print('--------OCR STARTING-----------')
    Process(target=target_ocr, args=(t, input_queue,output_queue)).start()


if __name__ == "__main__":
    run_detection('E:\\project\\major\\ocrs\\backend\\yolov5-master\\data\\e.png')
    print('in run OCR main....')