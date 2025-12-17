# Changelog

All notable changes to ImgPro will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Planned
- Custom field selection for `imgpro info` command
- AVIF output format support
- `--no-srgb` flag for convert command
- `--verbose` and `--quiet` modes

---

## [1.2.0] - 2025-12-06

### Added
- **WebP output format support** for `imgpro convert` command
- **Batch processing scripts** in `scripts/` directory:
  - `rename-all.sh` - Add EXIF date prefix and correct extensions
  - `convert-all.sh` - Convert images to JPEG with sRGB profile
  - `resize-all.sh` - Resize images to specified width(s)
  - `organize-by-orientation.sh` - Organize by orientation or aspect ratio
- `scripts/README.md` with comprehensive usage examples
- sRGB color profile conversion (automatic) for convert command
- EXIF preservation by default in convert command
- `--strip-exif` flag for convert command

### Fixed
- Case-insensitive filesystem handling for rename command (macOS/Windows)

### Changed
- Default JPEG quality changed from 90 to 80 for convert command
- Updated documentation (README, TASKS, PRD) to reflect v1.2.0 features

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
- Initial release of ImgPro CLI tool
- `imgpro info` subcommand for image metadata inspection
  - Pixel dimensions with EXIF orientation handling
  - Orientation classification (portrait, landscape, square)
  - Aspect ratio calculation using GCD
  - Common ratio matching (1:1, 4:3, 3:2, 16:9, 5:4, 4:5, 9:16, 1.91:1)
  - File metadata (name, path, size in KB)
  - EXIF extraction with curated subset (date taken, camera make/model, DPI)
  - Three output formats: default (human-readable), `--json`, `--short` (CSV)
  - `--exif` and `--exif-all` flags for EXIF data display
- `imgpro resize` subcommand for responsive image generation
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
- Single-file architecture (`imgpro.py`)
- Python 3.8+ requirement
- Pillow dependency for image processing
- argparse subcommand pattern for CLI routing

---

## Document History

| Version | Date | Description |
|---------|------|-------------|
| 1.2.0 | 2025-12-06 | WebP support, batch scripts, sRGB conversion |
| 1.1.0 | 2025-12-06 | Added HEIF/HEIC support, rename/convert commands |
| 1.0.0 | 2025-11-12 | Initial release with info and resize commands |
