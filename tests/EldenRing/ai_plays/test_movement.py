import time
from src.EldenRing.ai_plays.util import movement, camera, take_action

# Mouse sensitivity set to 10

time.sleep(10)
camera(0,1,0)

time.sleep(1)
camera(0,1,1)

time.sleep(1)
camera(0,1,2)

time.sleep(1)
camera(1,0,0)

time.sleep(1)
camera(1,2,1)

time.sleep(1)
camera(1,0,2)

time.sleep(1)
movement(0,1)
camera(2,2,2)
take_action(0)

time.sleep(1)
movement(1,2)
camera(0,1,1)
take_action(1)

time.sleep(1)
movement(1,1)
camera(1,0,0)
take_action(2)

time.sleep(1)
take_action(3)

time.sleep(1)
take_action(4)

time.sleep(1)
take_action(5)

#time.sleep(1)
#take_action(6)
