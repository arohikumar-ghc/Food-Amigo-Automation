"""
Configuration settings for Food Amigo automation.
"""
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv


@dataclass
class AutomationConfig:
    """Configuration for automation system."""

    email: str
    password: str
    restaurant_name: str

    base_url: str = "https://restaurant.foodamigos.io"

    # Google Drive sync folder (change this to your actual Google Drive path)
    seo_files_dir: str = r"C:\Users\Arohi\Google Drive\My Drive\SEO Pages"
    logs_dir: str = "logs"

    headless: bool = False
    timeout: int = 30000

    slow_mo: int = 100

    screenshot_on_error: bool = True

    @classmethod
    def from_env(cls) -> "AutomationConfig":
        """
        Load configuration from environment variables.

        Environment variables:
            FOODAMIGO_EMAIL: Login email
            FOODAMIGO_PASSWORD: Login password
            FOODAMIGO_RESTAURANT: Restaurant name
            FOODAMIGO_HEADLESS: Run browser in headless mode (default: false)
            FOODAMIGO_TIMEOUT: Timeout in milliseconds (default: 30000)

        Returns:
            AutomationConfig instance

        Raises:
            ValueError: If required environment variables are missing
        """
        # Load .env file from current directory
        load_dotenv()

        email = os.getenv("FOODAMIGO_EMAIL")
        password = os.getenv("FOODAMIGO_PASSWORD")
        restaurant_name = os.getenv("FOODAMIGO_RESTAURANT")

        if not email:
            raise ValueError("FOODAMIGO_EMAIL environment variable is required")
        if not password:
            raise ValueError("FOODAMIGO_PASSWORD environment variable is required")
        if not restaurant_name:
            raise ValueError("FOODAMIGO_RESTAURANT environment variable is required")

        headless = os.getenv("FOODAMIGO_HEADLESS", "false").lower() == "true"
        timeout = int(os.getenv("FOODAMIGO_TIMEOUT", "30000"))

        # Google Drive sync folder (optional)
        seo_files_dir = os.getenv("FOODAMIGO_SEO_DIR", "seo_files")

        return cls(
            email=email,
            password=password,
            restaurant_name=restaurant_name,
            seo_files_dir=seo_files_dir,
            headless=headless,
            timeout=timeout
        )

    def validate(self) -> list[str]:
        """
        Validate configuration.

        Returns:
            List of validation errors (empty if valid)
        """
        errors = []

        if not self.email or not self.email.strip():
            errors.append("Email is required")

        if not self.password or not self.password.strip():
            errors.append("Password is required")

        if not self.restaurant_name or not self.restaurant_name.strip():
            errors.append("Restaurant name is required")

        if self.timeout < 1000:
            errors.append("Timeout must be at least 1000ms")

        seo_dir = Path(self.seo_files_dir)
        if not seo_dir.exists():
            errors.append(f"SEO files directory does not exist: {self.seo_files_dir}")

        return errors

    def is_valid(self) -> bool:
        """Check if configuration is valid."""
        return len(self.validate()) == 0


def load_config_from_file(config_file: str = ".env") -> Optional[AutomationConfig]:
    """
    Load configuration from a .env file.

    Args:
        config_file: Path to .env file

    Returns:
        AutomationConfig if file exists, None otherwise
    """
    env_path = Path(config_file)

    if not env_path.exists():
        return None

    # Use python-dotenv to load the file
    load_dotenv(dotenv_path=env_path)

    return AutomationConfig.from_env()


if __name__ == "__main__":
    print("Example .env file:\n")
    print("FOODAMIGO_EMAIL=your-email@example.com")
    print("FOODAMIGO_PASSWORD=your-password")
    print("FOODAMIGO_RESTAURANT=Your Restaurant Name")
    print("FOODAMIGO_HEADLESS=false")
    print("FOODAMIGO_TIMEOUT=30000")
