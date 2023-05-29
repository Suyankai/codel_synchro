import subprocess
import time
import datetime

def run_command(command):
    process = subprocess.Popen(
        command.split(),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=1,
        universal_newlines=True
    )

    for line in iter(process.stdout.readline, ''):
        print(line, end='')  # Print each line of the command's output in real-time

    process.stdout.close()
    return_code = process.wait()
    return return_code

if __name__ == "__main__":
    print(datetime.datetime.now(), "Iperf start")
    for i in range(4):
        print("Round: ", i+1, "/4")
        run_command("iperf -c 10.42.0.5 -u -b 1M -t 1 -i 0.5")
        time.sleep(4)
    
    print(datetime.datetime.now(), "Iperf stop")