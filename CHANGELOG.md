# Changelog

All notable changes to ImagePro will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Planned
- `imagepro rename` subcommand for fixing extensions and adding EXIF date prefixes
- `imagepro convert` subcommand for format conversion (HEIC to JPEG, etc.)
- Custom field selection for `imagepro info` command
- Bash utility scripts in `scripts/` directory
- `--strip-exif` option for commands that create file copies

---

## [1.1.0] - 2025-12-06

### Added
- HEIF/HEIC format support via `pillow-heif` package
- Comprehensive documentation updates (README, PRD, TASKS, CLAUDE.md)
- Test coverage improvements toward 100%
- Bash error handling patterns documented in README

### Changed
- Updated version to 1.1.0
- Improved test fixtures with synthetic EXIF data

---

## [1.0.0] - 2025-11-12

### Added
- Initial release of ImagePro CLI tool
- `imagepro info` subcommand for image metadata inspection
  - Pixel dimensions with EXIF orientation handling
  - Orientation classification (portrait, landscape, square)
  - Aspect ratio calculation using GCD
  - Common ratio matching (1:1, 4:3, 3:2, 16:9, 5:4, 4:5, 9:16, 1.91:1)
  - File metadata (name, path, size in KB)
  - EXIF extraction with curated subset (date taken, camera make/model, DPI)
  - Three output formats: default (human-readable), `--json`, `--short` (CSV)
  - `--exif` and `--exif-all` flags for EXIF data display
- `imagepro resize` subcommand for responsive image generation
  - Width-based resizing with `--width` option
  - Height-based resizing with `--height` option
  - Aspect ratio preservation
  - Upscaling prevention with warnings
  - JPEG quality control (1-100, default: 90)
  - Custom output directory with `--output`
  - Automatic output directory creation
  - EXIF stripping for web-optimized output
  - Lanczos resampling for high-quality results
- Comprehensive test suite (124 tests)
  - Unit tests for helper functions
  - CLI integration tests
  - Synthetic EXIF test fixtures
- GitHub Actions CI/CD pipeline
  - Automated testing on PRs
  - Multi-version Python support (3.8, 3.9, 3.10, 3.11)
- Error handling with specific exit codes
  - 0: Success
  - 1: Unsupported/unreadable format
  - 2: Invalid arguments
  - 3: File not found
  - 4: Cannot read/process image

### Technical Details
- Single-file architecture (`imagepro.py`)
- Python 3.8+ requirement
- Pillow dependency for image processing
- argparse subcommand pattern for CLI routing

---

## Document History

| Version | Date | Description |
|---------|------|-------------|
| 1.1.0 | 2025-12-06 | Added HEIF/HEIC support, improved test coverage |
| 1.0.0 | 2025-11-12 | Initial release with info and resize commands |
