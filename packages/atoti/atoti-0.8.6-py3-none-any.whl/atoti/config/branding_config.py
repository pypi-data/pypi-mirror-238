from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union

from atoti_core import keyword_only_dataclass

from ._config import Config, convert_path_to_absolute_string


@keyword_only_dataclass
@dataclass(frozen=True)
class BrandingConfig(Config):
    """The UI elements to `customize the app <../../how_tos/customize_the_app.html>`__ by replacing the Atoti branding with another one (also called white-labeling).

    Note:
        This feature is not part of the community edition: it needs to be `unlocked <../../how_tos/unlock_all_features.html>`__.

    When defined, the :guilabel:`By ActiveViam` signature at the bottom right corner of the app will be removed.

    Example:
        >>> config = tt.BrandingConfig(
        ...     favicon="favicon.ico",
        ...     logo="../logo.svg",
        ...     title="Custom title",
        ... )

    """

    favicon: Optional[Union[Path, str]] = None
    """The file path to a ``.ico`` image that will be used as the favicon."""

    logo: Optional[Union[Path, str]] = None
    """The file path to a 20px high ``.svg`` image that will be displayed in the upper-left corner."""

    title: str = "Atoti"
    """The title to give to the browser tab (in the home page)."""

    def __post_init__(self) -> None:
        convert_path_to_absolute_string(self, "favicon", "logo")
        _check_suffix(self.favicon, expected_suffix=".ico", name="favicon")
        _check_suffix(self.logo, expected_suffix=".svg", name="logo")


def _check_suffix(
    path: Optional[Union[Path, str]], *, expected_suffix: str, name: str
) -> None:
    if path is None:
        return

    suffix = Path(path).suffix

    if suffix != expected_suffix:
        raise ValueError(
            f"Expected {name} to be a {expected_suffix} file but got a {suffix} file."
        )
