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
    if args.mode != "Baseline" and args.mode != "Codelpp" and args.mode != "SynCodelpp":
        parser.error("No option selected. Please choose either Baseline/Codel/SynCodelpp.")
    naming = args.naming

    client_cmds = []
    server_cmds = []

    pih1 = "ssh pih1@10.42.0.5 'sudo tcpreplay -i eth1 --duration=20 /home/pih1/DA/TestResource/db_35_stiffness_90_sm_modified.pcapng'"  
    #pih2 = "ssh pih2@10.42.0.6 'ffmpeg -re -i /home/pih2/DA/TestResource/bigbuck_bunny_8bit_200kbps_360p_60.0fps_h264.mp4 -c copy -f flv udp://169.254.18.165:9001'" 
    #pi2  = f"ssh pi2@10.42.0.3  'iperf -c 169.254.18.165 -p 5020 -b 1M -t 60 -i 1 -e > DA/SoTA/{mode}/log_h3_c_tcp_synchro_{mode}_{naming}.txt' " 
    client_cmds.append(pih1)
    #client_cmds.append(pih2)  
    #client_cmds.append(pi2) 

    #pi4_pi2  = f"ssh pi4@10.42.0.2 'iperf -s -e -p 5020 -i 1 -P 1 > DA/SoTA/{mode}/log_h3_s_tcp_synchro_{mode}_{naming}.txt'" 
    #server_cmds.append(pi4_pi2)

    for server_cmd in server_cmds:
        Popen(server_cmd, shell=True)

    time.sleep(0.01)

    for client_cmd in client_cmds:
        Popen(client_cmd, shell=True)
    
    # periodic video data
    # for i in range(6):
    #     time.sleep(11)
    #     print("Round: ", i+2, "/6")
    #     run_command(pih2)
        