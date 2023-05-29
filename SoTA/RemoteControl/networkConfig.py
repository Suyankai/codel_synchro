import subprocess

def run_command(command):
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return output.decode().strip()

if __name__ == "__main__":
    # pih1
    print("Setting up pih1")
    run_command("ssh pih1@10.42.0.5 sudo ifconfig eth1 169.254.21.222 netmask 255.255.0.0;"
                +" sudo ip route add dev eth1 169.254.18.165;" 
                + " sudo arp -s 169.254.18.165 a0:ce:c8:1d:04:40")
    # pih2
    print("Setting up pih2")
    run_command("ssh pih2@10.42.0.6 sudo ifconfig eth1 169.254.21.223 netmask 255.255.0.0;"
                +" sudo ip route add dev eth1 169.254.18.165;" 
                + " sudo arp -s 169.254.18.165 a0:ce:c8:1d:04:40")
    # pi2
    print("Setting up pi2")
    run_command("ssh pi2@10.42.0.3 sudo ifconfig eth1 169.254.21.224 netmask 255.255.0.0;"
                +" sudo ip route add dev eth1 169.254.18.165;" 
                + " sudo arp -s 169.254.18.165 a0:ce:c8:1d:04:40")
    # pi4
    print("Setting up pi4")
    run_command("ssh pi4@10.42.0.2 sudo ifconfig eth1 169.254.18.165 netmask 255.255.0.0;"
                +" sudo ip route add dev eth1 169.254.21.222;" 
                +" sudo arp -s 169.254.21.222 a0:ce:c8:1d:04:6a;" 
                +" sudo ip route add dev eth1 169.254.21.223;"  
                +" sudo arp -s 169.254.21.223 a0:ce:c8:1d:40:1c;" 
                +" sudo ip route add dev eth1 169.254.21.224;"  
                +" sudo arp -s 169.254.21.224 a0:ce:c8:1d:04:e3")
