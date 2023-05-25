import subprocess

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

# Example usage
#str = "ssh pih1@10.42.0.5" + 
run_command("ssh pih1@10.42.0.5 iperf -c 10.42.0.1 -u -b 2M -t 3 -i 1")