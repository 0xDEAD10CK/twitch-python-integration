import tkinter as tk

class SceneConfigApp(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent

        # Labels and inputs
        self.APPID_Label = tk.Label(self, text="APP ID:")
        self.APPID_input = tk.Entry(self, width=50)

        self.APP_SECRET_Label = tk.Label(self, text="APP SECRET:")
        self.APP_SECRET_input = tk.Entry(self, width=50)

        self.TARGET_CHANNEL_Label = tk.Label(self, text="TARGET CHANNEL:")
        self.TARGET_CHANNEL_input = tk.Entry(self, width=50)

        self.OBS_PASSWORD_Label = tk.Label(self, text="OBS PASSWORD:")
        self.OBS_PASSWORD_input = tk.Entry(self, width=50)

        self.horizontal_line = tk.Label(self, text="---------------------")

        self.SceneCount_Label = tk.Label(self, text="Scene Count 1-10:")
        self.SceneCount_input = tk.Spinbox(self, from_=1, to=10, command=self.update_scenes)

        # Layout
        self.APPID_Label.grid(row=0, column=0, sticky=tk.W)
        self.APPID_input.grid(row=0, column=1, sticky=tk.W)

        self.APP_SECRET_Label.grid(row=1, column=0, sticky=tk.W)
        self.APP_SECRET_input.grid(row=1, column=1, sticky=tk.W)

        self.TARGET_CHANNEL_Label.grid(row=2, column=0, sticky=tk.W)
        self.TARGET_CHANNEL_input.grid(row=2, column=1, sticky=tk.W)

        self.OBS_PASSWORD_Label.grid(row=3, column=0, sticky=tk.W)
        self.OBS_PASSWORD_input.grid(row=3, column=1, sticky=tk.W)

        self.horizontal_line.grid(row=4, column=0, columnspan=2, sticky=tk.W)

        self.SceneCount_Label.grid(row=5, column=0, sticky=tk.W)
        self.SceneCount_input.grid(row=5, column=1, sticky=tk.W)

        # Scene container
        self.scenes_frame = tk.Frame(self)
        self.scenes_frame.grid(row=6, column=0, columnspan=2, sticky=tk.W)

        self.update_scenes()

    def update_scenes(self):
        # Clear current scenes
        for widget in self.scenes_frame.winfo_children():
            widget.destroy()

        # Create new scenes based on spinbox value
        scene_count = int(self.SceneCount_input.get())
        for i in range(scene_count):
            scene_frame = tk.LabelFrame(self.scenes_frame, text=f"Scene {i + 1}")
            scene_frame.grid(row=i, column=0, sticky=tk.W, padx=5, pady=5)

            # Elements per scene
            tk.Label(scene_frame, text="Number of Elements:").grid(row=0, column=0, sticky=tk.W)
            elements_spinbox = tk.Spinbox(scene_frame, from_=1, to=20, width=5)
            elements_spinbox.grid(row=0, column=1, sticky=tk.W)
            

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Dynamic Scene Configuration")
    app = SceneConfigApp(root)
    app.pack(padx=10, pady=10)
    root.mainloop()
