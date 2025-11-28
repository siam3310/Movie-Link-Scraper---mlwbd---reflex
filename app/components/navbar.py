import reflex as rx
from app.states.movie_state import MovieState


def navbar() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                rx.el.span("MLWBD", class_name="font-bold text-2xl tracking-tight"),
                rx.el.span("Scraper", class_name="ml-2 text-red-200 font-medium"),
                class_name="flex items-center text-white",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "search",
                        class_name="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 w-5 h-5",
                    ),
                    rx.el.input(
                        placeholder="Search movies...",
                        on_change=MovieState.set_search_query,
                        on_key_down=MovieState.handle_key_down,
                        class_name="w-full pl-10 pr-4 py-2 bg-white rounded-full text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-white/50 font-['JetBrains_Mono'] text-sm shadow-sm transition-all",
                        default_value=MovieState.search_query,
                    ),
                    class_name="relative w-full max-w-md",
                ),
                rx.el.button(
                    "Search",
                    on_click=MovieState.handle_search,
                    class_name="ml-4 px-6 py-2 bg-white text-red-600 font-medium rounded-full shadow-sm hover:shadow-md hover:bg-red-50 transition-all text-sm uppercase tracking-wide",
                ),
                class_name="flex-1 flex justify-center items-center mx-4",
            ),
            rx.el.div(class_name="w-[140px] hidden md:block"),
            class_name="container mx-auto px-4 h-16 flex items-center justify-between",
        ),
        class_name="bg-red-600 shadow-md sticky top-0 z-50",
    )