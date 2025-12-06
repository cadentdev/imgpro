# ImagePro Task List

This document tracks implementation progress based on `PRD.md`.

**Last Updated:** 2025-12-06

---

## ✅ Completed Tasks

### 1. Implement `imagepro info` (Section 4.1 of PRD)

**Status:** Completed via PR #3
**Test Coverage:** 69/69 tests passing (36 unit + 33 CLI integration)

- [x] Core CLI wiring
  - [x] Add an `info` subcommand to `imagepro.py`
  - [x] Use positional `<file>` argument: `imagepro info <file> [options]`
  - [x] Add flags: `--json`, `--short`, `--exif`, `--exif-all`

- [x] Core behavior
  - [x] Open file with Pillow; fail cleanly if unreadable or unsupported
  - [x] Read pixel dimensions, taking EXIF orientation into account
  - [x] Classify orientation: `portrait`, `landscape`, `square`
  - [x] Compute reduced integer aspect ratio (`ratio_raw`) using GCD
  - [x] Match `ratio_raw` against common ratios (1:1, 4:3, 3:2, 16:9, 5:4, 4:5, 9:16, 1.91:1)
  - [x] Report `common_ratio` or `none`

- [x] File and EXIF metadata
  - [x] Report filename, path, file size in KB
  - [x] Detect presence of EXIF
  - [x] Extract curated EXIF subset (date taken, make, model, orientation, DPI)
  - [x] Add `--exif-all` support to dump all EXIF tags

- [x] Output formats
  - [x] Default: human-readable multi-line summary
  - [x] `--json`: one JSON object per invocation (JSONL-friendly)
  - [x] `--short`: one CSV line per invocation with fixed column order

- [x] Error handling & exit codes
  - [x] Use exit code scheme (0=success, 3=not found, 1=error, 2=invalid args)
  - [x] Ensure errors go to stderr; normal output goes to stdout

### 2. Testing & TDD Setup (Section 5.6)

- [x] Add pytest to the project
  - [x] Add `pytest` to `requirements.txt`
  - [x] Create `tests/` directory structure
  - [x] Set up test fixtures with synthetic EXIF data

- [x] Unit tests for `info` helpers (36 tests)
  - [x] Aspect ratio calculation and common ratio matching
  - [x] Orientation classification
  - [x] EXIF extraction logic

- [x] CLI integration tests for `info` (33 tests)
  - [x] Success and error paths
  - [x] Test `--json`, `--short`, `--exif`, `--exif-all` flags
  - [x] Assert on exit codes and stderr/stdout separation

- [x] Unit tests for `resize` helpers (28 tests)
  - [x] Test `parse_sizes`, `validate_jpeg`, `get_file_size_kb`
  - [x] Test resize_image function with various dimensions
  - [x] Test upscaling prevention and aspect ratio preservation
  - [x] Test quality settings and output directory creation

- [x] CLI integration tests for `resize` (27 tests)
  - [x] Success and error paths
  - [x] Width/height mutual exclusion
  - [x] Quality validation and output directory creation
  - [x] Upscaling prevention and output format

- [x] CI/CD Setup
  - [x] GitHub Actions workflow for automated testing on PRs
  - [x] Tests across Python 3.8, 3.9, 3.10, 3.11

---

## 📋 In Progress / Planned

### 3. Implement `imagepro rename` (Section 4.4 of PRD) - Priority 1

> **Status:** Not started
> **Depends on:** None

The `rename` command provides two key features for organizing image files:
1. Fix mismatched extensions based on actual file format
2. Prepend EXIF date/time for chronological sorting

- [ ] Write tests first (TDD)
  - [ ] Unit tests for format detection and extension mapping
  - [ ] Unit tests for EXIF date extraction and formatting
  - [ ] Unit tests for filename transformation logic
  - [ ] CLI integration tests for `--ext` flag
  - [ ] CLI integration tests for `--prefix-exif-date` flag
  - [ ] CLI integration tests for combined flags
  - [ ] Tests for missing EXIF date (skip with warning)
  - [ ] Tests for output directory option

- [ ] Implement `rename` command
  - [ ] Add `rename` subparser with positional `<file>` argument
  - [ ] Implement `--ext` flag for extension correction
    - [ ] Read actual image format from file content
    - [ ] Map format to lowercase extension (JPEG→.jpg, PNG→.png, HEIF→.heic)
    - [ ] Create copy with corrected extension
  - [ ] Implement `--prefix-exif-date` flag
    - [ ] Extract DateTimeOriginal from EXIF
    - [ ] Format as YYYY-MM-DDTHHMMSS_ (no colons for macOS)
    - [ ] Skip file with warning if no EXIF date
  - [ ] Support `--output <directory>` option
  - [ ] Exit codes: 0=success, 3=not found, 4=cannot read

### 4. Implement `imagepro convert` (Section 4.3 of PRD) - Priority 2

> **Status:** Not started
> **Depends on:** None

The `convert` command enables format conversion, primarily HEIC→JPEG.

- [ ] Write tests first (TDD)
  - [ ] Unit tests for format conversion logic
  - [ ] Unit tests for EXIF preservation/stripping
  - [ ] CLI integration tests for basic conversion
  - [ ] CLI integration tests for `--strip-exif` flag
  - [ ] CLI integration tests for `--quality` option
  - [ ] Tests for output directory and naming

- [ ] Implement `convert` command
  - [ ] Add `convert` subparser with positional `<source>` argument
  - [ ] Implement `--format` option (required: jpeg, png; future: webp)
  - [ ] Default output to `./converted/` directory
  - [ ] Preserve EXIF by default
  - [ ] Implement `--strip-exif` flag to remove metadata
  - [ ] Support `--quality` option for lossy formats
  - [ ] Handle existing output files (overwrite with warning)

### 5. Create Bash Scripts in `scripts/` Directory - Priority 3

> **Status:** Not started
> **Depends on:** rename and convert commands

Utility scripts demonstrating batch workflows with imagepro.

- [ ] Create `scripts/` directory structure

- [ ] Script 1: `resize-all.sh`
  - [ ] Resize all images in directory to specified width
  - [ ] Skip files already smaller than target width
  - [ ] Use `python3 imagepro.py` invocation

- [ ] Script 2: `organize-by-orientation.sh`
  - [ ] Move images to subdirectories by orientation (landscape/, portrait/, square/)
  - [ ] Variant: organize by aspect ratio (4x3/, 3x4/, 16x9/, etc.)
  - [ ] Handle directory naming without colons

- [ ] Script 3: `generate-responsive-set.sh` (lower priority)
  - [ ] Create multiple width versions for srcset
  - [ ] Output organized for HTML integration

### 6. Enhanced `imagepro info` Field Selection (Section 4.1 of PRD) - Priority 4

> **Status:** Not started
> **Depends on:** None

Add individual field flags for selective metadata output.

- [ ] Write tests first (TDD)
  - [ ] Tests for individual field flags (-w, -h, --format, etc.)
  - [ ] Tests for multiple field combination
  - [ ] Tests for output formats (space-separated, --csv, --json, --key-value)
  - [ ] Tests for JSON always including filename

- [ ] Implement field selection
  - [ ] Add `-w`/`--width` flag
  - [ ] Add `-h`/`--height` flag (note: conflicts with --help, may need adjustment)
  - [ ] Add `--format` flag
  - [ ] Add `--aspect-ratio` flag
  - [ ] Add `--orientation` flag
  - [ ] Implement space-separated output (default)
  - [ ] Implement `--csv` output format
  - [ ] Implement `--key-value` output format
  - [ ] Ensure `--json` includes filename

### 7. Align `imagepro resize` with PRD (Section 4.2) - Backlog

> **Note:** Current code uses `--input`; PRD specifies positional `<file>`. Tests are complete but CLI needs refactoring.

- [ ] Refactor CLI to match PRD
  - [ ] Introduce positional `<file>` for `resize`
  - [ ] Keep `--input` working for backwards compatibility (or plan breaking change)
  - [ ] Ensure help text matches PRD style

- [ ] Verify behavior matches spec
  - [ ] Confirm width/height mutual exclusion (already tested)
  - [ ] Confirm upscaling prevention (already tested)
  - [ ] Confirm output directory behavior (already tested)
  - [ ] Verify EXIF stripping and ICC profile preservation

- [ ] Update documentation
  - [ ] Update `README.md` examples to use positional `<file>`
  - [ ] Update help text to match PRD

---

## 🎯 Future Enhancements

### 5. Nice-to-Haves (PRD Section 7.x)

- [ ] Add `--verbose` and `--quiet` modes (PRD 4.6.3–4.6.4)
  - [ ] Implement verbose mode with detailed processing info
  - [ ] Implement quiet mode (errors only)
  - [ ] Add tests for both modes

- [ ] Explore batch-oriented UX (PRD 7.1)
  - [ ] Design multi-file input interface
  - [ ] Add progress bar for batch operations
  - [ ] Consider glob pattern support

- [ ] Add image format detection to `info` command
  - [ ] Detect actual image format from file content (not just extension)
  - [ ] Report format via Pillow's `Image.format` attribute
  - [ ] Add to default, JSON, and CSV outputs
  - [ ] Distinguish between file extension and actual format (e.g., .HEIC file containing JPEG data)

- [ ] Additional EXIF features
  - [ ] Revisit DPI reporting for IG workflows
  - [ ] Add more EXIF fields based on user feedback
  - [ ] EXIF editing capabilities

- [ ] Advanced resizing features (PRD 7.2)
  - [ ] Crop modes (center, smart, focal point)
  - [ ] Fit modes (contain, cover, fill)

- [ ] Format expansion (PRD 7.3)
  - [ ] WebP support
  - [ ] AVIF support
  - [ ] Additional format conversions

---

## 📊 Project Status

**Current Version:** 1.1.0
**Test Coverage:** 46% (124 tests)
- Info command: 100% (69 tests)
- Resize command: ~95% (55 tests)

**Completed:**
- ✅ Info command (full implementation)
- ✅ Resize command (implementation complete, CLI refactor pending)
- ✅ HEIF/HEIC format support via pillow-heif
- ✅ Comprehensive test suite
- ✅ CI/CD pipeline
- ✅ Documentation updates for v1.1.0

**Next Priorities (in order):**
1. Implement `imagepro rename` command (extension fix + EXIF date prefix)
2. Implement `imagepro convert` command (HEIC→JPEG, format conversion)
3. Create bash utility scripts in `scripts/` directory
4. Add field selection to `imagepro info` command

**Core Principle:** All file-modifying commands create copies by default (non-destructive).
