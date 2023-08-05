from json_manager import JSONManager
from blocker_app import ProcessKiller


state_file = "log/process_killer_state.json"
jsonm = JSONManager(state_file)
kill = ProcessKiller()
jsonm.set_active(active=True)
jsonm.save_state()
process_input = jsonm.get_processes_to_kill()

def prepare_processes_list(processes_input):
    # No need to join the processes_input, as it's already a list of strings
    processes_list = [process.strip() for process in processes_input]
    return processes_list

process_done = prepare_processes_list(process_input)

print(process_input)
print(process_done)
#active = jsonm.is_active()
#while active == True:
#    print("Hi")
        