from logging import info
from typing import List
from deep_sort.utils.parser import get_config
from deep_sort.deep_sort import DeepSort
from Color_extract import Color_Extractor
from numpy import inf, zeros,float32,tile,set_printoptions,sqrt
from operator import indexOf, itemgetter
from time import mktime
from datetime import datetime
import imutils
import torch
import cv2
import csv
import numpy as np
import time




palette = (2 ** 11 - 1, 2 ** 15 - 1, 2 ** 20 - 1)
cfg = get_config()
cfg.merge_from_file("deep_sort/configs/deep_sort.yaml")
deepsort = DeepSort(cfg.DEEPSORT.REID_CKPT,
                    max_dist=cfg.DEEPSORT.MAX_DIST, min_confidence=cfg.DEEPSORT.MIN_CONFIDENCE,
                    nms_max_overlap=cfg.DEEPSORT.NMS_MAX_OVERLAP, max_iou_distance=cfg.DEEPSORT.MAX_IOU_DISTANCE,
                    max_age=cfg.DEEPSORT.MAX_AGE, n_init=cfg.DEEPSORT.N_INIT, nn_budget=cfg.DEEPSORT.NN_BUDGET,
                    use_cuda=True)





def plot_bboxes(image, bboxes, line_thickness=None, CameraID='0'):
    # Plots one bounding box on image img
    tl = line_thickness or round(
        0.002 * (image.shape[0] + image.shape[1]) / 2) + 1  # line/font thickness

    for (x1, y1, x2, y2, cls_id, pos_id) in bboxes:
        if cls_id in ['person']:
            color = (0, 0, 255)
        else:
            color = (0, 255, 0)
        c1, c2 = (x1, y1), (x2, y2)
            
        cv2.rectangle(image, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(cls_id, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(image, c1, c2, color, -1, cv2.LINE_AA)  # filled
        cv2.putText(image, '{} ID{}-{}'.format(cls_id, CameraID,pos_id), (c1[0], c1[1] - 2), 0, tl / 3,
                    [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)



    return image



def update_tracker(target_detector, image, matching=None, CameraID=None, TimeStamp=None):
    new_faces = []

    _, bboxes = target_detector.detect(image)

    bbox_xywh = []
    confs = []
    clss = []

    '''
        放缩系数kx, ky
    '''
    kx = int(2560 / image.shape[1])
    ky = int(1440 / image.shape[0])


    for x1, y1, x2, y2, cls_id, conf in bboxes:

        obj = [
            int((x1+x2)/2), int((y1+y2)/2),
            x2-x1, y2-y1
        ]
        bbox_xywh.append(obj)
        confs.append(conf)
        clss.append(cls_id)

    xywhs = torch.Tensor(bbox_xywh)
    confss = torch.Tensor(confs)

    outputs = deepsort.update(xywhs, confss, clss, image)

    bboxes2draw = []
    face_bboxes = []
    current_ids = []

    info = []

    for value in list(outputs):

        x1, y1, x2, y2, cls_, track_id = value
        bboxes2draw.append(
            (x1, y1, x2, y2, cls_, track_id)
        )

        current_ids.append(track_id)

        '''
            识别结果添加进列表
        '''
        if cls_ == 'car' or cls_ == 'bus' or cls_ == 'truck':
            extractor = Color_Extractor()
            if image.any():
                info.append(
                        [CameraID + str(track_id), kx*x1 - image.shape[1]/2, ky*y1 - image.shape[0]/2, kx*(x2 - x1), ky*(y2 - y1), cls_, None, extractor.Extract(image[y1:y2, x1:x2])]
                )

                
        else:
            info.append(
                [CameraID + str(track_id), kx*x1 - image.shape[1]/2, ky*y1 - image.shape[0]/2, kx*(x2 - x1), ky*(y2 - y1), cls_, None, None]
            )



        if cls_ == 'face':
            if not track_id in target_detector.faceTracker:
                target_detector.faceTracker[track_id] = 0
                face = image[y1:y2, x1:x2]
                new_faces.append((face, track_id))
            face_bboxes.append(
                (x1, y1, x2, y2)
            )

    ids2delete = []
    for history_id in target_detector.faceTracker:
        if not history_id in current_ids:
            target_detector.faceTracker[history_id] -= 1
        if target_detector.faceTracker[history_id] < -5:
            ids2delete.append(history_id)

    for ids in ids2delete:
        target_detector.faceTracker.pop(ids)
        print('-[INFO] Delete track id:', ids)

    image = plot_bboxes(image, bboxes2draw, CameraID=CameraID)
    


    '''
        通过接口传入类
    '''
    
    matching.AppendData(CameraID, TimeStamp, info)


    '''
        写入文件
    '''
    # with open("output/infor.csv", "a", newline='') as csvfile: 
    #     writer = csv.writer(csvfile)

    #     #writer.writerow(["dot1", "dot2", "Width", "Height", "class", "id"])
    #     writer.writerows(info)
        
        #writer.writerows([info[0], info[1], info[2], info[3], info[4]])


    # with open("test1.txt","a") as f:
    #     f.write(str(info))
    #     f.write('\n')
    return image, new_faces, face_bboxes

