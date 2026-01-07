# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ImgPro is a Python CLI tool for responsive image processing, designed for web developers working with static site generators. It provides commands for inspecting image metadata and generating multiple resolutions for responsive web design.

**Main file:** `imgpro.py` (single-file Python script, ~1100 lines)
**Current version:** 1.2.0
**Python requirement:** 3.8+
**Primary dependency:** Pillow (PIL), pillow-heif (for HEIF/HEIC support)

## Development Commands

### Running the Tool
```bash
# Info command - inspect image metadata
python3 imgpro.py info <file> [--json|--short] [--exif|--exif-all]

# Resize command - generate multiple image sizes
python3 imgpro.py resize <file> --width <sizes> [--quality 90] [--output ./resized/]
python3 imgpro.py resize <file> --height <sizes> [--quality 90] [--output ./resized/]
```

### Testing
```bash
# Run all tests (307 total)
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_info_cli.py -v
python -m pytest tests/test_resize_cli.py -v

# Run with coverage
python -m pytest tests/ --cov=imgpro --cov-report=term-missing

# Run specific test
python -m pytest tests/test_info_cli.py::TestInfoCommandBasics::test_info_command_exists -v
```

### CI/CD
- GitHub Actions runs tests automatically on PRs
- Tests across Python 3.8, 3.9, 3.10, 3.11
- Workflow: `.github/workflows/test.yml`

## Architecture

### Single-File Design
All code lives in `imgpro.py` - there are no separate modules. This keeps the tool simple and portable.

### Subcommand Structure
The CLI uses argparse subparsers for command routing:
1. `main()` - Sets up argument parser and subparsers
2. Each subcommand (`info`, `resize`) has a dedicated handler function:
   - `cmd_info(args)` - Handles info subcommand (lines 342-432)
   - `cmd_resize(args)` - Handles resize subcommand (lines 434-508)
3. Handler functions are set via `parser.set_defaults(func=cmd_*)` pattern

### Key Helper Functions

**Image Information (`info` command):**
- `get_image_info(filepath)` - Main orchestrator for gathering all image metadata (lines 177-228)
- `calculate_aspect_ratio(width, height)` - Computes reduced integer ratio using GCD (lines 42-56)
- `classify_orientation(width, height)` - Returns "square", "landscape", or "portrait" (lines 59-75)
- `match_common_ratio(ratio_str)` - Matches against common ratios (1:1, 16:9, etc.) (lines 78-102)
- `extract_exif_data(filepath)` - Extracts EXIF metadata using Pillow (lines 105-132)
- `format_exif_curated(exif_dict)` - Returns friendly subset of EXIF fields (lines 135-174)
- `serialize_exif_value(value)` - Converts Pillow EXIF types to JSON-serializable types (lines 318-339)

**Image Resizing (`resize` command):**
- `resize_image(input_path, output_dir, sizes, dimension, quality)` - Core resize logic (lines 231-315)
- `parse_sizes(size_str)` - Parses comma-separated size list (lines 18-26)
- `validate_jpeg(filepath)` - Checks for JPEG extension (lines 29-34)
- `get_file_size_kb(filepath)` - Returns file size in KB (lines 37-39)

### Exit Code Convention
- `0` - Success
- `1` - Unsupported format or unreadable image
- `2` - Invalid arguments (quality, width/height conflict, etc.)
- `3` - File not found
- `4` - Cannot read/process image

## Test-Driven Development (TDD)

This project follows strict TDD practices:

### Test Organization
```
tests/
├── conftest.py           # Pytest configuration
├── fixtures.py           # Test image generation with synthetic EXIF
├── test_info_helpers.py  # Unit tests for info helper functions (36 tests)
├── test_info_cli.py      # CLI integration tests for info (33 tests)
├── test_resize_helpers.py # Unit tests for resize helpers (28 tests)
└── test_resize_cli.py    # CLI integration tests for resize (27 tests)
```

### TDD Workflow for New Features
1. **Write tests first** - Define expected behavior through tests before implementation
2. **Run tests and watch them fail** - Confirm tests fail as expected (red)
3. **Implement minimal code** - Write just enough to make tests pass (green)
4. **Refactor** - Improve code while keeping tests green
5. **Maintain coverage** - Aim for >80% on core logic

### Test Coverage
- **Info command:** 100% coverage (69 tests)
- **Resize command:** ~95% coverage (55 tests)
- **Convert command:** 100% coverage (52 tests)
- **Rename command:** 100% coverage (50 tests)
- **Overall:** ~50% coverage (307 total tests)

## PRD and Task Tracking

**Critical:** Always reference `PRD.md` (Product Requirements Document) for feature specifications and requirements. It is the source of truth for expected behavior.

**Task tracking:** `TASKS.md` tracks implementation progress against the PRD. Check it to understand what's done and what's planned.

## File Naming Convention

Resized images use pattern: `{basename}_{size}.{ext}`
- `photo.jpg` resized to 300px → `photo_300.jpg`
- Size suffix represents the controlled dimension (width or height)

## Image Processing Details

### Resize Behavior
- **Algorithm:** Lanczos resampling (high-quality)
- **Aspect ratio:** Always preserved
- **Upscaling:** Automatically prevented with warnings
- **EXIF:** Stripped by default from resized outputs
- **Transparency:** Converted to white background for JPEG
- **Color mode:** Converts to RGB for JPEG output

### Info Command Specifics
- **EXIF orientation:** Automatically handled by Pillow
- **Aspect ratios:** Exact integer matching only (uses GCD for reduction)
- **Common ratios:** 1:1, 4:3, 3:2, 16:9, 5:4, 4:5, 9:16, 1.91:1 (as 191:100)
- **Format support:** Any Pillow-compatible format (JPEG, PNG, HEIF, etc.)

### Resize Command Specifics
- **Format support:** JPEG only in v1.0 (validation enforced)
- **Quality range:** 1-100 (default: 90)
- **Output directory:** Default is `./resized/`, created if doesn't exist

## Adding New Commands

To add a new subcommand (e.g., `convert`):

1. **Write tests first** (TDD):
   - Create `tests/test_<command>_helpers.py` for unit tests
   - Create `tests/test_<command>_cli.py` for CLI integration tests

2. **Create command handler** in `imgpro.py`:
   ```python
   def cmd_convert(args):
       """Handle the convert subcommand."""
       # Implementation here
       pass
   ```

3. **Add subparser** in `main()`:
   ```python
   # After line 520 (in subparsers section)
   convert_parser = subparsers.add_parser(
       'convert',
       help='Convert image formats',
       description='Convert images between formats'
   )
   convert_parser.add_argument('--format', required=True)
   convert_parser.set_defaults(func=cmd_convert)
   ```

4. **Follow exit code convention** for error handling

## Important Patterns

### Error Handling
- Print errors to `stderr`, normal output to `stdout`
- Use descriptive error messages with context
- Exit with appropriate status codes (see convention above)

### Output Formatting
The `info` command supports three output modes:
- **Default:** Human-readable multi-line (for terminal use)
- **`--json`:** Single JSON object per invocation (JSONL-compatible)
- **`--short`:** Single CSV line with fixed column order (for batch processing)

This multi-format design enables both interactive use and shell scripting.

## Dependencies

Keep dependencies minimal:
- **Pillow (>=10.0.0):** Core image processing library
- **pillow-heif (>=0.13.0):** HEIF/HEIC format support (enables iPhone photo formats)
- **pytest (>=7.0.0):** Testing framework

**Note:** The `pillow-heif` dependency is automatically registered on import with graceful fallback if unavailable. See lines 14-19 in `imgpro.py`.

Avoid adding new dependencies unless absolutely necessary.

## Format Support

**Info Command (Read):**
- JPEG, PNG, HEIF/HEIC (requires pillow-heif), DNG (RAW), BMP, GIF, TIFF, WebP
- Format detection based on file content, not extension

**Resize Command (v1.0):**
- JPEG only (PNG, WebP, AVIF planned for future versions)
