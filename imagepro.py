#!/usr/bin/env python3
"""
ImagePro - Command-line tool for responsive image processing
"""

import argparse
import sys
from pathlib import Path
from PIL import Image
import os
import json
import math

# Register HEIF opener if pillow-heif is available
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
except ImportError:
    pass  # pillow-heif not installed, HEIF support unavailable


__version__ = "1.1.0"


def parse_sizes(size_str):
    """Parse comma-separated list of sizes into integers."""
    try:
        sizes = [int(s.strip()) for s in size_str.split(',')]
        if any(s <= 0 for s in sizes):
            raise ValueError("Sizes must be positive integers")
        return sizes
    except ValueError as e:
        raise argparse.ArgumentTypeError(f"Invalid size format: {e}")


def validate_jpeg(filepath):
    """Validate that the file is a JPEG."""
    valid_extensions = ['.jpg', '.jpeg', '.JPG', '.JPEG']
    if filepath.suffix not in valid_extensions:
        return False
    return True


def get_file_size_kb(filepath):
    """Get file size in KB."""
    return os.path.getsize(filepath) / 1024


def calculate_aspect_ratio(width, height):
    """
    Calculate aspect ratio as a reduced integer ratio string.

    Args:
        width: Image width in pixels
        height: Image height in pixels

    Returns:
        String in format "W:H" (e.g., "16:9", "4:3")
    """
    gcd = math.gcd(width, height)
    ratio_w = width // gcd
    ratio_h = height // gcd
    return f"{ratio_w}:{ratio_h}"


def classify_orientation(width, height):
    """
    Classify image orientation based on dimensions.

    Args:
        width: Image width in pixels
        height: Image height in pixels

    Returns:
        String: "square", "landscape", or "portrait"
    """
    if width == height:
        return "square"
    elif width > height:
        return "landscape"
    else:
        return "portrait"


def match_common_ratio(ratio_str):
    """
    Match a ratio string against common aspect ratios.

    Args:
        ratio_str: Ratio string in format "W:H" (e.g., "16:9")

    Returns:
        String: matched common ratio name or "none"
    """
    # Define common ratios with their standard names
    common_ratios = {
        "1:1": "1:1",
        "4:3": "4:3",
        "3:4": "3:4",
        "3:2": "3:2",
        "2:3": "2:3",
        "16:9": "16:9",
        "9:16": "9:16",
        "5:4": "5:4",
        "4:5": "4:5",
        "191:100": "1.91:1",  # Instagram landscape
    }

    return common_ratios.get(ratio_str, "none")


def extract_exif_data(filepath):
    """
    Extract EXIF metadata from an image file.

    Args:
        filepath: Path to image file

    Returns:
        Dictionary of EXIF data or None if no EXIF present
    """
    try:
        img = Image.open(filepath)
        exif = img.getexif()

        if not exif:
            return None

        # Convert to dictionary with tag names
        from PIL.ExifTags import TAGS
        exif_dict = {}
        for tag_id, value in exif.items():
            tag_name = TAGS.get(tag_id, tag_id)
            exif_dict[tag_name] = value

        return exif_dict if exif_dict else None

    except Exception:
        return None


def format_exif_curated(exif_dict):
    """
    Format curated subset of EXIF data.

    Args:
        exif_dict: Dictionary of EXIF data

    Returns:
        Dictionary with curated EXIF fields using friendly names
    """
    if not exif_dict:
        return {}

    curated = {}

    # Date taken (prefer DateTimeOriginal, fall back to DateTime)
    if 'DateTimeOriginal' in exif_dict:
        curated['date_taken'] = exif_dict['DateTimeOriginal']
    elif 'DateTime' in exif_dict:
        curated['date_taken'] = exif_dict['DateTime']

    # Camera make and model
    if 'Make' in exif_dict:
        curated['camera_make'] = exif_dict['Make']
    if 'Model' in exif_dict:
        curated['camera_model'] = exif_dict['Model']

    # Orientation
    if 'Orientation' in exif_dict:
        curated['orientation'] = exif_dict['Orientation']

    # DPI/Resolution
    if 'XResolution' in exif_dict:
        curated['dpi_x'] = exif_dict['XResolution']
    if 'YResolution' in exif_dict:
        curated['dpi_y'] = exif_dict['YResolution']
    if 'ResolutionUnit' in exif_dict:
        curated['resolution_unit'] = exif_dict['ResolutionUnit']

    return curated


def get_image_info(filepath):
    """
    Get comprehensive information about an image file.

    Args:
        filepath: Path to image file

    Returns:
        Dictionary containing image metadata
    """
    filepath = Path(filepath)

    # Open image
    img = Image.open(filepath)

    # Get dimensions (EXIF orientation is already handled by Pillow in most cases)
    width, height = img.size

    # Calculate ratios and orientation
    ratio_raw = calculate_aspect_ratio(width, height)
    common_ratio = match_common_ratio(ratio_raw)
    orientation = classify_orientation(width, height)

    # Extract EXIF
    exif_data = extract_exif_data(filepath)
    has_exif = exif_data is not None and len(exif_data) > 0

    # Format curated EXIF
    exif_curated = format_exif_curated(exif_data) if has_exif else None

    # Get file metadata
    size_kb = get_file_size_kb(filepath)

    # Get creation date from EXIF if available
    creation_date = None
    if exif_curated and 'date_taken' in exif_curated:
        creation_date = exif_curated['date_taken']

    return {
        'filename': filepath.name,
        'path': str(filepath.absolute()),
        'width': width,
        'height': height,
        'orientation': orientation,
        'ratio_raw': ratio_raw,
        'common_ratio': common_ratio,
        'size_kb': size_kb,
        'has_exif': has_exif,
        'exif': exif_curated,
        'exif_all': exif_data,
        'creation_date': creation_date,
    }


def resize_image(input_path, output_dir, sizes, dimension='width', quality=90):
    """
    Resize an image to multiple sizes.

    Args:
        input_path: Path to input image
        output_dir: Directory for output images
        sizes: List of target sizes
        dimension: 'width' or 'height'
        quality: JPEG quality (1-100)

    Returns:
        List of created files with metadata
    """
    # Open and validate image
    try:
        img = Image.open(input_path)
    except Exception as e:
        print(f"Error: Cannot read image: {input_path}", file=sys.stderr)
        print(f"Details: {e}", file=sys.stderr)
        sys.exit(4)

    # Get original dimensions
    orig_width, orig_height = img.size

    # Prepare output
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Get base name and extension
    base_name = input_path.stem
    extension = input_path.suffix

    created_files = []
    skipped_sizes = []

    # Process each size
    for size in sizes:
        # Calculate new dimensions
        if dimension == 'width':
            if size > orig_width:
                skipped_sizes.append((size, f"original is only {orig_width}px wide"))
                continue
            new_width = size
            new_height = int((size / orig_width) * orig_height)
        else:  # height
            if size > orig_height:
                skipped_sizes.append((size, f"original is only {orig_height}px tall"))
                continue
            new_height = size
            new_width = int((size / orig_height) * orig_width)

        # Resize image using high-quality Lanczos resampling
        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Prepare output filename
        output_filename = f"{base_name}_{size}{extension}"
        output_path = output_dir / output_filename

        # Strip EXIF by converting to RGB if needed and not saving exif
        if resized_img.mode in ('RGBA', 'LA', 'P'):
            # Handle transparency by converting to RGB with white background
            background = Image.new('RGB', resized_img.size, (255, 255, 255))
            if resized_img.mode == 'P':
                resized_img = resized_img.convert('RGBA')
            background.paste(resized_img, mask=resized_img.split()[-1] if resized_img.mode in ('RGBA', 'LA') else None)
            resized_img = background
        elif resized_img.mode != 'RGB':
            resized_img = resized_img.convert('RGB')

        # Save without EXIF data
        resized_img.save(output_path, 'JPEG', quality=quality, optimize=True)

        # Get file size
        file_size = get_file_size_kb(output_path)

        created_files.append({
            'path': output_path,
            'filename': output_filename,
            'width': new_width,
            'height': new_height,
            'size_kb': file_size
        })

    return created_files, skipped_sizes


def serialize_exif_value(value):
    """Convert EXIF values to JSON-serializable types."""
    from PIL.TiffImagePlugin import IFDRational

    if isinstance(value, IFDRational):
        # Convert IFDRational to float
        return float(value)
    elif isinstance(value, bytes):
        # Convert bytes to string
        try:
            return value.decode('utf-8', errors='ignore')
        except:
            return str(value)
    elif isinstance(value, (tuple, list)):
        # Recursively handle tuples and lists
        return [serialize_exif_value(v) for v in value]
    elif isinstance(value, dict):
        # Recursively handle dicts
        return {k: serialize_exif_value(v) for k, v in value.items()}
    else:
        # Return as-is for JSON-serializable types
        return value


def cmd_info(args):
    """Handle the info subcommand."""
    input_path = Path(args.file)

    # Validate input file exists
    if not input_path.exists():
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        sys.exit(3)

    # Try to get image info
    try:
        info = get_image_info(input_path)
    except Exception as e:
        # If Pillow can't open it, it's unsupported or corrupt
        print(f"Error: Unsupported or unreadable image format: {args.file}", file=sys.stderr)
        sys.exit(1)

    # Determine output format
    if args.json:
        # JSON output
        output_data = {
            'filename': info['filename'],
            'path': info['path'],
            'width': info['width'],
            'height': info['height'],
            'orientation': info['orientation'],
            'ratio_raw': info['ratio_raw'],
            'common_ratio': info['common_ratio'],
            'size_kb': round(info['size_kb'], 2),
            'has_exif': info['has_exif'],
        }

        # Add creation date if available
        if info['creation_date']:
            output_data['creation_date'] = info['creation_date']
        else:
            output_data['creation_date'] = None

        # Add EXIF data based on flags (serialize for JSON compatibility)
        if args.exif_all and info['exif_all']:
            output_data['exif'] = {k: serialize_exif_value(v) for k, v in info['exif_all'].items()}
        elif info['exif']:
            output_data['exif'] = {k: serialize_exif_value(v) for k, v in info['exif'].items()}
        else:
            output_data['exif'] = None

        print(json.dumps(output_data))

    elif args.short:
        # CSV short output
        # Order: filename,width,height,orientation,ratio_raw,common_ratio,size_kb,creation_date
        fields = [
            info['filename'],
            str(info['width']),
            str(info['height']),
            info['orientation'],
            info['ratio_raw'],
            info['common_ratio'],
            f"{info['size_kb']:.2f}",
            info['creation_date'] if info['creation_date'] else ''
        ]
        print(','.join(fields))

    else:
        # Default human-readable output
        print(f"File: {info['filename']}")
        print(f"Path: {info['path']}")
        print(f"Dimensions: {info['width']}x{info['height']}")
        print(f"Orientation: {info['orientation']}")
        print(f"Aspect Ratio: {info['ratio_raw']}", end='')
        if info['common_ratio'] != 'none':
            print(f" ({info['common_ratio']})")
        else:
            print()
        print(f"File Size: {info['size_kb']:.2f} KB")
        print(f"EXIF Present: {'Yes' if info['has_exif'] else 'No'}")

        # Show EXIF data if requested or if present
        if (args.exif or args.exif_all) and info['has_exif']:
            print("\nEXIF Data:")
            if args.exif_all and info['exif_all']:
                # Show all EXIF tags
                for key, value in info['exif_all'].items():
                    print(f"  {key}: {value}")
            elif info['exif']:
                # Show curated EXIF
                for key, value in info['exif'].items():
                    # Format key nicely
                    formatted_key = key.replace('_', ' ').title()
                    print(f"  {formatted_key}: {value}")


def cmd_resize(args):
    """Handle the resize subcommand."""
    input_path = Path(args.input)

    # Validate input file exists
    if not input_path.exists():
        print(f"Error: File not found: {args.input}", file=sys.stderr)
        sys.exit(3)

    # Validate it's a JPEG
    if not validate_jpeg(input_path):
        print(f"Error: Unsupported format. Version 1.0 supports JPEG only.", file=sys.stderr)
        print(f"Supported extensions: .jpg, .jpeg, .JPG, .JPEG", file=sys.stderr)
        sys.exit(1)

    # Determine dimension and sizes
    if args.width and args.height:
        print("Error: Cannot specify both --width and --height", file=sys.stderr)
        sys.exit(2)
    elif args.width:
        dimension = 'width'
        sizes = parse_sizes(args.width)
    elif args.height:
        dimension = 'height'
        sizes = parse_sizes(args.height)
    else:
        print("Error: Must specify either --width or --height", file=sys.stderr)
        sys.exit(2)

    # Validate quality
    if not (1 <= args.quality <= 100):
        print("Error: Quality must be between 1-100", file=sys.stderr)
        sys.exit(2)

    # Get image dimensions for output
    try:
        with Image.open(input_path) as img:
            orig_width, orig_height = img.size
    except Exception as e:
        print(f"Error: Cannot read image: {input_path}", file=sys.stderr)
        sys.exit(4)

    # Print processing info
    print(f"Processing: {input_path.name} ({orig_width}x{orig_height})")
    print(f"Output directory: {args.output}")
    print()

    # Process the image
    created_files, skipped_sizes = resize_image(
        input_path,
        args.output,
        sizes,
        dimension=dimension,
        quality=args.quality
    )

    # Print results
    for file_info in created_files:
        print(f"✓ Created: {file_info['filename']} "
              f"({file_info['width']}x{file_info['height']}, "
              f"{file_info['size_kb']:.0f} KB)")

    # Print warnings for skipped sizes
    if skipped_sizes:
        print()
        for size, reason in skipped_sizes:
            print(f"⚠ Skipped {size}px: {reason}")

    # Print summary
    print()
    if created_files:
        print(f"Successfully created {len(created_files)} image(s) from {input_path.name}")
    else:
        print(f"Warning: No images created (all sizes would require upscaling)")
        sys.exit(0)


def main():
    """Main entry point for imagepro CLI."""
    parser = argparse.ArgumentParser(
        description='ImagePro - Command-line tool for responsive image processing',
        epilog='Use "imagepro.py <command> --help" for more information about a command.'
    )

    parser.add_argument('--version', '-v', action='version', version=f'ImagePro {__version__}')

    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Info command
    info_parser = subparsers.add_parser(
        'info',
        help='Display image information and metadata',
        description='Inspect an image file and report metadata, orientation, and aspect ratio'
    )

    info_parser.add_argument(
        'file',
        help='Path to image file'
    )

    info_parser.add_argument(
        '--json',
        action='store_true',
        help='Output in JSON format'
    )

    info_parser.add_argument(
        '--short',
        action='store_true',
        help='Output as a single CSV line'
    )

    info_parser.add_argument(
        '--exif',
        action='store_true',
        help='Show curated EXIF metadata'
    )

    info_parser.add_argument(
        '--exif-all',
        action='store_true',
        help='Show all EXIF metadata tags'
    )

    info_parser.set_defaults(func=cmd_info)

    # Resize command
    resize_parser = subparsers.add_parser(
        'resize',
        help='Resize images to multiple dimensions',
        description='Resize an image to multiple widths or heights while maintaining aspect ratio'
    )

    resize_parser.add_argument(
        '--width',
        type=str,
        help='Comma-separated list of target widths (e.g., 300,600,900)'
    )

    resize_parser.add_argument(
        '--height',
        type=str,
        help='Comma-separated list of target heights (e.g., 400,800)'
    )

    resize_parser.add_argument(
        '--input',
        required=True,
        help='Path to input image file'
    )

    resize_parser.add_argument(
        '--output',
        default='./resized/',
        help='Output directory (default: ./resized/)'
    )

    resize_parser.add_argument(
        '--quality',
        type=int,
        default=90,
        help='JPEG quality 1-100 (default: 90)'
    )

    resize_parser.set_defaults(func=cmd_resize)

    # Parse arguments
    args = parser.parse_args()

    # If no command specified, show help
    if not args.command:
        parser.print_help()
        sys.exit(0)

    # Execute the command
    args.func(args)


if __name__ == '__main__':
    main()
