import reflex as rx
from app.states.game_state import GameState


def timer_display() -> rx.Component:
    """
    Component that displays the timer.
    Shows target time when idle.
    Shows pulsing animation when running.
    Shows elapsed time and result when stopped.
    """
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.cond(
                    GameState.is_running,
                    rx.el.span(
                        "Tracking internal clock...",
                        class_name="text-indigo-400 font-medium tracking-wider text-sm uppercase animate-pulse",
                    ),
                    rx.cond(
                        GameState.show_result,
                        rx.el.span(
                            "Result",
                            class_name="text-slate-400 font-medium tracking-wider text-sm uppercase",
                        ),
                        rx.el.span(
                            "Target Time",
                            class_name="text-slate-400 font-medium tracking-wider text-sm uppercase",
                        ),
                    ),
                ),
                class_name="absolute top-8 left-0 right-0 text-center z-20",
            ),
            rx.el.div(
                rx.cond(
                    GameState.is_running,
                    rx.el.div(
                        rx.el.div(
                            class_name="w-4 h-4 bg-indigo-500 rounded-full animate-bounce"
                        ),
                        rx.el.div(
                            class_name="w-4 h-4 bg-indigo-500 rounded-full animate-bounce delay-100"
                        ),
                        rx.el.div(
                            class_name="w-4 h-4 bg-indigo-500 rounded-full animate-bounce delay-200"
                        ),
                        class_name="flex gap-3 items-center justify-center h-24",
                    ),
                    rx.cond(
                        GameState.show_result,
                        rx.el.div(
                            rx.el.span(
                                GameState.formatted_last_elapsed,
                                class_name="text-5xl sm:text-7xl font-bold text-white tracking-tight tabular-nums",
                            ),
                            rx.el.div(
                                rx.el.span(
                                    "Diff: ", class_name="text-slate-500 mr-2 text-lg"
                                ),
                                rx.el.span(
                                    GameState.formatted_diff,
                                    class_name=rx.cond(
                                        GameState.is_success,
                                        "text-emerald-400 font-mono text-lg font-bold",
                                        "text-rose-400 font-mono text-lg font-bold",
                                    ),
                                ),
                                class_name="mt-2 flex items-center justify-center",
                            ),
                            rx.cond(
                                GameState.is_success,
                                rx.el.div(
                                    rx.el.span(
                                        "+",
                                        class_name="text-amber-400 text-sm font-bold mr-1",
                                    ),
                                    rx.el.span(
                                        GameState.attempts[0]["score"],
                                        class_name="text-amber-400 font-bold font-mono text-lg",
                                    ),
                                    rx.cond(
                                        GameState.combo_multiplier > 1,
                                        rx.el.span(
                                            f" (x{GameState.combo_multiplier})",
                                            class_name="text-amber-500 text-sm font-bold ml-1 animate-pulse",
                                        ),
                                    ),
                                    class_name="mt-2 flex items-center justify-center bg-amber-500/10 px-3 py-1 rounded-full border border-amber-500/20",
                                ),
                            ),
                            class_name="flex flex-col items-center animate-in fade-in zoom-in duration-300",
                        ),
                        rx.el.span(
                            GameState.formatted_target,
                            class_name="text-5xl sm:text-7xl font-bold text-white tracking-tight tabular-nums",
                        ),
                    ),
                ),
                class_name="flex items-center justify-center h-full w-full",
            ),
            class_name=rx.cond(
                GameState.is_running,
                "relative w-72 h-72 sm:w-96 sm:h-96 rounded-full border-4 border-indigo-500/30 bg-slate-900/50 backdrop-blur-sm shadow-[0_0_50px_-12px_rgba(99,102,241,0.25)] flex items-center justify-center transition-all duration-500 animate-pulse",
                rx.cond(
                    GameState.show_result & GameState.is_success,
                    "relative w-72 h-72 sm:w-96 sm:h-96 rounded-full border-4 border-emerald-400 bg-slate-900/50 backdrop-blur-sm shadow-[0_0_100px_-10px_rgba(52,211,153,0.5)] flex items-center justify-center transition-all duration-500 ring-2 ring-emerald-500/20",
                    rx.cond(
                        GameState.show_result & ~GameState.is_success,
                        "relative w-72 h-72 sm:w-96 sm:h-96 rounded-full border-4 border-rose-500 bg-slate-900/50 backdrop-blur-sm shadow-[0_0_100px_-10px_rgba(244,63,94,0.5)] flex items-center justify-center transition-all duration-500 ring-2 ring-rose-500/20 animate-[shake_0.5s_ease-in-out]",
                        "relative w-72 h-72 sm:w-96 sm:h-96 rounded-full border-4 border-slate-700/30 bg-slate-900/50 backdrop-blur-sm shadow-xl flex items-center justify-center transition-all duration-500 hover:border-indigo-500/30 hover:shadow-indigo-500/10",
                    ),
                ),
            ),
        ),
        rx.el.div(
            rx.cond(
                GameState.is_running,
                rx.el.p(
                    "Focus... click Stop when you feel the time is right.",
                    class_name="text-slate-400 text-lg font-medium animate-pulse",
                ),
                rx.cond(
                    GameState.show_result,
                    rx.el.div(
                        rx.cond(
                            GameState.is_success,
                            rx.el.p(
                                "Perfect timing! Your internal clock is synced.",
                                class_name="text-emerald-400 text-lg font-medium",
                            ),
                            rx.el.p(
                                "Not quite there. Try again to calibrate.",
                                class_name="text-rose-400 text-lg font-medium",
                            ),
                        ),
                        rx.el.p(
                            f"Target was {GameState.formatted_target}",
                            class_name="text-slate-500 text-sm mt-1",
                        ),
                        class_name="flex flex-col items-center",
                    ),
                    rx.el.p(
                        "Internalize this duration. Click Start when ready.",
                        class_name="text-slate-400 text-lg font-medium",
                    ),
                ),
            ),
            class_name="mt-8 text-center h-16 flex items-center justify-center",
        ),
        class_name="flex flex-col items-center justify-center mb-8",
    )