#REPLACE THESE WITH THE ACTUAL FUNCTION WHERE THEY OCCUR
centerButtonPressed = False
topButtonPressed = False
bottomButtonPressed = False

TIME_UP = 27.5 #seconds
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
        MotorDrive(deviation)
    MotorDrive(0)
    
