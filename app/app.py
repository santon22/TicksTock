import reflex as rx
from app.components.layout import layout
from app.components.timer_display import timer_display
from app.components.controls import controls
from app.components.stats_sidebar import stats_sidebar
from app.states.game_state import GameState


def index() -> rx.Component:
    return layout(
        rx.el.div(
            rx.el.header(
                rx.icon("clock", class_name="w-10 h-10 text-indigo-500 mb-4"),
                rx.el.h1(
                    "TicksTock",
                    class_name="text-4xl sm:text-5xl font-black bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-violet-400 tracking-tight mb-2",
                ),
                rx.el.p(
                    "Master Your Inner Clock",
                    class_name="text-slate-400 font-medium tracking-wide",
                ),
                class_name="flex flex-col items-center mb-12",
            ),
            rx.el.main(
                rx.el.div(
                    timer_display(),
                    controls(),
                    class_name="w-full flex flex-col items-center col-span-1 lg:col-span-2 order-1",
                ),
                rx.el.div(
                    stats_sidebar(),
                    class_name="w-full col-span-1 order-2 mt-12 lg:mt-0",
                ),
                class_name="w-full grid grid-cols-1 lg:grid-cols-3 gap-8 lg:gap-16",
            ),
            rx.el.footer(
                rx.el.div(
                    rx.el.h3(
                        "How to Play",
                        class_name="text-indigo-400 font-bold uppercase tracking-wider text-sm mb-6 text-center",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.span(
                                "1",
                                class_name="w-8 h-8 rounded-full bg-slate-800 text-slate-300 text-sm flex items-center justify-center font-bold mr-4 border border-slate-700 shrink-0",
                            ),
                            rx.el.p(
                                "Internalize the target duration shown.",
                                class_name="text-slate-400 text-sm font-medium",
                            ),
                            class_name="flex items-center mb-4",
                        ),
                        rx.el.div(
                            rx.el.span(
                                "2",
                                class_name="w-8 h-8 rounded-full bg-slate-800 text-slate-300 text-sm flex items-center justify-center font-bold mr-4 border border-slate-700 shrink-0",
                            ),
                            rx.el.p(
                                "Click START. The timer is hidden!",
                                class_name="text-slate-400 text-sm font-medium",
                            ),
                            class_name="flex items-center mb-4",
                        ),
                        rx.el.div(
                            rx.el.span(
                                "3",
                                class_name="w-8 h-8 rounded-full bg-slate-800 text-slate-300 text-sm flex items-center justify-center font-bold mr-4 border border-slate-700 shrink-0",
                            ),
                            rx.el.p(
                                "Click STOP when you feel time is up.",
                                class_name="text-slate-400 text-sm font-medium",
                            ),
                            class_name="flex items-center",
                        ),
                        class_name="flex flex-col items-start max-w-md mx-auto bg-slate-900/30 p-6 rounded-2xl border border-slate-800/30",
                    ),
                    class_name="w-full flex flex-col items-center",
                ),
                rx.el.p(
                    "No counting allowed! Rely on your gut feeling.",
                    class_name="mt-8 text-slate-600 text-xs font-bold uppercase tracking-widest",
                ),
                class_name="mt-16 flex flex-col items-center border-t border-slate-800/50 pt-12 w-full",
            ),
            class_name="flex flex-col items-center max-w-6xl mx-auto w-full",
        )
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;900&family=JetBrains+Mono:wght@400;700&display=swap",
            rel="stylesheet",
        ),
        rx.el.script(
            src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"
        ),
        rx.el.script("""
            const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            function playTone(freq, type, duration, delay=0) {
                setTimeout(() => {
                    if (audioCtx.state === 'suspended') audioCtx.resume();
                    const osc = audioCtx.createOscillator();
                    const gain = audioCtx.createGain();
                    osc.type = type;
                    osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
                    gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
                    gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + duration);
                    osc.connect(gain);
                    gain.connect(audioCtx.destination);
                    osc.start();
                    osc.stop(audioCtx.currentTime + duration);
                }, delay * 1000);
            }
            function playSuccess() {
                playTone(440, 'sine', 0.1, 0);
                playTone(554, 'sine', 0.1, 0.1);
                playTone(659, 'sine', 0.2, 0.2);
                playTone(880, 'sine', 0.4, 0.3);
            }
            function playFailure() {
                playTone(300, 'sawtooth', 0.3, 0);
                playTone(200, 'sawtooth', 0.4, 0.2);
            }
            function playClick() {
                playTone(800, 'sine', 0.05, 0);
            }
            function playStart() {
                playTone(600, 'sine', 0.1, 0);
                playTone(1200, 'sine', 0.2, 0.1);
            }
            """),
    ],
)
app.add_page(index, route="/")