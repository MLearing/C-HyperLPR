# -*- coding:utf-8 -*-
"""
   the program only add nms to remove duplicate license plates on the original basis
"""

import sys
import cv2
import hyperlpr as pr
import numpy as np
from PIL import Image, ImageDraw, ImageFont

reload(sys)
sys.setdefaultencoding('utf-8')

def _interval_overlap(interval_a, interval_b):
  x1, x2 = interval_a
  x3, x4 = interval_b
  
  if x3<x1:
    if x4<x1:
      return 0
    else:
      return min(x2, x4) - x1
  else:
    if x2<x3:
      return 0
    else:
      return min(x2, x4) - x3
    
def bbox_iou(box1, box2):
  intersect_w = _interval_overlap([box1[0], box1[2]], [box2[0], box2[2]])
  intersect_h = _interval_overlap([box1[1], box1[3]], [box2[1], box2[3]])
  intersect = intersect_w * intersect_h
  
  w1, h1 = box1[2] - box1[0], box1[3] - box1[1]
  w2, h2 = box2[2] - box2[0], box2[3] - box2[1]
  union = w1 * h1 + w2 * h2 - intersect
  
  return float(intersect) / union

def nms(plate, thresh):
  plate = [idx for idx in sorted(plate, key=lambda x:x[1], reverse=Ture)]
  num = len(plate)
  bbox = [pt[2] for pt in plate]
  
  for i in range(nums):
    for j in range(i+1,nums):
      if bbox_iou(bbox[i], bbox[j]) >= thresh:
        plate.pop(j)
  
  return plate

if __name__="__main__":
  iamge = cv2.imread("timg.jpg")
  plate = pr.HyperLPR_PlateRecogntion(image)
  num = len(plate)
  
  if num>0:
    plate = nms(len(plate), 0.5)
    for i in range(len(plate)):
      p = plate[i][0]
      p.decode('utf-8')
      box = plate[i][2]
      cv2.rectangle(image, (box[0], box[1]), (box[2], box[3]), (0,0,255), 2)
      
      image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
      image = Image.fromarray(image)
      draw = ImageDraw.Draw(image)
      # simsun.ttc字体包可以从wins系统C:\Windows\Fonts复制到该项目下面
      font = ImageFont.truetype("simsun.ttc", 30, encoding='utf-8')
      draw.text((box[0], box[1]-33), p, (255,255,0), font=font)
      image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
      
    cv2.imwrite("res.jpg", image)
   else:
    print("The code cannot detect plates in the picture !")
