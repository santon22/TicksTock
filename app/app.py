import reflex as rx
from app.components.layout import layout
from app.components.timer_display import timer_display
from app.components.controls import controls
from app.components.stats_sidebar import stats_sidebar
from app.states.game_state import GameState


def feature_card(icon: str, title: str, description: str) -> rx.Component:
    return rx.el.div(
        rx.icon(icon, class_name="w-8 h-8 text-[#556B2F] mb-4"),
        rx.el.h3(title, class_name="text-lg font-bold text-white mb-2"),
        rx.el.p(description, class_name="text-slate-400 text-sm"),
        class_name="bg-slate-900/50 p-6 rounded-2xl border border-slate-800/50 flex flex-col items-center text-center group hover:border-[#556B2F]/30 transition-all duration-300",
    )


def social_link(
    href: str, icon_src: str, label: str, custom_style: str = ""
) -> rx.Component:
    return rx.el.a(
        rx.el.div(
            rx.image(src=icon_src, class_name=f"w-12 h-12 {custom_style}"),
            class_name="transition-transform hover:scale-110 duration-200",
        ),
        rx.el.span(label, class_name="mt-2 text-slate-400 text-xs font-medium"),
        href=href,
        target="_blank",
        class_name="flex flex-col items-center group",
    )


def discord_link() -> rx.Component:
    return rx.el.a(
        rx.el.div(
            rx.el.div(
                "Discord",
                class_name="w-[69px] h-[48px] bg-[#5865F2] text-white flex items-center justify-center rounded-[60%] font-bold text-[13px] shadow-lg",
            ),
            class_name="transition-transform hover:scale-110 duration-200",
        ),
        rx.el.span("Discord", class_name="mt-2 text-slate-400 text-xs font-medium"),
        href="https://discord.gg/C6qYRV4fnW",
        target="_blank",
        class_name="flex flex-col items-center group",
    )


def index() -> rx.Component:
    return layout(
        rx.el.div(
            rx.el.nav(
                rx.el.a(
                    rx.image(src="/HypnoTicks.png", class_name="h-36 w-auto"), href="/"
                ),
                class_name="w-full flex justify-center items-center mb-12",
            ),
            rx.el.section(
                rx.el.div(
                    rx.image(
                        src="/EEGHAT.png",
                        class_name="h-72 w-auto hidden lg:block opacity-50 hover:opacity-100 transition-opacity duration-500",
                    ),
                    rx.el.div(
                        rx.el.h1(
                            "HypnoTicks",
                            class_name="text-5xl sm:text-6xl md:text-8xl font-black text-[#556B2F] mb-8 tracking-tighter",
                        ),
                        rx.el.p(
                            "Real-time EEG analysis for emotion-driven trading decisions. Become the Indicator!",
                            class_name="text-base sm:text-lg md:text-xl text-slate-400 font-medium max-w-2xl px-4 sm:px-0 mb-8",
                        ),
                        rx.el.div(
                            "COMING SOON",
                            class_name="text-2xl sm:text-4xl md:text-5xl font-black text-emerald-400 mb-8 animate-pulse tracking-widest",
                            style={"text-shadow": "0 0 20px rgba(52, 211, 153, 0.5)"},
                        ),
                        class_name="flex flex-col items-center text-center px-4 flex-1",
                    ),
                    rx.image(
                        src="/EEGHAT.png",
                        class_name="h-72 w-auto hidden lg:block opacity-50 hover:opacity-100 transition-opacity duration-500 scale-x-[-1]",
                    ),
                    class_name="w-full flex justify-between items-center px-8 mb-24",
                ),
                rx.el.div(
                    rx.image(
                        src="/EEGHAT.png",
                        class_name="h-64 w-auto block lg:hidden opacity-80 mb-12",
                    ),
                    class_name="w-full flex justify-center",
                ),
                rx.el.div(
                    rx.el.h2(
                        "The Future of Trading Mastery",
                        class_name="text-sm font-black text-[#556B2F] tracking-[0.3em] uppercase mb-8",
                    ),
                    rx.el.div(
                        feature_card(
                            "brain-circuit",
                            "😱 Emotional Profiles 🤑",
                            "Monitor and Track 14 emotions like Fear & Greed in real-time.",
                        ),
                        feature_card(
                            "eye",
                            "🌀 Hypnosis Tracking 👁️",
                            "Track hypnosis factors and time distortions.",
                        ),
                        feature_card(
                            "brain",
                            "❓ Memory 🧠",
                            "Remembers your success and mistakes.",
                        ),
                        feature_card(
                            "square_check",
                            "😤 Decisions ✅",
                            "Overrides bad trade decisions based on brain state quality.",
                        ),
                        class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 w-full max-w-6xl",
                    ),
                    class_name="w-full flex flex-col items-center mb-24",
                ),
                class_name="w-full flex flex-col items-center",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Train While You Wait",
                        class_name="text-3xl font-black text-white mb-2 tracking-tight",
                    ),
                    rx.el.p(
                        "Sharpen your internal clock with our core calibration module.",
                        class_name="text-slate-500 font-medium mb-12",
                    ),
                    class_name="text-center",
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
                class_name="w-full flex flex-col items-center bg-slate-900/20 p-8 rounded-3xl border border-slate-800/30 mb-24",
            ),
            rx.el.footer(
                rx.el.div(
                    rx.el.h3(
                        "How to Play",
                        class_name="text-[#556B2F] font-bold uppercase tracking-wider text-sm mb-6 text-center",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.span(
                                "1",
                                class_name="w-8 h-8 rounded-full bg-slate-800 text-slate-300 text-sm flex items-center justify-center font-bold mr-4 border border-slate-700 shrink-0",
                            ),
                            rx.el.p(
                                "Target: Stop the timer as close as possible to the target.",
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
                                "Focus: Breathe slowly and feel time pass internally.",
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
                                "Success: Levels 1-3 pass; Level 4+ requires ±10% accuracy.",
                                class_name="text-slate-400 text-sm font-medium",
                            ),
                            class_name="flex items-center",
                        ),
                        class_name="flex flex-col items-start max-w-md mx-auto bg-slate-900/30 p-6 rounded-2xl border border-slate-800/30 mb-16",
                    ),
                    class_name="w-full",
                ),
                rx.el.div(
                    rx.image(src="/HypnoTicks.png", class_name="h-16 w-auto mb-8"),
                    rx.el.p(
                        "Join the community & stay connected",
                        class_name="text-slate-400 text-lg mb-8 font-medium",
                    ),
                    rx.el.div(
                        social_link(
                            "https://youtube.com/@HypnoTicks",
                            "https://upload.wikimedia.org/wikipedia/commons/0/09/YouTube_full-color_icon_%282017%29.svg",
                            "Youtube",
                        ),
                        social_link(
                            "https://x.com/@Hypno_Ticks",
                            "https://upload.wikimedia.org/wikipedia/commons/5/57/X_logo_2023_%28white%29.png",
                            "X",
                            "invert brightness-0",
                        ),
                        social_link(
                            "https://www.linkedin.com/in/rusticktrading/",
                            "https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png",
                            "LinkedIn",
                        ),
                        discord_link(),
                        social_link(
                            "mailto:support@hypnoticks.com",
                            "https://upload.wikimedia.org/wikipedia/commons/7/7e/Gmail_icon_%282020%29.svg",
                            "Email",
                        ),
                        class_name="flex flex-wrap justify-center items-center gap-12 mb-16",
                    ),
                    rx.el.p(
                        "© 2025 Rusticktrading/HypnoTicks • Mastering the mind for better trading",
                        class_name="text-slate-600 text-sm font-medium",
                    ),
                    class_name="w-full flex flex-col items-center pt-16 border-t border-slate-800/50",
                ),
                class_name="w-full",
            ),
            class_name="flex flex-col items-center max-w-6xl mx-auto w-full",
        )
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="icon", href="/eeg_icon.ico.ico"),
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
app.add_page(index, route="/", title="HypnoTicks")