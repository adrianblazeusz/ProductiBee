import tkinter
import tkinter.messagebox
import customtkinter
from blocker_app import ProcessKiller
from blocker_web import Web_blocker
from json_manager import JSONManager

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue") 


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("ProductiBee")
        self.geometry("700x450")

        self.state_file = "log/process_killer_state.json"
        self.json_m = JSONManager(self.state_file)

        # Load ProcessKiller state (if it exists)
        self.process_killer = ProcessKiller()
        self.web_blocker = Web_blocker()
        self.json_m.load_state()
        active = self.json_m.is_active()

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.create_navigation_frame()
        self.create_home_frame()
        self.create_work_frame()
        self.create_blocker_frame()

        # Select default frame
        self.select_frame_by_name("home")

        # If ProcessKiller is active, disable the "Block" button and enable the "Unblock" button
        if  active == True:
            self.block_button.configure(state="disabled")
            self.unblock_button.configure(state="normal")
        else: 
            self.block_button.configure(state="normal")
            self.unblock_button.configure(state="disabled")

    def create_navigation_frame(self):
        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        # create navigation frame label
        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="ProductiBee",
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        # create home button
        self.home_button_frame = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   anchor="w", command=self.frame_home_button_event)
        self.home_button_frame.grid(row=1, column=0, sticky="ew")

        # create work mode button
        self.work_button_frame = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Work Mode",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      anchor="w", command=self.frame_work_button_event)
        self.work_button_frame.grid(row=2, column=0, sticky="ew")

        # create blocker button
        self.blocker_button_frame = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Blocker",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      anchor="w", command=self.frame_blocker_button_event)
        self.blocker_button_frame.grid(row=3, column=0, sticky="ew")

        # create appearance mode menu
        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Dark", "Light",  "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

    def create_home_frame(self):
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="Logo ProductiBee")
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        self.home_frame_button_1 = customtkinter.CTkButton(self.home_frame, text="HI")
        self.home_frame_button_1.grid(row=1, column=0, padx=20, pady=10)

    def create_work_frame(self):
        self.work_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.work_frame.grid_columnconfigure(0, weight=1)
        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self.work_frame, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="new")
        self.navigation_frame.grid_rowconfigure(1, weight=1)

        # create navigation frame label
        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="Work Mode",
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=225, pady=20)

        self.tabview_work = customtkinter.CTkTabview(self.work_frame, width=250, height=425)
        self.tabview_work.grid(row=1, column=0, columnspan=3, sticky="ew")
        self.home_frame_button_1 = customtkinter.CTkButton(self.tabview_work, text="Work Time!")
        self.home_frame_button_1.grid(row=1, column=0, padx=20, pady=10)


    def create_blocker_frame(self):
        self.blocker_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.blocker_frame.grid_columnconfigure(1, weight=1)

        self.tabview = customtkinter.CTkTabview(self.blocker_frame, width=250, height=425)
        self.tabview.grid(row=0, column=0, columnspan=3, sticky="ew")
        self.tabview.add("BLOCK")
        self.tabview.add("UNBLOCK")
        self.tabview.tab("BLOCK").grid_columnconfigure(1, weight=1)
        self.tabview.tab("UNBLOCK").grid_columnconfigure(2, weight=1)


        ### Block tab
        self.entry_exe = customtkinter.CTkEntry(self.tabview.tab("BLOCK"), placeholder_text="Discord, Steam ...", width=325)
        self.entry_exe.grid(row=1, column=0, columnspan=2, padx=(10, 10), pady=(20, 10), sticky="nw")

        self.add_exe_button = customtkinter.CTkButton(self.tabview.tab("BLOCK"), text="Add App",
                                                      command=self.on_add_app_button_click)
        self.add_exe_button.grid(row=1, column=1, columnspan=2, padx=(10, 20), pady=(20, 10), sticky="se")

        self.entry_web = customtkinter.CTkEntry(self.tabview.tab("BLOCK"), placeholder_text="facebook.com, youtube.com ...", width=325)
        self.entry_web.grid(row=2, column=0, columnspan=2, padx=(10, 10), pady=(10, 10), sticky="nw")

        self.add_web_button = customtkinter.CTkButton(self.tabview.tab("BLOCK"), text="Add Site",
                                                      command=self.on_add_web_button_click)
        self.add_web_button.grid(row=2, column=1, columnspan=2, padx=(10, 20), pady=(10, 20), sticky="se")

        # App listbox in BLOCK
        self.blocked_app_listbox = customtkinter.CTkTextbox(self.tabview.tab("BLOCK"),width=225)
        self.blocked_app_listbox.grid(row=3, column=0, padx=(10, 5), pady=(0, 20), sticky="nsw")
        self.blocked_app_listbox.configure(state="normal")

        # Disable the listbox so that the user can't select the text
        self.blocked_app_listbox.bind("<1>", lambda event: "break")
        self.blocked_app_listbox.bind("<Key>", lambda event: "break")

        #Web listbox in BLOCK
        self.blocked_web_listbox = customtkinter.CTkTextbox(self.tabview.tab("BLOCK"),width=225)
        self.blocked_web_listbox.grid(row=3, column=1, padx=(5, 10), pady=(0, 20), sticky="nse")
        self.blocked_web_listbox.configure(state="normal")

        # Disable the listbox so that the user can't select the text
        self.blocked_web_listbox.bind("<1>", lambda event: "break")
        self.blocked_web_listbox.bind("<Key>", lambda event: "break")

        self.block_button = customtkinter.CTkButton(self.tabview.tab("BLOCK"), text="Block", 
                                                    command=self.start_process_killer)
        self.block_button.grid(row=4, column=0, columnspan=4, padx=(10, 10), pady=(10, 20), sticky="sew")


        ### Unblock tab
        self.delete_exe = customtkinter.CTkEntry(self.tabview.tab("UNBLOCK"), placeholder_text="Discord, Steam ...", width=325)
        self.delete_exe.grid(row=1, column=0, columnspan=2, padx=(10, 10), pady=(20, 10), sticky="nw")

        self.delete_app_button = customtkinter.CTkButton(self.tabview.tab("UNBLOCK"), text="Delete App",
                                            command=self.on_delete_app_button_click) 
        self.delete_app_button.grid(row=1, column=1, columnspan=2, padx=(10, 20), pady=(20, 10), sticky="se")

        self.delete_web = customtkinter.CTkEntry(self.tabview.tab("UNBLOCK"), placeholder_text="facebook.com, youtube.com ...", width=325)
        self.delete_web.grid(row=2, column=0, columnspan=2, padx=(10, 10), pady=(10, 10), sticky="nw")

        self.delete_web_button = customtkinter.CTkButton(self.tabview.tab("UNBLOCK"), text="Delete Site",
                                                        command=self.on_delete_web_button_click)
        self.delete_web_button.grid(row=2, column=1, columnspan=2, padx=(10, 20), pady=(10, 20), sticky="se")

        # App listbox in UNBLOCK 
        self.unblocked_app_listbox = customtkinter.CTkTextbox(self.tabview.tab("UNBLOCK"), width=225)
        self.unblocked_app_listbox.grid(row=3, column=0, padx=(10, 5), pady=(0, 20), sticky="nsw")
        self.unblocked_app_listbox.configure(state="normal")

        # Disable the listbox so that the user can't select the text
        self.unblocked_app_listbox.bind("<1>", lambda event: "break")
        self.unblocked_app_listbox.bind("<Key>", lambda event: "break")


        #Web listbox in UNBLOCK
        self.unblocked_web_listbox = customtkinter.CTkTextbox(self.tabview.tab("UNBLOCK"), width=225)
        self.unblocked_web_listbox.grid(row=3, column=1, padx=(30, 10), pady=(0, 20), sticky="nse")

        # Disable the listbox so that the user can't select the text
        self.unblocked_web_listbox.bind("<1>", lambda event: "break")
        self.unblocked_web_listbox.bind("<Key>", lambda event: "break")

        self.unblock_button = customtkinter.CTkButton(self.tabview.tab("UNBLOCK"), text="Unblock",
                                                    command=self.stop_process_killer)
        self.unblock_button.grid(row=4, column=0, columnspan=4, padx=(10, 10), pady=(10, 20), sticky="sew")

                
        self.update_blocked_app_listbox()
        self.update_blocked_web_listbox()
        
    ## APP LISTBOX FUNC
    def on_add_app_button_click(self):
        processes_input = self.entry_exe.get().strip()

        if processes_input:
            processes_list = self.prepare_processes_list(processes_input)

            self.json_m.add_processes_to_kill(processes_list)
            self.json_m.save_state()

            self.update_blocked_app_listbox()

    def on_delete_app_button_click(self):
        processes_input = self.delete_exe.get().strip()

        if processes_input:
            processes_list = self.prepare_processes_list(processes_input)

            self.json_m.remove_processes_to_kill(processes_list)
            self.json_m.save_state()

            self.update_blocked_app_listbox()


    def update_blocked_app_listbox(self):
        blocked_list = self.json_m.get_processes_to_kill()

        self.blocked_app_listbox.delete(1.0, "end")
        self.unblocked_app_listbox.delete(1.0, "end")
        separator = "\n-----------------------------------------------\n"


        self.blocked_app_listbox.insert("end", f"APP:{separator}")
        self.unblocked_app_listbox.insert("end", f"APP:{separator}")

        for app in blocked_list:
            self.blocked_app_listbox.insert("end", f"{app}{separator}")
            self.unblocked_app_listbox.insert("end", f"{app}{separator}")

        self.blocked_app_listbox.delete("end-1c", "end")


    def prepare_processes_list_to_block(self, processes_input):
        processes_list = [process.strip(",") for process in processes_input]
        return processes_list
    
    
    def prepare_processes_list(self, processes_input):
        processes_list = [process.strip() for process in processes_input.split(",") if process.strip()]

        processes_list = [process + ".exe" if not process.lower().endswith(".exe") else process for process in processes_list]

        return processes_list


    ## WEB LISTBOX FUNC
    def on_add_web_button_click(self):
        processes_input = self.entry_web.get().strip()

        if processes_input:
            processes_list = self.prepare_websites_list(processes_input)
            self.json_m.add_sites_to_kill(processes_list)
            self.json_m.save_state()
            self.update_blocked_web_listbox()

    def on_delete_web_button_click(self):
        websites_input = self.delete_web.get().strip()

        if websites_input:
            websites_list = self.prepare_websites_list(websites_input)
            self.json_m.remove_sites_to_kill(sites_list=websites_list)
            self.json_m.save_state()
            self.update_blocked_web_listbox()
            

    def update_blocked_web_listbox(self):
        blocked_list = self.json_m.get_sites_to_kill()

        self.blocked_web_listbox.delete(1.0, "end")
        self.unblocked_web_listbox.delete(1.0, "end")
        separator = "\n-----------------------------------------------\n"

        self.blocked_web_listbox.insert("end", f"SITE:{separator}")
        self.unblocked_web_listbox.insert("end", f"SITE:{separator}")

        for site in blocked_list:
            self.blocked_web_listbox.insert("end", f"{site}{separator}")
            self.unblocked_web_listbox.insert("end", f"{site}{separator}")

        self.blocked_web_listbox.delete("end-1c", "end")

    def prepare_websites_list(self, websites_input):
        website_list = [website.strip(",") for website in websites_input]
        return website_list


    def start_process_killer(self):
        #website_input = self.json_m.get_sites_to_kill()
        #website_list = self.prepare_websites_list(website_input)
        processes_input = self.json_m.get_processes_to_kill()
        processes_list = self.prepare_processes_list_to_block(processes_input)

        #self.web_blocker.set_blocked_websites(website_list)
        #self.web_blocker.block_websites()
        self.process_killer.set_blocked_processes(processes_list)
        self.process_killer.start()

        self.json_m.set_active(True)  
        self.json_m.save_state()

        self.block_button.configure(state="disabled")
        self.unblock_button.configure(state="normal")

    def stop_process_killer(self):
        self.process_killer.stop()
        #self.web_blocker.unblock_websites()

        self.json_m.set_active(False)  # Set the "active" state to False
        self.json_m.save_state()

        self.block_button.configure(state="normal")
        self.unblock_button.configure(state="disabled")


    def select_frame_by_name(self, name):
        self.home_frame.grid_remove()
        self.work_frame.grid_remove()
        self.blocker_frame.grid_remove()

        # Show the selected frame based on the given name
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        elif name == "work":
            self.work_frame.grid(row=0, column=1, sticky="nsew")
        elif name == "blocker":
            self.blocker_frame.grid(row=0, column=1, sticky="nsew")

    def frame_home_button_event(self):
        self.select_frame_by_name("home")

    def frame_work_button_event(self):
        self.select_frame_by_name("work")

    def frame_blocker_button_event(self):
        self.select_frame_by_name("blocker")


    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)