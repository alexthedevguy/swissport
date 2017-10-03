#!/usr/bin/env python

#--------------------------------------------
# 4D2 Engineering
# Author:
# Email: alexs@4d2.ca
# Project code: swissport
#--------------------------------------------

# Notes
# A simple test program to confirm motor controls are functioning. Place in utilities rather than standard bin directory
#  need to install the pyusb library from source or pipy, debian/raspbian stable repo still on ver 0.4, need 1.0:
#http://goo.gl/N9L4e
# pretty good code example here
#http://www.rkblog.rk.edu.pl/w/p/controlling-usb-missile-launchers-python/

# imports
import usb.core, usb.util
import platform, time, sys

# connection to Missle LAuncher
def prepusb():
    # hardcoding USB vendor and prod numbers
    VENN=0x2123
    VENI=0x1010
    thisdev = usb.core.find(idVendor=VENN, idProduct=VENI)
    if thisdev is None:
        raise  ValueError("Missle launcher not found")
        return None
    else:
        return thisdev

def detachHID(MDEV):
    if platform.system() == "Linux":
        try:
            MDEV.detach_kernel_driver(0)
        except Exception, e:
            print(e)
            print("USB HID driver not loaded")
            return True
    return True

def loadMDEV(VMDEV):
    # kernel driver should be free but place in try catch just to be sure
    try:
        VMDEV.set_configuration()
    except Exception, e:
        print (e)
        return False
    return True

def lrdemo(thisusb):
    for i in range(0, 3):
        # commands:  light is 0x03 and motor is 0x02, instructions are the second value
        # to do, validate the instructions are 1,2,4,8,10 or 20.  Fire an error to the HMI
        # otherwise the command just drops in the bit bucket.
        # Also need to put a min and max test in for the times. the motor seems to stop but we
        # should put a check in and warn the operator. ( Assuming we don't fill in default since
        # that would affect trajectory of the missile)
        print("Initating test sequence")
        thisusb.ctrl_transfer(0x21, 0x09, 0, 0, [0x03, 1, 0x00,0x00,0x00,0x00,0x00,0x00])
        time.sleep(5)
        # and stop
        thisusb.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        print("Initate roation right")
        # Move right for 2.5 seconds
        thisusb.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, 0x08, 0x00,0x00,0x00,0x00,0x00,0x00])
        time.sleep(2500 / 1000.0)
        # and stop
        thisusb.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, 0x20, 0x00,0x00,0x00,0x00,0x00,0x00])
        time.sleep(3)
        # turn off light
        #thisusb.ctrl_transfer(0x21, 0x09, 0, 0, [0x03, 0, 0x00,0x00,0x00,0x00,0x00,0x00])
        #time.sleep(5)
        # turn on light
        #thisusb.ctrl_transfer(0x21, 0x09, 0, 0, [0x03, 1, 0x00,0x00,0x00,0x00,0x00,0x00])
        #time.sleep(5)
        # move left for 2.5 seconds
        print("initate rotation left")
        thisusb.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, 0x04, 0x00,0x00,0x00,0x00,0x00,0x00])
        time.sleep(2500 / 1000.0)
        # and stop
        thisusb.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, 0x20, 0x00,0x00,0x00,0x00,0x00,0x00])
        time.sleep(3)
        # move up for 500 milliseconds
        print("increase elevation")
        thisusb.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        time.sleep(500 / 1000.0)
        # and stop
        thisusb.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        time.sleep(3)
        # Move right for 2.5 seconds
        print("initate rotation right")
        thisusb.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        time.sleep(2500 / 1000.0)
        # and stop
        thisusb.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        time.sleep(3)
        # move down for 500 milliseconds
        print("lower elevation")
        thisusb.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        time.sleep(500 / 1000.0)
        # and stop
        thisusb.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        time.sleep(3)
        print("test fire")
        thisusb.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        print("reset")
        thisusb.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        time.sleep(10 / 1000.0)
        # and stop
        thisusb.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        # turn off light
        thisusb.ctrl_transfer(0x21, 0x09, 0, 0, [0x03, 0, 0x00,0x00,0x00,0x00,0x00,0x00])
        time.sleep(15)
        i +=1
    thisdev.reset()


if __name__ == "__main__":
    testhid=False
    loadUML=False
    thisdev = prepusb()
    if thisdev is not None:
        testhid = detachHID(thisdev)
    if testhid:
        loadUML = loadMDEV(thisdev)
    if loadUML:
        lrdemo(thisdev)
