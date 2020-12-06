# from PIL import Image


# if __name__ == '__main__':
#     img = Image.open("2.png")
#     print(img.size)
#     cropped = img.crop((0, 0, 512, 128))  # (left, upper, right, lower)
#     cropped.save("crop2.png")
# from multiprocessing import Process,Queue
# import time,random,os
#
#
# def consumer(q):
#     while True:
#         res=q.get()
#         # time.sleep(random.randint(1,3))
#         print('\033[45m%s 吃 %s\033[0m' %(os.getpid(),res))
#
#
# def producer(q):
#     pass
#     # for i in range(10):
#         # time.sleep(random.randint(1,3))
#         # res='包子%s' %i
#         # q.put(res)
#         # print('\033[44m%s 生产了 %s\033[0m' %(os.getpid(),res))
#
#
# if __name__ == '__main__':
#     q=Queue()
#     # 生产者们:即厨师们
#     p1=Process(target=producer,args=(q,))
#
#     # 消费者们:即吃货们
#     c1=Process(target=consumer,args=(q,))
#
#     # 开始
#     p1.start()
#     c1.start()
#     print('主')
#     q.put(11)
#     q.put(11)
#     q.put(11)
#     q.put(11)
#     q.put(11)

from multiprocessing import Process,Queue
import time



def sub_process(q):
    print('sub')
    q.put(3)
    q.put(4)
    q.put(4)
    q.put(4)


if __name__ == '__main__':

    # p.start()
    q = Queue(3)
    p = Process(target=sub_process, args=(q,))
    p.start()
    q.put(1)
    print(q.empty())
    a = q.get()
    print('a', a)
    a = q.get()
    print(a)
    a = q.get()
    print(q.full())


# print(q.get())
# print(q.get())
# print(q.get())
# print(q.empty()) #空了



#
#
# import numpy as np
#
# import cv2
# from PIL import Image
#
# image = cv2.imread("text_ocr/2.png")
#
# b  = np.array([[100,100],  [250,100], [300,220],[100,230]], dtype = np.int32)
#
# roi_t = []
# for i in range(4):
#     roi_t.append(b[i])
#
# roi_t = np.asarray(roi_t)
# roi_t = np.expand_dims(roi_t, axis=0)
# im = np.zeros(image.shape[:2], dtype = "uint8")
# cv2.polylines(im, roi_t, 1, 255)
# cv2.fillPoly(im, roi_t, 255)
#
# mask = im
# # cv2.imshow("Mask", mask)
# masked = cv2.bitwise_and(image, image, mask=mask)
# # cv2.imshow("Mask to Image", masked)
#
#
# imp = Image.fromarray(image)
#
# array = np.zeros((masked.shape[0], masked.shape[1], 4), np.uint8)
# array[:, :, 0:3] = masked
# array[:, :, 3] = 0
# array[:,:,3][np.where(array[:,:,0]>2)]=255
# array[:,:,3][np.where(array[:,:,1]>2)]=255
# array[:,:,3][np.where(array[:,:,2]>2)]=255
# # print(array.max())
# image_1 = Image.fromarray(array)
# image_1.save("text_ocr/crop222.png","PNG")