import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import time
import sys
import RPi.GPIO as GPIO
GPIO.setwarnings(False)

EMULATE_HX711=False
referenceUnit = 1

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

def cleanAndExit():
    print("Cleaning...")

    if not EMULATE_HX711:
        GPIO.cleanup()
        
    print("Bye!")
    sys.exit()

hx = HX711(5, 6)
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(referenceUnit)
hx.reset()
hx.tare()    
# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)
# Create the ADC object using the I2C bus
ads = ADS.ADS1015(i2c)
# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0)
# Create differential input between channel 0 and 1
#chan = AnalogIn(ads, ADS.P0, ADS.P1)
#print("{:>5}\t{:>5}".format('raw', 'v'))
while True:
    height = ((chan.value-(chan.value*0.9))/18)+8
    val = hx.get_weight(5)
    weight=((val*0.466)/10000)
    hx.power_down()
    hx.power_up()
    time.sleep(0.1)
    print("{:>5}/t{}".format(height, weight))
    time.sleep(0.5)
                                   

#print("Tare done! Add weight now...")

# to use both channels, you'll need to tare them both
#hx.tare_A()
#hx.tare_B()

#while True:
    try:
        # Prints the weight. Comment if you're debbuging the MSB and LSB issue.
       

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()


