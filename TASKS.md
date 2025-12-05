# ImagePro Task List

This document tracks implementation progress based on `PRD.md`.

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

### 3. Align `imagepro resize` with PRD (Section 4.2)

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

### 4. Prepare for `imagepro convert` (Section 4.3)

- [ ] Design initial `convert` CLI
  - [ ] Define subcommand: `imagepro convert <source> --format <target> [options]`
  - [ ] Decide initial supported formats (at minimum: jpeg, png)
  - [ ] Design output naming and directory rules

- [ ] Plan implementation
  - [ ] Identify shared helpers with `resize` and `info`
  - [ ] Define format conversion strategy
  - [ ] Plan EXIF handling for different formats

- [ ] Write tests first (TDD)
  - [ ] Unit tests for format conversion logic
  - [ ] CLI integration tests for `convert` command
  - [ ] Test all supported format combinations

- [ ] Implement `convert` command
  - [ ] Only after `info` and `resize` are fully aligned with PRD

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

**Current Version:** 1.0
**Test Coverage:** 46% (124 tests)
- Info command: 100% (69 tests)
- Resize command: ~95% (55 tests)

**Completed:**
- ✅ Info command (full implementation)
- ✅ Resize command (implementation complete, CLI refactor pending)
- ✅ Comprehensive test suite
- ✅ CI/CD pipeline

**Next Priorities:**
1. Refactor resize CLI to use positional arguments
2. Implement convert command
3. Add verbose/quiet modes
