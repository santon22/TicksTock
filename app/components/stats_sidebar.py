import reflex as rx
from app.states.game_state import GameState, Badge
from app.components.history_list import history_list


def stat_card(
    label: str, value: str, subtext: str = None, color: str = "text-white"
) -> rx.Component:
    return rx.el.div(
        rx.el.p(
            label,
            class_name="text-slate-500 text-xs font-bold uppercase tracking-wider mb-1",
        ),
        rx.el.p(value, class_name=f"text-2xl font-black {color} tracking-tight"),
        rx.cond(
            subtext,
            rx.el.p(subtext, class_name="text-slate-600 text-xs font-medium mt-1"),
        ),
        class_name="bg-slate-900/50 rounded-xl p-4 border border-slate-800/50 flex flex-col items-start justify-center",
    )


def badge_item(badge: Badge) -> rx.Component:
    return rx.el.div(
        rx.icon(badge["icon"], class_name=f"w-5 h-5 {badge['color']} mb-1"),
        rx.el.p(
            badge["name"],
            class_name="text-[10px] font-bold text-slate-300 text-center leading-tight",
        ),
        rx.el.div(
            badge["description"],
            class_name="absolute -top-8 left-1/2 -translate-x-1/2 bg-slate-800 text-slate-200 text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none border border-slate-700 shadow-lg z-50",
        ),
        class_name="group relative flex flex-col items-center justify-center p-2 bg-slate-800/40 rounded-lg border border-slate-700/50 hover:bg-slate-800/60 transition-colors cursor-help",
    )


def progress_bar() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                "PROGRESS",
                class_name="text-slate-500 text-xs font-bold uppercase tracking-wider",
            ),
            rx.el.div(
                rx.el.span(
                    rx.el.span(
                        GameState.max_unlocked_idx + 1, class_name="text-[#556B2F]"
                    ),
                    f" / {GameState.total_levels}",
                    class_name="text-slate-600",
                ),
                class_name="text-xs font-bold",
            ),
            class_name="flex justify-between items-center mb-2",
        ),
        rx.el.div(
            rx.el.div(
                class_name="h-full bg-gradient-to-r from-[#556B2F] to-[#6B8E23] rounded-full transition-all duration-500",
                style={"width": f"{GameState.progress_percent}%"},
            ),
            class_name="h-2 w-full bg-slate-800 rounded-full overflow-hidden",
        ),
        class_name="w-full mb-6",
    )


def stats_sidebar() -> rx.Component:
    return rx.el.div(
        progress_bar(),
        rx.el.div(
            stat_card("Rank", GameState.current_rank, color="text-[#556B2F]"),
            stat_card(
                "Total Score", GameState.score.to_string(), color="text-amber-400"
            ),
            class_name="grid grid-cols-2 gap-3 w-full mb-3",
        ),
        rx.el.div(
            stat_card("Attempts", GameState.total_attempts_count.to_string()),
            stat_card(
                "Success Rate",
                f"{GameState.formatted_success_rate}%",
                color=rx.cond(
                    GameState.success_rate >= 50, "text-emerald-400", "text-slate-200"
                ),
            ),
            stat_card(
                "Avg Error",
                f"{GameState.formatted_avg_error}%",
                color=rx.cond(
                    GameState.avg_error <= 10, "text-emerald-400", "text-rose-400"
                ),
            ),
            stat_card(
                "Best Streak",
                GameState.best_streak.to_string(),
                subtext=f"Current: {GameState.current_streak} (x{GameState.combo_multiplier})",
                color="text-amber-400",
            ),
            class_name="grid grid-cols-2 gap-3 w-full mb-6",
        ),
        rx.cond(
            GameState.badges_list.length() > 0,
            rx.el.div(
                rx.el.h3(
                    "Badges",
                    class_name="text-slate-500 text-xs font-bold uppercase tracking-wider mb-2",
                ),
                rx.el.div(
                    rx.foreach(GameState.badges_list, badge_item),
                    class_name="grid grid-cols-4 gap-2",
                ),
                class_name="w-full mb-6",
            ),
        ),
        rx.el.div(
            rx.el.h3(
                "Difficulty",
                class_name="text-slate-500 text-xs font-bold uppercase tracking-wider mb-2",
            ),
            rx.el.div(
                rx.el.span(
                    GameState.difficulty,
                    class_name=f"px-4 py-1.5 rounded-full text-sm font-bold {GameState.difficulty_badge_classes} transition-colors duration-300",
                ),
                rx.el.span(
                    f"Target: {GameState.formatted_target}",
                    class_name="text-slate-400 text-sm ml-auto font-mono",
                ),
                class_name="flex items-center bg-slate-900/50 rounded-xl p-4 border border-slate-800/50",
            ),
            class_name="w-full mb-6",
        ),
        history_list(),
        class_name="w-full flex flex-col",
    )