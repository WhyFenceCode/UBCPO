#TIME = 27.5 #seconds
#MAX = 1.5 #meters
#MIN = -0.18 #meters
STARTSPEED = 0.001 #m/s


MAX = float(input("Max: "))
while True:
    if (MAX <= 0.5 or MAX >= 2):
        MAX = float(input("Max: "))
    else:    
        break


MIN = float(input("Min: "))
while True:
    if (MIN <= -0.5 or MIN >= 1):
        MIN = float(input("MIN: "))
    else:   
        break


TIME = float(input("Time: "))
while True:
    if (TIME < 0 or TIME > 60):
        TIME = float(input("Time: "))
    elif (TIME > 30):
        TIME % 30
    else:
        break


DISTANCE = float(input("Distance: "))
while True:
    if (DISTANCE < MIN or DISTANCE > MAX):
        DISTANCE = float(input("Distance: "))
    else:    
        break


MINIMUMDISTANCE = (MAX - MIN) / 2 #under this distance min speed = STARTSPEED


def X(T):
    u = T / TIME
    return MIN + (MAX - MIN) * (3 * u**2 - 2 * u**3) - DISTANCE


def V(T):
    u = T / TIME
    return (6 * (MAX - MIN) / TIME) * u * (1 - u)


def speed_target():
    x = TIME / 2
    for _ in range(10):
        vel = V(x)
        if (V(x) == 0):
            vel += 0.1
        newx = x - X(x)/ vel
        if (abs(newx - x) < 1e-5):
            return V(newx)
        x = newx
    functionOut =  V(x)
    if (functionOut < STARTSPEED and DISTANCE < MINIMUMDISTANCE):
        functionOut = STARTSPEED
    return functionOut


if __name__ == "__main__":
    print(f"speed target = {speed_target()} m/s")



