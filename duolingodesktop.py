import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# %matplotlib inline

cv2.__version__
    
inputvideo = "H:\GameplayFootage\Jeremy\\DuolingoPolishBasics2-4.mp4"

filename, file_extension = os.path.splitext(inputvideo)
tempvid = filename + '.avi'
tempwav = filename + '.wav'
outvideo = filename + '-ffmpg.mp4'
    
cap = cv2.VideoCapture(inputvideo)
ret, frame1 = cap.read()
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps    = cap.get(cv2.CAP_PROP_FPS)
plt.imshow(cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB))

#duo lingo (col, row) (580,320) to (1334,736)
topr1 = 320
topr2 = 736
topc1 = 580 
topc2 = 1334
toph = topr2 - topr1
topw = topc2 - topc1

#vis = np.zeros((toph+both,max(topw,botw),3),np.dtype('uint8'))
origw = 1920
origh = 1080

outw = 1280
outh = 720

vis = np.zeros((outh,outw,3),np.dtype('uint8'))

sw=(outw-topw)/2
rowspad=outh/8
vis[rowspad:toph+rowspad, sw:sw+topw, :] = frame1[topr1:topr2,topc1:topc2,:]
plt.imshow(cv2.cvtColor(vis, cv2.COLOR_BGR2RGB))

video = cv2.VideoWriter(tempvid,cv2.VideoWriter_fourcc('X','V','I','D'),fps,(outw,outh))
video.write(vis)

i=1
while(i<length):
    print(i)
    ret, frame1 = cap.read()
    vis[rowspad:toph+rowspad, sw:sw+topw, :] = frame1[topr1:topr2,topc1:topc2,:]
    video.write(vis)
    i = i + 1
    
video.release()

#### rip audio from original
import subprocess
command = "C:/Video/ffmpeg -i " + inputvideo + " -ab 160k -ac 2 -ar 44100 -vn " + tempwav
subprocess.call(command, shell=True)

#### combine audio and video
import subprocess
command = "C:/Video/ffmpeg -i " + tempwav + " -i " + tempvid + " -vcodec copy " + outvideo
subprocess.call(command, shell=True)
