import json

class JSONManager:
    def __init__(self, state_file):
        self.state_file = state_file
        self.state = self.load_state()

    def load_state(self):
        try:
            with open(self.state_file, "r") as f:
                state = json.load(f)
                return state
        except FileNotFoundError:
            return {
                "active": [],
                "processes_to_kill": [],
                "site_to_kill": [],
            }

    def save_state(self):
        with open(self.state_file, "w") as f:
            json.dump(self.state, f)

    def set_active(self, active):
        self.state["active"] = active

    def is_active(self):
        return self.state["active"]

    def add_processes_to_kill(self, processes_list):
        for process in processes_list:
            if process not in self.state["processes_to_kill"]:
                self.state["processes_to_kill"].append(process)

    def remove_processes_to_kill(self, processes_list):
        self.state["processes_to_kill"] = [proc for proc in self.state["processes_to_kill"] if proc not in processes_list]

    def get_processes_to_kill(self):
        return self.state["processes_to_kill"]

    def add_sites_to_kill(self, sites_list):
        for site in sites_list:
            if site not in self.state["site_to_kill"]:
                self.state["site_to_kill"].append(site)

    def remove_sites_to_kill(self, sites_list):
        self.state["site_to_kill"] = [site for site in self.state["site_to_kill"] if site not in sites_list]

    def get_sites_to_kill(self):
        return self.state["site_to_kill"]
    
    def get_num_blocked_apps(self):
        state = self.load_state()
        return len(state.get("processes_to_kill", []))

    def get_num_blocked_sites(self):
        state = self.load_state()
        return len(state.get("site_to_kill", []))