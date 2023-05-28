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
    run_command("ssh pih1@10.42.0.5 sudo tshark -i eth1 -f 'udp' -w /home/pih1/DA/SoTA/Baseline/Synchro/pih1_baseline_synchro_test3.pcap ")

