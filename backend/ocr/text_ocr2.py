import paddlehub as hub
import cv2
import json
import timeit
import numpy as np
from PIL import Image, ImageDraw


# 加载移动端预训练模型
ocr = hub.Module(name="chinese_ocr_db_crnn_mobile")
# 读取图像，解决imread不能读取中文路径的问题
def cv_imread(file_path):
    cv_img = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), -1)
    return cv_img


# 多张图片ocr
def ocr_batch(image_list):
    start = timeit.default_timer()

    np_images = [cv2.imread(image) for image in image_list]
    result = ocr.recognize_text(
        images=np_images,  # 图片数据，ndarray.shape 为 [H, W, C]，BGR格式；
        use_gpu=False,  # 是否使用 GPU；若使用GPU，请先设置CUDA_VISIBLE_DEVICES环境变量；
        output_dir='ocr_result',  # 图片的保存路径；
        visualization=True,  # 是否将识别结果保存为图片文件；
        box_thresh=0.5,  # 检测文本框置信度的阈值；
        text_thresh=0.5)  # 识别中文文本置信度的阈值；

    result_json = json.dumps(result, ensure_ascii=False)

    end = timeit.default_timer()
    time_cost = end - start  # 秒

    return result_json, time_cost


# 单张图片ocr
def ocr_single(image):
    start = timeit.default_timer()

    np_image = [cv2.imread(image)]
    result = ocr.recognize_text(
        images=np_image,  # 图片数据，ndarray.shape 为 [H, W, C]，BGR格式；
        use_gpu=False,  # 是否使用 GPU；若使用GPU，请先设置CUDA_VISIBLE_DEVICES环境变量；
        output_dir='ocr_result',  # 图片的保存路径；
        visualization=True,  # 是否将识别结果保存为图片文件；
        box_thresh=0.5,  # 检测文本框置信度的阈值；
        text_thresh=0.5)  # 识别中文文本置信度的阈值；
    # print(result)

    # print(type(result))
    position = result[0]["data"][0]["text_box_position"]
    # print("!!!")
    # print(position)
    result_json = json.dumps(result, ensure_ascii=False)

    end = timeit.default_timer()
    time_cost = end - start  # 秒

    return result, result_json, time_cost, position


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def get_feature():
    two = {}
    # 服务端加载大模型，效果更好
    # ocr = hub.Module(name="chinese_ocr_db_crnn_server")

    # 单张图片示例
    # image = './1/02.jpg'
    image = '1.png'

    # save_image = 'D:\\text.png'
    data, res, time, position = ocr_single(image)  # 图片无法返回，可在output_dir中指定图片的保存路径 获取直流电阻测试仪的矩阵坐标，根据坐标计算数值坐标位置
    # print(position)
    # 纵坐标选择较小值，横坐标选择较大值
    pos = [position[1][1], position[3][1], position[0][0], position[1][0]]
    # print(pos)
    one = data[0]['data'][0]

    img = cv2.imread(image)

    cha = pos[1] - pos[0]
    x = cha * 4 + pos[0]
    x1 = int(cha * 6) + pos[0]
    y = pos[2]

    y1 = int(pos[3] * 0.8)
    distance = cha * 2 + pos[0]
    img2 = img
    im = Image.open(image)
    draw = ImageDraw.Draw(im)
    draw.line([(position[0][0], position[0][1]), (position[1][0], position[1][1]), (position[2][0], position[2][1]),
               (position[3][0], position[3][1]), (position[0][0], position[0][1])], width=1, fill='red')
    pt1 = (position[1][0], position[1][1])  # 左边，上边   #数1 ， 数2
    pt2 = (position[3][0], position[3][1])  # 右边，下边  #数1+数3，数2+数4
    cv2.rectangle(img2, pt1, pt2, (0, 255, 0), 1)
    for i in range(len(data)):
        for j in range(len(data[i]['data'])):
            if is_number(data[i]['data'][j]['text']) and data[i]["data"][j]["text_box_position"][1][1] > distance:
                # position = data[i]["data"][j]["text_box_position"]
                two = data[i]['data'][j]
                # draw = ImageDraw.Draw(im)
                # draw.line([(position[0][0], position[0][1]), (position[1][0], position[1][1]),
                #            (position[2][0], position[2][1]), (position[3][0], position[3][1]),
                #            (position[0][0], position[0][1])], width=1, fill='red')
                # pt1 = (int(position[1][0] * 1.1), position[1][1])  # 左边，上边   #数1 ， 数2
                # pt2 = (position[3][0], position[3][1])  # 右边，下边  #数1+数3，数2+数4
                # cv2.rectangle(img2, pt1, pt2, (0, 255, 0), 1)
                break
    return one, two


if __name__ == "__main__":
    one,two = get_feature()
    print(one,two)