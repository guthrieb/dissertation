import subprocess
import sys


def run_training():
    command = "cd ../model_handling/training/darknet; make clean;" \
              "make; ls ; " \
              "./darknet detector train cfg/obj.data cfg/yolo-obj.cfg darknet19_448.conv.23"

    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
    # output, error = process.communicate()

    while True:
        out = p.stdout.read(1)
        if out == '' and p.poll() != None:
            break
        if out != '':
            sys.stdout.write(out)
            sys.stdout.flush()

