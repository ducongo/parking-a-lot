import numpy as np
import cv2

class ParkingDetector:

    def __init__(self, parking_layout):
        self.parking_layout = parking_layout


    def detect_vaccant_lots(self, parking_img, use_corner = False):
        
        if use_corner:
            return self._corner_detector(parking_img)
        else:
            return self._average_detector(parking_img)



    def _corner_detector(self, parking_img):
        vaccant_lots = {}
        masked = self.select_rgb_white_yellow(parking_img)
        src_gray = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
        # parking_img = np.array(parking_img)
        imgesss2 = []

        # Detector parameters
        blockSize = 2
        apertureSize = 3
        k = 0.04
        thresh = 83

        # blockSize = 2
        # apertureSize = 3
        # k = 0.06
        # thresh = 83

        #using Harris corner detector
        dst = cv2.cornerHarris(src_gray, blockSize, apertureSize, k)

        # Normalizing
        dst_norm = np.empty(dst.shape, dtype=np.float32)
        cv2.normalize(dst, dst_norm, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
        dst_norm_scaled = cv2.convertScaleAbs(dst_norm)
        
        for key,lots in self.parking_layout.items():
            for index, (parking_id,parking_rect) in enumerate(lots.items()):
                numberOfCornor = 0
                for x in range(parking_rect[0]+4, parking_rect[2]-4):
                    for y in range(parking_rect[1]+4, parking_rect[3]-4):
                        if int(dst_norm[y,x]) > thresh:
                            numberOfCornor += 1
                        
                if numberOfCornor <= 0:
                    # cv2.rectangle(parking_img, (parking_rect[0],parking_rect[1]),(parking_rect[2],parking_rect[3]),(0,255,0),2)
                    
                    crop_img = src_gray[parking_rect[1]:parking_rect[3] + 1, parking_rect[0]:parking_rect[2] + 1]
                    if np.sum(crop_img) > 166000:
                        vaccant_lots[parking_id] = [parking_rect]
                        print(np.sum(crop_img))
                # print(f"number of corners: {numberOfCornor}")
        print("-------------------------------------------------------")
        return vaccant_lots  


    def _average_detector(self, parking_img):
        vaccant_lots = {}
        masked = self.select_rgb_white_yellow(parking_img)
        src_gray = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
        # iterate over the green parking lots defined in the previous sections
        # parking_img = self.select_rgb_white_yellow(parking_img)
        for key,lots in self.parking_layout.items():
            for index, (parking_id,parking_rect) in enumerate(lots.items()):
                grayCounter = 0
                padding = 8
                # for each lot, define a gray counter to count the gray(ish) pixels in the lot
                # and a padding to focus on the center of the lot
                for x in range(parking_rect[0]+padding, parking_rect[2]-padding):
                    for y in range(parking_rect[1]+padding, parking_rect[3]-padding):
                        # get rgb from images
                        r,g,b = parking_img[y][x][0],parking_img[y][x][1],parking_img[y][x][2]
                        # calculate diff from colors (to find gray)
                        r = int(r)
                        g = int(g)
                        b = int(b)
                        diffRG = abs(r-g)
                        diffGB = abs(g-b)
                        diffBR = abs(b-r)
                        diffSum = diffRG + diffGB + diffBR
                        # if the difference between all r,g,b is less than a threshold (30) 
                        # and 255 >r > 0 (to prevent white and black from being detected)
                        if (diffSum < 30 and r > 30 and r < 225):
                            # to see which spots are detected as "grayish" uncomment the line below
                            # parking_img[y][x] = [0,0,255]
                            grayCounter += 1
                    # take the parking lot size in pixels minus the padding
                    pSize = (parking_rect[2]-parking_rect[0]- 2*padding)*(parking_rect[3]-parking_rect[1]- 2*padding)
                    # find percent gray pixels inside the lot by dividing gray counter with lot size
                    percentGray = grayCounter/pSize
                    # if the percent of gray in the lot is greater than a threshold, then we have an empty lot
                    if not (0.93 > percentGray > 0.90) and percentGray > 0.90:
                        crop_img = src_gray[parking_rect[1]:parking_rect[3] + 1, parking_rect[0]:parking_rect[2] + 1]
                        if np.sum(crop_img) > 466000:
                            vaccant_lots[parking_id] = [parking_rect]
                            # print(np.sum(crop_img))
                        # cv2.rectangle(parking_img, (parking_rect[0],parking_rect[1]),(parking_rect[2],parking_rect[3]),(0,255,0),2)
                        vaccant_lots[parking_id] = [parking_rect]     
        return vaccant_lots


    def select_rgb_white_yellow(self, parking_img): 
        # white color mask
        lower = np.uint8([120, 120, 120])
        upper = np.uint8([255, 255, 255])
        white_mask = cv2.inRange(parking_img, lower, upper)
        # yellow color mask
        lower = np.uint8([190, 190,   0])
        upper = np.uint8([255, 255, 255])
        yellow_mask = cv2.inRange(parking_img, lower, upper)
        # combine the mask
        mask = cv2.bitwise_or(white_mask, yellow_mask)
        masked = cv2.bitwise_and(parking_img, parking_img, mask = mask)
        return masked