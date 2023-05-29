import subprocess

def run_command(command):
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return output.decode().strip()

# Example usage
result = run_command("ssh pih1@10.42.0.5 sudo ifconfig eth1 169.254.21.222 netmask 255.255.0.0")
print(result)