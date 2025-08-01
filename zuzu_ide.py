import tkinter as tk
from tkinter import filedialog, messagebox
from interpreter import Env

class ZuzuIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("Zuzu IDE")
        self.root.geometry("800x600")

        self.filename = None

        # Code editor
        self.editor = tk.Text(root, font=("Consolas", 12), wrap="word", height=20)
        self.editor.pack(fill="both", expand=True)

        # Output area
        self.output = tk.Text(root, height=10, bg="#111", fg="#0f0", font=("Courier", 11))
        self.output.pack(fill="x")

        # Menu
        self.create_menu()

        # Keyboard shortcut: Alt+Enter to run code
        self.editor.bind("<Alt-Return>", lambda event: self.run_code())

    def create_menu(self):
        menu = tk.Menu(self.root)

        file_menu = tk.Menu(menu, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu.add_cascade(label="File", menu=file_menu)

        run_menu = tk.Menu(menu, tearoff=0)
        run_menu.add_command(label="Run (Alt+Enter)", command=self.run_code)
        menu.add_cascade(label="Run", menu=run_menu)

        self.root.config(menu=menu)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Zuzu Files", "*.zuzu"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                self.filename = file_path
                self.editor.delete("1.0", tk.END)
                self.editor.insert(tk.END, file.read())

    def save_file(self):
        if self.filename:
            with open(self.filename, "w") as file:
                file.write(self.editor.get("1.0", tk.END))
        else:
            self.save_file_as()

    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".zuzu", filetypes=[("Zuzu Files", "*.zuzu")])
        if file_path:
            self.filename = file_path
            self.save_file()

    def run_code(self):
        code = self.editor.get("1.0", tk.END)
        self.output.delete("1.0", tk.END)
        try:
            # Remove comments before interpretation
            cleaned_code = "\n".join(line for line in code.splitlines() if not line.strip().startswith("#"))

            import io, sys
            buffer = io.StringIO()
            sys.stdout = buffer
            env = Env()
            env.run(cleaned_code)
            sys.stdout = sys.__stdout__
            output = buffer.getvalue()
            self.output.insert("1.0", output)
        except Exception as e:
            self.output.insert("1.0", f"Error: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ZuzuIDE(root)
    root.mainloop()
