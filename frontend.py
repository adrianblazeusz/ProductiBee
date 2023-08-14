from tkinter import messagebox
import customtkinter
from blockers.blocker_app import ProcessKiller
from blockers.blocker_web import Web_blocker
from func.json_manager import JSONManager
from func.timer_set import Timer
#from analys_work.autotimer import Autotimer



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

        self.timer = Timer()
        #self.autotimer = Autotimer()

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.create_navigation_frame()
        self.create_work_frame()
        self.create_blocker_frame()

        # Select default frame
        self.select_frame_by_name("work")


    def create_navigation_frame(self):
        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        # create navigation frame label
        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="ProductiBee",
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)


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
        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Dark", "Light", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

    def create_work_frame(self):
        self.work_frame = customtkinter.CTkFrame(self, corner_radius=4, fg_color="transparent")
        self.work_frame.grid_columnconfigure(1, weight=1)
        self.work_frame.grid_rowconfigure(6, weight=1)

        self.tabview_timer = customtkinter.CTkTabview(self.work_frame, width=235, height=50)
        self.tabview_timer.grid(row=2, column=0, columnspan=2, sticky="ew", padx=(10,10), pady=(0,10))

        self.timer_label = customtkinter.CTkLabel(self.tabview_timer, text="00:00:00", font=customtkinter.CTkFont(size=40))
        self.timer_label.grid(row=2, column=0, columnspan=2, padx=(20, 20), pady=(20, 10), stick="ew")
        self.timer.set_display_label(self.timer_label)

        self.start_timer_button = customtkinter.CTkButton(self.tabview_timer, text="Start", 
                                                      command=self.start_timer_event)
        self.start_timer_button.grid(row=3, column=0, columnspan=2, stick="sew", padx=(10,10), pady=(10,50))

        self.set_lable = customtkinter.CTkTabview(self.work_frame, width=235, height=70)
        self.set_lable.grid(row=2, column=1, columnspan=4, sticky="nse", padx=(10,10), pady=(0,50))

        self.set_time = customtkinter.CTkButton(self.tabview_timer, text="Set time",
                                                command=self.open_input_dialog_event)
        self.set_time.grid(row=3, column=0,columnspan=2, padx=(10,10), pady=(25,10), stick="swe")
        
        self.analys_list = customtkinter.CTkTextbox(self.work_frame, width=500, height=250)
        self.analys_list.grid(row=1, column=0, padx=(10, 10), pady=(10, 0), sticky="sew")
        self.analys_list.configure(state="normal")

        #self.update_analysis_list()

        # Start the autotimer loop
        # self.update_autotimer()


    def create_blocker_frame(self):
        self.blocker_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.blocker_frame.grid_columnconfigure(1, weight=1)

        self.tabview = customtkinter.CTkTabview(self.blocker_frame, width=250, height=425)
        self.tabview.grid(row=0, column=0, columnspan=3, sticky="ew", padx=(10,10))
        self.tabview.add("BLOCK")
        self.tabview.add("UNBLOCK")
        self.tabview.tab("BLOCK").grid_columnconfigure(1, weight=1)
        self.tabview.tab("UNBLOCK").grid_columnconfigure(2, weight=1)


        ### Block tab
        self.entry_exe = customtkinter.CTkEntry(self.tabview.tab("BLOCK"), placeholder_text="Discord, Steam ...", width=325)
        self.entry_exe.grid(row=1, column=0, columnspan=2, padx=(10, 10), pady=(20, 10), sticky="nw")

        self.add_exe_button = customtkinter.CTkButton(self.tabview.tab("BLOCK"), text="Add App",
                                                      command=self.on_add_app_button_click)
        self.add_exe_button.grid(row=1, column=1, columnspan=2, padx=(10, 10), pady=(20, 10), sticky="se")

        self.entry_web = customtkinter.CTkEntry(self.tabview.tab("BLOCK"), placeholder_text="facebook.com, youtube.com ...", width=325)
        self.entry_web.grid(row=2, column=0, columnspan=2, padx=(10, 10), pady=(10, 10), sticky="nw")

        self.add_web_button = customtkinter.CTkButton(self.tabview.tab("BLOCK"), text="Add Site",
                                                      command=self.on_add_web_button_click)
        self.add_web_button.grid(row=2, column=1, columnspan=2, padx=(10, 10), pady=(10, 20), sticky="se")

        # App listbox in BLOCK
        self.blocked_app_listbox = customtkinter.CTkTextbox(self.tabview.tab("BLOCK"),width=225,height=250)
        self.blocked_app_listbox.grid(row=3, column=0, padx=(10, 5), pady=(0, 20), sticky="nsw")
        self.blocked_app_listbox.configure(state="normal")

        # Disable the listbox so that the user can't select the text
        #self.blocked_app_listbox.bind("<1>", lambda event: "break")
        self.blocked_app_listbox.bind("<Key>", lambda event: "break")

        #Web listbox in BLOCK
        self.blocked_web_listbox = customtkinter.CTkTextbox(self.tabview.tab("BLOCK"),width=225,height=250)
        self.blocked_web_listbox.grid(row=3, column=1, padx=(5, 10), pady=(0, 20), sticky="nse")
        self.blocked_web_listbox.configure(state="normal")

        # Disable the listbox so that the user can't select the text
        #self.blocked_web_listbox.bind("<1>", lambda event: "break")
        self.blocked_web_listbox.bind("<Key>", lambda event: "break")

        ### Unblock tab
        self.delete_exe = customtkinter.CTkEntry(self.tabview.tab("UNBLOCK"), placeholder_text="Discord, Steam ...", width=325)
        self.delete_exe.grid(row=1, column=0, columnspan=2, padx=(10, 10), pady=(20, 10), sticky="nw")

        self.delete_app_button = customtkinter.CTkButton(self.tabview.tab("UNBLOCK"), text="Delete App",
                                            command=self.on_delete_app_button_click) 
        self.delete_app_button.grid(row=1, column=1, columnspan=2, padx=(10, 10), pady=(20, 10), sticky="se")

        self.delete_web = customtkinter.CTkEntry(self.tabview.tab("UNBLOCK"), placeholder_text="facebook.com, youtube.com ...", width=325)
        self.delete_web.grid(row=2, column=0, columnspan=2, padx=(10, 10), pady=(10, 10), sticky="nw")

        self.delete_web_button = customtkinter.CTkButton(self.tabview.tab("UNBLOCK"), text="Delete Site",
                                                        command=self.on_delete_web_button_click)
        self.delete_web_button.grid(row=2, column=1, columnspan=2, padx=(10, 10), pady=(10, 20), sticky="se")

        # App listbox in UNBLOCK 
        self.unblocked_app_listbox = customtkinter.CTkTextbox(self.tabview.tab("UNBLOCK"), width=225, height=250)
        self.unblocked_app_listbox.grid(row=3, column=0, padx=(10, 5), pady=(0, 20), sticky="nsw")
        self.unblocked_app_listbox.configure(state="normal")

        # Disable the listbox so that the user can't select the text
        # self.unblocked_app_listbox.bind("<1>", lambda event: "break")
        self.unblocked_app_listbox.bind("<Key>", lambda event: "break")

        # Web listbox in UNBLOCK
        self.unblocked_web_listbox = customtkinter.CTkTextbox(self.tabview.tab("UNBLOCK"), width=225, height=250)
        self.unblocked_web_listbox.grid(row=3, column=1, padx=(10, 10), pady=(0, 20), sticky="nse")
        self.unblocked_web_listbox.configure(state="normal")

        # Disable the listbox so that the user can't select the text
        # self.unblocked_web_listbox.bind("<1>", lambda event: "break")
        self.unblocked_web_listbox.bind("<Key>", lambda event: "break")

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
        website_list = [website.strip() for website in websites_input.split(",") if website.strip()]
        return website_list

    def prepare_website_list_to_block(self, websites_input):
        websites_list = [website.strip(",") for website in websites_input]
        return websites_list

    def start_process_killer(self):
        websites_input = self.json_m.get_sites_to_kill()
        websites_list = self.prepare_website_list_to_block(websites_input)
        processes_input = self.json_m.get_processes_to_kill()
        processes_list = self.prepare_processes_list_to_block(processes_input)

        self.web_blocker.set_blocked_websites(websites_list)
        self.web_blocker.block_websites()
        self.process_killer.set_blocked_processes(processes_list)
        self.process_killer.start()

        self.json_m.set_active(True)  
        self.json_m.save_state()

    def stop_process_killer(self):
        self.process_killer.stop()
        self.web_blocker.unblock_websites()

        self.json_m.set_active(False)  
        self.json_m.save_state()

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Set your time for work:\n(hh:mm or mm)", title="Set time")
        input_time = dialog.get_input()
        if input_time:
            self.timer.set_timer(input_time)
    
    def start_timer_event(self):
        if self.timer.total_seconds <= 0:
            messagebox.showwarning("Warning", "Please set the timer first.")
        else:
            self.set_time.configure(state="disabled")
            self.start_timer_button.configure(state="disabled")
            self.timer.start_timer()

            self.start_process_killer()
            #self.autotimer.start_auto_timer()  

            self.update_timer_display()

    def stop_timer_event(self):
        self.set_time.configure(state="normal")
        self.start_timer_button.configure(state="normal")
        self.timer.stop_timer()
        self.stop_process_killer()
        #self.autotimer.stop_auto_timer()  # Stop the autotimer
        self.update_timer_display()
        
    def update_timer_display(self):
        if self.timer.is_running:
            self.timer.update_display()
            self.after(1000, self.update_timer_display)  # Continue the timer update loop
        else:
            self.set_time.configure(state="normal")
            self.start_timer_button.configure(state="normal")

            if self.timer.total_seconds <= 0 and self.json_m.is_active():
                self.stop_timer_event()

            self.json_m.set_active(False)
            self.json_m.save_state()
                
    #def update_autotimer(self):
    #    self.autotimer.update_active_window()
    #    self.after(1000, self.update_autotimer)
        
    def update_analysis_list(self):
        json_file_path = r"C:\Users\asus\Desktop\Saving-time\analys_work\json\activities.json"

        try:
            with open(json_file_path, 'r') as json_file:
                activities_json = json_file.read()

            # Wstawienie danych do widżetu
            self.analys_list.delete(1.0, "end")  # Wyczyść widżet
            self.analys_list.insert("end", activities_json)  # Wstaw dane
        except FileNotFoundError:
            self.analys_list.delete(1.0, "end")
            self.analys_list.insert("end", "File not found.")


    def select_frame_by_name(self, name):
        self.work_frame.grid_remove()
        self.blocker_frame.grid_remove()

        if name == "work":
            self.work_frame.grid(row=0, column=1, sticky="nsew")
        elif name == "blocker":
            self.blocker_frame.grid(row=0, column=1, sticky="nsew")


    def frame_work_button_event(self):
        self.select_frame_by_name("work")

    def frame_blocker_button_event(self):
        self.select_frame_by_name("blocker")


    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)