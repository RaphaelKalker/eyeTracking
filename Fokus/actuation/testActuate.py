import Actuate
import time
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

#left, then right pin order
actuator = Actuate.Actuate("P8_13", "P9_14", 3,-1)
#actuator = Actuate.Actuate("P8_19", 3,-1)

actuator.startup()

actuator.actuatePercent(5)
time.sleep(2)

actuator.actuatePercent(95)
time.sleep(2)

actuator.actuatePrescription(-5)
time.sleep(2)

actuator.actuatePrescription(2.75)
time.sleep(2)

actuator.actuate("NEAR")
time.sleep(2)

actuator.actuate("FAR")
time.sleep(2)

actuator.actuate("NEARISH")
time.sleep(2)
