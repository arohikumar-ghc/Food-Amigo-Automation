"""
Data models for SEO page content.
"""
from dataclasses import dataclass
from typing import List


@dataclass
class FAQ:
    """FAQ item with question and answer."""
    question: str
    answer: str


@dataclass
class SEOPageData:
    """Complete SEO page data extracted from Word document."""
    href: str
    page_name: str
    seo_title: str
    seo_description: str
    subtitle: str
    title: str
    description: str
    faqs: List[FAQ]

    def __post_init__(self):
        """Ensure href starts with '/' after initialization."""
        if self.href and not self.href.startswith('/'):
            self.href = '/' + self.href

    def validate(self) -> List[str]:
        """Validate required fields and return list of missing fields."""
        missing = []

        if not self.href:
            missing.append("href")
        elif not self.href.startswith('/'):
            missing.append("href (must start with '/')")

        if not self.page_name:
            missing.append("page_name")
        if not self.seo_title:
            missing.append("seo_title")
        if not self.seo_description:
            missing.append("seo_description")
        if not self.subtitle:
            missing.append("subtitle")
        if not self.title:
            missing.append("title")
        if not self.description:
            missing.append("description")
        if not self.faqs:
            missing.append("faqs (at least one FAQ required)")

        return missing

    def is_valid(self) -> bool:
        """Check if all required fields are present."""
        return len(self.validate()) == 0
