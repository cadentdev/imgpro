## Summary

Implemented the `imagepro info` feature using Test-Driven Development, following PRD Section 4.1.

## Changes

### 1. Test Suite (Commit: dc59fb9)
- **69 comprehensive tests** covering all requirements
  - 36 unit tests for helper functions
  - 33 CLI integration tests
- Synthetic test fixtures with programmatic EXIF data
- Pytest configuration and shared fixtures

### 2. Implementation (Commit: 002604c)
- **Helper functions:**
  - `calculate_aspect_ratio()` - GCD-based ratio reduction
  - `classify_orientation()` - Portrait/landscape/square detection
  - `match_common_ratio()` - Match against 10 standard ratios (1:1, 4:3, 3:2, 16:9, 9:16, 4:5, 5:4, 3:4, 2:3, 1.91:1)
  - `extract_exif_data()` - EXIF metadata extraction
  - `format_exif_curated()` - Curated EXIF subset formatting
  - `get_image_info()` - Main metadata aggregation
  - `serialize_exif_value()` - JSON serialization for EXIF types

- **CLI command:**
  - Added `info` subcommand with positional `<file>` argument
  - Flags: `--json`, `--short`, `--exif`, `--exif-all`
  - Proper exit codes (0=success, 3=not found, 1=error, 2=invalid args)

- **Output formats:**
  - Default: Human-readable multi-line summary
  - `--json`: Single JSON object (JSONL-compatible)
  - `--short`: CSV line for batch processing
  - `--exif/--exif-all`: EXIF metadata display

### 3. CI/CD (Commit: 3baf778)
- GitHub Actions workflow for automated testing
- Tests across Python 3.8, 3.9, 3.10, 3.11
- Runs on all PRs and pushes to main/master

## Test Results

```
✓ 69/69 tests passing
  - Unit tests: 36/36
  - CLI tests: 33/33
```

## Examples

```bash
# Default human-readable output
python imagepro.py info photo.jpg

# JSON output
python imagepro.py info photo.jpg --json

# CSV for batch processing
for img in *.jpg; do python imagepro.py info "$img" --short >> info.csv; done
```

## Checklist

- [x] All tests passing locally
- [x] TDD approach followed (tests written first)
- [x] PRD Section 4.1 requirements met
- [x] CI workflow added
- [x] Multiple Python versions tested (3.8-3.11)
- [x] Updated TASKS.md with TODOs for resize tests
- [x] Added pytest to requirements.txt

## Related

- Addresses TASKS.md Section 1: "Implement imagepro info"
- Implements PRD Section 4.1 completely
