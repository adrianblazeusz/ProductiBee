from func.json_manager import JSONManager


class Web_blocker:
    def __init__(self):
        self.site_to_kill = set()
        self.hosts_path = r'C:\Windows\System32\drivers\etc\hosts'
        self.redirect = "127.0.0.1"
        self.state_file = "log/process_killer_state.json"
        self.json_m = JSONManager(self.state_file)


    def block_websites(self):
        print("Block sites")
        with open(self.hosts_path, 'r+') as hostfile:
            hosts_content = hostfile.read()
            for site in self.site_to_kill:
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
        if add_new:
            self.site_to_kill.update(websites)  
        else:
            self.site_to_kill = set(websites)

if __name__ == "__main__":

    web = Web_blocker()
    web.block_websites()
    print(web.site_to_kill)