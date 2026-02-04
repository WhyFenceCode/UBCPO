#REPLACE THESE WITH THE ACTUAL FUNCTION WHERE THEY OCCUR
centerButtonPressed = False
topButtonPressed = False
bottomButtonPressed = False

TIME_UP = 27.5 #seconds
TIME = TIME_UP
STARTSPEED = 0.001 #m/s
MAX = 0
MIN = 0
DISTANCEHOLDOFFSET = 10 #offset to reduce the level of %dev while holding position. increase to lower responsiveness

def PercentDeviation(current, expected):
    return (expected - current) / expected

def MotorDrive(speed):
    clockwiseMotor = speed
    counterClockwiseMotor = -speed

def GetDistance():
    return 0.5

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
            MotorDrive(25)
        elif bottomButtonPressed:
            MotorDrive(-20)
        else:
            MotorDrive(0)
    MAX = GetDistance()
    while not centerButtonPressed:
        if topButtonPressed:
            MotorDrive(25)
        elif bottomButtonPressed:
            MotorDrive(-20)
        else:
            MotorDrive(0)
    MIN = GetDistance()
    while not centerButtonPressed:
        currentDistance = GetDistance() + DISTANCEHOLDOFFSET
        targetDistance = MIN + DISTANCEHOLDOFFSET
        deviation = PercentDeviation(currentDistance, targetDistance)
        MotorDrive(deviation * 100)
    MotorDrive(0)
 
def AutonomousControl():
    TIME = TIME_UP
    while GetDistance() < MAX:
        currentSpeed = GetSpeed()
        currentDistance = GetDistance()
        targetSpeed = speed_target(currentDistance)
        deviation = PercentDeviation(currentSpeed, targetSpeed)
        MotorDrive(deviation * 100)
    MotorDrive(0)

DriverControl()

MINIMUMDISTANCE = (MAX - MIN) / 2 #under this distance min speed = STARTSPEED, this must stay after driver control to get correct MAX and MIN

AutonomousControl()