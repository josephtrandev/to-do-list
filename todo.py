import tkinter as tk
import customtkinter as ctk
import os
from PIL import Image

class ToplevelWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")
        self.resizable(0,0)

        self.label = ctk.CTkLabel(self, text="Enter a task:")
        self.label.grid(row=0, column=0, columnspan=2, padx=20, pady=20)
        self.attributes("-topmost",True)

class App(ctk.CTk):
    ctk.set_appearance_mode("Dark")
    def __init__(self):
        super().__init__()

        self.title("To-Do List App")
        self.geometry("1280x720")

        self.toplevel_window = None

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images in light and dark mode
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.after(201, lambda :self.iconbitmap(os.path.join(image_path, "Note_logo_single.ico")))
        self.logo_image = ctk.CTkImage(Image.open(os.path.join(image_path, "Note_logo_single.png")), size=(26, 26))
        self.image_icon_image = ctk.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
        self.home_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))

        # create navigation frame
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="  To-Do List App", image=self.logo_image,
                                                             compound="left", font=ctk.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.appearance_mode_menu = ctk.CTkOptionMenu(self.navigation_frame, values=["Dark", "Light", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_large_image_label = ctk.CTkLabel(self.home_frame, text="Home")
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10, sticky="ew")


        self.listbox_frame = ctk.CTkFrame(self.home_frame)
        self.listbox_frame.grid(row=1, column=0, padx=40, sticky="ew")
        self.listbox_frame.grid_rowconfigure(0, weight=1)  # Allow listbox to expand vertically
        self.listbox_frame.grid_columnconfigure(0, weight=1)  # Allow listbox to expand horizontally

        self.listbox_task = tk.Listbox(self.listbox_frame, bg="black", fg="white", height=20, width=50, font="Helvetica")
        self.listbox_task.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=(0, 10))


        self.button_frame = ctk.CTkFrame(self.home_frame)
        self.button_frame.grid(row=2, column=0, sticky="ew")
        self.button_frame.grid_columnconfigure((0, 1, 2), weight=1)  # Equal weight for columns

        self.home_frame_button_1 = ctk.CTkButton(self.button_frame, text="Add task", width=10, image=self.image_icon_image, command=self.open_toplevel)
        self.home_frame_button_1.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.home_frame_button_2 = ctk.CTkButton(self.button_frame, text="Delete task", width=10, image=self.image_icon_image, command=self.delete_task)
        self.home_frame_button_2.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.home_frame_button_3 = ctk.CTkButton(self.button_frame, text="Mark as complete", width=10, image=self.image_icon_image, command=self.mark_completed)
        self.home_frame_button_3.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        # select default frame
        self.select_frame_by_name("home")

    def add_task(self):
        input_text = self.toplevel_window.textbox.get(1.0,'end-1c')
        if input_text.strip():
            self.listbox_task.insert(tk.END,input_text)
            self.toplevel_window.destroy()
            self.toplevel_window.update()
        else:
            tk.messagebox.showwarning(title="Warning!",message="Please enter a task")

    def delete_task(self):
        selected=self.listbox_task.curselection()
        self.listbox_task.delete(selected[0])

    def mark_completed(self):
        marked=self.listbox_task.curselection()
        if not marked:
            tk.messagebox.showwarning(title="Warning!",message="Please select a task to mark")
        else:
            temp=marked[0]
            temp_marked=self.listbox_task.get(marked)
            temp_marked=temp_marked+" ✔"
            self.listbox_task.delete(temp)
            self.listbox_task.insert(temp,temp_marked)

    def cancel_button(self):
        self.toplevel_window.destroy()
        self.toplevel_window.update()

    def open_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(self)  # create window if its None or destroyed
            self.toplevel_window.grab_set()
            self.toplevel_window.title("New Task")
            self.toplevel_window.after(201, lambda :self.toplevel_window.iconbitmap("images\\Note_logo_single.ico"))
            self.toplevel_window.textbox = ctk.CTkTextbox(master=self.toplevel_window, width=400, height=100, corner_radius=0)
            self.toplevel_window.textbox.grid(row=1, column=0, columnspan=2)

            self.toplevel_window.confirm = ctk.CTkButton(master=self.toplevel_window, text="Add Task", command=self.add_task)
            self.toplevel_window.confirm.grid(row=2, column=0, padx=10, pady=10)
            self.toplevel_window.cancel = ctk.CTkButton(master=self.toplevel_window, text="Cancel", command=self.cancel_button)
            self.toplevel_window.cancel.grid(row=2, column=1, padx=10, pady=10)

            self.toplevel_window.after(300, lambda: self.toplevel_window.textbox.focus_force())
        else:
            self.toplevel_window.focus()  # if window exists focus it

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def change_appearance_mode_event(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()