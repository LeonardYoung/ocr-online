import os
import datetime
import random
import subprocess
def delete_images(dir):

    project_root = os.path.dirname(os.path.realpath("core"))  # 获取项目根目录
    rootpath=project_root[:-10]
    print(rootpath)
    dir=project_root[:-10]+dir
    imgList = os.listdir(dir)  # 该文件夹下的图片列表
    num_imgs = len(imgList)  # 所含图片的数目
    BLACK = [0, 0, 0]
    for i in range(0, num_imgs):


        imgPath = os.path.join(dir, imgList[i])  # 每一张图片的全路径

        os.remove(imgPath)
    print("删除成功")

def create_name():
    nowTime =datetime.datetime.now().strftime("%Y%m%d%h%M%S")
    randomNum = random.randint(0,100)
    if(randomNum<=10):
        randomNum=str(0)+str(randomNum)
    uniqueNum=str(nowTime)+str(randomNum)
    return uniqueNum

#执行检测文件
def run_detection():
    project_root = os.path.dirname(os.path.realpath("yolov5-master"))  # 获取项目根目录
    rootpath=project_root
    rootpath=rootpath[:-4]
    # print(rootpath)
    Pyfile=rootpath+"detect.py"
    weight=rootpath+"runs/train/exp13/weights/best.pt"
    data=rootpath+"test"
    ranlan="python "+Pyfile+" --source "+data+" --weights "+weight
    # print(ranlan)
    p=os.system(ranlan)
    print(p)

def run_detection_mp4():
    project_root = os.path.dirname(os.path.realpath("core"))  # 获取项目根目录
    rootpath = project_root[:-10]  # 获取到CGAI
    print(project_root)
    Pyfile = rootpath + "CGAI_model/Smart_Construction-master/area_detect.py"
    weight = rootpath + "CGAI_model/Smart_Construction-master/runs/exp48/weights/best.pt"
    data = rootpath + "CGAI_model/Smart_Construction-master/vedio_test"
    ranlan = "python " + Pyfile + " --source " + data + " --weights " + weight
    print(ranlan)
    p = os.system(ranlan)
    print(p)

def change_type(root):
    inputfile=root+"CGAI_flask/static/save_vedio/test.mp4"
    outfile=root+"CGAI_flask/static/save_vedio/output.mp4"
    print("save"+outfile)
    cmd="ffmpeg -i "+inputfile+" -vcodec h264 "+outfile
    res=os.popen(cmd)
    text=res.read().strip()
    res.close()
    return text

run_detection()