from cvzone.HandTrackingModule import HandDetector
import numpy as np

class CVZoneModel(object):
    def __init__(self, conf = 0.5):
        self.detector = HandDetector(detectionCon=conf)



    def inference(self, img):
        hands_info, img_info = self.detector.findHands(img)
        return hands_info, img_info



class HandsClassfier(object):
    def __init__(self):
        self.decay_factor = 0.5
        self.conf = np.zeros(4)
        self.conf_base = np.ones(4) * 0.2
        self.conf_thres = 0.5

    def simplify(self, hands_info):
        if (len(hands_info) >= 2):
            # 双手
            return 3
        elif (len(hands) == 1):
            if hands[0]["type"] == "Right":
                # 右手
                return 2
            elif hands[0]["type"] == "Left":
                return 1

        return 0


    def classfier(self, hands_info):
        cls = self.simplify(hands_info)
        self.conf[cls] *= self.decay_factor
        self.conf[cls] += self.conf_base[cls]

        index = np.argmax(self.conf)
        if (self.conf[index]) > self.conf_thres:
            return index
        else:
            return 0
