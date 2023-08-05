from time import sleep
from json_manager import JSONManager

class Web_blocker:     
    def __init__(self):
        self.site_to_kill = set()  
        self.hosts_path = 'C:\Windows\System32\drivers\etchosts'
        self.redirect = "127.0.0.1"
        self.state_file = "log/process_killer_state.json"
        self.json_m = JSONManager(self.state_file)
        self.site_to_kill = self.json_m.get_sites_to_kill()


    def block_websites(self):
        print("Block sites")
        with open(self.hosts_path, 'r+') as hostfile:
            hosts_content = hostfile.read()
            for site in  self.site_to_kill:
                if site not in hosts_content:
                    hostfile.write(self.redirect + ' ' + site + '\n')
            

    def unblock_websites(self):
        print('Unblock sites')
        with open(self.hosts_path, 'r+') as hostfile:
            lines = hostfile.readlines()
            hostfile.seek(0)
            for line in lines:
                if not any(site in line for site in self.site_to_kill):
                    hostfile.write(line)
            hostfile.truncate()
    
    def set_blocked_websites(self, websites, add_new=True):
        websites_set = set(websites)  # Convert the list to a set
        if add_new:
            self.site_to_kill.update(websites_set)
        else:
            self.site_to_kill = websites_set
                