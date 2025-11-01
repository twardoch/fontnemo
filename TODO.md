# fontnemo TODO List

## Phase 1: Project Setup

- [ ] Create `src/fontnemo/` directory structure
- [ ] Create `src/fontnemo/__init__.py`
- [ ] Create `src/fontnemo/__main__.py` skeleton
- [ ] Create `src/fontnemo/core.py` skeleton
- [ ] Create `src/fontnemo/utils.py` skeleton
- [ ] Create `pyproject.toml` with hatch-vcs configuration
- [ ] Add dependencies: fonttools, fire, loguru, pytest, pytest-cov
- [ ] Create `tests/` directory
- [ ] Create `tests/fixtures/` directory
- [ ] Find or create test font files (minimum 2)
- [ ] Document test font nameID contents
- [ ] Verify `uv sync` works
- [ ] Verify `uvx hatch test` runs
- [ ] Verify `uv run fontnemo --help` works

## Phase 2: Core Utilities

### Slug Generation
- [ ] Write `make_slug()` function signature
- [ ] Write test for normal ASCII text → slug
- [ ] Write test for Unicode text → slug (strips non-ASCII)
- [ ] Write test for forbidden characters removal
- [ ] Write test for empty string
- [ ] Write test for text with only forbidden chars
- [ ] Implement `make_slug()` function
- [ ] Run tests for slug generation

### Timestamp Generation
- [ ] Write `make_timestamp()` function signature
- [ ] Write test for valid base-36 output
- [ ] Write test for lowercase output
- [ ] Write test for sortable timestamps
- [ ] Write test for consistent length
- [ ] Implement `make_timestamp()` function
- [ ] Run tests for timestamp generation

## Phase 3: Font Name Reading

### Read Operations
- [ ] Create `FontNameHandler` class skeleton
- [ ] Write test for reading nameID 16 (when exists)
- [ ] Write test for fallback to nameID 21
- [ ] Write test for fallback to nameID 1
- [ ] Write test for platform/encoding priority
- [ ] Implement `read_family_name()` method
- [ ] Run tests for family name reading
- [ ] Write test for reading nameID 25 (when exists)
- [ ] Write test for fallback to nameID 6 with hyphen
- [ ] Write test for nameID 6 without hyphen
- [ ] Implement `read_family_slug()` method
- [ ] Run tests for family slug reading

### Write Operations
- [ ] Write test for writing to nameIDs 1,4,16,18,21
- [ ] Write test for updating multiple platform/encoding records
- [ ] Write test for handling missing nameIDs gracefully
- [ ] Implement `write_family_name()` method
- [ ] Run tests for family name writing
- [ ] Write test for writing to nameIDs 6,20,25 with space removal
- [ ] Write test for slug space removal
- [ ] Implement `write_family_slug()` method
- [ ] Run tests for family slug writing

## Phase 4: Safe File Operations

- [ ] Write test for output mode "0" (replace input)
- [ ] Write test for output mode "1" (backup + replace)
- [ ] Write test for output mode "2" (timestamped output)
- [ ] Write test for explicit output path
- [ ] Write test for temp file cleanup on success
- [ ] Write test for temp file cleanup on failure
- [ ] Write test for original file unchanged until move
- [ ] Implement `save_font_safely()` function
- [ ] Run tests for safe file operations

## Phase 5: CLI Commands

### view Command
- [ ] Write test for short output format
- [ ] Write test for long output format
- [ ] Write test for invalid file error
- [ ] Implement `view()` command
- [ ] Implement `v()` alias
- [ ] Run tests for view command

### new Command
- [ ] Write test for setting new family name
- [ ] Write test for slug generation from new name
- [ ] Write test for all nameIDs updated
- [ ] Write test for output mode "0"
- [ ] Write test for output mode "1"
- [ ] Write test for output mode "2"
- [ ] Write test for explicit output path
- [ ] Implement `new()` command
- [ ] Implement `n()` alias
- [ ] Run tests for new command

### replace Command
- [ ] Write test for simple text replacement
- [ ] Write test for Unicode find/replace
- [ ] Write test for slug transformation independence
- [ ] Write test for no match scenario
- [ ] Implement `replace()` command
- [ ] Implement `r()` alias
- [ ] Run tests for replace command

### suffix Command
- [ ] Write test for suffix appended to name
- [ ] Write test for suffix slug appended to slug
- [ ] Write test for space handling
- [ ] Implement `suffix()` command
- [ ] Implement `s()` alias
- [ ] Run tests for suffix command

### prefix Command
- [ ] Write test for prefix prepended to name
- [ ] Write test for prefix slug prepended to slug
- [ ] Implement `prefix()` command
- [ ] Implement `p()` alias
- [ ] Run tests for prefix command

### timestamp Command
- [ ] Write test for default space separator
- [ ] Write test for custom separator
- [ ] Write test for timestamp format
- [ ] Implement `timestamp()` command
- [ ] Implement `t()` alias
- [ ] Run tests for timestamp command

### Fire CLI Setup
- [ ] Create `FontNemoCLI` class
- [ ] Set up command routing
- [ ] Set up command aliases
- [ ] Write test for all aliases work
- [ ] Write test for fire help text
- [ ] Write test for invalid command error
- [ ] Implement `main()` entry point
- [ ] Run tests for CLI routing

## Phase 6: Logging and Error Handling

### Logging
- [ ] Add verbose parameter to CLI
- [ ] Configure loguru based on verbose flag
- [ ] Write test for --verbose enables debug
- [ ] Write test for default quiet mode
- [ ] Add logging throughout code

### Error Handling
- [ ] Write test for missing file error
- [ ] Write test for invalid font error
- [ ] Write test for permission error
- [ ] Add error handling for font not found
- [ ] Add error handling for invalid font
- [ ] Add error handling for missing nameIDs
- [ ] Add error handling for file permissions
- [ ] Verify all errors exit with non-zero status

## Phase 7: Documentation and Polish

### Examples
- [ ] Create `examples/` directory
- [ ] Create `examples/basic_usage.sh`
- [ ] Add example for each command
- [ ] Add comments explaining examples
- [ ] Test all examples work

### Test Script
- [ ] Create `test.sh`
- [ ] Add autoflake command
- [ ] Add pyupgrade command
- [ ] Add ruff check command
- [ ] Add ruff format command
- [ ] Add pytest command
- [ ] Make script executable
- [ ] Test script runs successfully

### Documentation
- [ ] Create `DEPENDENCIES.md`
- [ ] Create `CHANGELOG.md` for v0.1.0
- [ ] Update `README.md` with usage examples
- [ ] Add installation instructions
- [ ] Add contributing guidelines
- [ ] Verify all documentation accurate

## Final Validation

- [ ] Run full test suite
- [ ] Verify test coverage ≥ 80%
- [ ] Run `test.sh` successfully
- [ ] Test all CLI commands manually
- [ ] Test all command aliases manually
- [ ] Test all output modes manually
- [ ] Verify can be installed via uv
- [ ] Review code for compliance with CLAUDE.md guidelines
- [ ] Update WORK.md with completion status
