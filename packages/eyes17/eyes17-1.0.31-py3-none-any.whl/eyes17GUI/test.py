from .layouts.advancedLoggerTools import inputs
from . eyes17 import eyes
import time
dev = eyes17.eyes.open()

print('clear')
dev.set_state(OD1=0)
time.sleep(1)
print('measure')
print(dev.set2ftime('OD1','SEN'))
