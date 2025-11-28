import reflex as rx
from app.states.movie_state import MovieState
from app.components.navbar import navbar
from app.components.movie_card import movie_card


def manual_fetch_section() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.input(
                placeholder="Or paste a movie/episode URL directly...",
                on_change=MovieState.set_manual_url,
                class_name="flex-1 bg-transparent border-none focus:ring-0 text-sm placeholder-gray-400 text-gray-700 font-['JetBrains_Mono']",
                default_value=MovieState.manual_url,
            ),
            rx.el.button(
                rx.icon("arrow-right", size=16),
                on_click=MovieState.handle_manual_fetch,
                class_name="p-2 bg-red-50 text-red-600 rounded-md hover:bg-red-100 transition-colors",
            ),
            class_name="flex items-center bg-white border border-gray-200 rounded-md px-4 py-2 shadow-sm max-w-2xl mx-auto",
        ),
        class_name="container mx-auto px-4 mt-6",
    )


def index() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            manual_fetch_section(),
            rx.el.div(
                rx.cond(
                    MovieState.is_loading,
                    rx.el.div(
                        rx.spinner(size="3", color="red"),
                        rx.el.p(
                            rx.cond(
                                MovieState.search_query,
                                "Searching movies...",
                                "Loading latest releases...",
                            ),
                            class_name="mt-4 text-gray-500 font-medium animate-pulse",
                        ),
                        class_name="flex flex-col items-center justify-center py-32",
                    ),
                    rx.cond(
                        MovieState.movies.length() > 0,
                        rx.el.div(
                            rx.el.h2(
                                rx.cond(
                                    MovieState.search_query,
                                    "Search Results",
                                    "Latest Movies",
                                ),
                                class_name="text-2xl font-normal text-gray-800 mb-6 border-l-4 border-red-600 pl-4",
                            ),
                            rx.el.div(
                                rx.foreach(MovieState.movies, movie_card),
                                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 items-start",
                            ),
                            class_name="w-full",
                        ),
                        rx.el.div(
                            rx.icon("film", size=64, class_name="text-gray-200 mb-4"),
                            rx.el.h3(
                                "No movies found",
                                class_name="text-xl font-medium text-gray-900",
                            ),
                            rx.el.p(
                                "Try searching for a movie title above.",
                                class_name="text-gray-500 mt-2",
                            ),
                            class_name="flex flex-col items-center justify-center py-32 text-center",
                        ),
                    ),
                ),
                class_name="container mx-auto px-4 py-8 min-h-[calc(100vh-64px)]",
            ),
            class_name="bg-gray-50 min-h-screen font-['Roboto']",
        ),
        class_name="min-h-screen bg-gray-50",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&family=Roboto:wght@300;400;500;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, route="/", on_load=MovieState.on_load)