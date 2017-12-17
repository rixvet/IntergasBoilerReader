#!/usr/bin/env python
import argparse
import csv
import ctypes
import glob
import serial
import sys
import time

from struct import *


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

def parse_packet(s):
  d = map(ord,unpack('=cccccccccccccccccccccccccccccccc', s))
  
  msb = float(d[1])
  lsb = float(d[0])
  
  def getFloat(msb, lsb):
    if msb > 127:
      f = -(float(msb ^ 255) + 1) * 256 - lsb / 100
    else:
      f = float(msb * 265 + lsb) / 100
    return f
  
  t1 = getFloat(d[1],d[0]) # Rookgassensor (?)
  t2 = getFloat(d[3],d[2]) # Aanvoersensor S1
  t3 = getFloat(d[5],d[4]) # Retoursensor S2
  t4 = getFloat(d[7],d[6]) # Warmwatersensor S3
  t5 = getFloat(d[9],d[8]) # Boilersensor S4
  t6 = getFloat(d[11],d[10]) # buitenvoeler (?)
  ch_pressure = getFloat(d[13],d[12])
  temp_set = getFloat(d[15],d[14])
  fanspeed_set = getFloat(d[17],d[16])
  fanspeed = getFloat(d[19],d[18])
  fan_pwm = getFloat(d[21],d[20])
  io_curr = getFloat(d[23],d[22])
  
  
  
  flags = B27Flags()
  flags.asbyte = d[27]
  gp_switch = flags.b.gp_switch
  tap_switch = flags.b.tap_switch
  roomtherm = flags.b.roomtherm
  pump = flags.b.pump
  dwk = flags.b.dwk
  alarm_status = flags.b.alarm_status
  ch_cascade_relay = flags.b.ch_cascade_relay
  opentherm = flags.b.opentherm
  
  B29flags = B29Flags()
  B29flags.asbyte = d[29]
  gasvalve = B29flags.b.gasvalve
  spark =  B29flags.b.spark
  io_signal = B29flags.b.io_signal
  ch_ot_disabled = B29flags.b.ch_ot_disabled
  low_water_pressure = B29flags.b.low_water_pressure
  pressure_sensor = B29flags.b.pressure_sensor
  burner_block = B29flags.b.burner_block
  grad_flag = B29flags.b.grad_flag
  
  ch_pressure = None
  if not B29flags.b.pressure_sensor:
      ch_pressure = -35
  displ_code = d[24]
  
  # '-' => uit
  # ' ' => CV in rust
  # '1' => Gewenste temperatuur bereikt
  # '2' => Zelftest
  # '3' => Ventileren (voor en na-ventileren)
  # '4' => Ontsteken
  # '5' => CV Bedrijf
  # '6' => Tapwaterbedrijf
  # '7' => Opwarming boiler (tussenstap dmv omschakelventiel)

  
  ch_pressure = ch_pressure
  
  c2s = {
      51: "Warm water",
      102: "CV Brandt",
      126: "CV in rust",
      204: "Tapwater nadraaien",
      231: "CV nadraaien",
  }
  
  status = c2s.get(displ_code, "Onbekend (%s)" % displ_code)
  status = status

  return [t1, t2, t3, t4, t5, t6, ch_pressure, temp_set, fanspeed_set, fanspeed, fan_pwm, \
        io_curr, gp_switch, tap_switch, roomtherm, pump, dwk, alarm_status, ch_cascade_relay, opentherm, \
        gasvalve, spark, io_signal, ch_ot_disabled, low_water_pressure, pressure_sensor, burner_block, grad_flag, \
        ch_pressure] 
        

  
def parse_file(csvfile):
  print 'time t1 t2 t3 t4 t5 t6 ch_pressure temp_set fanspeed_set fanspeed fan_pwm ' + \
        'io_curr gp_switch tap_switch roomtherm pump dwk alarm_status ch_cascade_relay opentherm ' + \
        'gasvalve spark io_signal ch_ot_disabled low_water_pressure pressure_sensor burner_block grad_flag ' + \
        'ch_pressure'
  with open(csvfile, "r") as fh:
    reader = csv.reader(fh, delimiter=";", lineterminator='\n')
    for row in reader:
      print " ".join(map(str, [row[0]] + parse_packet(row[1].decode("base64"))))
  


def store_packet(packet):
  """ 
  Storing the file 'readable' one-line ascii format, no compression this
  could be done an at later stage to reduce filesize. Normal month will 
  be (every 1 seconds packet of roughly 50 bytes) ~ 150MB uncompressed.
  Compression ratio will be around 10:1.
  """

  line = packet.encode('base64').replace('\n', '')
  csvfile = time.strftime("/home/pi/INTERGAS_DATA_%Y_%m.csv")
  with open(csvfile, "a") as output:
    data = [int(time.time()), line]
    writer = csv.writer(output, delimiter=";", lineterminator='\n')
    writer.writerow(data)


def get_packet(port):
  with serial.Serial(port, 9600, timeout=2) as ser:
    while True:
      ts = time.time()
      ser.write('S?\r')
      s = ser.read(32)
      # Only store valid responses
      if len(s) == 32:
      	store_packet(s)
      time.sleep(1)


if __name__ == '__main__':
  parser = argparse.ArgumentParser(prog=sys.argv[0]) 
  parser.add_argument('action', choices=('get', 'parse'))
  parser.add_argument('file')
  args = parser.parse_args()

  if args.action == 'get':
    get_packet(args.file)
  elif args.action == 'parse':
    parse_file(args.file)
