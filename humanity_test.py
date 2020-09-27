#!/usr/bin/env python3

from humanity import Humanity
import csv2dict as c2d
from time import time,\
localtime,\
strftime

k = c2d.csv2dict('.keys.txt')

user_id = k.get('user_id')
passwd = k.get('passwd')
client_id = k.get('client_id')
client_secret = k.get('client_secret')


h = Humanity(user_id,passwd,client_id,client_secret)

#h.searchPIs('willi')

#h.clockinPI(3221580)

#h.clockoutPI(2071455)
#my id is 2071455
my_buzzcard = ''
my_id = 2071455
#h.updateEmployeeBuzzcardId(my_id,str(my_buzzcard))

t = time()
h.getOnNow() # Took about 1.1s
print('Ran in ' +  str(time() - t))

#################

testLocation = h.createLocation('testLocation')

testPosition = h.createPosition('testPosition',testLocation['id'])

testShiftLen = 60*60 # 1 hour

testShiftStart = localtime() # now
testShiftEnd = localtime(time() + testShiftLen)

start_time = strftime('%I:%M%p',testShiftStart).lower()
end_time = strftime('%I:%M%p',testShiftEnd).lower()
start_date = strftime('%Y-%m-%d',testShiftStart)
end_date = strftime('%Y-%m-%d',testShiftEnd)

test_id = h.me()['id']

testShift = h.createShift(start_time,end_time,start_date,end_date,testPosition['id'])
h.addEmployeeToShift(testShift['id'],test_id)

#input('Paused before approve...\n')
h.approveShift(testShift['id'])

#input('Paused before publish...\n')
h.publishShift(testShift['id'])

#input('Paused before clockin...\n')
# t = time()
# h.clockinPI(test_id)
# print('Clockin : '  +  str(time() - t) + 's')

# t = time()
# h.isOnNow(test_id)
# print('IsOnNow : '  +  str(time() - t) + 's')

input('Enter to delete test data structures from Humanity...\n')
t = time()
h.clockoutPI(test_id)
print('Clockout : '  +  str(time() - t) + 's')


h.deleteShift(testShift['id'])
h.deletePosition(testPosition['id'])
h.deleteLocation(testLocation['id'])

####################
h.deletePosition(testPosition['id'])

