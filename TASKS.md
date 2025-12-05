# ImagePro Task List

This document outlines the next implementation steps based on the current `PRD.md`.

## 1. Implement `imagepro info` (Section 4.1 of PRD)

- **[ ] Core CLI wiring**
  - Add an `info` subcommand to `imagepro.py`.
  - Use positional `<file>` argument: `imagepro info <file> [options]`.
  - Add flags: `--json`, `--short`, `--exif`, `--exif-all`.

- **[ ] Core behavior**
  - Open the file with Pillow; fail cleanly if unreadable or unsupported (e.g., MP4).
  - Read pixel dimensions, taking EXIF orientation into account.
  - Classify orientation: `portrait`, `landscape`, `square`.
  - Compute reduced integer aspect ratio (`ratio_raw`) using GCD.
  - Match `ratio_raw` exactly against common ratios from PRD (e.g., `1:1`, `4:3`, `3:2`, `16:9`, `5:4`, `4:5`, `9:16`, `1.91:1`).
  - Report `common_ratio` or `none`.

- **[ ] File and EXIF metadata**
  - Report filename, path, file size in KB.
  - Detect presence of EXIF.
  - Extract curated EXIF subset (date taken, make, model, orientation, DPI fields) as described in PRD.
  - Add `--exif-all` support to dump all EXIF tags.

- **[ ] Output formats**
  - Default: human-readable multi-line summary.
  - `--json`: one JSON object per invocation (JSONL-friendly), including core fields and EXIF subset.
  - `--short`: one CSV line per invocation, using a fixed column order (see PRD 4.1 for canonical list).

- **[ ] Error handling & exit codes**
  - Use existing exit code scheme from `imagepro.py` / `README.md` (see PRD 4.5 and 9.4).
  - Ensure errors go to stderr; normal output goes to stdout.

## 2. Align `imagepro resize` with PRD (Section 4.2)

> Note: Current code still uses `--input`; PRD is forward-looking with positional `<file>`.

- **[ ] Refactor CLI**
  - Introduce positional `<file>` for `resize` while keeping `--input` working for now (backwards compatibility), or plan a breaking change with clear versioning.
  - Ensure help text and usage examples match the PRD style.

- **[ ] Confirm behavior matches spec**
  - Verify width/height mutual exclusion and validation.
  - Confirm upscaling prevention and skipped-size messages.
  - Confirm output directory behavior and naming pattern `{basename}_{size}.{ext}`.
  - Confirm EXIF stripping and ICC profile preservation align with PRD.

- **[ ] Update docs**
  - Once CLI refactor is done, update `README.md` examples to use positional `<file>` consistently.

## 3. Prepare for `imagepro convert` (Section 4.3)

- **[ ] Design initial `convert` CLI**
  - Subcommand shape: `imagepro convert <source> --format <target_format> [options]`.
  - Decide initial supported target formats (at least `jpeg` and `png`).

- **[ ] Implementation plan**
  - Identify shared helpers between `resize` and `convert` (e.g., file validation, Pillow open/save wrappers).
  - Define output naming and default output directory rules in line with PRD.

- **[ ] Defer actual implementation**
  - Do not implement until `info` is solid and tested; treat this as a follow-up milestone.

## 4. Testing & TDD Setup (Section 5.6)

- **[ ] Add pytest to the project**
  - Ensure `pytest` is listed in development dependencies (e.g., `requirements.txt` or a separate dev requirements file).
  - Create a `tests/` directory.

- **[ ] Unit tests for `info`-related helpers**
  - Add new tests for `info`-related helpers:
    - Aspect ratio calculation and common ratio matching.
    - Orientation classification.
    - EXIF extraction logic (using small test images or fixtures).

- **[ ] CLI integration tests for `info`**
  - Use `pytest` to invoke `imagepro.py` (e.g., via `subprocess`) for:
    - `imagepro info` success and error paths.
    - Test `--json`, `--short`, `--exif`, `--exif-all` flags.
  - Assert on exit codes and key stderr/stdout fragments.

- **[ ] Unit tests for `resize` helpers (TODO - add later)**
  - Add tests for existing helpers in `imagepro.py` (e.g., `parse_sizes`, `validate_jpeg`, `get_file_size_kb`).
  - Test edge cases for resize logic (upscaling prevention, aspect ratio preservation).

- **[ ] CLI integration tests for `resize` (TODO - add later)**
  - Use `pytest` to invoke `imagepro.py` (e.g., via `subprocess`) for:
    - `imagepro resize` success and error paths.
    - Test width/height mutual exclusion.
    - Test quality validation and output directory creation.
  - Assert on exit codes and key stderr/stdout fragments.

- **[ ] Adopt TDD for new features**
  - For future features (`info` refinements, `convert`), write failing tests first using the PRD sections as the source of truth.
  - Keep coverage high (>80% on core logic) with emphasis on file handling, EXIF, and aspect-ratio edge cases.

## 5. Nice-to-Haves / Future Iterations

- **[ ] Add `--verbose` and `--quiet` modes (PRD 4.6.3–4.6.4).**
- **[ ] Explore batch-oriented UX once single-file flows are stable (PRD 7.1).**
- **[ ] Revisit DPI reporting and additional EXIF fields based on real-world IG workflows.**
