#-*- coding:utf-8 –*- #
import cv2
import numpy as np

class Color_Extractor:
    def __init__(self):
        dict = {}
        dict_HLS = {}

        # 黑色
        lower_black = np.array([0, 0, 0])
        upper_black = np.array([255, 30, 255])
        dict_HLS['black'] = [lower_black, upper_black]

        # # 灰色
        # lower_gray = np.array([0, 50, 0])
        # upper_gray = np.array([255, 205, 10])
        # dict_HLS['gray']=[lower_gray, upper_gray]

        # 白色
        lower_white = np.array([0, 230, 0])
        upper_white = np.array([255, 255, 255])
        dict_HLS['white'] = [lower_white, upper_white]

        # # 红色
        # lower_red = np.array([156, 43, 46])
        # upper_red = np.array([180, 255, 255])
        # dict['red2'] = [lower_red, upper_red]

        # 红色
        lower_red = np.array([0, 80, 66])
        upper_red = np.array([10, 255, 255])
        dict['red'] = [lower_red, upper_red]

        # 橙色
        # lower_orange = np.array([11, 43, 46])
        lower_orange = np.array([11, 80, 66])
        upper_orange = np.array([25, 255, 255])
        dict['orange'] = [lower_orange, upper_orange]

        # 黄色
        # lower_yellow = np.array([26, 43, 46])
        lower_yellow = np.array([26, 80, 66])
        upper_yellow = np.array([34, 255, 255])
        dict['yellow'] = [lower_yellow, upper_yellow]

        # 绿色
        # lower_green = np.array([35, 43, 46])
        lower_green = np.array([35, 80, 66])
        upper_green = np.array([77, 255, 255])
        dict['green'] = [lower_green, upper_green]

        # 青色
        # lower_cyan = np.array([78, 43, 46])
        lower_cyan = np.array([78, 80, 66])
        upper_cyan = np.array([99, 255, 255])
        dict['cyan'] = [lower_cyan, upper_cyan]

        # 蓝色
        lower_blue = np.array([100, 80, 66])
        upper_blue = np.array([124, 255, 255])
        dict['blue'] = [lower_blue, upper_blue]

        # 紫色
        # lower_purple = np.array([125, 43, 46])
        lower_purple = np.array([125, 80, 66])
        upper_purple = np.array([155, 255, 255])
        dict['purple'] = [lower_purple, upper_purple]

        self.HSV_dict = dict
        self.HLS_dict = dict_HLS


    def Extract(self, img):

        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        imgHLS = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
        # H,S,V = cv2.split(imgHSV)
        # V = cv2.equalizeHist(V)
        # imgHSV = cv2.merge([H, S, V])
        maxCount = 0
        Maxkey = None
        # mask = cv2.inRange(imgHLS, self.HLS_dict['white'][0], self.HLS_dict['white'][1])
        # cv2.imshow("", mask)
        # cv2.waitKey(0)
        # mask = cv2.inRange(imgHSV, self.HSV_dict['blue'][0], self.HSV_dict['blue'][1])
        # cv2.imshow("", mask)
        # cv2.waitKey(0)

        for key in self.HSV_dict:
            mask = cv2.inRange(imgHSV, self.HSV_dict[key][0], self.HSV_dict[key][1])
            count = mask.sum()/255
            if count > maxCount:
                maxCount = count
                Maxkey = key
        for key in self.HLS_dict:
            mask = cv2.inRange(imgHLS, self.HLS_dict[key][0], self.HLS_dict[key][1])
            count = mask.sum()/255
            if count > maxCount:
                maxCount = count
                Maxkey = key

        return Maxkey


if __name__ == '__main__':
    img = cv2.imread("./red.png")
    extractor = Color_Extractor()
    if img.any():

        print (extractor.Extract(img))
        # cv2.imshow("", img)
        # cv2.waitKey(0)


