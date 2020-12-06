from . import text_ocr
from multiprocessing import Process, Queue
import json
import os
import time

print('in module run_ocr')
MAX_SIZE = 1024

input_queue = Queue(MAX_SIZE)
output_queue = Queue(MAX_SIZE)


def target_ocr(t, inq, ouq):
    ocr = text_ocr.TextOcr(t)
    while True:
        one = inq.get()
        print('ocr start one :', one)
        file_path = 'input/' + one['new_file_name']
        f = open(file_path, mode='wb')
        f.write(one['img_blob'])
        f.close()
        # 因为不熟悉ocr所使用的格式，这里的图片是写入再读取，有需要可以优化
        # 调用识别算法
        res, dtime = ocr.ocr_single(file_path)
        # res= [
        #     {
        #         'text': 'Hello',
        #         'data': 'World'
        #     }
        # ]
        # dtime = 2
        print(type(res))
        print(json.loads(res)[0], '\n', dtime)

        # 放入输出队列
        out_data = {
            'uid': one['uuid'],
            # 'data': res[0]
            'ocr_data': json.loads(res)[0]['data']
        }
        ouq.put(out_data)


def run_ocr(t):
    print('--------OCR STARTING-----------')
    Process(target=target_ocr, args=(t, input_queue,output_queue)).start()


if __name__ == "__main__":
    print('in run OCR main....')