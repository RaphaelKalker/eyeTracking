import Adafruit_BBIO.PWM as PWM
import time
import logging

logger = logging.getLogger(__name__)

class Actuate():
    dutyMax = 88.667
    dutyMin = 85.1103
    prescriptionMin = -6.0
    prescriptionMax = 3.0

    # values of the state of the system
    duty = 85.1103
    _PIN = "P8_13"

    # the user's prescription
    nearP = 2.0
    farP = -2.0

    def __init__(self, pin=None, nearPrescription=None, farPrescription=None):
        self.duty = self.dutyMin
	logger.info("%s", self.duty)
        if pin is None:
            self._PIN = "P8_13"
        else:
            self._PIN = pin

        if nearPrescription is not None and farPrescription is not None:
            self.nearP = nearPrescription
            self.farP = farPrescription
        return

    def setPrescriptions(self, nearPrescription, farPrescription):
        self.nearP = nearPrescription
        self.farP = farPrescription
        return
        
    def startup(self, dutyCycle=None):
        #do an init sweep to ensure actuation
        PWM.start(self._PIN, self.dutyMin, 60, 1)
        time.sleep(2)
        PWM.set_duty_cycle(self._PIN, self.dutyMax)
        time.sleep(2)
        if dutyCycle is not None:
            self.duty = dutyCycle
	logger.info("%s", self.duty)
        PWM.set_duty_cycle(self._PIN, self.duty)
        return

    def __del__(self):
        #cleanup the PWM thing
        PWM.stop(self._PIN)
        PWM.cleanup()
        return

    def actuatePercent(self, percent):
        if percent > 100:
            logger.info("INVALID ACTUATION SIGNAL")
            return

        p = percent / float(100)
        dutyC = p*(self.dutyMax-self.dutyMin) + self.dutyMin
	if dutyC <= self.dutyMax and dutyC >= self.dutyMin:
            self.duty = dutyC
            PWM.set_duty_cycle(self._PIN, self.duty)
        else:
            logger.info("actuation signal failure : %s", dutyC)
        return

    def prescriptionToPercent(self, prescription):
        p = prescription - self.prescriptionMin
        r = self.prescriptionMax - self.prescriptionMin
        return 100*p / float(r)
    
    def actuatePrescription(self, prescription):
        self.actuatePercent(self.prescriptionToPercent(prescription))
        return

    def actuate(self, dist):
        if dist is "NEAR":
            self.actuatePrescription(self.nearP)
        elif dist is "FAR":
            self.actuatePrescription(self.farP)
        else:
            logger.info("Not valid selection of prescription")
        return
        
