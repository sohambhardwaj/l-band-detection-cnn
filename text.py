import cv2
import os
import pymysql
from skimage.measure import compare_ssim
import imutils
from datetime import date, datetime,timedelta

connection = pymysql.connect(host='localhost', user = 'root', db='db')
cursor = connection.cursor()

def add_rectangle(img):
    h,w,_=img.shape
    hr=int(0.77*h)
    wr=int(0.79*w)
    img=cv2.rectangle(img,(w,0),(w-wr,hr),(0,0,0),-1)
    return img

def check_similarity(img,channel_name,current_time):
    cursor.execute("SELECT * FROM `test` WHERE `channel`={}".format(channel_name))
    q=cursor.fetchall()
    threshold=0.85 #needs to be set
    if(len(q)==0):
        return False
    for ad in q:
        imgA=img
        imgB=cv2.imread(ad[4])
        (score, diff) = compare_ssim(imgA,imgB, full=True, multichannel=True)
        time_diff=(datetime.strptime(current_time,"%Y-%m-%d %H:%M:%S")-datetime.strptime(ad[3],"%Y-%m-%d %H:%M:%S"))/timedelta(minutes=1)
        if(score>threshold & time_diff>=1):
            print("Ad already detected on this channel")
            cursor.execute("INSERT INTO `test`(`channel`,`advertiser`,`tagline`,`time_found`,`path_to_image`) VALUES ({},{},{},{},{})".format(channel_name,ad[1],ad[2],current_time,ad[4]))
            return True
    return False

def extract_text(img,channel_name,current_time):
    img=add_rectangle(img)
    txt=text_on_screen(img)
    if(len(txt)<7):
        return
    check=check_similarity(img,channel_name,current_time)
    if(check==False):
        #manual check. inputs for advertiser and tagline
        advertiser="Maruti"
        tagline="Dzire"
        PATH="local_storage/file" + advertiser + "-" +tagline + "-" + current_time +".jpg"
        cv2.imwrite(PATH,img)
        cursor.execute("INSERT INTO `test`(`channel`,`advertiser`,`tagline`,`time_found`,`path_to_image`) VALUES ({},{},{},{},{})".format(channel_name,advertiser,tagline,current_time,PATH))
    return
       




