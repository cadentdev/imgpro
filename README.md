# ImagePro

**Cross-platform image processing tools written in Python**

A command-line tool for generating multiple resolutions of images to support responsive web design workflows, specifically for static site generators like 11ty. ImagePro enables developers to create `srcset`-ready images from source files with configurable dimensions and quality settings.

## Features

### Info Command (v1.0)
- **Image Metadata Inspection**: View dimensions, orientation, aspect ratio, and file size
- **EXIF Support**: Extract and display EXIF metadata (camera, date, DPI, etc.)
- **Multiple Output Formats**: Human-readable, JSON, or CSV for batch processing
- **Common Aspect Ratios**: Automatic detection of standard ratios (16:9, 4:3, 1:1, Instagram 1.91:1, etc.)
- **Format Support**: Works with any Pillow-compatible format (JPEG, PNG, HEIF, etc.)

### Resize Command (v1.0)
- **Multiple Resolutions**: Generate multiple image sizes from a single source
- **Width/Height Based**: Resize by width or height while maintaining aspect ratio
- **Smart Upscaling Prevention**: Automatically skips sizes larger than the original
- **High-Quality Resampling**: Uses Lanczos algorithm for best quality
- **JPEG Optimization**: Control quality (1-100) with EXIF stripping by default
- **Organized Output**: Configurable output directory with clean naming (`photo_300.jpg`)
- **Format Support**: JPEG only in v1.0 (PNG, WebP, AVIF planned for future versions)

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/cadentdev/imagepro.git
   cd imagepro
   ```

2. **Install dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Make the script executable** (optional):
   ```bash
   chmod +x imagepro.py
   ```

### Dependencies

- **Pillow** (>=10.0.0): Python Imaging Library for image processing
- **pytest** (>=7.0.0): Testing framework (for development)

## Usage

ImagePro provides two main commands: `info` for inspecting image metadata and `resize` for generating multiple image sizes.

### Basic Syntax

```bash
# Info command - inspect image metadata
python3 imagepro.py info <file> [options]

# Resize command - generate multiple sizes
python3 imagepro.py resize --width <sizes> --input <file> [options]
python3 imagepro.py resize --height <sizes> --input <file> [options]
```

---

## Info Command

Inspect image files to view dimensions, orientation, aspect ratio, and EXIF metadata.

### Usage

```bash
python3 imagepro.py info <file> [options]
```

### Parameters

**Required:**
- `<file>`: Path to image file (supports JPEG, PNG, HEIF, and all Pillow-compatible formats)

**Optional:**
- `--json`: Output as JSON (JSONL-compatible)
- `--short`: Output as CSV line (for batch processing)
- `--exif`: Display curated EXIF metadata
- `--exif-all`: Display all EXIF tags

### Examples

#### Basic Image Info

```bash
python3 imagepro.py info photo.jpg
```

**Output:**
```
File: photo.jpg
Path: /home/user/photos/photo.jpg
Dimensions: 1920x1080
Orientation: landscape
Aspect Ratio: 16:9 (16:9)
File Size: 245.32 KB
EXIF Present: Yes
```

#### JSON Output

```bash
python3 imagepro.py info photo.jpg --json
```

**Output:**
```json
{"filename": "photo.jpg", "path": "/home/user/photos/photo.jpg", "width": 1920, "height": 1080, "orientation": "landscape", "ratio_raw": "16:9", "common_ratio": "16:9", "size_kb": 245.32, "has_exif": true, "creation_date": "2024:11:12 14:30:00", "exif": {"date_taken": "2024:11:12 14:30:00", "camera_make": "Canon", "camera_model": "Canon EOS 5D"}}
```

#### CSV Output for Batch Processing

```bash
# Generate CSV of all images in a directory
for img in *.jpg; do
  python3 imagepro.py info "$img" --short >> images.csv
done
```

**Output (images.csv):**
```
photo1.jpg,1920,1080,landscape,16:9,16:9,245.32,2024:11:12 14:30:00
photo2.jpg,1080,1920,portrait,9:16,9:16,189.45,2024:11:12 15:00:00
photo3.jpg,1000,1000,square,1:1,1:1,156.78,
```

#### View EXIF Metadata

```bash
python3 imagepro.py info photo.jpg --exif
```

**Additional output:**
```
EXIF Data:
  Date Taken: 2024:11:12 14:30:00
  Camera Make: Canon
  Camera Model: Canon EOS 5D Mark IV
  Orientation: 1
  Dpi X: 72.0
  Dpi Y: 72.0
```

---

## Resize Command

Generate multiple image sizes from a single source while maintaining aspect ratio.

### Usage

```bash
python3 imagepro.py resize --width <sizes> --input <file> [options]
python3 imagepro.py resize --height <sizes> --input <file> [options]
```

### Parameters

**Required:**
- `--width <sizes>` OR `--height <sizes>` (mutually exclusive)
  - Comma-separated list of integers
  - Example: `--width 300,600,900,1200`
- `--input <filepath>`
  - Path to source image file (JPEG only in v1.0)

**Optional:**
- `--quality <1-100>` (default: 90)
  - JPEG compression quality
- `--output <directory>` (default: `./resized/`)
  - Directory for output images
- `--help` / `-h`
  - Display usage information
- `--version` / `-v`
  - Display version number

### Examples

#### Resize to Multiple Widths

```bash
python3 imagepro.py resize --width 300,600,900,1200 --input photo.jpg
```

**Output:**
```
Processing: photo.jpg (2400x1600)
Output directory: ./resized/

✓ Created: photo_300.jpg (300x200, 45 KB)
✓ Created: photo_600.jpg (600x400, 128 KB)
✓ Created: photo_900.jpg (900x600, 256 KB)
✓ Created: photo_1200.jpg (1200x800, 412 KB)

Successfully created 4 image(s) from photo.jpg
```

#### Custom Quality and Output Directory

```bash
python3 imagepro.py resize --width 300,600 --input photo.jpg --quality 85 --output ~/web/images/
```

#### Resize by Height

```bash
python3 imagepro.py resize --height 400,800 --input banner.jpg
```

#### Batch Processing with Shell Loop

```bash
for img in *.jpg; do
  python3 imagepro.py resize --width 300,600,900 --input "$img"
done
```

#### Process with Find Command

```bash
find ./photos -name "*.jpg" | while read img; do
  python3 imagepro.py resize --width 300,600 --input "$img" --output ./resized/
done
```

## Testing

### Manual Testing

1. **Create a test image**:
   ```bash
   python3 -c "
   from PIL import Image, ImageDraw
   img = Image.new('RGB', (1200, 800), color='lightblue')
   draw = ImageDraw.Draw(img)
   draw.rectangle([100, 100, 1100, 700], outline='navy', width=5)
   draw.ellipse([300, 200, 900, 600], fill='yellow', outline='orange', width=3)
   img.save('test_photo.jpg', 'JPEG', quality=95)
   print('Created test_photo.jpg (1200x800)')
   "
   ```

2. **Test basic resize**:
   ```bash
   python3 imagepro.py resize --width 300,600,900 --input test_photo.jpg
   ```

3. **Verify output**:
   ```bash
   ls -lh resized/
   ```

4. **Test upscaling prevention**:
   ```bash
   python3 imagepro.py resize --width 300,600,1500 --input test_photo.jpg
   # Should skip 1500px with a warning
   ```

5. **Test error handling**:
   ```bash
   # Test missing file
   python3 imagepro.py resize --width 300 --input nonexistent.jpg

   # Test non-JPEG file
   touch test.png
   python3 imagepro.py resize --width 300 --input test.png
   ```

### Test Scenarios Covered

- ✓ Resize by width with multiple sizes
- ✓ Resize by height with multiple sizes
- ✓ Custom quality settings (1-100)
- ✓ Custom output directory
- ✓ Upscaling prevention with warnings
- ✓ File not found error handling
- ✓ Non-JPEG format rejection
- ✓ Mutually exclusive width/height validation
- ✓ Quality range validation
- ✓ EXIF metadata stripping
- ✓ Aspect ratio preservation

### Automated Testing

The project includes a comprehensive `pytest`-based test suite:

**Run all tests:**
```bash
python -m pytest tests/ -v
```

**Run with coverage report:**
```bash
python -m pytest tests/ --cov=imagepro --cov-report=term-missing
```

**Test Coverage:**
- **Info command:** 100% coverage (69 tests)
  - 36 unit tests for helper functions
  - 33 CLI integration tests
- **Resize command:** ~95% coverage (55 tests)
  - 28 unit tests for helper functions and shared utilities
  - 27 CLI integration tests
- **Overall project:** 46% coverage (124 total tests)

**CI/CD:**
- GitHub Actions automatically runs tests on all PRs
- Tests across Python 3.8, 3.9, 3.10, 3.11

See `PRD.md` (Section 5.6) and `TASKS.md` for the complete testing roadmap.

## Output File Naming

ImagePro uses a simple, predictable naming pattern:

**Pattern**: `{basename}_{size}.{ext}`

**Examples**:
- `photo.jpg` at 300px → `photo_300.jpg`
- `vacation.jpeg` at 600px → `vacation_600.jpeg`
- `banner.JPG` at 1200px → `banner_1200.JPG`

The size suffix represents the dimension specified (width or height) in pixels.

## Error Handling

ImagePro provides clear error messages and appropriate exit codes:

### Exit Codes

- `0` - Success
- `1` - Unsupported format
- `2` - Invalid arguments (quality, width/height conflict, etc.)
- `3` - File not found
- `4` - Cannot read/process image

### Common Errors

**File not found:**
```
Error: File not found: photo.jpg
```

**Unsupported format (v1.0 JPEG-only):**
```
Error: Unsupported format. Version 1.0 supports JPEG only.
Supported extensions: .jpg, .jpeg, .JPG, .JPEG
```

**Invalid quality value:**
```
Error: Quality must be between 1-100
```

**Both width and height specified:**
```
Error: Cannot specify both --width and --height
```

## Technical Details

### Image Processing

- **Resampling Algorithm**: Lanczos (high-quality downsampling)
- **Aspect Ratio**: Always preserved
- **Color Mode**: Converts to RGB for JPEG output
- **Transparency Handling**: Converts to white background for JPEG
- **EXIF Data**: Stripped by default for web optimization
- **ICC Profiles**: Maintained during conversion

### File System

- Creates output directory if it doesn't exist
- Supports absolute and relative paths
- Handles spaces and special characters in filenames
- Supports Unicode filenames

## Roadmap

See [PRD.md](PRD.md) for the complete product requirements and future enhancements.

### Planned Features

- **v1.0.x**: `imagepro info` subcommand for image metadata, orientation, aspect ratio, and EXIF inspection with JSON/CSV output.
- **v1.1**: Batch processing (multiple files, glob patterns, directories)
- **v1.2**: Advanced resizing (crop modes, fit modes)
- **v1.3**: Format support (PNG, WebP, AVIF, format conversion)
- **v1.4**: Metadata options (preserve EXIF, progressive JPEG)
- **v1.5**: Responsive web features (generate HTML srcset, picture elements)
- **v1.6**: Configuration files (presets, per-project config)
- **v2.0**: Advanced features (watermarking, filters, parallel processing)

## Development

### Project Structure

```
imagepro/
├── imagepro.py         # Main CLI tool
├── requirements.txt    # Python dependencies
├── PRD.md             # Product Requirements Document
└── README.md          # This file
```

### Adding New Commands

The script uses a subcommand architecture. To add a new command:

1. Create a command handler function (e.g., `cmd_convert`)
2. Add a subparser in the `main()` function
3. Set the function as the default handler: `parser.set_defaults(func=cmd_convert)`

Example structure:
```python
def cmd_convert(args):
    """Handle the convert subcommand."""
    # Implementation here
    pass

# In main():
convert_parser = subparsers.add_parser('convert', help='Convert image formats')
convert_parser.add_argument('--format', required=True)
convert_parser.set_defaults(func=cmd_convert)
```

## Contributing

This is currently a development project. For issues or feature requests, please refer to the [Product Requirements Document](PRD.md).

## License

[To be determined]

## Acknowledgments

- Built with [Pillow](https://pillow.readthedocs.io/) - The friendly PIL fork
- Designed for use with static site generators like [11ty](https://www.11ty.dev/)
