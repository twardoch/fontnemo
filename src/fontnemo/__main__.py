#!/usr/bin/env python3
# this_file: src/fontnemo/__main__.py
"""CLI entry point for fontnemo using Fire."""

import sys

import fire
from loguru import logger

from fontnemo.core import FontNameHandler, save_font_safely
from fontnemo.utils import make_slug, make_timestamp


class FontNemoCLI:
    """fontnemo CLI - Modify font family names in OpenType/TrueType fonts."""

    def __init__(self, verbose: bool = False) -> None:
        """Initialize CLI with optional verbose logging.

        Args:
            verbose: Enable debug logging
        """
        # Configure loguru
        logger.remove()  # Remove default handler
        if verbose:
            logger.add(sys.stderr, level="DEBUG")
        else:
            logger.add(sys.stderr, level="WARNING")

        self.verbose = verbose

    def view(self, input_path: str, long: bool = False) -> None:
        """Display current font family name.

        Args:
            input_path: Input font file (.ttf, .otf)
            long: If True, show path prefix in output

        Examples:
            fontnemo view font.ttf
            fontnemo v font.ttf --long
        """
        try:
            handler = FontNameHandler(input_path)
            family_name = handler.read_family_name()
            handler.close()

            if long:
                print(f"{input_path}:{family_name}")
            else:
                print(family_name)

        except Exception as e:
            logger.error(f"Error: {e}")
            sys.exit(1)

    def v(self, input_path: str, long: bool = False) -> None:
        """Alias for view command."""
        return self.view(input_path=input_path, long=long)

    def new(
        self,
        input_path: str,
        new_family: str,
        output_path: str = "0",
    ) -> None:
        """Set new font family name.

        Args:
            input_path: Input font file
            new_family: New family name
            output_path: Output mode:
                - "0" (default): Replace input file
                - "1": Backup original, then replace
                - "2": Save with timestamp suffix
                - path string: Save to specific path

        Examples:
            fontnemo new font.ttf --new_family="My New Font"
            fontnemo n font.ttf --new_family="Test" --output_path="output.ttf"
        """
        try:
            handler = FontNameHandler(input_path)

            # Generate slug from new family name
            new_slug = make_slug(new_family)

            logger.info(f"Setting family_name: {new_family!r}")
            logger.info(f"Setting family_slug: {new_slug!r}")

            # Write changes
            handler.write_family_name(new_family)
            handler.write_family_slug(new_slug)

            # Save with appropriate mode
            final_path = save_font_safely(handler, output_path)
            handler.close()

            print(f"Updated: {final_path}")

        except Exception as e:
            logger.error(f"Error: {e}")
            sys.exit(1)

    def n(
        self,
        input_path: str,
        new_family: str,
        output_path: str = "0",
    ) -> None:
        """Alias for new command."""
        return self.new(
            input_path=input_path,
            new_family=new_family,
            output_path=output_path,
        )

    def replace(
        self,
        input_path: str,
        find: str,
        replace: str,
        output_path: str = "0",
    ) -> None:
        """Find and replace in font family name.

        Args:
            input_path: Input font file
            find: String to find
            replace: String to replace with
            output_path: Output mode (see 'new' command)

        Examples:
            fontnemo replace font.ttf --find="Old" --replace="New"
            fontnemo r font.ttf --find="Test" --replace="Production"
        """
        try:
            handler = FontNameHandler(input_path)

            # Read current names
            family_name = handler.read_family_name()
            family_slug = handler.read_family_slug()

            # Replace in family name
            new_family_name = family_name.replace(find, replace)

            # Replace in slug (convert find/replace to slugs first)
            find_slug = make_slug(find)
            replace_slug = make_slug(replace)
            new_family_slug = family_slug.replace(find_slug, replace_slug)

            logger.info(f"family_name: {family_name!r} → {new_family_name!r}")
            logger.info(f"family_slug: {family_slug!r} → {new_family_slug!r}")

            # Write changes
            handler.write_family_name(new_family_name)
            handler.write_family_slug(new_family_slug)

            # Save
            final_path = save_font_safely(handler, output_path)
            handler.close()

            print(f"Updated: {final_path}")

        except Exception as e:
            logger.error(f"Error: {e}")
            sys.exit(1)

    def r(
        self,
        input_path: str,
        find: str,
        replace: str,
        output_path: str = "0",
    ) -> None:
        """Alias for replace command."""
        return self.replace(
            input_path=input_path,
            find=find,
            replace=replace,
            output_path=output_path,
        )

    def suffix(
        self,
        input_path: str,
        suffix: str,
        output_path: str = "0",
    ) -> None:
        """Append suffix to font family name.

        Args:
            input_path: Input font file
            suffix: Suffix to append
            output_path: Output mode (see 'new' command)

        Examples:
            fontnemo suffix font.ttf --suffix=" Beta"
            fontnemo s font.ttf --suffix=" v2"
        """
        try:
            handler = FontNameHandler(input_path)

            # Read current names
            family_name = handler.read_family_name()
            family_slug = handler.read_family_slug()

            # Append suffix
            new_family_name = family_name + suffix
            new_family_slug = family_slug + make_slug(suffix)

            logger.info(f"family_name: {family_name!r} → {new_family_name!r}")
            logger.info(f"family_slug: {family_slug!r} → {new_family_slug!r}")

            # Write changes
            handler.write_family_name(new_family_name)
            handler.write_family_slug(new_family_slug)

            # Save
            final_path = save_font_safely(handler, output_path)
            handler.close()

            print(f"Updated: {final_path}")

        except Exception as e:
            logger.error(f"Error: {e}")
            sys.exit(1)

    def s(
        self,
        input_path: str,
        suffix: str,
        output_path: str = "0",
    ) -> None:
        """Alias for suffix command."""
        return self.suffix(
            input_path=input_path,
            suffix=suffix,
            output_path=output_path,
        )

    def prefix(
        self,
        input_path: str,
        prefix: str,
        output_path: str = "0",
    ) -> None:
        """Prepend prefix to font family name.

        Args:
            input_path: Input font file
            prefix: Prefix to prepend
            output_path: Output mode (see 'new' command)

        Examples:
            fontnemo prefix font.ttf --prefix="Beta "
            fontnemo p font.ttf --prefix="Draft "
        """
        try:
            handler = FontNameHandler(input_path)

            # Read current names
            family_name = handler.read_family_name()
            family_slug = handler.read_family_slug()

            # Prepend prefix
            new_family_name = prefix + family_name
            new_family_slug = make_slug(prefix) + family_slug

            logger.info(f"family_name: {family_name!r} → {new_family_name!r}")
            logger.info(f"family_slug: {family_slug!r} → {new_family_slug!r}")

            # Write changes
            handler.write_family_name(new_family_name)
            handler.write_family_slug(new_family_slug)

            # Save
            final_path = save_font_safely(handler, output_path)
            handler.close()

            print(f"Updated: {final_path}")

        except Exception as e:
            logger.error(f"Error: {e}")
            sys.exit(1)

    def p(
        self,
        input_path: str,
        prefix: str,
        output_path: str = "0",
    ) -> None:
        """Alias for prefix command."""
        return self.prefix(
            input_path=input_path,
            prefix=prefix,
            output_path=output_path,
        )

    def timestamp(
        self,
        input_path: str,
        separator: str = " ",
        output_path: str = "0",
    ) -> None:
        """Append timestamp suffix to font family name.

        Args:
            input_path: Input font file
            separator: Separator before timestamp (default: space)
            output_path: Output mode (see 'new' command)

        Examples:
            fontnemo timestamp font.ttf
            fontnemo t font.ttf --separator="-"
        """
        timestamp = make_timestamp()
        suffix_str = separator + timestamp

        return self.suffix(
            input_path=input_path,
            suffix=suffix_str,
            output_path=output_path,
        )

    def t(
        self,
        input_path: str,
        separator: str = " ",
        output_path: str = "0",
    ) -> None:
        """Alias for timestamp command."""
        return self.timestamp(
            input_path=input_path,
            separator=separator,
            output_path=output_path,
        )


def main() -> None:
    """Main entry point for CLI."""
    fire.Fire(FontNemoCLI)


if __name__ == "__main__":
    main()
