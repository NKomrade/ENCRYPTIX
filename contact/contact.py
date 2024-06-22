import tkinter as tk
from tkinter import messagebox, ttk

class ContactApp:
    def __init__(self, root):
        self.root = root
        self.root.title("My Contact Book")
        self.root.geometry("950x500")
        self.contacts = {
            "Rajeev Mehra": ["+91-9822331144", "rajeev.mehra@gmail.com", "Greater Noida"],
            "Manoj Pandey": ["+91-7821341125", "manoj.pandey@outlook.com", "Mumbai"]
        }
        
        self.create_widgets()

    def create_widgets(self):
        self.header = tk.Label(self.root, text="MY CONTACT BOOK", font=('Helvetica', 18, 'bold'), fg='white', bg='black')
        self.header.pack(side=tk.TOP, fill=tk.X)

        self.sidebar = tk.Frame(self.root, bg='black')
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        button_style = {'font': ('Helvetica', 12), 'bg': 'grey', 'fg': 'white', 'relief': 'flat', 'highlightthickness': 0}
        tk.Button(self.sidebar, text="Edit Contacts", command=self.manage_contacts, **button_style).pack(pady=10, padx=10, fill=tk.X)
        tk.Button(self.sidebar, text="Add New Contact", command=self.add_contact_screen, **button_style).pack(pady=10, padx=10, fill=tk.X)

        self.content_frame = tk.Frame(self.root, bg='white')
        self.content_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        self.manage_contacts()  # Initially show the manage_contacts screen

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def manage_contacts(self):
        self.clear_content()
        self.root.geometry("950x500")
        
        self.name_label = tk.Label(self.content_frame, text="NAME:", font=('Helvetica', 12), bg='white')
        self.name_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        
        self.name_entry = tk.Entry(self.content_frame, font=('Helvetica', 12))
        self.name_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        # Using a plain "Search" button instead of an image
        self.search_button = tk.Button(self.content_frame, text="Search", command=self.search_contact, borderwidth=0, bg='grey', fg='white')
        
        self.search_button.grid(row=0, column=2, padx=10, pady=10, sticky='w')

        self.tree = ttk.Treeview(self.content_frame, columns=("Name", "Phone Number", "Email Id", "City"), show='headings')
        self.tree.heading("Name", text="Name", command=lambda: self.sort_column("Name"))
        self.tree.heading("Phone Number", text="Phone No.", command=lambda: self.sort_column("Phone Number"))
        self.tree.heading("Email Id", text="Email - ID", command=lambda: self.sort_column("Email Id"))
        self.tree.heading("City", text="City", command=lambda: self.sort_column("City"))

        # Bind double-click to open edit screen
        self.tree.bind("<Double-1>", self.open_edit_screen)

        self.tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')
        
        self.content_frame.grid_rowconfigure(1, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        self.load_contacts()

    def load_contacts(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for name, details in self.contacts.items():
            self.tree.insert('', tk.END, values=(name, details[0], details[1], details[2]))

    def search_contact(self):
        query = self.name_entry.get()
        matching_contacts = {name: details for name, details in self.contacts.items() if query.lower() in name.lower()}
        for item in self.tree.get_children():
            self.tree.delete(item)
        for name, details in matching_contacts.items():
            self.tree.insert('', tk.END, values=(name, details[0], details[1], details[2]))

    def open_edit_screen(self, event):
        item_id = self.tree.selection()[0]
        values = self.tree.item(item_id, "values")
        
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Contact")
        edit_window.geometry("400x300")

        tk.Label(edit_window, text="Name", font=('Helvetica', 12)).grid(row=0, column=0, padx=10, pady=10)
        name_entry = tk.Entry(edit_window, font=('Helvetica', 12))
        name_entry.grid(row=0, column=1, padx=10, pady=10)
        name_entry.insert(0, values[0])

        tk.Label(edit_window, text="Phone", font=('Helvetica', 12)).grid(row=1, column=0, padx=10, pady=10)
        phone_entry = tk.Entry(edit_window, font=('Helvetica', 12))
        phone_entry.grid(row=1, column=1, padx=10, pady=10)
        phone_entry.insert(0, values[1])

        tk.Label(edit_window, text="Email", font=('Helvetica', 12)).grid(row=2, column=0, padx=10, pady=10)
        email_entry = tk.Entry(edit_window, font=('Helvetica', 12))
        email_entry.grid(row=2, column=1, padx=10, pady=10)
        email_entry.insert(0, values[2])

        tk.Label(edit_window, text="City", font=('Helvetica', 12)).grid(row=3, column=0, padx=10, pady=10)
        city_entry = tk.Entry(edit_window, font=('Helvetica', 12))
        city_entry.grid(row=3, column=1, padx=10, pady=10)
        city_entry.insert(0, values[3])

        def save_changes():
            new_name = name_entry.get()
            new_phone = phone_entry.get()
            new_email = email_entry.get()
            new_city = city_entry.get()

            if new_name and new_phone and new_email and new_city:
                # Update the contacts dictionary
                if new_name != values[0]:  # If name is changed, delete the old name entry
                    del self.contacts[values[0]]
                self.contacts[new_name] = [new_phone, new_email, new_city]

                # Update the Treeview
                self.tree.item(item_id, values=(new_name, new_phone, new_email, new_city))

                messagebox.showinfo("Success", "Contact updated successfully!")
                edit_window.destroy()
            else:
                messagebox.showerror("Error", "Please fill in all fields.")

        def delete_contact():
            del self.contacts[values[0]]
            self.tree.delete(item_id)
            messagebox.showinfo("Success", "Contact deleted successfully!")
            edit_window.destroy()

        tk.Button(edit_window, text="Save", font=('Helvetica', 12), command=save_changes, bg='grey', fg='white').grid(row=4, column=0, pady=10, padx=10)
        tk.Button(edit_window, text="Delete", font=('Helvetica', 12), command=delete_contact, bg='red', fg='white').grid(row=4, column=1, pady=10, padx=10)

    def add_contact_screen(self):
        self.clear_content()
        self.root.geometry("500x500")

        tk.Label(self.content_frame, text="Add Contact", font=('Helvetica', 18, 'bold'), bg='white').grid(row=0, column=0, columnspan=2, pady=20)

        tk.Label(self.content_frame, text="Name", font=('Helvetica', 12), bg='white').grid(row=1, column=0, padx=10, pady=5, sticky='w')
        name_entry = tk.Entry(self.content_frame, font=('Helvetica', 12))
        name_entry.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        tk.Label(self.content_frame, text="Phone", font=('Helvetica', 12), bg='white').grid(row=2, column=0, padx=10, pady=5, sticky='w')
        phone_entry = tk.Entry(self.content_frame, font=('Helvetica', 12))
        phone_entry.grid(row=2, column=1, padx=10, pady=5, sticky='w')

        tk.Label(self.content_frame, text="Email", font=('Helvetica', 12), bg='white').grid(row=3, column=0, padx=10, pady=5, sticky='w')
        email_entry = tk.Entry(self.content_frame, font=('Helvetica', 12))
        email_entry.grid(row=3, column=1, padx=10, pady=5, sticky='w')

        tk.Label(self.content_frame, text="City", font=('Helvetica', 12), bg='white').grid(row=4, column=0, padx=10, pady=5, sticky='w')
        city_entry = tk.Entry(self.content_frame, font=('Helvetica', 12))
        city_entry.grid(row=4, column=1, padx=10, pady=5, sticky='w')

        def save_contact():
            name = name_entry.get()
            phone = phone_entry.get()
            email = email_entry.get()
            city = city_entry.get()
            if name and phone and email and city:
                if not phone.startswith("+91-"):
                    phone = "+91-" + phone
                self.contacts[name] = [phone, email, city]
                messagebox.showinfo("Success", "Contact added successfully!")
                self.manage_contacts()
            else:
                messagebox.showerror("Error", "Please fill in all fields.")

        tk.Button(self.content_frame, text="Save", font=('Helvetica', 12), command=save_contact, bg='grey', fg='white').grid(row=5, column=0, columnspan=2, pady=10)
        tk.Button(self.content_frame, text="Back", font=('Helvetica', 12), command=self.manage_contacts, bg='grey', fg='white').grid(row=6, column=0, columnspan=2, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactApp(root)
    root.mainloop()
