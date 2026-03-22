import reflex as rx
from app.states.game_state import GameState, Badge
from app.components.history_list import history_list


def stat_card(
    label: str,
    value: rx.Var | str,
    subtext: rx.Var | str | None = None,
    color: rx.Var | str = "text-white",
) -> rx.Component:
    return rx.el.div(
        rx.el.p(
            label,
            class_name="text-slate-500 text-xs font-bold uppercase tracking-wider mb-1",
        ),
        rx.el.p(
            value,
            class_name=rx.match(
                color,
                ("text-[#556B2F]", "text-2xl font-black text-[#556B2F] tracking-tight"),
                ("text-amber-400", "text-2xl font-black text-amber-400 tracking-tight"),
                (
                    "text-emerald-400",
                    "text-2xl font-black text-emerald-400 tracking-tight",
                ),
                ("text-rose-400", "text-2xl font-black text-rose-400 tracking-tight"),
                ("text-slate-200", "text-2xl font-black text-slate-200 tracking-tight"),
                "text-2xl font-black text-white tracking-tight",
            ),
        ),
        rx.cond(
            subtext,
            rx.el.p(subtext, class_name="text-slate-600 text-xs font-medium mt-1"),
        ),
        class_name="bg-slate-900/50 rounded-xl p-4 border border-slate-800/50 flex flex-col items-start justify-center",
    )


def badge_item(badge: Badge) -> rx.Component:
    return rx.el.div(
        rx.icon(
            badge["icon"],
            class_name=rx.match(
                badge["color"],
                ("text-emerald-400", "w-5 h-5 text-emerald-400 mb-1"),
                ("text-blue-400", "w-5 h-5 text-blue-400 mb-1"),
                ("text-indigo-400", "w-5 h-5 text-indigo-400 mb-1"),
                ("text-amber-400", "w-5 h-5 text-amber-400 mb-1"),
                "w-5 h-5 text-slate-400 mb-1",
            ),
        ),
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
                        (GameState.max_unlocked_idx + 1).to(str),
                        class_name="text-[#556B2F]",
                    ),
                    " / ",
                    GameState.total_levels.to(str),
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
                GameState.formatted_success_rate + "%",
                color=rx.cond(
                    GameState.success_rate >= 50, "text-emerald-400", "text-slate-200"
                ),
            ),
            stat_card(
                "Avg Error",
                GameState.formatted_avg_error + "%",
                color=rx.cond(
                    GameState.avg_error <= 10, "text-emerald-400", "text-rose-400"
                ),
            ),
            stat_card(
                "Best Streak",
                GameState.best_streak.to_string(),
                subtext="Current: "
                + GameState.current_streak.to(str)
                + " (x"
                + GameState.combo_multiplier.to(str)
                + ")",
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
                    class_name=rx.match(
                        GameState.difficulty,
                        (
                            "Easy",
                            "px-4 py-1.5 rounded-full text-sm font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 shadow-[0_0_15px_-3px_rgba(52,211,153,0.3)] transition-colors duration-300",
                        ),
                        (
                            "Medium",
                            "px-4 py-1.5 rounded-full text-sm font-bold bg-blue-500/10 text-blue-400 border border-blue-500/20 shadow-[0_0_15px_-3px_rgba(96,165,250,0.3)] transition-colors duration-300",
                        ),
                        (
                            "Hard",
                            "px-4 py-1.5 rounded-full text-sm font-bold bg-amber-500/10 text-amber-400 border border-amber-500/20 shadow-[0_0_15px_-3px_rgba(251,191,36,0.3)] transition-colors duration-300",
                        ),
                        (
                            "Expert",
                            "px-4 py-1.5 rounded-full text-sm font-bold bg-rose-500/10 text-rose-400 border border-rose-500/20 shadow-[0_0_15px_-3px_rgba(251,113,133,0.3)] transition-colors duration-300",
                        ),
                        "px-4 py-1.5 rounded-full text-sm font-bold bg-slate-800 text-slate-400 transition-colors duration-300",
                    ),
                ),
                rx.el.span(
                    rx.el.span("Target: "),
                    rx.el.span(GameState.formatted_target),
                    class_name="text-slate-400 text-sm ml-auto font-mono",
                ),
                class_name="flex items-center bg-slate-900/50 rounded-xl p-4 border border-slate-800/50",
            ),
            class_name="w-full mb-6",
        ),
        history_list(),
        class_name="w-full flex flex-col",
    )