from dataclasses import dataclass

PER_PAGE = 50


@dataclass
class Pagination:
    """Handles pagination within DOMO Api"""

    number_results: int = PER_PAGE  # max init
    offset: int = 0
    per_page: int = PER_PAGE
    should_stop: bool = False

    @property
    def needs_increment(self) -> bool:
        if (self.number_results < self.per_page) or self.should_stop:
            return False
        return True

    def increment_offset(self, number_results: int) -> None:
        self.offset += self.per_page
        self.number_results = number_results
