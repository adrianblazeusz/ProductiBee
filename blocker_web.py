from time import sleep
from json_manager import JSONManager

class Web_blocker:     
    def __init__(self):
        self.site_to_kill = set()  
        self.hosts_path = '/etc/hosts'
        self.redirect = "127.0.0.1"
        self.state_file = "log/process_killer_state.json"
        self.json_m = JSONManager(self.state_file)
        self.site_to_kill = self.json_m.get_sites_to_kill()


    def set_blocked_websites(self, websites, add_new=True):
        if add_new:
            self.site_to_kill.update(websites)
        else:
            self.site_to_kill = set(websites)

    def block_websites(self):
        if self.site_to_kill:
            print("Block sites")
            with open(self.hosts_path, 'r+') as hostfile:
                hosts_content = hostfile.read()
                for site in  self.site_to_kill:
                    if site not in hosts_content:
                        hostfile.write(self.redirect + ' ' + site + '\n')
            sleep(1)

    def unblock_websites(self):
        if self.site_to_kill:
            print('Unblock sites')
            with open(self.hosts_path, 'r+') as hostfile:
                lines = hostfile.readlines()
                hostfile.seek(0)
                for line in lines:
                    if not any(site in line for site in self.site_to_kill):
                        hostfile.write(line)
                hostfile.truncate()
            sleep(1)

    def set_blocked_websites(self, websites, add_new=True):
        self.set_blocked_websites(websites, add_new)

    def block_websites(self):
        self.block_websites()

    def unblock_websites(self):
        self.unblock_websites()