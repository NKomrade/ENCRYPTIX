import tkinter as tk

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("640x600")
        self.root.resizable(0, 0)
        
        self.expression = ""
        
        self.input_text = tk.StringVar()
        
        # Input Frame
        self.input_frame = tk.Frame(self.root, width=312, height=50, bd=0, highlightbackground="black", highlightcolor="black", highlightthickness=2, bg="#1C1C1C")
        self.input_frame.pack(side=tk.TOP)
        
        self.input_field = tk.Entry(self.input_frame, font=('arial', 24, 'bold'), textvariable=self.input_text, width=50, bg="#1C1C1C", fg="#FFFFFF", bd=0, justify=tk.RIGHT, insertbackground='white')
        self.input_field.grid(row=0, column=0)
        self.input_field.pack(ipady=10)
        
        # Buttons Frame
        self.btns_frame = tk.Frame(self.root, width=312, height=272.5, bg="#1C1C1C")
        self.btns_frame.pack()
        
        self.create_buttons()
        
    def create_buttons(self):
        button_texts = [
            ('AC', 1, 0), ('%', 1, 1), ('x^2', 1, 2), ('/', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('*', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('-', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('+', 4, 3),
            ('0', 5, 0), ('.', 5, 1), ('=', 5, 2)
        ]
        
        for text, row, col in button_texts:
            if text == '=':
                button = tk.Button(self.btns_frame, text=text, fg="white", width=21, height=3, bd=0, bg="#FE9505", cursor="hand2", font=('arial', 18, 'bold'),
                                   command=lambda t=text: self.click(t))
                button.grid(row=row, column=col, columnspan=2, padx=1, pady=1)
            else:
                button = tk.Button(self.btns_frame, text=text, fg="white", width=10, height=3, bd=0, bg="#333333", activebackground="#555555", activeforeground="#FFFFFF", cursor="hand2", font=('arial', 18, 'bold'),
                                   command=lambda t=text: self.click(t))
                button.grid(row=row, column=col, padx=1, pady=1)
            
    def click(self, item):
        if item == 'AC':
            self.expression = ""
            self.input_text.set("")
        elif item == '=':
            try:
                self.expression = str(eval(self.expression))
            except:
                self.expression = "Error"
            self.input_text.set(self.expression)
        elif item == 'x^2':
            try:
                self.expression = str(eval(f"{self.expression}**2"))
            except:
                self.expression = "Error"
            self.input_text.set(self.expression)
        else:
            self.expression += str(item)
            self.input_text.set(self.expression)

if __name__ == "__main__":
    root = tk.Tk()
    Calculator(root)
    root.mainloop()
