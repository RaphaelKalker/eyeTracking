import Adafruit_BBIO.PWM as PWM
import time

#do the start thing
PWM.start("P8_13", 85.1103, 60, 1)

#wait for the thing to actuate
time.sleep(1)

#oscillate between maximum values for the glasses:
# MIN values : 85.1103
# MAX values : 88.667
#for i in range(0,4):
PWM.set_duty_cycle("P8_13", 88.667)
time.sleep(1)
#    PWM.set_duty_cycle("P8_13", 85.1103)
#    time.sleep(1)

#need to stop the thing from doing more stuff
PWM.stop("P8_13")
PWM.cleanup()
