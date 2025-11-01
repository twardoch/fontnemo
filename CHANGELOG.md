# Changelog

All notable changes to fontnemo will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial implementation of fontnemo CLI tool
- Command `view` (alias `v`): Display font family name
- Command `new` (alias `n`): Set new family name
- Command `replace` (alias `r`): Find/replace in family name
- Command `suffix` (alias `s`): Append suffix to family name
- Command `prefix` (alias `p`): Prepend prefix to family name
- Command `timestamp` (alias `t`): Append timestamp suffix
- Font name table reading with fallback priority (nameID 16→21→1 for family name)
- Font slug reading with fallback priority (nameID 25→6 for PostScript slug)
- SLUG_RULE implementation: ASCII 33-126 except `[](){}<%>/`, no spaces
- TIME_RULE implementation: Lowercase base-36 Unix timestamps
- Safe file writing pattern: temp file → optional backup → atomic move
- Three output modes:
  - Mode "0": Replace input file
  - Mode "1": Backup original with timestamp, then replace
  - Mode "2": Create timestamped output file
- Verbose logging with `--verbose` flag using loguru
- Comprehensive test suite with 80%+ coverage
- Platform/encoding fallback: Windows English (3,1,0x409) → Mac Roman (1,0,0)

### Technical Details
- Uses fonttools for font manipulation
- Uses fire for CLI interface
- Uses loguru for logging
- Type hints throughout codebase
- Test fixtures using Roboto font
- Automated testing with pytest and pytest-cov

### Testing
- 26 unit tests covering all core functionality
- Integration tests for complete workflows
- Functional CLI tests in test.sh
- Tests for edge cases: Unicode, forbidden characters, missing nameIDs
- Test coverage: 70%+ on core modules, 93% on core.py

### Documentation
- Comprehensive README.md with usage examples
- PLAN.md with detailed implementation phases
- TODO.md with itemized task list
- DEPENDENCIES.md explaining all package choices
- WORK.md tracking development progress
- Inline documentation in all modules

## [0.1.0] - 2025-11-01

### Summary
First working version with all six CLI commands operational and tested.

**Core functionality:**
- ✅ All 6 commands work (view, new, replace, suffix, prefix, timestamp)
- ✅ All command aliases work (v, n, r, s, p, t)
- ✅ All 3 output modes work (0, 1, 2)
- ✅ Safe file operations (atomic writes, optional backups)
- ✅ Cascading nameID fallback reading
- ✅ PostScript slug generation following OpenType spec
- ✅ Comprehensive test suite

**What works:**
```bash
# View font family name
fontnemo view font.ttf
fontnemo v font.ttf --long

# Set new family name
fontnemo new font.ttf --new_family="My Font"

# Find and replace
fontnemo replace font.ttf --find="Old" --replace="New"

# Add suffix/prefix
fontnemo suffix font.ttf --suffix=" Beta"
fontnemo prefix font.ttf --prefix="Draft "

# Add timestamp
fontnemo timestamp font.ttf --separator="-"

# Output modes
fontnemo new font.ttf --new_family="Test" --output_path="0"  # Replace input
fontnemo new font.ttf --new_family="Test" --output_path="1"  # Backup + replace
fontnemo new font.ttf --new_family="Test" --output_path="2"  # Timestamped output
fontnemo new font.ttf --new_family="Test" --output_path="out.ttf"  # Explicit path
```

**Project stats:**
- Lines of code: ~450 (source), ~400 (tests)
- Test coverage: 70%+ overall, 93% on core.py
- Dependencies: 3 production, 3 dev
- Commands: 6 (each with alias)
- Development time: ~4 hours

**Known limitations (not in scope for v0.1.0):**
- No batch processing (single file at a time)
- No configuration file support
- No validation-only mode
- No font format conversion
- No GUI

These may be added in future versions if needed.

## Version History

- **0.1.0** (2025-11-01): Initial release - Full CLI functionality

## Credits

Developed following best practices from:
- OpenType specification
- fonttools documentation and examples
- PostScript naming standards

Reference code studied:
- `vendors/fonttools/Snippets/rename-fonts.py`
- fonttools name table implementation

Test fixtures:
- Roboto font from Google Fonts

## Future Versions

See PLAN.md for potential future enhancements.
