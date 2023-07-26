# Run this script as root
  
import time
from datetime import datetime

end_time = datetime(2023, 7, 26, 12)

# change hosts path according to your OS
hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
# localhost's IP
redirect = "127.0.0.1"
  
# websites That you want to block
sites_to_block = ["www.facebook.com","facebook.com"]

def block_sites():
    if datetime.now() < end_time:
        print("block sites")
        with open(hosts_path, 'r+') as hostfile:
            host_content = hostfile.read()
            for site in sites_to_block:
                if site not in host_content:
                    hostfile.write(redirect + " " + site + "\n")

    else:
        print("unblock sites")
        with open(hosts_path, 'r+') as hostfile:
            lines = hostfile.readlines()
            hostfile.seek(0)
            for line in lines:
                if not any(site in line for site in sites_to_block):
                    hostfile.write(line)
            hostfile.truncate()

if __name__ == '__main__':
    while True:
        block_sites()
        time.sleep(5)
            

  
