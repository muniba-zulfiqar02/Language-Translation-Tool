# main.py
# This is the main file - builds the GUI window
 
import tkinter as tk
from tkinter import ttk, messagebox
import pyperclip # for copy to clipboard
from translator import translate, get_language_list
from history import save_to_history, load_history, clear_history

# ─── MAIN APPLICATION CLASS ───────────────────────────────────────────────────

class TranslationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Language Translation Tool")
        self.root.geometry("750x600")
        self.root.configure(bg="#1e1e2e")
        self.root.resizable(False, False)

        self.build_ui()

    def build_ui(self):
        # ── Title Label ──
        title = tk.Label(
            self.root, text="🌍 Language Translator",
            font=("Helvetica", 22, "bold"),
            bg="#1e1e2e", fg="#cdd6f4"
        )
        title.pack(pady=15) 

         # ── Input Frame ──
        input_frame = tk.Frame(self.root, bg="#1e1e2e")
        input_frame.pack(padx=20, fill="x")
        tk.Label(input_frame, text="Enter Text:", font=("Helvetica",11),
                 bg="#1e1e2e", fg="#a6adc8") .pack(anchor="w")
        
        self. input_box = tk . Text(
            input_frame, height=5, font=("Helvetica", 12),
            bg="#313244", fg="#cdd6f4", insertbackground="white", 
            relief="flat", padx=10, pady=10
           
        )
        self.input_box .pack(fill="x", pady=5)

        # ── Language Selection Row ──
        lang_frame = tk.Frame(self.root, bg="#1e1e2e")
        lang_frame.pack(padx=20, pady=5, fill="x")

        tk.Label(lang_frame, text="Translate To:",
                 font=("Helvetica", 11), bg="#1e1e2e", fg="#a6adc8").pack(side="left")

        self.lang_var = tk.StringVar(value="French")
        lang_dropdown = ttk.Combobox(
            lang_frame, textvariable=self.lang_var,
            values=get_language_list(), state="readonly",
            font=("Helvetica", 11), width=22
        )
        lang_dropdown.pack(side="left", padx=10)

        # ── Buttons ──
        btn_frame = tk.Frame(self.root, bg="#1e1e2e")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Translate ▶", command=self.do_translate,
                  bg="#89b4fa", fg="#1e1e2e", font=("Helvetica", 11, "bold"),
                  relief="flat", padx=15, pady=6, cursor="hand2").pack(side="left", padx=8)

        tk.Button(btn_frame, text="Copy Result", command=self.copy_result,
                  bg="#a6e3a1", fg="#1e1e2e", font=("Helvetica", 11),
                  relief="flat", padx=15, pady=6, cursor="hand2").pack(side="left", padx=8)

        tk.Button(btn_frame, text="Clear", command=self.clear_all,
                  bg="#f38ba8", fg="#1e1e2e", font=("Helvetica", 11),
                  relief="flat", padx=15, pady=6, cursor="hand2").pack(side="left", padx=8)

        tk.Button(btn_frame, text="History 📋", command=self.show_history,
                  bg="#fab387", fg="#1e1e2e", font=("Helvetica", 11),
                  relief="flat", padx=15, pady=6, cursor="hand2").pack(side="left", padx=8)

        # ── Output Box ──
        output_frame = tk.Frame(self.root, bg="#1e1e2e")
        output_frame.pack(padx=20, fill="x")

        tk.Label(output_frame, text="Translation:",
                 font=("Helvetica", 11), bg="#1e1e2e", fg="#a6adc8").pack(anchor="w")

        self.output_box = tk.Text(
            output_frame, height=5, font=("Helvetica", 12),
            bg="#313244", fg="#a6e3a1", insertbackground="white",
            relief="flat", padx=10, pady=10, state="disabled"
        )
        self.output_box.pack(fill="x", pady=5)

        # ── Status Bar ──
        self.status = tk.Label(
            self.root, text="Ready.", font=("Helvetica", 10),
            bg="#181825", fg="#6c7086", anchor="w", padx=10
        )
        self.status.pack(fill="x", side="bottom", ipady=5)

    # ─── FUNCTIONS ────────────────────────────────────────────────────────────

    def do_translate(self):
        text = self.input_box.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Empty Input", "Please enter some text first.")
            return

        target = self.lang_var.get()
        self.status.config(text="Translating...")
        self.root.update()

        result = translate(text, target)

        self.output_box.config(state="normal")
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, result)
        self.output_box.config(state="disabled")

        save_to_history(text, result, target)
        self.status.config(text=f"✅ Translated to {target} successfully.")

    def copy_result(self):
        result = self.output_box.get("1.0", tk.END).strip()
        if result:
            self.root.clipboard_clear()
            self.root.clipboard_append(result)
            self.status.config(text="📋 Copied to clipboard!")
        else:
            messagebox.showinfo("Nothing to copy", "Translate something first.")

    def clear_all(self):
        self.input_box.delete("1.0", tk.END)
        self.output_box.config(state="normal")
        self.output_box.delete("1.0", tk.END)
        self.output_box.config(state="disabled")
        self.status.config(text="Cleared.")

    def show_history(self):
        history = load_history()
        history_win = tk.Toplevel(self.root)
        history_win.title("Translation History")
        history_win.geometry("600x400")
        history_win.configure(bg="#1e1e2e")

        tk.Label(history_win, text="Past Translations",
                 font=("Helvetica", 14, "bold"),
                 bg="#1e1e2e", fg="#cdd6f4").pack(pady=10)

        box = tk.Text(history_win, font=("Helvetica", 10),
                      bg="#313244", fg="#cdd6f4", relief="flat",
                      padx=10, pady=10)
        box.pack(fill="both", expand=True, padx=15, pady=5)

        if history:
            for entry in history:
                box.insert(tk.END, entry + "\n")
        else:
            box.insert(tk.END, "No history yet.")

        box.config(state="disabled")

        tk.Button(history_win, text="Clear History",
                  command=lambda: [clear_history(), history_win.destroy()],
                  bg="#f38ba8", fg="#1e1e2e", font=("Helvetica", 10),
                  relief="flat", padx=10, pady=4).pack(pady=8)

# ─── RUN THE APP ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    root = tk.Tk()
    app = TranslationApp(root)
    root.mainloop()

