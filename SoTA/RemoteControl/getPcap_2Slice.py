import subprocess
from subprocess import Popen
import argparse

def run_command(command):
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return output.decode().strip()

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

    # Get .pcap from pih1
    run_command(f"ssh pih1@10.42.0.5 sudo chown pih1:pih1 /home/pih1/DA/SoTA/{mode}/Synchro/pih1_{mode}_synchro_{naming}.pcap")
    run_command(f"scp pih1@10.42.0.5:/home/pih1/DA/SoTA/{mode}/Synchro/pih1_{mode}_synchro_{naming}.pcap  /home/su/Project/codel_synchro/LogMountain ")
    # Get .pcap from pih2
    run_command(f"ssh pih2@10.42.0.6 sudo chown pih2:pih2 /home/pih2/DA/SoTA/{mode}/Synchro/pih2_{mode}_synchro_{naming}.pcap")
    run_command(f"scp pih2@10.42.0.6:/home/pih2/DA/SoTA/{mode}/Synchro/pih2_{mode}_synchro_{naming}.pcap  /home/su/Project/codel_synchro/LogMountain ")
    # Get .pcap from pi4
    run_command(f"ssh pi4@10.42.0.2 sudo chown pi4:pi4 /home/pi4/DA/SoTA/{mode}/Synchro/pi4_{mode}_synchro_{naming}.pcap")
    run_command(f"scp pi4@10.42.0.2:/home/pi4/DA/SoTA/{mode}/Synchro/pi4_{mode}_synchro_{naming}.pcap  /home/su/Project/codel_synchro/LogMountain ")
    # Get log file from switch
    run_command(f"scp p4switch@10.42.0.11:/home/p4switch/p4/SoTA/{mode}/log/{mode}_p4_{naming}.txt  /home/su/Project/codel_synchro/LogMountain")