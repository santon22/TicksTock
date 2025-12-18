import reflex as rx
from app.states.game_state import GameState


def controls() -> rx.Component:
    """Navigation and Game Controls."""
    return rx.el.div(
        rx.el.div(
            rx.cond(
                GameState.is_running,
                rx.el.button(
                    "STOP TIMER",
                    on_click=GameState.stop_timer,
                    class_name="w-64 py-4 rounded-xl bg-rose-600 hover:bg-rose-500 text-white font-bold tracking-widest shadow-lg shadow-rose-900/20 transform hover:scale-[1.02] active:scale-[0.98] transition-all duration-200 border border-rose-400/20",
                ),
                rx.cond(
                    GameState.show_result,
                    rx.el.button(
                        "RETRY LEVEL",
                        on_click=GameState.retry_level,
                        class_name="w-64 py-4 rounded-xl bg-slate-700 hover:bg-slate-600 text-white font-bold tracking-widest shadow-lg transform hover:scale-[1.02] active:scale-[0.98] transition-all duration-200 border border-slate-500/20",
                    ),
                    rx.el.button(
                        "START TIMER",
                        on_click=GameState.start_timer,
                        class_name="w-64 py-4 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold tracking-widest shadow-lg shadow-indigo-900/20 transform hover:scale-[1.02] active:scale-[0.98] transition-all duration-200 border border-indigo-400/20",
                    ),
                ),
            ),
            class_name="mb-12",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("chevron-left", class_name="w-6 h-6 mr-1"),
                "Prev Level",
                on_click=GameState.prev_level,
                disabled=GameState.is_running | (GameState.current_level_idx == 0),
                class_name=rx.cond(
                    GameState.is_running | (GameState.current_level_idx == 0),
                    "flex items-center px-6 py-3 rounded-lg bg-slate-800/50 text-slate-600 font-semibold cursor-not-allowed border border-slate-800",
                    "flex items-center px-6 py-3 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white font-semibold transition-all duration-200 border border-slate-700 hover:border-slate-600",
                ),
            ),
            rx.el.div(
                rx.el.span(
                    "LEVEL ",
                    class_name="text-xs font-bold text-slate-500 tracking-widest mb-1 block",
                ),
                rx.el.div(
                    rx.el.span(
                        GameState.current_level_idx + 1,
                        class_name="text-2xl font-bold text-white",
                    ),
                    rx.el.span(
                        f" / {GameState.total_levels}",
                        class_name="text-lg font-medium text-slate-500 ml-1",
                    ),
                    class_name="flex items-baseline justify-center",
                ),
                class_name="flex flex-col items-center px-8",
            ),
            rx.el.button(
                "Next Level",
                rx.icon("chevron-right", class_name="w-6 h-6 ml-1"),
                on_click=GameState.next_level,
                disabled=GameState.is_running
                | (GameState.current_level_idx == GameState.total_levels - 1)
                | (GameState.current_level_idx >= GameState.max_unlocked_idx),
                class_name=rx.cond(
                    GameState.is_running
                    | (GameState.current_level_idx == GameState.total_levels - 1)
                    | (GameState.current_level_idx >= GameState.max_unlocked_idx),
                    "flex items-center px-6 py-3 rounded-lg bg-slate-800/50 text-slate-600 font-semibold cursor-not-allowed border border-slate-800",
                    "flex items-center px-6 py-3 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white font-semibold transition-all duration-200 border border-slate-700 hover:border-slate-600",
                ),
            ),
            class_name="flex items-center justify-between w-full max-w-2xl bg-slate-900/50 p-2 rounded-2xl border border-slate-800/50 backdrop-blur-sm",
        ),
        class_name="flex flex-col items-center w-full",
    )