
import numpy as np
import cv2
import sys
from adafruit_servokit import ServoKit
import board
import busio
from sshkeyboard import listen_keyboard
import time
import pulseio
#import qwiic_twist

#import qwiic_joystick
import qwiic





#############################################################################
        
# Set channels to the number of servo channels on your kit.
# There are 16 channels on the PCA9685 chip.
kit = ServoKit(channels=16)
kit2 = ServoKit(channels=16,address=0x41)


# Name and set up the servo according to the channel you are using.
servo2 = kit.servo[1]  # Back Right
servo1 = kit.servo[2]  # tile pusher
servo3 = kit.servo[3]  # Front Right
#servo4 = kit2.servo[15] # Nailing Arm

servo4 = kit2.servo[15] # Nailing Arm
servo5 = kit2.servo[2] # Front Left
servo6 = kit2.servo[4] # Back Left
servo7 = kit2.servo[3] # camera mount



# Set the pulse width range of your servo for PWM control of rotating 0-180 degree (min_pulse, max_pulse)
# Each servo might be different, you can normally find this information in the servo datasheet
servo1.set_pulse_width_range(500,2500)
servo2.set_pulse_width_range(500,2500)
servo3.set_pulse_width_range(500,2500)

servo4.set_pulse_width_range(500,2500)
servo5.set_pulse_width_range(500,2500)
servo6.set_pulse_width_range(500,2500)



# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
#oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)


############# open and close #############

def open_and_close():
  
    # Set the servo to 90 degree position
    servo4.angle = 90
    time.sleep(1)
    
    servo4.angle = 0
    #time.sleep(2) 

##################################################
def open_slowly():

    x = 0
    for x in range(6):
        servo1.angle = x*10
        x = x + 1 
        time.sleep(.1)
    
################# distance sensor #########################
    
def distances():

    ToF.start_ranging()
    distance = ToF.get_distance()	 # Get the result of the measurement from the sensor
    ToF.stop_ranging()
    
    distanceFeet = distance / 304.8 
    
    print("distance to edge: ", distanceFeet)
    
    
   
##################  get key presses  ######################   
    
def press(key):
    print(f"'{key}' pressed")   
    
    global two_adjuster
    global three_adjuster
    
    global five_adjuster
    global six_adjuster
    
    if key == ']':
        two_adjuster = two_adjuster + 1
        print("Back Right backward ", two_adjuster)
    if key == '[':
        two_adjuster = two_adjuster - 1
        print("Back Right forward ", two_adjuster)
    if key == 'p':
        three_adjuster = three_adjuster + 1
        print("Front Right backward", three_adjuster)
    if key == 'o':
        three_adjuster = three_adjuster - 1
        print("Front Right forward ", three_adjuster)
    if key == 'i':
        five_adjuster = five_adjuster + 1
        print("Front Left forward ", five_adjuster)
    if key == 'u':
        five_adjuster = five_adjuster - 1
        print("Front Left backward ", five_adjuster)
    if key == 'y':
        six_adjuster = six_adjuster + 1
        print("Back Left forward", six_adjuster)
    if key == 't':
        six_adjuster = six_adjuster - 1
        print("Back Left backward ", six_adjuster)    
        
    #if key == 'right':
        #servo.angle = 50
    #if key == 'left':
        #servo.angle = 0
    if key == 'v':
        camera()
    if key == 'c':
        contours()
    if key == 'e':
        #servo1.angle = 60
        open_slowly()
    if key == 'w':
        servo1.angle = 0
                     
    if key == 'up':
        servo2.angle = 45 + two_adjuster
        servo3.angle = 45 + three_adjuster
        servo5.angle = 135 + five_adjuster
        servo6.angle = 135 + six_adjuster                
    if key == 'down':
        servo2.angle = 135 + two_adjuster
        servo3.angle = 135 + three_adjuster
        servo5.angle = 45 + five_adjuster
        servo6.angle = 45 + six_adjuster        
    if key == 'right':
        servo2.angle = 135 + two_adjuster
        servo3.angle = 135 + three_adjuster
        servo5.angle = 135 + five_adjuster 
        servo6.angle = 135 + six_adjuster        
    if key == 'left':
        servo2.angle = 45 + two_adjuster
        servo3.angle = 45 + three_adjuster
        servo5.angle = 45 + five_adjuster 
        servo6.angle = 45 + six_adjuster
        
    if key == 'n':
        servo4.angle = 90
        #open_and_close()
    if key == 'b':
        servo4.angle = 0
        
    if key == 'h':
        servo7.angle = 45
    if key == 'g':
        servo7.angle = 90
    if key == 'f':
        servo7.angle = 135
 
        
    if key == 'd':
        distances()

def release(key):
    
    global two_adjuster
    global three_adjuster
    
    global five_adjuster
    global six_adjuster
    
    #print(f"'{key}' released")
    servo2.angle = 90 + two_adjuster
    servo3.angle = 90 + three_adjuster
    servo5.angle = 90 + five_adjuster
    servo6.angle = 90 + six_adjuster

################################################################

def listen():
    #servo1.angle = 25    
    listen_keyboard(on_press=press, on_release=release,)
    #listen_keyboard(on_press=press)

def contours():
    #start_time = time.time()
    img=None
    webCam = False
    if(len(sys.argv)>1):
        try:
            print("I'll try to read your image")
            img = cv2.imread(sys.argv[1])
            if img is None:
                print("Failed to load image file:", sys.argv[1])
        except:
            print("Failed to load the image are you sure that:", sys.argv[1],"is a path to an image?")
    else:
        try:
            print("Trying to open the Webcam.")
            cap = cv2.VideoCapture(0)
            if cap is None or not cap.isOpened():
                raise("No camera")
            webCam = True
        except:
            img = cv2.imread("../data/test.jpg")
            print("Using default image.")
    
    while(True):
        if webCam:
            ret, img = cap.read()
            
        imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(imgray,127,255,0)
    
        contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        img_c = cv2.drawContours(img, contours, -1, (0,255,0), 3)
        if webCam:
            cv2.imshow('contours( press q to quit.)',img_c) 
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                break
        else:
            break
    
    cv2.imwrite('contour_out.jpg',img_c)
    cv2.destroyAllWindows()
    
def camera():
    cap = cv2.VideoCapture(0)
    
    while(True):
        ret, frame = cap.read()
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()    
                      

while True:
    
    two_adjuster = 0
    three_adjuster = 0 
    five_adjuster = 0
    six_adjuster = 0
    
    print("VL53L1X Qwiic Test\n")
    ToF = qwiic.QwiicVL53L1X()
    if (ToF.sensor_init() == None):					 # Begin returns 0 on a good init
        print("Sensor online!\n")    

    #contours()
    listen()
