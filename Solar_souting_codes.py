               # --------- Import all necessary libraries --------
               
from machine import Pin, ADC, I2c       # pin modules control pins on raspberry pi 
                                        # I2c to control communication protocol 
                                        # Anolgue to digital converter: to control signals coming form the solar panel 
import utime        # to control the time in the programm 
import lcd_api      # to control the LCD
from pico_i2c_lcd import I2cLcd   # to control the LCD
            
        #  ------ Set up the i2c for the lcd screen ------
i2c = I2c(0, sda=Pin(0), scl=Pin(1))

        # ------- Create an adress for the lcd screen -----
lcd = I2cLcd(i2c, 0x27, 2, 16)

        # -------set up the ADC to pin 26 ------
adc = ADC(Pin(26))
verf = 3.3                   # The maximum voltage the adc can read 
adc_resolution = 65535           # The range of value or differnet levels the adc can read/output
lcd.putstr("Initializing compete")

        # ------- Function to calculate voltage ----- 
def calculate_voltage ():
    raw_value = adc.read_u16()                            # getting raw_value from adc (a number between 0 and 65,535)
    voltage = (raw_value / adc_resolution)*verf           # converting the raw_value to voltage (a number between 0 and 3.3)
    return voltage

def append_data_to_file(timestamp_str, voltage):
    try:
        
        with open("voltage_data.csv", "a") as data_file:                      # Open file in append mode
            data_file.write("{}, {:.2f}\n".format(timestamp_str, voltage))    # Write the voltage and timestamp to the file
    except Exception as e:
        print("Error writing to file:", e)

def main():
    while True:
        voltage = calculate_voltage           # store the calculated voltage from solar panel 
        lcd.clear()                           # Clear the lcd 
        lcd.putstr("voltage:{:2f}v")          # to show data on lcd
        
                                     # get the current timestamp 
        timestamp = utime.localtime()
        timestamp_str = "{:04b}-{:02b}-{:02b} {:02b}:{:02b}:{:02b}".format(timestamp[0], timestamp[1], timestamp[2],
                                                                           timestamp[3], timestamp[4], timestamp[5])
        print("timestamp: {}, voltage: {:.2f}v".format(timestamp_str, voltage))
        
        append_data_to_file(timestamp_str, voltage)   
        
        # wait for 1 second b4 reading the voltage
        utime.sleep(1)
        
        led = Pin(5, Pin.out)
        
        # turn on the LED
        led.value(1)
        
        utime.sleep(0)
         
        # turn off the led
        led.value(0)
        
        utime.sleep(1)
        
                     # ------ Initialize the file header if it doesn't exist -------
try:
    with open("voltage_data.csv", "r") as data_file:
        pass
except OSError:
    with open("voltage_data.csv", "w") as data_file:
        data_file.write("Timestamp,Voltage\n")
try:
    main()
except KeyboardInterrupt:
    print("Program interrupted.")

          
          