# Requirements
```
apt-get install python-serial
```

# Usage
My FTDI-USB TTL is exposed at `/dev/ttyUSB1`, so this will be:
`python intergas_prestige_cw6.py /dev/ttyUSB1`

Output data is (hard-coded) stored at `/home/pi/INTERGAS_DATA_%Y_%m.csv`.

# IntergasBoilerReader
Reading of Intergas Prestige CW6 using the PC-interface.

Thanks to the [folks of CircuitsOnline.net](https://www.circuitsonline.net/forum/view/80667/3) for
doing all hard work decoding most of the protocol and connector layout.

I am the owner of of Intergas Prestige CW6 boiler and like to be able to read
the data from the header for the SmartHouse Monitoring project.

The Intergas Prestige CW6 has an pc-interface found at X5. This is an ATX P4
connector which you can commonly source from old ATX power supplies.

I use a RaspberryPi with python coding to be a bit more versatile when it comes
to storage, coding and forwarding. 

Serial connection details: `9600 8-N-1` TTL found at X5:
![](https://github.com/rickvanderzwet/IntergasBoilerReader/blob/master/intergas-cw6-connector-layout.png "Connector layout")

I use a [FTDI TTL @ Ebay.com](http://www.ebay.com/sch/i.html?_from=R40&_sacat=0&LH_BIN=1&_nkw=FTDI+usb+TTL&rt=nc&LH_FS=1)
 set at logic level TTL of 5V using the jumper, connectors setup:

```
WARNING: For safety purposes use galvanic isolation to safety of the systems.
WARNING: 
WARNING: POTENTIAL HIGH-VOLTAGES, DISCONNECT MAINS WHEN WORKING ON SYSTEM.
WARNING: 
WARNING: Proceed at own risk, you may ruin your equipment or kill yourself.
```



FTDI TTL | X5 Interface
---------|-------------
DTR      | N/C
RX       | Rx
TX       | Tx
5V       | N/C
3.3V     | N/C
GND      | Gnd
N/C      | V+ (5V)


# License
```
Copyright 2017 Rick van der Zwet

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```
