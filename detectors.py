import numpy
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
        #using corner detector to find parking spot
        src_gray = cv2.cvtColor(parking_img, cv2.COLOR_BGR2GRAY)

        # Detector parameters
        blockSize = 2
        apertureSize = 3
        k = 0.04
        thresh = 69

        #using Harris corner detector
        dst = cv2.cornerHarris(src_gray, blockSize, apertureSize, k)

        # Normalizing
        dst_norm = np.empty(dst.shape, dtype=np.float32)
        cv2.normalize(dst, dst_norm, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
        dst_norm_scaled = cv2.convertScaleAbs(dst_norm)

        empty_parking = []

        for parking_rect in self.parking_layout:
            numberOfCornor = 0
            for x in range(parking_rect[0]+5, parking_rect[2]-5):
                for y in range(parking_rect[1]+5, parking_rect[3]-5):
                    if int(dst_norm[y,x]) > thresh:
                        numberOfCornor += 1
            if numberOfCornor <= 3:
                cv2.rectangle(parking_img2, (parking_rect[0],parking_rect[1]),(parking_rect[2],parking_rect[3]),(0,255,0),2)
                empty_parking.append(parking_rect)

        return empty_parking    


    def _average_detector(self, parking_img):
        vaccant_lots = {}
        # iterate over the green parking lots defined in the previous sections
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
                        if(diffSum < 30 and r > 0 and r < 225):
                            # to see which spots are detected as "grayish" uncomment the line below
                            # parking_img[y][x] = [0,0,255]
                            grayCounter += 1
                    # take the parking lot size in pixels minus the padding
                    pSize = (parking_rect[2]-parking_rect[0]- 2*padding)*(parking_rect[3]-parking_rect[1]- 2*padding)
                    # find percent gray pixels inside the lot by dividing gray counter with lot size
                    percentGray = grayCounter/pSize
                    # if the percent of gray in the lot is greater than a threshold, then we have an empty lot
                    if percentGray > 0.93:
                        # cv2.rectangle(parking_img, (parking_rect[0],parking_rect[1]),(parking_rect[2],parking_rect[3]),(0,255,0),2)
                        vaccant_lots[parking_id] = [parking_rect]     
        return vaccant_lots
