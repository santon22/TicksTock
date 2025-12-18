import tkinter as tk
from tkinter import messagebox, filedialog
import time
import csv
from collections import defaultdict

levels = []
num1 = 10
start_t = 1.0
end1 = 30.0
for i in range(num1):
    t = start_t + i * (end1 - start_t) / (num1 - 1)
    levels.append(round(t, 2))
num2 = 7
start2 = 31.0
end2 = 60.0
for i in range(num2):
    t = start2 + i * (end2 - start2) / (num2 - 1)
    levels.append(round(t, 2))
levels += [75.0, 90.0, 120.0, 420.0]
assert len(levels) == 21


def format_time(seconds):
    if seconds <= 0:
        return "0.0s"
    mins = int(seconds // 60)
    secs = seconds % 60
    if mins == 0:
        return f"{secs:.1f}s"
    elif secs < 0.1:
        return f"{mins}m"
    else:
        return f"{mins}m {secs:.1f}s"


class TicksTockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TicksTock - Master Your Inner Clock")
        self.root.geometry("600x600")
        self.root.configure(bg="#0f0f19")
        self.root.resizable(False, False)
        self.current_level = 0
        self.max_unlocked = 0
        self.state = "start"
        self.start_time = 0
        self.target_time = levels[0]
        self.elapsed = 0.0
        self.error = 0.0
        self.error_pct = 0.0
        self.this_success = False
        self.attempts = []
        self.font_large = ("Arial", 36, "bold")
        self.font_medium = ("Arial", 24)
        self.font_small = ("Arial", 16)
        self.bg = "#0f0f19"
        self.fg = "#ffffff"
        self.gray = "#787878"
        self.green = "#64ff64"
        self.red = "#ff6464"
        self.dark_gray = "#3c3c"
        self.setup_ui()
        self.root.config(menu=self.create_menu())

    def create_menu(self):
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Export CSV", command=self.export_csv)
        menubar.add_cascade(label="File", menu=file_menu)
        return menubar

    def export_csv(self):
        if not self.attempts:
            messagebox.showinfo("No Data", "No attempts to export yet.")
            return
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Export Attempts to CSV",
        )
        if filename:
            with open(filename, "w", newline="") as f:
                writer = csv.DictWriter(
                    f, fieldnames=["Level", "Target", "Elapsed", "Error_s", "Error_%"]
                )
                writer.writeheader()
                for attempt in self.attempts:
                    writer.writerow(attempt)
            messagebox.showinfo("Export Complete", f"Data exported to {filename}")

    def setup_ui(self):
        self.title_label = tk.Label(
            self.root, text="", font=self.font_medium, bg=self.bg, fg=self.fg
        )
        self.title_label.pack(pady=20)
        self.progress_label = tk.Label(
            self.root, text="", font=self.font_small, bg=self.bg, fg=self.gray
        )
        self.progress_label.pack()
        self.avg_label = tk.Label(
            self.root, text="", font=self.font_small, bg=self.bg, fg=self.gray
        )
        self.avg_label.pack()
        self.content_frame = tk.Frame(self.root, bg=self.bg)
        self.content_frame.pack(expand=True, pady=20)
        self.target_label = tk.Label(
            self.content_frame, text="", font=self.font_medium, bg=self.bg, fg=self.gray
        )
        self.target_label.pack(pady=10)
        self.time_label = tk.Label(
            self.content_frame, text="", font=self.font_large, bg=self.bg, fg=self.fg
        )
        self.time_label.pack(pady=10)
        self.instr_label = tk.Label(
            self.content_frame,
            text="",
            font=self.font_small,
            bg=self.bg,
            fg=self.gray,
            wraplength=500,
        )
        self.instr_label.pack(pady=20)
        self.btn_frame = tk.Frame(self.root, bg=self.bg)
        self.btn_frame.pack(pady=20)
        self.prev_btn = tk.Button(
            self.btn_frame,
            text="Previous",
            command=self.prev_level,
            state=tk.DISABLED,
            bg=self.gray,
            fg=self.fg,
            font=self.font_small,
        )
        self.prev_btn.pack(side=tk.LEFT, padx=10)
        self.start_btn = tk.Button(
            self.btn_frame,
            text="Start",
            command=self.start_timer,
            bg=self.green,
            fg=self.fg,
            font=self.font_small,
            width=10,
        )
        self.start_btn.pack(side=tk.LEFT, padx=10)
        self.stop_btn = tk.Button(
            self.btn_frame,
            text="Stop",
            command=self.stop_timer,
            state=tk.DISABLED,
            bg=self.red,
            fg=self.fg,
            font=self.font_small,
            width=10,
        )
        self.stop_btn.pack(side=tk.LEFT, padx=10)
        self.next_btn = tk.Button(
            self.btn_frame,
            text="Next",
            command=self.next_level,
            state=tk.DISABLED,
            bg=self.green,
            fg=self.fg,
            font=self.font_small,
        )
        self.next_btn.pack(side=tk.LEFT, padx=10)
        self.update_display()

    def get_running_average(self):
        if not self.attempts:
            return 0.0
        abs_errors = [abs(attempt["Error_%"]) for attempt in self.attempts]
        return sum(abs_errors) / len(abs_errors)

    def update_display(self):
        self.prev_btn.pack_forget()
        self.start_btn.pack_forget()
        self.stop_btn.pack_forget()
        self.next_btn.pack_forget()
        self.title_label.config(text=f"Level {self.current_level + 1}/21")
        self.progress_label.config(text=f"Unlocked up to {self.max_unlocked + 1}/21")
        avg = self.get_running_average()
        avg_text = (
            f"Avg Abs % Error: {avg:.2f}%" if self.attempts else "No attempts yet"
        )
        avg_color = self.green if avg < 5 else self.gray
        self.avg_label.config(text=avg_text, fg=avg_color)
        if self.state == "start":
            self.target_label.config(text="Target:")
            self.time_label.config(text=format_time(self.target_time))
            self.instr_label.config(
                text="""Breathe... relax, and focus.
Click Start to begin."""
            )
            self.start_btn.config(text="Start", command=self.start_timer)
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.prev_btn.config(
                state=tk.NORMAL if self.current_level > 0 else tk.DISABLED
            )
            self.next_btn.config(state=tk.DISABLED)
            self.prev_btn.pack(side=tk.LEFT, padx=10)
            self.start_btn.pack(side=tk.LEFT, padx=10)
            self.next_btn.pack(side=tk.LEFT, padx=10)
        elif self.state == "running":
            self.target_label.config(text=f"Target: {format_time(self.target_time)}")
            self.time_label.config(text="...")
            self.instr_label.config(
                text="""Focus on your internal clock.
Click Stop when you think the target time has passed."""
            )
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.stop_btn.pack(side=tk.LEFT, padx=10)
        elif self.state == "result":
            self.target_label.config(text="Target:")
            self.time_label.config(text=format_time(self.target_time))
            your_time_text = f"Your time: {format_time(self.elapsed)}"
            self.instr_label.config(
                text=your_time_text
                + f"\nError: {self.error:+.3f}s ({self.error_pct:+.2f}%)\n{('🎉 Success!' if self.this_success else 'Try again!')}"
            )
            self.start_btn.config(text="Retry", command=self.retry_level)
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.next_btn.config(
                state=tk.NORMAL
                if self.current_level < 20
                and self.current_level + 1 <= self.max_unlocked
                else tk.DISABLED
            )
            self.prev_btn.config(
                state=tk.NORMAL if self.current_level > 0 else tk.DISABLED
            )
            self.prev_btn.pack(side=tk.LEFT, padx=10)
            self.start_btn.pack(side=tk.LEFT, padx=10)
            self.next_btn.pack(side=tk.LEFT, padx=10)
        elif self.state == "complete":
            self.title_label.config(text="Congratulations!")
            self.progress_label.config(text="")
            self.target_label.config(text="")
            self.time_label.config(text="All 21 levels mastered!")
            avg = self.get_running_average()
            self.instr_label.config(
                text=f"Your internal clock is legendary.\nFinal Avg Abs % Error: {avg:.2f}%\nClose the window or restart."
            )
            self.start_btn.config(text="Restart", command=self.restart)
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.prev_btn.config(state=tk.DISABLED)
            self.next_btn.config(state=tk.DISABLED)
            self.start_btn.pack(side=tk.LEFT, padx=10)
        self.root.after(100, self.check_complete)

    def check_complete(self):
        if self.max_unlocked >= 21 and self.state == "result":
            self.state = "complete"
            self.update_display()
        elif self.state != "complete":
            self.root.after(100, self.check_complete)

    def start_timer(self):
        self.state = "running"
        self.start_time = time.time()
        self.elapsed = 0.0
        self.update_display()

    def stop_timer(self):
        self.elapsed = time.time() - self.start_time
        self.error = self.elapsed - self.target_time
        self.error_pct = (
            self.error / self.target_time * 100 if self.target_time > 0 else 0.0
        )
        self.attempts.append(
            {
                "Level": self.current_level + 1,
                "Target": self.target_time,
                "Elapsed": self.elapsed,
                "Error_s": self.error,
                "Error_%": self.error_pct,
            }
        )
        if self.current_level < 3:
            self.this_success = True
        else:
            self.this_success = abs(self.error) <= 0.1 * self.target_time
        if self.this_success:
            self.max_unlocked = max(self.max_unlocked, self.current_level + 1)
        self.state = "result"
        self.update_display()

    def retry_level(self):
        self.state = "start"
        self.update_display()

    def next_level(self):
        if self.current_level < 20 and self.current_level + 1 <= self.max_unlocked:
            self.current_level += 1
            self.target_time = levels[self.current_level]
            self.state = "start"
            self.update_display()

    def prev_level(self):
        if self.current_level > 0:
            self.current_level -= 1
            self.target_time = levels[self.current_level]
            self.state = "start"
            self.update_display()

    def restart(self):
        self.current_level = 0
        self.max_unlocked = 0
        self.target_time = levels[0]
        self.attempts = []
        self.state = "start"
        self.update_display()


if __name__ == "__main__":
    root = tk.Tk()
    app = TicksTockApp(root)
    root.mainloop()