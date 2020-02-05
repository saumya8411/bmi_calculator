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
print("Tare Done! Add Weight Now...")
#print("{:>5}       {:>5}".format('Height(CM)', 'Weight(KG)'))
while True:
    height = ((chan.value-(chan.value*0.9))/18)+8
    val = hx.get_weight(5)
    weight=(-(val*0.466)/10000)
    BMI = (10000*weight)/(height*height)
    height = format(height, '.2f')
    weight = format(weight, '.2f')
    BMI = format(BMI, '.2f')
    hx.power_down()
    hx.power_up()
    time.sleep(0.1)
   # print("{height}{weight}{bmi}".format("height is:"\n,"weight:"\n,"bmi"))
    print('Your Weight is:',weight,'Kg`s')
    print('Your Height is :', height,'CM`s')
    print('Your BMI is :',BMI,'kg/m^2')
    #print("{:>5}       {:}".format(height, weight))
    time.sleep(4)
    file_h=open("bmi_height.txt","w")
    file_h.write(height)
    file_w=open("bmi_weight.txt","w")
    file_w.write(weight)
    file_b=open("bmi_bmi.txt","w")
    file_b.write(BMI)
   # sys.exit()

                                   





