# fontnemo Implementation Plan

## Project Scope

**One-sentence scope:** CLI tool that modifies font family names and PostScript slugs in OpenType/TrueType fonts using exact nameID field manipulation rules.

## Research Summary

### Existing Solutions Analysis

Researched existing tools:
- **fontname.py**: Simple script for renaming family names, but doesn't handle slug generation rules or multiple nameID fallback logic
- **ftCLI**: Full-featured but complex, more than needed for our focused use case
- **FoundryTools-CLI**: Similar to ftCLI, too broad for our specific requirements

**Decision:** Build custom tool. Existing solutions don't match our exact nameID reading priority (16→21→1 for family, 25→6 for slug) and SLUG_RULE requirements.

### PostScript Naming Standards

Confirmed standards:
- ASCII codes 33-126 (printable ASCII)
- Forbidden: `[](){}<%>/` (10 characters)
- No spaces in PostScript names
- Max length: 63 characters (not enforced in MVP)

### Reference Code

`vendors/fonttools/Snippets/rename-fonts.py` provides patterns for:
- Platform/encoding priority: Windows English (3,1,0x409) → Mac Roman (1,0,0)
- Name record iteration and modification
- Safe file handling with TTFont

## Technical Architecture

### Core Modules

**src/fontnemo/**
1. `__init__.py`: Package initialization, version info
2. `__main__.py`: Fire CLI entry point with command routing
3. `core.py`: Font name reading/writing operations (150-180 lines)
4. `utils.py`: Slug conversion, timestamp generation (50-70 lines)

### Key Design Decisions

1. **Two-phase name operations**: Separate `family_name` (human-readable) and `family_slug` (PostScript-safe) with independent transformation rules
2. **Cascading fallback reads**: Implement priority-based nameID reading exactly as specified
3. **Safe file writes**: Always temp file → backup (optional) → move pattern
4. **No rich output**: Use plain stdout per updated CLAUDE.md requirements
5. **Verbose logging**: Optional `--verbose` flag with loguru for debugging

### Dependencies Justification

| Package | Why Chosen | Stars/Activity |
|---------|-----------|----------------|
| fonttools | Industry standard for font manipulation, well-maintained | 4.3k stars, active |
| fire | Simplest CLI with command aliases, zero boilerplate | 27k stars, stable |
| loguru | Clean logging API with --verbose support | 20k stars, active |
| pytest | Standard testing framework | 12k stars, active |
| pytest-cov | Test coverage reporting | 1.8k stars, active |

**Explicitly NOT using:**
- ~~rich~~: Removed per CLAUDE.md line 103 update

## Phase 1: Project Setup (Priority: CRITICAL)

### 1.1 Initialize Project Structure
- Create `src/fontnemo/` directory structure
- Set up `pyproject.toml` with hatch-vcs for git-tag versioning
- Configure pytest and mypy
- Create `tests/` directory with `fixtures/` subdirectory

**Acceptance criteria:**
- `uv sync` runs successfully
- `uvx hatch test` runs (even with 0 tests)
- `uv run fontnemo --help` shows fire help

### 1.2 Set Up Test Fixtures
- Find or create minimal test font files (.ttf/.otf)
- Place in `tests/fixtures/`
- Document fixture font characteristics (which nameIDs exist)

**Acceptance criteria:**
- At least 2 test fonts available
- Documented nameID contents for each fixture

## Phase 2: Core Utilities (Priority: HIGH)

### 2.1 Implement SLUG_RULE Function
**File:** `src/fontnemo/utils.py`

**Function:** `make_slug(text: str) -> str`
- Input: Any string (Unicode allowed)
- Filter: Keep only ASCII 33-126
- Remove: `[](){}<%>/`
- Remove: All spaces
- Return: Valid PostScript identifier

**Tests:** `tests/test_utils.py`
- Normal ASCII text
- Unicode input (should strip non-ASCII)
- Text with forbidden characters
- Empty string edge case
- Text with only forbidden characters

### 2.2 Implement TIME_RULE Function
**File:** `src/fontnemo/utils.py`

**Function:** `make_timestamp() -> str`
- Get current Unix timestamp
- Convert to base-36
- Return lowercase string

**Tests:** `tests/test_utils.py`
- Returns valid base-36 string
- Returns lowercase
- Timestamp is sortable (later timestamp > earlier)
- Consistent length (approximately 7-8 chars in 2024)

## Phase 3: Font Name Reading (Priority: CRITICAL)

### 3.1 Implement Name Record Reading
**File:** `src/fontnemo/core.py`

**Class/Functions:**
- `FontNameHandler` class to encapsulate operations
- `read_family_name(font: TTFont) -> str`: Reads with fallback 16→21→1
- `read_family_slug(font: TTFont) -> str`: Reads with fallback 25→6 (pre-hyphen)

**Platform/encoding priority:**
1. Windows English: (platformID=3, platEncID=1, langID=0x409)
2. Mac Roman: (platformID=1, platEncID=0, langID=0)

**Tests:** `tests/test_core.py`
- Read when nameID 16 exists
- Fallback to 21 when 16 missing
- Fallback to 1 when 16 and 21 missing
- Read slug from nameID 25
- Fallback to nameID 6 with hyphen parsing
- Handle fonts with no hyphen in nameID 6
- Handle missing name records gracefully

### 3.2 Implement Name Record Writing
**File:** `src/fontnemo/core.py`

**Functions:**
- `write_family_name(font: TTFont, new_name: str) -> None`: Writes to nameIDs 1,4,16,18,21
- `write_family_slug(font: TTFont, new_slug: str) -> None`: Writes to nameIDs 6,20,25 (no spaces)

**Logic:**
- Iterate all name records in `font["name"].names`
- Update `.string` property for matching nameIDs
- Apply space removal for slug-related nameIDs

**Tests:** `tests/test_core.py`
- Write family name updates all target nameIDs
- Write slug removes spaces correctly
- Verify multiple platform/encoding records updated
- Handle fonts with missing nameIDs gracefully (no error)

## Phase 4: Safe File Operations (Priority: HIGH)

### 4.1 Implement Safe Write Pattern
**File:** `src/fontnemo/core.py`

**Function:** `save_font_safely(font: TTFont, input_path: Path, output_mode: str | Path) -> Path`

**Output mode logic:**
- `"0"` or `None`: Replace input file (temp → move)
- `"1"`: Backup original with `--TIMESTAMP` suffix, then replace
- `"2"`: Save as input path with `--TIMESTAMP` suffix
- Explicit path string: Save to that path

**Implementation:**
- Use `tempfile.NamedTemporaryFile` in same directory as final output
- Save font to temp file
- If mode="1", copy original to backup
- Move temp file to final location
- Return final output path

**Tests:** `tests/test_core.py`
- Mode "0" replaces input
- Mode "1" creates backup and replaces input
- Mode "2" creates timestamped output
- Explicit path saves correctly
- Temp file cleaned up on success
- Temp file cleaned up on failure (exception handling)
- Verify original file unchanged until move

## Phase 5: CLI Commands (Priority: CRITICAL)

### 5.1 Implement `view` Command
**File:** `src/fontnemo/__main__.py`

**Function:** `view(input_path: str, long: bool = False) -> None`
- Load font
- Read `family_name`
- Print: `{family_name}` or `{input_path}:{family_name}` if long
- Use plain `print()` (no rich)

**Tests:** `tests/test_cli.py`
- Short output format
- Long output format
- Invalid file path error handling

### 5.2 Implement `new` Command
**File:** `src/fontnemo/__main__.py`

**Function:** `new(input_path: str, new_family: str, output_path: str = "0") -> None`
- Read current `family_name` and `family_slug`
- Set `new_family_name = new_family`
- Generate `new_family_slug = make_slug(new_family)`
- Write both to font
- Save with output_path mode
- Log operation with --verbose

**Tests:** `tests/test_cli.py`
- New family name applied correctly
- Slug generated following SLUG_RULE
- All nameIDs updated
- Output modes 0, 1, 2 work
- Explicit output path works

### 5.3 Implement `replace` Command
**File:** `src/fontnemo/__main__.py`

**Function:** `replace(input_path: str, find: str, replace: str, output_path: str = "0") -> None`
- Read `family_name` and `family_slug`
- `new_family_name = family_name.replace(find, replace)`
- `find_slug = make_slug(find)`
- `replace_slug = make_slug(replace)`
- `new_family_slug = family_slug.replace(find_slug, replace_slug)`
- Write and save

**Tests:** `tests/test_cli.py`
- Simple text replacement
- Unicode find/replace handling
- Slug transformation independence
- No match (no change)

### 5.4 Implement `suffix` Command
**File:** `src/fontnemo/__main__.py`

**Function:** `suffix(input_path: str, suffix: str, output_path: str = "0") -> None`
- Read `family_name` and `family_slug`
- `new_family_name = family_name + suffix`
- `new_family_slug = family_slug + make_slug(suffix)`
- Write and save

**Tests:** `tests/test_cli.py`
- Suffix appended to name
- Suffix slug appended to slug
- Space handling in suffix

### 5.5 Implement `prefix` Command
**File:** `src/fontnemo/__main__.py`

**Function:** `prefix(input_path: str, prefix: str, output_path: str = "0") -> None`
- Read `family_name` and `family_slug`
- `new_family_name = prefix + family_name`
- `new_family_slug = make_slug(prefix) + family_slug`
- Write and save

**Tests:** `tests/test_cli.py`
- Prefix prepended to name
- Prefix slug prepended to slug

### 5.6 Implement `timestamp` Command
**File:** `src/fontnemo/__main__.py`

**Function:** `timestamp(input_path: str, separator: str = " ", output_path: str = "0") -> None`
- Generate timestamp string = `separator + make_timestamp()`
- Call `suffix()` with timestamp as suffix

**Tests:** `tests/test_cli.py`
- Default space separator
- Custom separator
- Timestamp format valid

### 5.7 Set Up Fire CLI Routing
**File:** `src/fontnemo/__main__.py`

**Structure:**
```python
class FontNemoCLI:
    def view(self, ...): ...
    def v(self, ...): return self.view(...)

    def new(self, ...): ...
    def n(self, ...): return self.new(...)

    # etc for all commands

def main():
    fire.Fire(FontNemoCLI)

if __name__ == "__main__":
    main()
```

**Tests:** `tests/test_cli.py`
- All command aliases work (`v` = `view`, etc.)
- Fire help text displays
- Invalid command shows error

## Phase 6: Logging and Error Handling (Priority: MEDIUM)

### 6.1 Configure Loguru
**File:** `src/fontnemo/__main__.py`

**Setup:**
- Add `verbose: bool = False` parameter to CLI class `__init__`
- Configure loguru level based on verbose flag
- Default: WARNING (quiet)
- Verbose: DEBUG

**Tests:** `tests/test_cli.py`
- --verbose flag enables debug output
- Default mode is quiet

### 6.2 Add Error Handling
**Throughout all modules:**
- Font file not found: Clear error message
- Invalid font file: Clear error message
- Missing required nameIDs: Graceful handling
- File permission errors: Clear error message
- All errors exit with non-zero status code

**Tests:** `tests/test_error_handling.py`
- Missing file error
- Invalid font error
- Permission error (if testable)

## Phase 7: Documentation and Polish (Priority: LOW)

### 7.1 Create Usage Examples
**File:** `examples/basic_usage.sh`
- Example of each command
- Example output
- Comments explaining what's happening

### 7.2 Create Test Script
**File:** `test.sh`
- Run autoflake, pyupgrade, ruff check, ruff format
- Run pytest with coverage
- Run functional examples
- Report results

### 7.3 Update Documentation
- Finalize `README.md` with usage examples
- Create `DEPENDENCIES.md` with rationale
- Create `CHANGELOG.md` with version 0.1.0 notes

## Testing Strategy

### Unit Tests (tests/test_*.py)
- Every function has at least one test
- Edge cases: empty strings, None, special characters
- Error cases: missing files, invalid fonts
- Coverage target: 80% minimum

### Integration Tests
- Full command workflows
- File operations (input → output verification)
- Multiple platform/encoding records

### Functional Tests (examples/)
- Real-world usage scenarios
- Executable examples that double as tests

## Risks and Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Test font fixtures hard to find | Medium | High | Create minimal test fonts with fonttools or use Google Fonts |
| nameID reading fallback complex | Low | High | Study reference code carefully, test each fallback level |
| Safe file write pattern has edge cases | Medium | High | Use proven tempfile patterns, test thoroughly |
| Fire CLI doesn't support aliases well | Low | Medium | Test aliases early, use explicit method forwarding |
| SLUG_RULE interpretation ambiguous | Low | Medium | Follow PostScript spec exactly, validated in research |

## Future Considerations (Post-MVP)

Not in scope for initial release:
- Batch processing multiple files
- Configuration file support
- Validation mode (check without modifying)
- GUI or web interface
- Font format conversion
- Advanced name table operations (beyond family names)

## Success Criteria

MVP is complete when:
1. All 6 CLI commands work (view, new, replace, suffix, prefix, timestamp)
2. All command aliases work (v, n, r, s, p, t)
3. All 3 output modes work (0, 1, 2)
4. Test coverage ≥ 80%
5. All tests pass
6. Documentation complete
7. Can be installed via `uv add git+...` or local install
8. Follows all development guidelines in CLAUDE.md

## Implementation Order

1. **Setup** (Phase 1): Project structure, dependencies
2. **Utils** (Phase 2): Slug and timestamp functions (easiest, no fonttools needed)
3. **Core Reading** (Phase 3.1): Font name reading with fallbacks
4. **Core Writing** (Phase 3.2): Font name writing
5. **Safe Write** (Phase 4): File handling pattern
6. **CLI Commands** (Phase 5): Implement all commands in order: view, new, replace, suffix, prefix, timestamp
7. **Polish** (Phase 6-7): Logging, error handling, documentation

Total estimated implementation: 4-6 hours for MVP, 2-3 hours for testing and polish.
