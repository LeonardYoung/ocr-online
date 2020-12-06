import cv2
import json
import timeit
import paddlehub as hub


class TextOcr:
    def __init__(self, t):
        if t == 'mobile':
            self.__ocr = hub.Module(name="chinese_ocr_db_crnn_mobile")
        elif t == 'server':
            self.__ocr = hub.Module(name="chinese_ocr_db_crnn_server")
        else:
            print('wrong type ;would run server mode')
            self.__ocr = hub.Module(name="chinese_ocr_db_crnn_server")

    # 读取图像，解决imread不能读取中文路径的问题
    def cv_imread(self,file_path):
        # cv_img = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), -1)
        # return cv_img
        cv_img = cv2.imread(file_path)
        return cv_img

    # 多张图片ocr
    def ocr_batch(self,image_list):
        start = timeit.default_timer()

        np_images = [cv2.imread(image) for image in image_list]
        result = self.__ocr.recognize_text(
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
    def ocr_single(self,image):
        start = timeit.default_timer()

        np_image = [self.cv_imread(image)]
        result = self.__ocr.recognize_text(
            images=np_image,  # 图片数据，ndarray.shape 为 [H, W, C]，BGR格式；
            use_gpu=False,  # 是否使用 GPU；若使用GPU，请先设置CUDA_VISIBLE_DEVICES环境变量；
            output_dir='ocr_result',  # 图片的保存路径；
            visualization=True,  # 是否将识别结果保存为图片文件；
            box_thresh=0.5,  # 检测文本框置信度的阈值；
            text_thresh=0.5)  # 识别中文文本置信度的阈值；

        result_json = json.dumps(result, ensure_ascii=False)

        end = timeit.default_timer()
        time_cost = end - start  # 秒

        return result_json, time_cost


if __name__ == "__main__":
    print('in text_ocr main....')

    # 加载移动端预训练模型
    # ocr = hub.Module(name="chinese_ocr_db_crnn_mobile")
    ocr = TextOcr(t='mobile')
    # 服务端加载大模型，效果更好
    # ocr = hub.Module(name="chinese_ocr_db_crnn_server")
    # ocr = TextOcr(t='server')

    # 单张图片示例
    image = 'samples/2.png'
    res, time = ocr.ocr_single(image)  # 图片无法返回，可在output_dir中指定图片的保存路径
    print(res, '\n', time)

    # 多张图片示例
    # image_list = ['1.png', '2.png']
    # res, time = ocr_batch(image_list)  # 图片无法返回，可在output_dir中指定图片的保存路径
    # print(res, '\n', time)
