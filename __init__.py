import multiprocessing
import subprocess
import threading
from datetime import datetime
from os import system, _exit
from random import randint
from time import sleep

StarOn = datetime.now()
selcted_device = "adb -s "
class_name = ["MainActivity","B","C","D","E","F","G","H"]
devices = []

control = [
    # BACK Control
    " shell input keyevent KEYCODE_BACK",
    # GET FORNTVIEW ACTIVITY
    " shell 'dumpsys activity | grep top-activity'"
]

home = [
    # Samsung Home
    "com.sec.android.app.launcher",
    # MI Home
    "com.miui.home"
]

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def Check_Network(device_name,device):
    result = ''
    error = ''

    # TEST INTERNET CONNECTIVITY
    p = subprocess.Popen(
        device + " shell ping -c 1 google.com"
        , shell=True
        , stdout=subprocess.PIPE
        , stderr=subprocess.PIPE
    )

    while p.stdout is not None:
        # read stdout and block untill complete
        p_line = p.stdout.readline()
        result = result + str(p_line.strip().decode("utf-8"))
        p.stdout.flush()

        error = str(p.stderr.readline().decode("utf-8"))

        # When no lines appears:
        if not p_line:
            break
        if error:
            break

    if not result and error:
        result = error
    if not error and result:
        result = result

    if "unknown host " in result:
        print(device_name + "Exe CMD [ " + bcolors.BOLD + bcolors.FAIL + "INTERNET TEST" + bcolors.ENDC + " ] [ " + bcolors.BOLD + bcolors.FAIL + "NO INTERNET" + bcolors.ENDC + " ] [ " + bcolors.BOLD + bcolors.FAIL + "TASK SUSPENDED" + bcolors.ENDC + " ]")
        return False

    return True

def execute(device_name,cmd,display_log):
    if display_log:
        print(device_name + "Exe CMD [ " + bcolors.BOLD + bcolors.FAIL + cmd + bcolors.ENDC + " ]")

    result = ''
    error = ''

    p = subprocess.Popen(
        cmd
        , shell=True
        , stdout=subprocess.PIPE
        , stderr=subprocess.PIPE
    )

    while p.stdout is not None:
        # read stdout and block untill complete
        p_line = p.stdout.readline()
        result = result + str(p_line.strip().decode("utf-8"))
        p.stdout.flush()

        error = str(p.stderr.readline().decode("utf-8"))

        # When no lines appears:
        if not p_line:
            break
        if error:
            break

    if not result and error:
            return error
    if not error and result:
            return result

def do_back(device_name,device):
    global control,home
    # Execute Controll Statements
    result = execute(device_name ,device + control[0],True)
    result = execute(device_name ,device + control[1],True)
    # Check Status
    for check in home:
        # Check for Home Screen
        if result == None : return True
        if check in result:
            return True
        # Check if Std ERROR WHILE EXECUTING STATEMENTS
        if "more than one device/emulator" in result or "ERROR" in result or "error" in result or "not" in result:
            # Kill FRONTVIEW
            forntactivity = execute(device + " shell 'dumpsys activity | grep top-activity ' | grep -o  '[com.][A-Za-z.]*/'")
            print(bcolors.BOLD + bcolors.FAIL)
            print(device_name + "!!RUNTIME ERROR IN BACK LOOP!!")
            print(device_name + "Activity error on : " + forntactivity)
            print(bcolors.ENDC)
            system(device_name + device + " shell am force-stop "  + forntactivity.split("/")[0])
            return True

    return False

def go_home(device_name,device,app):
    print(device_name + "Back To Home [ " + bcolors.BOLD + bcolors.FAIL + "Function Called" + bcolors.ENDC + "  ]")
    back = False
    while back == False:
        back = do_back(device_name , device)

    execute(device_name, device + " shell am force-stop  " + app , True)

def get_devices():
    global devices
    print("GET DEVICES [ " + bcolors.BOLD + bcolors.FAIL + "Function Called" + bcolors.ENDC + "  ]")
    get = execute("GET DEVICES LIST > ","adb devices > devices",True)
    with open("devices" , "r") as f:
        for line in f:
            if "unauthoriz" not in line :
                device = execute("GET DEVICES LIST > ","echo '" + line+ "' | awk '{print $1}'",False)
                if device != None and "List" not in device and device != None:
                    devices.append(device)
            else:
                device = execute("GET DEVICES LIST > ", "echo '" + line + "' | awk '{print $1}'", False)
                if device != "List" and device != None:
                    print(bcolors.BOLD + bcolors.FAIL)
                    print("!!!!RUNTIME ERROR IN GET DEVICE!!")
                    print(" " + line)
                    print(bcolors.ENDC)
                    _exit(1)

def make_impression(device_name,device,app):
    global class_name
    tap_cod = [
        # native top
        " ",
        # interst 1st
        " shell input tap 135 760 ",
        # interst 2nd
        " shell input tap 380 780 ",
        # interst 3rd
        " shell input tap 380 780 ",
        # 1st banner
        " ",
        # 2nd banner
        " ",
        # 3rd banner
        " ",
        # 4th banner
        " "
    ]
    print(device_name + "make_click [ " + bcolors.BOLD + bcolors.FAIL + "Function Called" + bcolors.ENDC + "  ]")


    # open app
    execute(device_name , device + " shell am  start -n com.doc4fun.GirlsClothRemove/." + class_name[randint(0 , len(class_name) -1 )],True)
    # Synced
    sleep(2)
    # make impression
    sleep(2)
    # MAKE IMpression
    tap_cmd = tap_cod[randint(0, len(tap_cod) - 1)]
    if " " != tap_cmd:
        print(device_name + "make_impression_tap [ " + bcolors.BOLD + bcolors.FAIL + "TAP TOUCH" + bcolors.ENDC + "  ]")
        execute(device_name,device + tap_cmd,True)
    # close app
    go_home(device_name, device,app)

    if Check_Network(device_name,device):
        print(device_name + "make_impression [ " + bcolors.BOLD + bcolors.FAIL + "Function Call Succussful" + bcolors.ENDC + " ]" )
        return True
    else:
        print(device_name + "make_impression [ " + bcolors.BOLD + bcolors.FAIL + "Function Call Failed" + bcolors.ENDC + "  ]")
        return False


def make_click(device_name,device):
    print(device_name + "make_click [ " + bcolors.BOLD + bcolors.FAIL + "Function Called" + bcolors.ENDC + "  ]")
    # open app
    # sleep
    # make impression
    # if splash then press back or click
    # if banner click
    # if intersetler then click then click
    # close app
    # go_home(device_name,selcted_device + device)
    if Check_Network(device_name,device):
        print(device_name + "Make_Click [ " + bcolors.BOLD + bcolors.FAIL + "Function Call Succussful" + bcolors.ENDC + " ]" )
        return True
    else:
        print(device_name + "Make_Click [ " + bcolors.BOLD + bcolors.FAIL + "Function Call Failed" + bcolors.ENDC + "  ]")
        return False


def make_random(device_name,device,app,repeat):
    # while count do statical impression
    while repeat:
        if make_impression("JOBS_LEFT [ " + str(repeat) + " ] " + device_name,device,app):
            repeat = repeat - 1
        elif make_click("JOBS_LEFT [ " + str(repeat) + " ] " + device_name,device,app):
            repeat = repeat - 1

def make_random_impression(device_name,device,app,repeat):
    # while count do impression
    while repeat:
        if make_impression("Count [ " + str(repeat) + " ]" + device_name,device,app):
            repeat = repeat - 1

def make_random_click(device_name,device,app,repeat):
    # while count do only clicks
    while repeat:
        if make_click("Count [ " + str(repeat) + " ]" + device_name,device,app):
            repeat = repeat - 1

def make_log():
    # make json str
    # save to file with date-log.db
    pass

def Work(device_name,device,app,work,repeat):
    # perform task
    if work == 1:
        make_random(device_name, selcted_device + device,app,repeat)
    elif work == 2:
        make_impression(device_name, selcted_device + device,app,repeat)
    elif work == 3:
        make_click(device_name, selcted_device + device,app,repeat)
    else:
        print("no option")

def work_manager(device_name,device,app,work,repeat):
    # make parellel process for device
    p = multiprocessing.Process(target=Work, args=(device_name,device,app,work,repeat,))
    p.start()
    p.join()

def main(app):
    global devices,selcted_device
    # get devices
    get_devices()
    # get work
    print("\n################## SELECT WORK TYPE ################# \n\n1. Only Impression \n2. Only Click \n3. Statically Random Oprations \n")
    print("_____________________ Configure ____________________\n")
    work = int(input("--------- Option : "))
    # get count limit
    repeat = int(input("------------ Max : "))
    print("\n_____________________ RUNTIME LOGGER [ LOG.R ] ____________________\n")
    if len(devices) > 0 :
        # Count devices
        dcount = 0
        for device in devices:
            # make monitor for each device
            d_name = execute("Get DEVICE NAME > ",selcted_device + device + " shell getprop | grep ro.product.brand | awk {'print $2'}",True)
            device_name = "Device [" + bcolors.HEADER  + str(dcount) + bcolors.ENDC + "] [" + bcolors.HEADER  +  d_name.strip('[').strip("]") + bcolors.ENDC  + "] [" + bcolors.HEADER + device + bcolors.ENDC + "] > "
            thread = threading.Thread(target=work_manager, args=(device_name,device,app,work,repeat,))
            thread.start()
            dcount = dcount + 1
    else:
        print("NO DEVICE FOUND !! [ LOG.D ] [" +  ', '.join(str(x) for x in devices) + "]" )

if __name__:
    app = "com.doc4fun.GirlsClothRemove"
    main(app)
