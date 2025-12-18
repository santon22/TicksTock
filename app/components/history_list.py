import reflex as rx
from app.states.game_state import GameState, Attempt


def history_item(attempt: Attempt) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                f"Lvl {attempt['level']}",
                class_name="text-slate-500 text-xs font-bold w-12",
            ),
            rx.el.div(
                rx.el.span(
                    f"{attempt['error_pct']:.1f}%",
                    class_name=rx.cond(
                        attempt["success"],
                        "text-emerald-400 font-bold",
                        "text-rose-400 font-bold",
                    ),
                ),
                class_name="text-sm w-16 text-right",
            ),
            class_name="flex items-center",
        ),
        rx.el.div(
            rx.el.span(
                f"{attempt['elapsed']:.2f}s",
                class_name="text-slate-300 font-mono text-sm",
            ),
            rx.el.span("/", class_name="text-slate-600 mx-1 text-xs"),
            rx.el.span(
                f"{attempt['target']}s", class_name="text-slate-500 font-mono text-xs"
            ),
            class_name="flex items-center ml-auto",
        ),
        class_name="flex items-center justify-between p-3 rounded-lg bg-slate-800/20 border border-slate-800/50 mb-2 hover:bg-slate-800/40 transition-colors",
    )


def history_list() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Recent Attempts",
            class_name="text-slate-500 text-xs font-bold uppercase tracking-wider mb-3",
        ),
        rx.el.div(
            rx.foreach(GameState.attempts, history_item),
            class_name="w-full overflow-y-auto max-h-[300px] pr-2 custom-scrollbar",
        ),
        class_name="w-full border-t border-slate-800/50 pt-6",
    )