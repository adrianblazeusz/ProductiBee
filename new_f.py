import tkinter
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("ProductiBee")
        self.geometry("700x450")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)


       
        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        # create navigation frame label
        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  ProductiBee",
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        # create home button 
        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   anchor="w", command=self.frame_home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        # create work mode button
        self.work_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Work Mode",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      anchor="w", command=self.frame_work_button_event)
        self.work_button.grid(row=2, column=0, sticky="ew")

        # create blocker button
        self.blocker_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Blocker",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      anchor="w", command=self.frame_blocker_button_event)
        self.blocker_button.grid(row=3, column=0, sticky="ew")

        # create appearance mode menu
        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Dark", "Light",  "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="Logo ProductiBee")
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        self.home_frame_button_1 = customtkinter.CTkButton(self.home_frame, text="HI")
        self.home_frame_button_1.grid(row=1, column=0, padx=20, pady=10)
       
        

        # create work frame
        self.work_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.work_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_button_2 = customtkinter.CTkButton(self.work_frame, text="Work", compound="right")
        self.home_frame_button_2.grid(row=2, column=0, padx=20, pady=10)



       # create blocker frame
        self.blocker_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.blocker_frame.grid_columnconfigure(0, weight=1)

        self.optionmenu_h = customtkinter.CTkOptionMenu(self.blocker_frame, dynamic_resizing=False,
                                                    width=60, height=28,
                                                    values=["1", "2", "3", "4", "5", "6", "7", "8", "9",
                                                            "10", "11", "12", "13", "14", "15", "16",
                                                            "17", "18", "19", "20", "21", "22", "23", "24"])
        self.optionmenu_h.grid(row=1, column=0, padx=10, pady=(10, 10))  # Changed row to 1

        self.optionmenu_min = customtkinter.CTkOptionMenu(self.blocker_frame, dynamic_resizing=False,
                                                        width=60, height=28,
                                                        values=["5", "10", "15", "20", "25", "30", "35", "40",
                                                                "45", "50", "55"])
        self.optionmenu_min.grid(row=1, column=1, padx=10, pady=(10, 10))  # Changed row to 1




        # select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # Hide all frames first using grid_remove() instead of grid_forget()
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


if __name__ == "__main__":
    app = App()
    app.mainloop()