import Adafruit_BBIO.PWM as PWM
import time
import logging

logger = logging.getLogger(__name__)

class Actuate():
    dutyMaxR = None
    dutyMinR = None
    dutyMaxL = None
    dutyMinL = None
    prescriptionMin = -6.0
    prescriptionMax = 3.0

    # values of the state of the system
    dutyR = None
    dutyL = None
    _PINR = "P8_13"
    _PINL = "P9_14"

    # the user's prescription
    nearP = 2.0
    farP = -2.0

    def __init__(self, pinL=None, pinR=None, nearPrescription=None, farPrescription=None):
        self.dutyMaxR = 91.62
        self.dutyMinR = 94.75
        
        self.dutyMaxL = 88.2
        self.dutyMinL = 84.5


        self.dutyR = self.dutyMinR
        self.dutyL = self.dutyMinL

        #logger.info("%s", self.duty)
        if pinR is None:
            self._PINR = "P8_13"
        else:
            self._PINR = pinR

        if pinL is None:
            self._PINL = _PINL
        else:
            self._PINL = pinL

        if nearPrescription is not None and farPrescription is not None:
            self.nearP = nearPrescription
            self.farP = farPrescription
        return

    def setPrescriptions(self, nearPrescription, farPrescription):
        self.nearP = nearPrescription
        self.farP = farPrescription
        return
        
    def startup(self): #, dutyCycle=None)
        #do an init sweep to ensure actuation
        PWM.start(str(self._PINR), self.dutyMinR, 60, 1)

        time.sleep(1)
        PWM.start(self._PINL, self.dutyMinL, 60, 1)
        
        time.sleep(2)
        PWM.set_duty_cycle(self._PINR, self.dutyMaxR)
        PWM.set_duty_cycle(self._PINL, self.dutyMaxL)
        time.sleep(2)
        return

    def __del__(self):
        #cleanup the PWM thing
        PWM.stop(self._PINR)
        PWM.stop(self._PINL)
        PWM.cleanup()
        return

    def actuatePercent(self, percent):
        if percent > 100:
            logger.info("INVALID ACTUATION SIGNAL")
            return

        p = percent / float(100)
        dutyCR = p*(self.dutyMaxR-self.dutyMinR) + self.dutyMinR
        dutyCL = p*(self.dutyMaxL-self.dutyMinL) + self.dutyMinL
        #right motor is flipped, that is why signs are opposite
	if dutyCR >= self.dutyMaxR and dutyCR <= self.dutyMinR:
            self.dutyR = dutyCR
            PWM.set_duty_cycle(self._PINR, self.dutyR)
	if dutyCL <= self.dutyMaxL and dutyCL >= self.dutyMinL:
            self.dutyL = dutyCL
            PWM.set_duty_cycle(self._PINL, self.dutyL)
        else:
            logger.info("actuation signal failure (L,R): %d, %d", dutyCL, dutyCR)
        return

    def prescriptionToPercent(self, prescription):
        p = prescription - self.prescriptionMin
        r = self.prescriptionMax - self.prescriptionMin
        return 100*p / float(r)
    
    def actuatePrescription(self, prescription):
        self.actuatePercent(self.prescriptionToPercent(prescription))
        return

    def actuate(self, dist):
        if dist == "NEAR":
            self.actuatePrescription(self.nearP)
        elif dist == "FAR":
            self.actuatePrescription(self.farP)
        else:
            logger.info("Not valid selection of prescription")
        return
        
