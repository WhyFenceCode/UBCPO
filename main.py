#REPLACE THESE WITH THE ACTUAL FUNCTION WHERE THEY OCCUR
from time import time


centerButtonPressed = False
topButtonPressed = False
bottomButtonPressed = False

TIME_UP = 27.5 #seconds
TIME = TIME_UP
STARTSPEED = 0.001 #m/s
MAX = 0
MIN = 0
DISTANCEHOLDOFFSET = 10 #offset to reduce the level of %dev while holding position. increase to lower responsiveness

leftmotor = None
rightmotor = None
distancesensor = None

def Setup():
    leftmotor = Motor("A", positive_direction = Direction.CLOCKWISE, gears = None)
    rightmotor = Motor("B", positive_direction = Direction.COUNTERCLOCKWISE, gears = None)
    distancesensor = UltrasonicSensor("1")

def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))


def PercentDeviation(current, expected):
    try:
        currentDeviation =  clamp((expected - current) / expected, -1, 1)
    except:
        currentDeviation = 0
    return currentDeviation

def MotorDrive(speed):
    leftmotor.dc(speed)
    rightmotor.dc(speed)  

def MotorHold():
    leftmotor.hold()
    rightmotor.hold()  

def GetDistance():
    return distancesensor.distance(silent=False)

def GetSpeed():
    return -0.01


def X(T, distance):
    u = T / TIME
    return MIN + (MAX - MIN) * (3 * u**2 - 2 * u**3) - distance


def V(T):
    u = T / TIME
    return (6 * (MAX - MIN) / TIME) * u * (1 - u)


def speed_target(distance):
    x = TIME / 2
    for _ in range(10):
        vel = V(x)
        if (V(x) == 0):
            vel += 0.1
        newx = x - X(x, distance)/ vel
        if (abs(newx - x) < 1e-5):
            return V(newx)
        x = newx
    functionOut =  V(x)
    if (functionOut < STARTSPEED and distance < MINIMUMDISTANCE):
        functionOut = STARTSPEED
    return functionOut

def DriverControl():
    while not centerButtonPressed:
        if topButtonPressed:
            MotorHold(25)
        elif bottomButtonPressed:
            MotorHold(-20)
        else:
            MotorHold(0)
    MAX = GetDistance()
    while centerButtonPressed:
        MAX = MAX
    while not centerButtonPressed:
        if topButtonPressed:
            MotorHold(25)
        elif bottomButtonPressed:
            MotorHold(-20)
        else:
            MotorHold(0)
    MIN = GetDistance()
    while centerButtonPressed:
        MIN = MIN
    while not centerButtonPressed:
        MotorHold()
        
 
def AutonomousControl():
    TIME = TIME_UP
    lastDistance = MIN
    lastTime = time.time_ns()
    while GetDistance() < MAX:
        currentTime = time.time_ns()
        currentDistance = GetDistance()
        currentSpeed = lastDistance - currentDistance / ((currentTime - lastTime) / 1e9)
        lastDistance = currentDistance
        lastTime = currentTime
        targetSpeed = speed_target(currentDistance)
        deviation = PercentDeviation(currentSpeed, targetSpeed)
        MotorDrive(deviation * 100)
    MotorHold()

DriverControl()

MINIMUMDISTANCE = (MAX - MIN) / 2 #under this distance min speed = STARTSPEED, this must stay after driver control to get correct MAX and MIN

AutonomousControl()