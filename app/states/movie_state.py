import reflex as rx
from typing import TypedDict
import asyncio
import logging
from app.services import scraper


class LinkItem(TypedDict):
    label: str
    url: str
    subtext: str
    direct_url: str
    resolving: bool


class LinkGroup(TypedDict):
    group: str
    items: list[LinkItem]


class Movie(TypedDict):
    title: str
    image: str
    link: str
    expanded: bool
    loading_links: bool
    links: list[LinkGroup]


class MovieState(rx.State):
    search_query: str = ""
    movies: list[Movie] = []
    is_loading: bool = False
    error_message: str = ""
    manual_url: str = ""

    @rx.event
    def on_load(self):
        """Load latest movies on startup."""
        return MovieState.fetch_latest_movies

    @rx.event
    async def fetch_latest_movies(self):
        self.is_loading = True
        self.error_message = ""
        yield
        try:
            results = await asyncio.to_thread(scraper.get_latest_movies)
            self.movies = [
                {**m, "expanded": False, "loading_links": False, "links": []}
                for m in results
            ]
        except Exception as e:
            logging.exception(f"Error fetching latest movies: {e}")
            self.error_message = "Could not load latest movies."
        finally:
            self.is_loading = False

    @rx.event
    async def handle_search(self):
        if not self.search_query:
            yield MovieState.fetch_latest_movies
            return
        self.is_loading = True
        self.error_message = ""
        self.movies = []
        yield
        try:
            results = await asyncio.to_thread(scraper.search_movie, self.search_query)
            self.movies = [
                {**m, "expanded": False, "loading_links": False, "links": []}
                for m in results
            ]
            if not results:
                self.error_message = "No movies found. Try a different search term."
        except Exception as e:
            logging.exception(f"Error searching movies: {e}")
            self.error_message = f"An error occurred while searching: {str(e)}"
        finally:
            self.is_loading = False

    @rx.event
    def set_search_query(self, value: str):
        self.search_query = value

    @rx.event
    def handle_key_down(self, key: str):
        if key == "Enter":
            return MovieState.handle_search

    @rx.var
    def displayed_movies(self) -> list[Movie]:
        """Return only the expanded movie if one exists, otherwise all movies."""
        for m in self.movies:
            if m["expanded"]:
                return [m]
        return self.movies

    @rx.event
    def toggle_movie_expand(self, movie_link: str):
        """Toggle expanded state for a movie and fetch links if needed."""
        target_movie = None
        for m in self.movies:
            if m["link"] == movie_link:
                target_movie = m
                break
        if not target_movie:
            return
        should_expand = not target_movie["expanded"]
        new_movies = []
        for m in self.movies:
            m_copy = m.copy()
            if m["link"] == movie_link:
                m_copy["expanded"] = should_expand
            elif should_expand:
                m_copy["expanded"] = False
            new_movies.append(m_copy)
        self.movies = new_movies
        if (
            should_expand
            and (not target_movie["links"])
            and (not target_movie["loading_links"])
        ):
            return MovieState.fetch_links_for_movie(movie_link)

    async def _resolve_link(
        self, url: str, g_idx: int, i_idx: int
    ) -> tuple[int, int, str]:
        try:
            direct = await asyncio.to_thread(scraper.get_direct_link, url)
            return (g_idx, i_idx, direct)
        except Exception as e:
            logging.exception(f"Error resolving link {url}: {e}")
            return (g_idx, i_idx, "")

    @rx.event
    async def fetch_links_for_movie(self, movie_link: str):
        idx = -1
        for i, m in enumerate(self.movies):
            if m["link"] == movie_link:
                idx = i
                break
        if idx == -1:
            return
        self.movies[idx]["loading_links"] = True
        yield
        try:
            raw_links = await asyncio.to_thread(scraper.get_download_links, movie_link)
            normalized: list[LinkGroup] = []
            for item in raw_links:
                if "links" in item:
                    group_items = []
                    for sub in item["links"]:
                        group_items.append(
                            {
                                "label": sub.get("label") or sub.get("type", "Link"),
                                "url": sub.get("url") or sub.get("link", ""),
                                "subtext": sub.get("type", ""),
                                "direct_url": "",
                                "resolving": True,
                            }
                        )
                    normalized.append(
                        {"group": item.get("title", "Links"), "items": group_items}
                    )
                else:
                    normalized.append(
                        {
                            "group": item.get("quality", "Download"),
                            "items": [
                                {
                                    "label": item.get("type", "Link"),
                                    "url": item.get("link") or item.get("url", ""),
                                    "subtext": "",
                                    "direct_url": "",
                                    "resolving": True,
                                }
                            ],
                        }
                    )
            current_idx = -1
            for i, m in enumerate(self.movies):
                if m["link"] == movie_link:
                    current_idx = i
                    break
            if current_idx != -1:
                self.movies[current_idx]["links"] = normalized
                self.movies[current_idx]["loading_links"] = False
            yield
            tasks = []
            for g_idx, group in enumerate(normalized):
                for i_idx, item in enumerate(group["items"]):
                    tasks.append(self._resolve_link(item["url"], g_idx, i_idx))
            if not tasks:
                return
            for coro in asyncio.as_completed(tasks):
                g_idx, i_idx, direct_url = await coro
                m_idx = -1
                for k, m in enumerate(self.movies):
                    if m["link"] == movie_link:
                        m_idx = k
                        break
                if m_idx != -1:
                    self.movies[m_idx]["links"][g_idx]["items"][i_idx]["resolving"] = (
                        False
                    )
                    if direct_url:
                        self.movies[m_idx]["links"][g_idx]["items"][i_idx][
                            "direct_url"
                        ] = direct_url
                    yield
        except Exception as e:
            logging.exception(f"Error fetching links for {movie_link}: {e}")
            yield rx.toast.error(f"Failed to fetch links: {e}")
            idx_err = -1
            for i, m in enumerate(self.movies):
                if m["link"] == movie_link:
                    idx_err = i
                    break
            if idx_err != -1:
                self.movies[idx_err]["loading_links"] = False

    @rx.event
    async def generate_direct_link(self, url: str):
        yield rx.toast.info("Generating direct link... This may take a few seconds.")
        try:
            direct_link = await asyncio.to_thread(scraper.get_direct_link, url)
            if direct_link and direct_link.startswith("http"):
                yield rx.set_clipboard(direct_link)
                yield rx.toast.success("Direct link copied to clipboard!")
            else:
                yield rx.toast.error("Could not generate direct link.")
        except Exception as e:
            logging.exception(f"Error generating direct link: {e}")
            yield rx.toast.error(f"Error: {e}")

    @rx.event
    def copy_text(self, text: str):
        yield rx.set_clipboard(text)
        yield rx.toast.success("Copied to clipboard!")

    @rx.event
    def set_manual_url(self, val: str):
        self.manual_url = val

    @rx.event
    def handle_manual_fetch(self):
        if not self.manual_url:
            return rx.toast.warning("Please enter a valid URL")
        updated_movies = []
        for m in self.movies:
            m_copy = m.copy()
            m_copy["expanded"] = False
            updated_movies.append(m_copy)
        manual_movie: Movie = {
            "title": "Manual Fetch Result",
            "image": "/placeholder.svg",
            "link": self.manual_url,
            "expanded": True,
            "loading_links": True,
            "links": [],
        }
        updated_movies.insert(0, manual_movie)
        self.movies = updated_movies
        return MovieState.fetch_links_for_movie(self.manual_url)