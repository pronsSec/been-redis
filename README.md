# been-redis

#### Redis Vulnerability Scanner and Exploiter

![DALL·E 2024-01-04 07 23 56 - Comic book style illustration of a person exploiting Redis servers while sitting at their desk  The character is depicted in an intense, focused state](https://github.com/pronsSec/been-redis/assets/93559326/3882af90-457c-4b21-bfb0-f96c344177fe)


Been-Redis is a cutting-edge tool designed to fill the tool belt of ethical hacking and cybersecurity experts. Harness the power of automation to detect and exploit unauthenticated Redis instances in a network. Whether you're a seasoned penetration tester or a cybersecurity enthusiast, this tool adds an edge to your arsenal, making vulnerability scanning and exploitation a breeze. 

## Features

- **Automated Scanning**: Quickly scans IP addresses for unauthenticated Redis instances.
- **Interactive Shell Deployment**: Offers a choice between deploying a PHP webshell or a PHP reverse shell.
- **User-Friendly Interaction**: Guided user input for precise and controlled operations.
- **Efficient Handling of IP Lists**: Processes multiple IPs smoothly with an option to revisit unauthenticated ones.
- **Colorful and Verbose Output**: Enhances the user experience with colored outputs and verbose descriptions.

## Prerequisites

Before diving into the world of Redis exploitation, ensure you have `redis-tools` installed on your system. This tool relies on `redis-cli` for its core functionalities.

Run the following command to install `redis-tools`:

sudo apt-get install redis-tools

## Installation

Clone the repository to your local machine using:

git clone https://github.com/pronsSec/been-redis.git && cd redis-vulnerability-scanner

## Usage

Run the tool with the following command:

python3 been-redis.py --ip <IP-ADDRESS>

or

python3 been-redis.py --file <path_to_IP_list>

## Parameters

- ip: Specify a single IP address to scan.
- file: Specify a path to a file containing a list of IP addresses, one per line.
The tool will guide you through the rest of the process with interactive prompts.

License
Redis Vulnerability Scanner and Exploiter is under the MIT License. See the LICENSE file for more details.

Disclaimer
This tool is created for educational and ethical testing purposes only. Unauthorized scanning and exploiting of Redis instances is illegal and unethical. It is the end user's responsibility to comply with all applicable local, state, and federal laws.
