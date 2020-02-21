from subprocess import Popen
import time
while True:
    cmd = "python ./get_times.py"
    proc = Popen(cmd.strip().split(" "))
    proc.wait()
    cmd = "python ./gen_timeline.py"
    proc2 = Popen(cmd.strip().split(" "))
    time.sleep(1200)
    proc2.terminate()
