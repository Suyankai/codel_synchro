import subprocess
from subprocess import Popen
import argparse
import time

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
    parser = argparse.ArgumentParser()
    group = parser
    group.add_argument("-m", "--mode", type=str, help="Mode of this test. Baseline/Codelpp")
    group.add_argument("-n", "--naming", type=str, help="Naming of this test")
    args = parser.parse_args()

    mode = args.mode
    if args.mode != "Baseline" and args.mode != "Codelpp":
        parser.error("No option selected. Please choose either Baseline/Codel.")
    naming = args.naming

    client_cmds = []
    server_cmds = []

    pih1 = "ssh pih1@10.42.0.5 'iperf -c 169.254.18.165 -u -p 5001 -b 1M -t 1 -i 0.5'"  
    pih2 = "ssh pih2@10.42.0.6 'iperf -c 169.254.18.165 -u -p 5010 -b 3m,2m -t 25 -i 0.5'" 
    #pi2  = "ssh pi2@10.42.0.3  'iperf -c 169.254.18.165 -u -p 5020 -b 3M -t 20 -i 0.5'" 
    client_cmds.append(pih1)
    client_cmds.append(pih2)  
    #client_cmds.append(pi2) 

    pi4_pih1 = "ssh pi4@10.42.0.2 'iperf -s -u -e -p 5001 -i 0.5 -P 4 > DA/SoTA/{mode}/log_h1_s_synchro_{naming}.txt'" 
    pi4_pih2 = "ssh pi4@10.42.0.2 'iperf -s -u -e -p 5010 -i 0.5 -P 1 > DA/SoTA/{mode}/log_h2_s_synchro_{naming}.txt'" 
    #pi4_pi2  = "ssh pi4@10.42.0.2 'iperf -s -u -e -p 5020 -i 0.5 -P 1 > DA/SoTA/Codelpp/log_h3_s_synchro_testtttt.txt'" 
    server_cmds.append(pi4_pih1)
    server_cmds.append(pi4_pih2)
    #server_cmds.append(pi4_pi2)

    for server_cmd in server_cmds:
        Popen(server_cmd, shell=True)

    time.sleep(1)

    for client_cmd in client_cmds:
        Popen(client_cmd, shell=True)
    
    # periodic haptic data
    time.sleep(4)
    for i in range(3):
        print("Round: ", i+2, "/4")
        run_command("ssh pih1@10.42.0.5 iperf -c 169.254.18.165 -u -p 5001 -b 1M -t 1 -i 0.5")
        time.sleep(4)