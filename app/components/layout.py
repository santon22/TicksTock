import reflex as rx


def layout(content: rx.Component) -> rx.Component:
    """Main layout wrapper with dark theme and gradients."""
    return rx.el.div(
        rx.el.div(
            content,
            class_name="container mx-auto px-4 py-16 min-h-screen flex flex-col items-center relative z-10",
        ),
        rx.el.div(class_name="fixed inset-0 bg-slate-950 z-0"),
        rx.el.div(
            class_name="fixed top-0 left-0 w-full h-full bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-slate-900 via-slate-950 to-black z-0 opacity-80"
        ),
        rx.el.div(
            class_name="fixed top-1/4 left-1/4 w-96 h-96 bg-indigo-900/20 rounded-full blur-3xl z-0 animate-pulse"
        ),
        rx.el.div(
            class_name="fixed bottom-1/4 right-1/4 w-96 h-96 bg-violet-900/10 rounded-full blur-3xl z-0 animate-pulse delay-1000"
        ),
        class_name="font-sans antialiased text-slate-100 min-h-screen w-full overflow-hidden relative selection:bg-indigo-500/30",
    )