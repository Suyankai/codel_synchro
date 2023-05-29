'''
Example of the command:
Baseline: python SoTA/RemoteControl/pcapture.py -m Baseline -n test3
Codelpp: python SoTA/RemoteControl/pcapture.py -m Codelpp -n test3
'''
import subprocess
from subprocess import Popen
import argparse

# def run_command(command):
#     process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
#     output, error = process.communicate()
#     return output.decode().strip()

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

    cmds = []

    # pih1
    print("Capturing pkts in pih1")
    cmd_pih1 = f"ssh pih1@10.42.0.5 sudo tshark -i eth1 -f 'udp' -w /home/pih1/DA/SoTA/{mode}/Synchro/pih1_{mode}_synchro_{naming}.pcap"
    print(f".pcap: /home/pih1/DA/SoTA/{mode}/Synchro/pih1_{mode}_synchro_{naming}.pcap")
    cmds.append(cmd_pih1)
    # pih2
    print("Capturing pkts in pih2")
    cmd_pih2 = f"ssh pih2@10.42.0.6 sudo tshark -i eth1 -f 'udp' -w /home/pih2/DA/SoTA/{mode}/Synchro/pih2_{mode}_synchro_{naming}.pcap"
    print(f".pcap: /home/pih2/DA/SoTA/{mode}/Synchro/pih2_{mode}_synchro_{naming}.pcap")
    cmds.append(cmd_pih2)
    # pi2
    print("Capturing pkts in pi2")
    cmd_pi2 = f"ssh pi2@10.42.0.3 sudo tshark -i eth1 -f 'udp' -w /home/pi2/DA/SoTA/{mode}/Synchro/pi2_{mode}_synchro_{naming}.pcap"
    print(f".pcap: /home/pi2/DA/SoTA/{mode}/Synchro/pi2_{mode}_synchro_{naming}.pcap")
    cmds.append(cmd_pi2)
    # pi4
    print("Capturing pkts in pi4")
    cmd_pi4 = f"ssh pi4@10.42.0.2 sudo tshark -i eth1 -f 'udp' -w /home/pi4/DA/SoTA/{mode}/Synchro/pi4_{mode}_synchro_{naming}.pcap"
    print(f".pcap: /home/pi4/DA/SoTA/{mode}/Synchro/pi4_{mode}_synchro_{naming}.pcap")
    cmds.append(cmd_pi2)

    for cmd in cmds:
        Popen(cmd, shell=True)