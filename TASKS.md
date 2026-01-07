# ImgPro Task List

This document tracks implementation progress based on `PRD.md`.

**Last Updated:** 2026-01-07

---

## 📋 In Progress / Planned

### 6. Align `imgpro resize` with PRD (Section 4.2) - Backlog

> **Note:** Current code uses `--input`; PRD specifies positional `<file>`. Tests are complete but CLI needs refactoring.

- [ ] Refactor CLI to match PRD
  - [ ] Introduce positional `<file>` for `resize`
  - [ ] Keep `--input` working for backwards compatibility (or plan breaking change)
  - [ ] Ensure help text matches PRD style

- [ ] Update documentation
  - [ ] Update `README.md` examples to use positional `<file>`
  - [ ] Update help text to match PRD

### 7. Enhanced `imgpro info` Field Selection (Section 4.1 of PRD) - Priority 4

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

---

## 🎯 Future Enhancements

### Nice-to-Haves (PRD Section 7.x)

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

- [ ] Script: `generate-responsive-set.sh` (lower priority)
  - [ ] Create multiple width versions for srcset
  - [ ] Output organized for HTML integration

- [ ] Convert command enhancements
  - [ ] Add `--no-srgb` flag to skip sRGB conversion

---

## 📊 Project Status

**Current Version:** 1.2.0
**Test Coverage:** ~50% (311 tests)

- Info command: 100% (69 tests)
- Resize command: ~95% (55 tests)
- Convert command: 100% (52 tests)
- Rename command: 100% (50 tests)

**Next Priorities (in order):**

1. Add field selection to `imgpro info` command
2. Align `imgpro resize` CLI with PRD (positional file argument)
3. Add `--verbose` and `--quiet` modes

**Core Principle:** All file-modifying commands create copies by default (non-destructive).

**See also:** `DONE.md` for completed tasks archive.
