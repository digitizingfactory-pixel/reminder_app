import datetime as dt
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class ReminderApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Desktop Reminder")
        self.root.geometry("460x340")
        self.root.resizable(False, False)

        self.reminders: list[dict[str, object]] = []

        self._build_ui()
        self._tick()

    def _build_ui(self) -> None:
        frame = ttk.Frame(self.root, padding=14)
        frame.pack(fill="both", expand=True)

        title = ttk.Label(frame, text="Set a Reminder", font=("Segoe UI", 14, "bold"))
        title.pack(anchor="w", pady=(0, 10))

        ttk.Label(frame, text="Date & time (YYYY-MM-DD HH:MM):").pack(anchor="w")
        self.when_var = tk.StringVar()
        self.when_entry = ttk.Entry(frame, textvariable=self.when_var)
        self.when_entry.pack(fill="x", pady=(2, 8))

        ttk.Label(frame, text="Reminder text:").pack(anchor="w")
        self.note_var = tk.StringVar()
        self.note_entry = ttk.Entry(frame, textvariable=self.note_var)
        self.note_entry.pack(fill="x", pady=(2, 10))

        add_btn = ttk.Button(frame, text="Add reminder", command=self.add_reminder)
        add_btn.pack(anchor="w", pady=(0, 12))

        ttk.Label(frame, text="Upcoming reminders:").pack(anchor="w")
        self.listbox = tk.Listbox(frame, height=8)
        self.listbox.pack(fill="both", expand=True)

        hint = ttk.Label(
            frame,
            text="Leave this window open. A pop-up appears when the reminder time is reached.",
            foreground="#555",
            wraplength=420,
        )
        hint.pack(anchor="w", pady=(8, 0))

    def add_reminder(self) -> None:
        when_text = self.when_var.get().strip()
        note = self.note_var.get().strip()

        if not when_text or not note:
            messagebox.showerror("Missing information", "Please enter both date/time and reminder text.")
            return

        try:
            remind_at = dt.datetime.strptime(when_text, "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showerror(
                "Invalid date/time",
                "Use this format: YYYY-MM-DD HH:MM\nExample: 2026-02-23 14:30",
            )
            return

        if remind_at <= dt.datetime.now():
            messagebox.showerror("Invalid date/time", "Reminder must be set in the future.")
            return

        self.reminders.append({"time": remind_at, "text": note, "triggered": False})
        self.reminders.sort(key=lambda r: r["time"])

        self.when_var.set("")
        self.note_var.set("")
        self.when_entry.focus_set()
        self._refresh_listbox()

    def _refresh_listbox(self) -> None:
        self.listbox.delete(0, tk.END)
        for reminder in self.reminders:
            remind_at = reminder["time"]
            text = reminder["text"]
            self.listbox.insert(tk.END, f"{remind_at:%Y-%m-%d %H:%M}  -  {text}")

    def _tick(self) -> None:
        now = dt.datetime.now()
        for reminder in self.reminders:
            if not reminder["triggered"] and now >= reminder["time"]:
                reminder["triggered"] = True
                self._notify(reminder["text"])

        self.reminders = [r for r in self.reminders if not r["triggered"]]
        self._refresh_listbox()
        self.root.after(1000, self._tick)

    def _notify(self, text: str) -> None:
        self.root.bell()
        messagebox.showinfo("Reminder", text)


def main() -> None:
    root = tk.Tk()
    ReminderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
