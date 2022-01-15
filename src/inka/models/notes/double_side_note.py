from typing import Iterable, Any, Callable, Dict, List

from rich.table import Table, Column

from .note import Note
from ..config import Config


class DoubleSideNote(Note):
    """Double side with common part note type"""

    def __init__(
        self,
        side1_md: str,
        side2_md: str,
        common_md: str,
        tags: Iterable[str],
        deck_name: str,
        anki_id: int = None,
    ):
        super().__init__(tags, deck_name, anki_id)
        self.raw_side1_md = side1_md
        self.raw_side2_md = side2_md
        self.raw_common_md = common_md
        self.updated_side1_md = side1_md  # With updated image links
        self.updated_side2_md = side2_md  # With updated image links
        self.updated_common_md = common_md  # With updated image links
        self.side1_html = ""
        self.side2_html = ""
        self.common_html = ""

    @property
    def search_query(self) -> str:
        """Query to search for note in Anki"""
        return self.create_anki_search_query(self.side1_html)

    def convert_fields_to_html(self, convert_func: Callable[[str], str]) -> None:
        """Convert note fields from markdown to html using provided function"""
        # self.front_html = convert_func(self.updated_front_md)
        # self.back_html = convert_func(self.updated_back_md)
        self.side1_html = convert_func(self.updated_side1_md)
        self.side2_html = convert_func(self.updated_side2_md)
        self.common_html = convert_func(self.updated_common_md)

    def update_fields_with(self, update_func: Callable[[str], str]) -> None:
        """Updates values of *updated* fields using provided function"""
        # self.updated_front_md = update_func(self.updated_front_md)
        # self.updated_back_md = update_func(self.updated_back_md)
        self.updated_side1_md = update_func(self.updated_side1_md)
        self.updated_side2_md = update_func(self.updated_side2_md)
        self.updated_common_md = update_func(self.updated_common_md)

    def get_raw_fields(self) -> List[str]:
        """Get list of all raw (as in file) fields of this note"""
        return [self.raw_side1_md, self.raw_side2_md, self.raw_common_md]

    def get_raw_question_field(self) -> str:
        """Get value of raw (as in file) question field"""
        return self.raw_side1_md

    def get_html_fields(self, cfg: Config) -> Dict[str, str]:
        """Return dictionary with Anki field names as keys and html strings as values"""
        return {
            cfg.get_option_value("anki", "side1_field"): self.side1_html,
            cfg.get_option_value("anki", "side2_field"): self.side2_html,
            cfg.get_option_value("anki", "common_field"): self.common_html,
        }

    @staticmethod
    def get_anki_note_type(cfg: Config) -> str:
        """Get name of Anki note type"""
        return cfg.get_option_value("anki", "double_side_type")

    def __eq__(self, other: Any) -> bool:
        if not super().__eq__(other):
            return False

        return (
            self.raw_side1_md == other.raw_side1_md
            and self.raw_side2_md == other.raw_side2_md
            and self.raw_common_md == other.raw_common_md
        )

    def __rich__(self) -> Table:
        """Table that is used to display info about note in case of error"""
        table = Table(
            Column("Field", justify="left", style="magenta"),
            Column("Value", justify="left", style="green"),
            title="Double Side Note",
        )
        table.add_row("Side1", self.raw_side1_md, end_section=True)
        table.add_row("Side2", self.raw_side2_md, end_section=True)
        table.add_row("Common", self.raw_common_md, end_section=True)
        table.add_row("Tags", ", ".join(self.tags), end_section=True)
        table.add_row("Deck", self.deck_name, end_section=True)

        return table

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(side1_md={self.raw_side1_md!r}, side2_md={self.raw_side2_md!r}, "
            f"common_md={self.raw_common_md!r}, "
            f"tags={self.tags!r}, deck_name={self.deck_name!r}, anki_id={self.anki_id!r})"
        )
