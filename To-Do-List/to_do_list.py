import tkinter as tk
from tkinter import ttk, messagebox
import pygame

#for sound effects
#can also add your own sound effect by adding it's path
pygame.mixer.init()
add_sound = pygame.mixer.Sound(r"path\to\Add_sound.mp3")
delete_sound = pygame.mixer.Sound(r"path\to\Del_sound.mp3")
check_sound = pygame.mixer.Sound(r"path\to\Del_sound.mp3")
uncheck_sound = pygame.mixer.Sound(r"path\to\Del_sound.mp3")

class TimePicker(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        
        self.hours = [f"{i:02d}" for i in range(1, 13)]
        self.minutes = [f"{i:02d}" for i in range(60)]
        self.periods = ["AM", "PM"]
        
        self.hour_var = tk.StringVar(value=self.hours[0])
        self.minute_var = tk.StringVar(value=self.minutes[0])
        self.period_var = tk.StringVar(value=self.periods[0])
        
        self.hour_spinbox = ttk.Spinbox(self, values=self.hours, width=5, textvariable=self.hour_var, wrap=True)
        self.minute_spinbox = ttk.Spinbox(self, values=self.minutes, width=5, textvariable=self.minute_var, wrap=True)
        self.period_spinbox = ttk.Spinbox(self, values=self.periods, width=5, textvariable=self.period_var, wrap=True)
        
        self.hour_spinbox.pack(side=tk.LEFT, padx=(0, 5))
        self.minute_spinbox.pack(side=tk.LEFT, padx=(0, 5))
        self.period_spinbox.pack(side=tk.LEFT)
    
    def get_time(self):
        return f"{self.hour_var.get()}:{self.minute_var.get()} {self.period_var.get()}"

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("512x512")
        self.root.configure(bg="#f0f0f0")
        self.center_window(self.root)
        self.create_widgets()

    def center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

    def create_widgets(self):
        self.tasks_frame = tk.Frame(self.root, padx=10, pady=10, bg="#ffffff", bd=2, relief=tk.SOLID)
        self.tasks_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.tasks_label = tk.Label(self.tasks_frame, text="To-Do List Tasks", font=("Arial", 18, "bold"), bg="#ffffff", fg="#333333")
        self.tasks_label.pack(anchor='w')

        self.task_list_frame = tk.Frame(self.tasks_frame, bg="#ffffff")
        self.task_list_frame.pack(fill=tk.BOTH, expand=True)

        self.add_task_button = tk.Button(self.tasks_frame, text="+", font=("Arial", 18, "bold"), bg="#FFA500", fg="#ffffff", command=self.add_task)
        self.add_task_button.pack(anchor='e')

        self.priority_var = tk.StringVar(value="All")
        self.priority_filter_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.priority_filter_frame.pack(fill=tk.X, pady=10)

        self.priority_filter_label = tk.Label(self.priority_filter_frame, text="Filter by Priority:", font=("Arial", 12), bg="#f0f0f0")
        self.priority_filter_label.pack(side=tk.LEFT, padx=(10, 0))

        self.priority_filter = ttk.Combobox(self.priority_filter_frame, textvariable=self.priority_var, values=["All", "High", "Medium", "Low"], state="readonly")
        self.priority_filter.pack(side=tk.LEFT)
        self.priority_filter.bind("<<ComboboxSelected>>", self.filter_tasks)

    def add_task(self):
        add_sound.play()
        self.new_task_window()

    def new_task_window(self):
        self.new_window = tk.Toplevel(self.root)
        self.new_window.title("Add new task")
        self.new_window.geometry("384x384")
        self.new_window.configure(bg="#f0f0f0")
        self.center_window(self.new_window)
        
        self.task_name_label = tk.Label(self.new_window, text="Task Name", bg="#f0f0f0")
        self.task_name_label.pack(pady=5)

        self.task_name_entry = tk.Entry(self.new_window, bd=2, relief=tk.SOLID)
        self.task_name_entry.pack(pady=5)

        self.task_time_label = tk.Label(self.new_window, text="Time", bg="#f0f0f0")
        self.task_time_label.pack(pady=5)

        self.time_picker = TimePicker(self.new_window)
        self.time_picker.pack(pady=5)

        self.task_priority_label = tk.Label(self.new_window, text="Priority", bg="#f0f0f0")
        self.task_priority_label.pack(pady=5)

        self.task_priority = ttk.Combobox(self.new_window, values=["High", "Medium", "Low"], state="readonly")
        self.task_priority.pack(pady=5)

        self.task_notes_label = tk.Label(self.new_window, text="Notes", bg="#f0f0f0")
        self.task_notes_label.pack(pady=5)

        self.task_notes_entry = tk.Text(self.new_window, height=5, bd=2, relief=tk.SOLID)
        self.task_notes_entry.pack(pady=5)

        self.add_task_button = tk.Button(self.new_window, text="Add Task", command=self.save_task, bg="#FFA500", fg="#ffffff")
        self.add_task_button.pack(pady=10)

    def save_task(self):
        task_name = self.task_name_entry.get()
        task_time = self.time_picker.get_time()
        task_priority = self.task_priority.get()
        task_notes = self.task_notes_entry.get("1.0", tk.END).strip()
        
        if not task_name or not task_time or not task_priority:
            messagebox.showwarning("Incomplete Data", "Please fill in all required fields (Task Name, Time, Priority).")
            return

        task = {
            "name": task_name,
            "time": task_time,
            "priority": task_priority,
            "notes": task_notes
        }

        self.add_task_to_frame(task)
        self.new_window.destroy()
        add_sound.play()

    def add_task_to_frame(self, task):
        var = tk.IntVar()
        text = f"{task['name']} - {task['time']} ({task['priority']})"
        checkbox = tk.Checkbutton(self.task_list_frame, text=text, variable=var, font=("Arial", 14), anchor='w', command=lambda: self.toggle_strike_through(checkbox, var), bg="#ffffff")
        checkbox.pack(fill=tk.X, anchor='w', pady=2)

        delete_button = tk.Button(self.task_list_frame, text="Delete", command=lambda: self.delete_task(checkbox, delete_button), bg="#ff6666", fg="#ffffff", bd=1, relief=tk.SOLID)
        delete_button.pack(anchor='e', pady=2)

        task["checkbox"] = checkbox
        task["delete_button"] = delete_button

        self.task_list_frame.tasks = getattr(self.task_list_frame, 'tasks', [])
        self.task_list_frame.tasks.append(task)

    def toggle_strike_through(self, checkbox, var):
        if var.get() == 1:
            checkbox.config(font=("Arial", 14, "overstrike"))
            check_sound.play()
        else:
            checkbox.config(font=("Arial", 14))
            uncheck_sound.play()

    def delete_task(self, checkbox, delete_button):
        checkbox.destroy()
        delete_button.destroy()
        delete_sound.play()

    def filter_tasks(self, event):
        priority = self.priority_var.get()
        for task in getattr(self.task_list_frame, 'tasks', []):
            if priority == "All" or task["priority"] == priority:
                task["checkbox"].pack(fill=tk.X, anchor='w', pady=2)
                task["delete_button"].pack(anchor='e', pady=2)
            else:
                task["checkbox"].pack_forget()
                task["delete_button"].pack_forget()

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
