import RPi.GPIO as GPIO
from time import sleep
from wsgiref.simple_server import make_server
import falcon
import json
import requests

#ML = Motor Left
#MR = Motor Right

R_PWM = 21
L_PWM = 12
R_EN = 20
L_EN = 16

ML_R_PWM = 24
ML_L_PWM = 23
ML_R_EN = 22
ML_L_EN = 27

BALLAST_IN = 17
BALLAST_OUT = 18

Pins = [[R_PWM, L_PWM, R_EN, L_EN],[ML_R_PWM, ML_L_PWM, R_EN, L_EN]]

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(R_PWM, GPIO.OUT)
GPIO.setup(L_PWM, GPIO.OUT)
GPIO.setup(R_EN, GPIO.OUT)
GPIO.setup(L_EN, GPIO.OUT)
GPIO.setup(ML_R_PWM, GPIO.OUT)
GPIO.setup(ML_L_PWM, GPIO.OUT)
GPIO.setup(ML_R_EN, GPIO.OUT)
GPIO.setup(ML_L_EN, GPIO.OUT)
GPIO.setup(BALLAST_IN, GPIO.OUT)
GPIO.setup(BALLAST_OUT, GPIO.OUT)
GPIO.output(R_EN, True)
GPIO.output(L_EN, True)
GPIO.output(ML_R_EN, True)
GPIO.output(ML_L_EN, True)

M1_Vitesse = GPIO.PWM(R_PWM, 100)
M2_Vitesse = GPIO.PWM(ML_R_PWM, 100)

def forward():
    GPIO.output(L_PWM, False)  # start turning right
    GPIO.output(R_PWM, True)  # stop turning left
    GPIO.output(ML_L_PWM, False)  # start turning right
    GPIO.output(ML_R_PWM, True)  # stop turning left
    print("les 2 moteurs tourne")
    
def stop():
    GPIO.output(L_PWM, False)
    GPIO.output(R_PWM, False)
    GPIO.output(ML_L_PWM, False)
    GPIO.output(ML_R_PWM, False)
    print ("stopper")

# Sens Moteur
def mr_right():
    GPIO.output(L_PWM, False)  # start turning right
    GPIO.output(R_PWM, True)  # stop turning left
    print("Moteur tourne dans le sens 1.")
        
def mr_left():
    GPIO.output(L_PWM, True)  # stop turning left
    GPIO.output(R_PWM, False)  # start turning right
    print("Moteur tourne dans le sens 2.")
    
def ml_right():
    GPIO.output(ML_L_PWM, False)  # start turning right
    GPIO.output(ML_R_PWM, True)  # stop turning left
    print("Moteur tourne dans le sens 1.")
        
def ml_left():
    GPIO.output(ML_L_PWM, True)  # stop turning left
    GPIO.output(ML_R_PWM, False)  # start turning right
    print("Moteur tourne dans le sens 2.")  
  
# Remplissage Poche 
def ballast_in():
    GPIO.output(BALLAST_IN, True)  # stop turning left
    GPIO.output(BALLAST_OUT, False)
    print("Remplissage de la poche dans le sens 1.")

def ballast_out():
    GPIO.output(BALLAST_IN, False)  # stop turning left
    GPIO.output(BALLAST_OUT, True)
    print("Remplissage de la poche dans le sens 2.")
        
def ballast_off():
    GPIO.output(BALLAST_IN, True)  # stop turning left
    GPIO.output(BALLAST_OUT, True)
    print("Arrêt du remplissage de la poche.")
        
     
# Arret des moteurs     
#def cleanup():
#    GPIO.cleanup()
#    print("Arrêt des moteurs.")
    
#def Stop():
 #   M1_Vitesse = GPIO.PWM(R_PWM, 0)
  #  print("les 2 moteurs arrete")
    #GPIO.cleanup()
    #M1_Vitesse = GPIO.PWM(R_PWM, 0)
   # print("Moteur arret.")    
        

# Appel de la fonction moteur dans le sens 1
def set_motor_forward():
    forward()
    return json.dumps({"result": "success forward"})

def set_mr_motor_right():
    mr_right()
    return json.dumps({"result": "success motor right right"})

def set_mr_motor_left():
    mr_left()
    return json.dumps({"result": "success motor right left"})

def set_ml_motor_right():
    ml_right()
    return json.dumps({"result": "success motor left right"})

def set_ml_motor_left():
    ml_left()
    return json.dumps({"result": "success motor left left"})

def set_motor_stop():
    stop()
    return json.dumps({"result": "success stop"})

# Activation de la poche dans un sens 
def set_ballast_in():
    ballast_in()
    return json.dumps({"result": "ballast_in"})

# Activation de la poche dans un autre sens 
def set_ballast_out():
    ballast_out()
    return json.dumps({"result": "ballast_out"})

# Arret du relais
def set_ballast_off():
    ballast_off()
    return json.dumps({"result": "ballast_off"})

# Activation du moteur avec speed comme variable de vitesse
class MotorResourceF:
    def on_post(self, req, resp):
        M1_Vitesse.start(req.media["speed"])
        M2_Vitesse.start(req.media["speed"])
        resp.text = set_motor_forward()
        print(req.media["speed"])
        
class MotorResourceS:
    def on_post(self, req, resp):
        M1_Vitesse.start(req.media["stop"])
        M2_Vitesse.start(req.media["stop"])
        resp.text = set_motor_stop()
        print(req.media["stop"])

class MrMotorResourceR:
    def on_post(self, req, resp):
        M1_Vitesse.start(req.media["speed"])
        resp.text = set_mr_motor_right()
        print(req.media["speed"])
        
class MrMotorResourceL:
    def on_post(self, req, resp):
        M1_Vitesse.start(req.media["speed"])
        resp.text = set_mr_motor_left()
        print(req.media["speed"])
        
class MlMotorResourceR:
    def on_post(self, req, resp):
        M2_Vitesse.start(req.media["speed"])
        resp.text = set_ml_motor_right()
        print(req.media["speed"])
        
class MlMotorResourceL:
    def on_post(self, req, resp):
        M2_Vitesse.start(req.media["speed"])
        resp.text = set_ml_motor_left()
        print(req.media["speed"])
        
        
class BallastInResource:
    def on_post(self, req, resp):
        resp.text = set_ballast_in()
        
class BallastOutResource:
    def on_post(self, req, resp):
        resp.text = set_ballast_out() 

# Arret des moteurs
#class StopFunc:
    #def on_post(self, req, resp):
        #arret()

# Arret de la poche
class StopBallastFunc:
    def on_post(self, req, resp):
        set_ballast_off()        


app = falcon.App()
motorOnF = MotorResourceF()
motorMrOnR = MrMotorResourceR()
motorMrOnL = MrMotorResourceL()
motorMlOnR = MlMotorResourceR()
motorMlOnL = MlMotorResourceL()
motorOnS = MotorResourceS()
ballastIn = BallastInResource()
ballastOut = BallastOutResource()
ballastStop = StopBallastFunc()

app.add_route("/motor_f", motorOnF)
app.add_route("/motor_mr_r", motorMrOnR)
app.add_route("/motor_mr_l", motorMrOnL)
app.add_route("/motor_ml_r", motorMlOnR)
app.add_route("/motor_ml_l", motorMlOnL)
app.add_route("/motor_s", motorOnS)
app.add_route("/ballast_in", ballastIn)
app.add_route("/ballast_out", ballastOut)
app.add_route("/ballast_stop", ballastStop)


if __name__ == "__main__":

    with make_server("", 80, app) as httpd:
        print("API ONLINE")
        httpd.serve_forever()


