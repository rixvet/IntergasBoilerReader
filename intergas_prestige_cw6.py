import sys
import serial
from struct import *

import ctypes

c_uint8 = ctypes.c_uint8
class B27Flags_bits(ctypes.LittleEndianStructure):
    _fields_ = [
            ("gp_switch", c_uint8, 1),
            ("tap_switch", c_uint8, 1),
            ("roomtherm", c_uint8, 1),
            ("pump", c_uint8, 1),
            ("dwk", c_uint8, 1),
            ("alarm_status", c_uint8, 1),
            ("ch_cascade_relay", c_uint8, 1),
            ("opentherm", c_uint8, 1),
        ]

class B27Flags(ctypes.Union):
    _fields_ = [("b", B27Flags_bits),
                ("asbyte", c_uint8)]

class B29Flags_bits(ctypes.LittleEndianStructure):
    _fields_ = [
            ("gasvalve", c_uint8, 1),
            ("spark", c_uint8, 1),
            ("io_signal", c_uint8, 1),
            ("ch_ot_disabled", c_uint8, 1),
            ("low_water_pressure", c_uint8, 1),
            ("pressure_sensor", c_uint8, 1),
            ("burner_block", c_uint8, 1),
            ("grad_flag", c_uint8, 1),
        ]

class B29Flags(ctypes.Union):
    _fields_ = [("b", B29Flags_bits),
                ("asbyte", c_uint8)]

with serial.Serial('/dev/ttyUSB0') as ser:
    ser.write('S?\r')
    s = ser.read(32)


d = map(ord,unpack('=cccccccccccccccccccccccccccccccc', s))

msb = float(d[1])
lsb = float(d[0])

def getFloat(msb, lsb):
  if msb > 127:
    f = -(float(msb ^ 255) + 1) * 256 - lsb / 100
  else:
    f = float(msb * 265 + lsb) / 100
  return f

print "t1=", getFloat(d[1],d[0])
print "t2=", getFloat(d[3],d[2])
print "t3=", getFloat(d[5],d[4])
print "t4=", getFloat(d[7],d[6])
print "t5=", getFloat(d[9],d[8])
print "t6=", getFloat(d[11],d[10])
print "ch_pressure=", getFloat(d[13],d[12])
print "temp_set=", getFloat(d[15],d[14])
print "fanspeed_set=", getFloat(d[17],d[16])
print "fanspeed=", getFloat(d[19],d[18])
print "fan_pwm=", getFloat(d[21],d[20])
print "io_curr=", getFloat(d[23],d[22])



flags = B27Flags()
print 'D27'
flags.asbyte = d[27]
print "gp_switch=", flags.b.gp_switch
print "tap_switch=", flags.b.tap_switch
print "roomtherm=", flags.b.roomtherm
print "pump=", flags.b.pump
print "dwk=", flags.b.dwk
print "alarm_status=", flags.b.alarm_status
print "ch_cascade_relay=", flags.b.ch_cascade_relay
print "opentherm=", flags.b.opentherm


print "D29"
B29flags = B29Flags()
B29flags.asbyte = d[29]
print "gasvalve=", B29flags.b.gasvalve
print "spark=", B29flags.b.spark
print "io_signal=", B29flags.b.io_signal
print "ch_ot_disabled=", B29flags.b.ch_ot_disabled
print "low_water_pressure=", B29flags.b.low_water_pressure
print "pressure_sensor=", B29flags.b.pressure_sensor
print "burner_block=", B29flags.b.burner_block
print "grad_flag=", B29flags.b.grad_flag


displ_code = 0
fault_code = 0

ch_pressure = None
if B29flags.b.pressure_sensor:
    ch_pressure = -35
displ_code = d[24]

print "D27", d[27]
if d[27] == 128:
    print "In loop", d[27]
    fault_code = d[29]
    displ_code = 256 + fault_code


print "ch_pressure=", ch_pressure
print "fault_code=", fault_code
print "displ_code=", displ_code

c2s = {
    51: "Warm water",
    102: "CV Brandt",
    126: "CV in rust",
    204: "Tapwater nadraaien",
    231: "CV nadraaien",
}

status = c2s.get(displ_code, "Onbekend (%s)" % displ_code)
print "status=", status



#      // ontbreken: ventileren, ontsteken, opwarmen boiler
#      // op display
#      // - uit; wachtstand; 0 Nadraaien CV; 1 Gew. temperatuur bereikt; 2 Zelftest
#//   3 Ventileren; 4  Ontsteken; 5 CV; 6 Warm water; 7 Opwarmen boiler

print d
print bin(d[27])
print bin(d[29])



    

