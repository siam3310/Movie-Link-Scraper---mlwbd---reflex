import reflex as rx
from app.states.movie_state import Movie, MovieState, LinkGroup, LinkItem


def action_button(
    icon: str, text: str, on_click: rx.event.EventType, disabled: bool = False
) -> rx.Component:
    return rx.el.button(
        rx.icon(icon, size=14, class_name="mr-1.5"),
        rx.el.span(text),
        on_click=on_click,
        disabled=disabled,
        class_name=rx.cond(
            disabled,
            "flex items-center px-3 py-1.5 text-xs font-medium rounded-md border border-gray-200 bg-gray-50 text-gray-400 cursor-not-allowed shadow-none",
            "flex items-center px-3 py-1.5 text-xs font-medium rounded-md border border-gray-200 bg-white text-gray-700 hover:bg-gray-50 hover:border-gray-300 transition-colors shadow-sm",
        ),
    )


def link_item_row(item: LinkItem) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                item["label"],
                class_name="text-sm font-medium text-gray-800 mr-2 break-all",
            ),
            rx.cond(
                item["subtext"],
                rx.el.span(
                    item["subtext"],
                    class_name="text-[10px] text-gray-500 px-1.5 py-0.5 bg-gray-100 rounded uppercase tracking-wider",
                ),
            ),
            class_name="flex items-center flex-wrap mb-2 sm:mb-0",
        ),
        rx.el.div(
            rx.cond(
                item["resolving"],
                rx.el.div(
                    rx.spinner(size="1", color="red"),
                    rx.el.span("Resolving...", class_name="ml-2 text-xs text-gray-500"),
                    class_name="flex items-center px-3 py-1.5 bg-gray-50 rounded-md border border-gray-100",
                ),
                rx.cond(
                    item["direct_url"],
                    rx.el.button(
                        rx.icon("copy", size=16, class_name="mr-2"),
                        rx.el.span("Copy Direct Link"),
                        on_click=MovieState.copy_text(item["direct_url"]),
                        class_name="flex items-center px-4 py-2 text-xs font-bold rounded-md border border-transparent bg-green-600 text-white hover:bg-green-700 transition-all shadow-sm hover:shadow focus:ring-2 focus:ring-green-500 focus:ring-offset-1",
                    ),
                    action_button(
                        "link", "Copy Link", MovieState.copy_text(item["url"])
                    ),
                ),
            ),
            class_name="flex items-center",
        ),
        class_name="flex flex-col sm:flex-row sm:items-center justify-between p-2 bg-gray-50/80 rounded-md hover:bg-gray-100 border border-transparent hover:border-gray-200 transition-all",
    )


def link_group(group: LinkGroup) -> rx.Component:
    return rx.el.div(
        rx.el.h4(
            group["group"],
            class_name="text-xs font-bold text-red-600 uppercase tracking-wider mb-2 flex items-center pt-2 border-t border-gray-100 mt-2 first:mt-0 first:border-t-0 first:pt-0",
        ),
        rx.el.div(rx.foreach(group["items"], link_item_row), class_name="space-y-2"),
        class_name="mb-4 last:mb-0",
    )


def movie_card(movie: Movie) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.image(
                src=movie["image"],
                alt=movie["title"],
                class_name="w-full h-[300px] object-cover transition-transform duration-500 group-hover:scale-105",
                loading="lazy",
            ),
            rx.cond(
                movie["expanded"],
                rx.el.div(
                    rx.icon(
                        "chevron-up", size=24, class_name="text-white drop-shadow-md"
                    ),
                    class_name="absolute bottom-0 left-0 right-0 p-2 bg-gradient-to-t from-black/60 to-transparent flex justify-center items-end h-20 opacity-100 transition-opacity",
                ),
                rx.el.div(
                    rx.icon(
                        "chevron-down", size=24, class_name="text-white drop-shadow-md"
                    ),
                    class_name="absolute bottom-0 left-0 right-0 p-2 bg-gradient-to-t from-black/60 to-transparent flex justify-center items-end h-20 opacity-0 group-hover:opacity-100 transition-opacity",
                ),
            ),
            class_name="overflow-hidden relative bg-gray-200 cursor-pointer",
            on_click=lambda: MovieState.toggle_movie_expand(movie["link"]),
        ),
        rx.el.div(
            rx.el.h3(
                movie["title"],
                class_name="text-base font-medium text-gray-900 line-clamp-2 leading-tight",
            ),
            class_name="p-4 bg-white border-b border-gray-50 cursor-pointer",
            on_click=lambda: MovieState.toggle_movie_expand(movie["link"]),
        ),
        rx.cond(
            movie["expanded"],
            rx.el.div(
                rx.cond(
                    movie["loading_links"],
                    rx.el.div(
                        rx.spinner(size="2", color="red"),
                        rx.el.p(
                            "Fetching links...",
                            class_name="text-xs text-gray-500 mt-2 animate-pulse",
                        ),
                        class_name="flex flex-col items-center justify-center py-8 bg-gray-50/30",
                    ),
                    rx.cond(
                        movie["links"].length() > 0,
                        rx.el.div(
                            rx.foreach(movie["links"], link_group),
                            class_name="p-4 bg-white space-y-1 max-h-[400px] overflow-y-auto custom-scrollbar border-t border-gray-100",
                        ),
                        rx.el.div(
                            rx.icon("file-x", size=24, class_name="text-gray-300 mb-2"),
                            rx.el.p(
                                "No links found", class_name="text-xs text-gray-400"
                            ),
                            class_name="flex flex-col items-center justify-center py-8 bg-gray-50/50",
                        ),
                    ),
                ),
                class_name="animate-in slide-in-from-top-2 duration-200",
            ),
        ),
        class_name="group flex flex-col rounded-lg overflow-hidden bg-white shadow-sm hover:shadow-md transition-all duration-300 border border-gray-200",
    )