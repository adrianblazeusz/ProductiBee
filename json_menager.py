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
                "active": False,
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
        self.state["processes_to_kill"].extend(processes_list)

    def remove_processes_to_kill(self, processes_list):
        self.state["processes_to_kill"] = [proc for proc in self.state["processes_to_kill"] if proc not in processes_list]

    def get_processes_to_kill(self):
        return self.state["processes_to_kill"]

    def add_sites_to_kill(self, sites_list):
        self.state["site_to_kill"].extend(sites_list)

    def remove_sites_to_kill(self, sites_list):
        self.state["site_to_kill"] = [site for site in self.state["site_to_kill"] if site not in sites_list]

    def get_sites_to_kill(self):
        return self.state["site_to_kill"]