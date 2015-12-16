# Captured video in 1080p
# Output video is 720p, extracting only DS screens
# Example Original: https://www.youtube.com/watch?v=NAoj_0xh81M
# Example Output: https://www.youtube.com/watch?v=GsepODXseMw

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

cv2.__version__
    
inputvideo = "E:\GameplayFootage\Jeremy\YoshisIslandDS1-1to1-2.mp4"

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

topr1 = 160
topr2 = 448
topc1 = 768 
topc2 = 1152
toph = topr2 - topr1
topw = topc2 - topc1

botr1 = 570
botr2 = 858
botc1 = 768
botc2 = 1152
both = botr2 - botr1
botw = botc2 - botc1

#vis = np.zeros((toph+both,max(topw,botw),3),np.dtype('uint8'))
origw = 1920
origh = 1080

outw = 1280
outh = 720

#ratio = origh/outh
sph = botr1 - topr2

vis = np.zeros((outh,outw,3),np.dtype('uint8'))

sw=(outw-max(topw,botw))/2
vis[:toph, sw:sw+max(topw,botw), :] = frame1[topr1:topr2,topc1:topc2,:]
vis[sph+toph:sph+toph+both, sw:sw+max(topw,botw), :] = frame1[botr1:botr2,botc1:botc2,:]
#vis[:toph, :max(topw,botw), :] = frame1[topr1:topr2,topc1:topc2,:]
#vis[toph:toph+both, :max(topw,botw), :] = frame1[botr1:botr2,botc1:botc2,:]
plt.imshow(cv2.cvtColor(vis, cv2.COLOR_BGR2RGB))

video = cv2.VideoWriter(tempvid,cv2.VideoWriter_fourcc('X','V','I','D'),fps,(outw,outh))
video.write(vis)

i=1
while(i<length):
    print(i)
    ret, frame1 = cap.read()
    vis[:toph, sw:sw+max(topw,botw), :] = frame1[topr1:topr2,topc1:topc2,:]
    vis[sph+toph:sph+toph+both, sw:sw+max(topw,botw), :] = frame1[botr1:botr2,botc1:botc2,:]
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
