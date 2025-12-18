import reflex as rx
import time
import math
from typing import TypedDict


class Attempt(TypedDict):
    level: int
    target: float
    elapsed: float
    diff: float
    error_pct: float
    success: bool
    score: int


class Badge(TypedDict):
    id: str
    name: str
    description: str
    icon: str
    color: str


class GameState(rx.State):
    """Manages the game state, timer, and levels for TicksTock."""

    current_level_idx: int = 0
    is_running: bool = False
    start_timestamp: float = 0.0
    last_elapsed: float = 0.0
    show_result: bool = False
    attempts: list[Attempt] = []
    max_unlocked_idx: int = 0
    current_streak: int = 0
    best_streak: int = 0
    score: int = 0
    combo_multiplier: int = 1
    earned_badges: list[str] = []
    BADGES_DATA: list[Badge] = [
        {
            "id": "perfect",
            "name": "Perfect Timing",
            "description": "< 1% Error",
            "icon": "target",
            "color": "text-emerald-400",
        },
        {
            "id": "sharpshooter",
            "name": "Sharpshooter",
            "description": "3 Streak",
            "icon": "crosshair",
            "color": "text-blue-400",
        },
        {
            "id": "marathon",
            "name": "Marathon",
            "description": "Reach Lvl 15",
            "icon": "mountain",
            "color": "text-indigo-400",
        },
        {
            "id": "legendary",
            "name": "Legendary",
            "description": "All Levels",
            "icon": "crown",
            "color": "text-amber-400",
        },
    ]
    _set1_count: int = 10
    _set1_start: float = 1.0
    _set1_end: float = 30.0
    _set2_count: int = 7
    _set2_start: float = 31.0
    _set2_end: float = 60.0
    _set3_fixed: list[float] = [75.0, 90.0, 120.0, 420.0]

    @rx.var
    def all_levels(self) -> list[float]:
        """Generates the list of target times for all 21 levels."""
        lvls = []
        if self._set1_count > 1:
            step1 = (self._set1_end - self._set1_start) / (self._set1_count - 1)
            for i in range(self._set1_count):
                lvls.append(round(self._set1_start + i * step1, 2))
        else:
            lvls.append(self._set1_start)
        if self._set2_count > 1:
            step2 = (self._set2_end - self._set2_start) / (self._set2_count - 1)
            for i in range(self._set2_count):
                lvls.append(round(self._set2_start + i * step2, 2))
        else:
            lvls.append(self._set2_start)
        lvls.extend(self._set3_fixed)
        return lvls

    @rx.var
    def current_target(self) -> float:
        """Returns the target time in seconds for the current level."""
        if 0 <= self.current_level_idx < len(self.all_levels):
            return self.all_levels[self.current_level_idx]
        return 0.0

    @rx.var
    def formatted_target(self) -> str:
        """Returns a formatted string of the current target time."""
        return self._format_time(self.current_target)

    @rx.var
    def formatted_last_elapsed(self) -> str:
        """Returns a formatted string of the last elapsed time."""
        return self._format_time(self.last_elapsed)

    @rx.var
    def time_diff(self) -> float:
        """Returns the difference between elapsed time and target time."""
        return self.last_elapsed - self.current_target

    @rx.var
    def formatted_diff(self) -> str:
        """Returns a formatted string of the time difference with sign."""
        diff = self.time_diff
        sign = "+" if diff > 0 else "-"
        return f"{sign}{self._format_time(abs(diff))}"

    @rx.var
    def error_percentage(self) -> float:
        """Returns the absolute error percentage."""
        if self.current_target == 0:
            return 0.0
        return abs(self.time_diff / self.current_target) * 100.0

    @rx.var
    def is_success(self) -> bool:
        """Determines if the attempt was successful based on error margin."""
        if self.current_level_idx < 3:
            return True
        return self.error_percentage <= 10.0

    @rx.var
    def total_levels(self) -> int:
        return len(self.all_levels)

    @rx.var
    def difficulty(self) -> str:
        t = self.current_target
        if t < 10:
            return "Easy"
        if t < 30:
            return "Medium"
        if t < 60:
            return "Hard"
        return "Expert"

    @rx.var
    def difficulty_color(self) -> str:
        d = self.difficulty
        if d == "Easy":
            return "text-emerald-400"
        if d == "Medium":
            return "text-blue-400"
        if d == "Hard":
            return "text-amber-400"
        return "text-rose-400"

    @rx.var
    def difficulty_badge_classes(self) -> str:
        d = self.difficulty
        if d == "Easy":
            return "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 shadow-[0_0_15px_-3px_rgba(52,211,153,0.3)]"
        if d == "Medium":
            return "bg-blue-500/10 text-blue-400 border border-blue-500/20 shadow-[0_0_15px_-3px_rgba(96,165,250,0.3)]"
        if d == "Hard":
            return "bg-amber-500/10 text-amber-400 border border-amber-500/20 shadow-[0_0_15px_-3px_rgba(251,191,36,0.3)]"
        return "bg-rose-500/10 text-rose-400 border border-rose-500/20 shadow-[0_0_15px_-3px_rgba(251,113,133,0.3)]"

    @rx.var
    def total_attempts_count(self) -> int:
        return len(self.attempts)

    @rx.var
    def success_rate(self) -> float:
        if not self.attempts:
            return 0.0
        wins = sum((1 for a in self.attempts if a["success"]))
        return wins / len(self.attempts) * 100.0

    @rx.var
    def formatted_success_rate(self) -> str:
        return f"{self.success_rate:.1f}"

    @rx.var
    def avg_error(self) -> float:
        if not self.attempts:
            return 0.0
        total_err = sum((a["error_pct"] for a in self.attempts))
        return total_err / len(self.attempts)

    @rx.var
    def formatted_avg_error(self) -> str:
        return f"{self.avg_error:.1f}"

    @rx.var
    def progress_percent(self) -> float:
        return (self.max_unlocked_idx + 1) / self.total_levels * 100.0

    @rx.var
    def current_rank(self) -> str:
        if self.max_unlocked_idx >= 20:
            return "Grandmaster"
        if self.max_unlocked_idx >= 15:
            return "Master"
        if self.max_unlocked_idx >= 10:
            return "Expert"
        if self.max_unlocked_idx >= 5:
            return "Apprentice"
        return "Beginner"

    @rx.var
    def rank_icon(self) -> str:
        r = self.current_rank
        if r == "Grandmaster":
            return "crown"
        if r == "Master":
            return "medal"
        if r == "Expert":
            return "star"
        if r == "Apprentice":
            return "award"
        return "user"

    @rx.var
    def badges_list(self) -> list[Badge]:
        return [b for b in self.BADGES_DATA if b["id"] in self.earned_badges]

    def _format_time(self, seconds: float) -> str:
        """Helper to format seconds into mm:ss.ms or ss.ms."""
        if seconds < 0:
            seconds = 0
        mins = int(seconds // 60)
        secs = seconds % 60
        if mins > 0:
            return f"{mins}m {secs:.2f}s"
        else:
            return f"{secs:.2f}s"

    @rx.event
    def start_timer(self):
        """Starts the timer."""
        self.is_running = True
        self.show_result = False
        self.start_timestamp = time.time()
        return rx.call_script("playStart()")

    @rx.event
    def stop_timer(self):
        """Stops the timer and calculates elapsed time."""
        if self.is_running:
            end_time = time.time()
            self.last_elapsed = end_time - self.start_timestamp
            self.is_running = False
            self.show_result = True
            diff = self.last_elapsed - self.current_target
            err_pct = 0.0
            if self.current_target > 0:
                err_pct = abs(diff / self.current_target) * 100.0
            success = False
            if self.current_level_idx < 3:
                success = True
            else:
                success = err_pct <= 10.0
            attempt_score = 0
            if success:
                base_points = 1000
                accuracy_bonus = max(0, 100 - err_pct) * 10
                attempt_score = int(
                    (base_points + accuracy_bonus) * self.combo_multiplier
                )
                self.score += attempt_score
                self.current_streak += 1
                self.combo_multiplier = min(5, 1 + self.current_streak // 3)
                if self.current_streak > self.best_streak:
                    self.best_streak = self.current_streak
                if (
                    self.current_level_idx == self.max_unlocked_idx
                    and self.max_unlocked_idx < self.total_levels - 1
                ):
                    self.max_unlocked_idx += 1
            else:
                self.current_streak = 0
                self.combo_multiplier = 1
            attempt: Attempt = {
                "level": self.current_level_idx + 1,
                "target": self.current_target,
                "elapsed": self.last_elapsed,
                "diff": diff,
                "error_pct": err_pct,
                "success": success,
                "score": attempt_score,
            }
            if self.current_level_idx < 3:
                existing_index = -1
                for i, a in enumerate(self.attempts):
                    if a["level"] == self.current_level_idx + 1:
                        existing_index = i
                        break
                if existing_index != -1:
                    if err_pct < self.attempts[existing_index]["error_pct"]:
                        self.attempts.pop(existing_index)
                        self.attempts.insert(0, attempt)
                else:
                    self.attempts.insert(0, attempt)
            else:
                self.attempts.insert(0, attempt)
            new_badges = []
            if success and err_pct < 1.0 and ("perfect" not in self.earned_badges):
                self.earned_badges.append("perfect")
                new_badges.append("Perfect Timing")
            if self.current_streak >= 3 and "sharpshooter" not in self.earned_badges:
                self.earned_badges.append("sharpshooter")
                new_badges.append("Sharpshooter")
            if (
                self.current_level_idx + 1 >= 15
                and "marathon" not in self.earned_badges
            ):
                self.earned_badges.append("marathon")
                new_badges.append("Marathon")
            if self.max_unlocked_idx >= 20 and "legendary" not in self.earned_badges:
                self.earned_badges.append("legendary")
                new_badges.append("Legendary")
            for b in new_badges:
                yield rx.toast(
                    f"Badge Unlocked: {b}!", duration=3000, position="top-center"
                )
            if success:
                yield rx.call_script("playSuccess()")
                if err_pct < 5.0:
                    yield rx.call_script(
                        "confetti({particleCount: 150, spread: 70, origin: { y: 0.6 }})"
                    )
                else:
                    yield rx.call_script(
                        "confetti({particleCount: 50, spread: 50, origin: { y: 0.6 }})"
                    )
            else:
                yield rx.call_script("playFailure()")

    @rx.event
    def next_level(self):
        """Advances to the next level."""
        if (
            self.current_level_idx < self.total_levels - 1
            and self.current_level_idx < self.max_unlocked_idx
        ):
            self.current_level_idx += 1
            self.show_result = False
            self.last_elapsed = 0.0
        rx.call_script("playClick()")

    @rx.event
    def prev_level(self):
        """Goes back to the previous level."""
        if self.current_level_idx > 0:
            self.current_level_idx -= 1
            self.show_result = False
            self.last_elapsed = 0.0
        rx.call_script("playClick()")

    @rx.event
    def retry_level(self):
        """Resets the current level state for a retry."""
        self.show_result = False
        self.last_elapsed = 0.0
        rx.call_script("playClick()")

    @rx.event
    def export_data(self):
        """Exports the attempts history as a CSV file."""
        if not self.attempts:
            return rx.toast("No data to export.", duration=3000)
        header = """Level,Target(s),Elapsed(s),Diff(s),Error(%),Success
"""
        rows = []
        for a in self.attempts:
            row = f"{a['level']},{a['target']},{a['elapsed']:.3f},{a['diff']:.3f},{a['error_pct']:.2f},{a['success']}"
            rows.append(row)
        csv_content = (
            header
            + """
""".join(rows)
        )
        return rx.download(data=csv_content, filename="ticks_tock_history.csv")