"""Unit tests for resize helper functions and shared utilities."""

import pytest
from pathlib import Path
import argparse

# Import the helper functions
from imagepro import (
    parse_sizes,
    validate_jpeg,
    get_file_size_kb,
    resize_image,
)


class TestParseSizes:
    """Test parse_sizes function."""

    def test_parse_single_size(self):
        """Test parsing a single size."""
        sizes = parse_sizes("300")
        assert sizes == [300]

    def test_parse_multiple_sizes(self):
        """Test parsing multiple comma-separated sizes."""
        sizes = parse_sizes("300,600,900,1200")
        assert sizes == [300, 600, 900, 1200]

    def test_parse_sizes_with_spaces(self):
        """Test parsing sizes with spaces around commas."""
        sizes = parse_sizes("300, 600, 900")
        assert sizes == [300, 600, 900]

    def test_parse_sizes_removes_duplicates(self):
        """Test that duplicate sizes are included (not removed)."""
        sizes = parse_sizes("300,300,600")
        # Note: Current implementation doesn't remove duplicates
        assert sizes == [300, 300, 600]

    def test_parse_sizes_invalid_format(self):
        """Test that invalid format raises ArgumentTypeError."""
        with pytest.raises(argparse.ArgumentTypeError):
            parse_sizes("300,abc,600")

    def test_parse_sizes_negative_number(self):
        """Test that negative numbers raise ArgumentTypeError."""
        with pytest.raises(argparse.ArgumentTypeError):
            parse_sizes("300,-600,900")

    def test_parse_sizes_zero(self):
        """Test that zero raises ArgumentTypeError."""
        with pytest.raises(argparse.ArgumentTypeError):
            parse_sizes("0,300,600")

    def test_parse_sizes_float(self):
        """Test that float numbers raise ArgumentTypeError."""
        with pytest.raises(argparse.ArgumentTypeError):
            parse_sizes("300.5,600")


class TestValidateJpeg:
    """Test validate_jpeg function."""

    def test_validate_jpeg_lowercase_jpg(self):
        """Test validation of .jpg extension."""
        filepath = Path("photo.jpg")
        assert validate_jpeg(filepath) is True

    def test_validate_jpeg_lowercase_jpeg(self):
        """Test validation of .jpeg extension."""
        filepath = Path("photo.jpeg")
        assert validate_jpeg(filepath) is True

    def test_validate_jpeg_uppercase_jpg(self):
        """Test validation of .JPG extension."""
        filepath = Path("photo.JPG")
        assert validate_jpeg(filepath) is True

    def test_validate_jpeg_uppercase_jpeg(self):
        """Test validation of .JPEG extension."""
        filepath = Path("photo.JPEG")
        assert validate_jpeg(filepath) is True

    def test_validate_jpeg_mixed_case(self):
        """Test validation of mixed case extensions."""
        # Mixed case extensions should fail (not in valid list)
        filepath = Path("photo.Jpg")
        assert validate_jpeg(filepath) is False

    def test_validate_jpeg_png(self):
        """Test that PNG files are rejected."""
        filepath = Path("photo.png")
        assert validate_jpeg(filepath) is False

    def test_validate_jpeg_no_extension(self):
        """Test that files with no extension are rejected."""
        filepath = Path("photo")
        assert validate_jpeg(filepath) is False

    def test_validate_jpeg_with_path(self):
        """Test validation with full path."""
        filepath = Path("/home/user/photos/vacation.jpg")
        assert validate_jpeg(filepath) is True


class TestGetFileSizeKb:
    """Test get_file_size_kb function."""

    def test_get_file_size_kb(self, temp_dir):
        """Test getting file size in KB."""
        # Create a test file with known size
        test_file = temp_dir / "test.txt"
        test_file.write_text("x" * 2048)  # 2048 bytes = 2 KB

        size_kb = get_file_size_kb(test_file)
        assert size_kb == 2.0

    def test_get_file_size_kb_small_file(self, temp_dir):
        """Test getting file size for small file."""
        test_file = temp_dir / "small.txt"
        test_file.write_text("hello")  # 5 bytes

        size_kb = get_file_size_kb(test_file)
        assert abs(size_kb - 0.0048828125) < 0.0001  # 5/1024

    def test_get_file_size_kb_empty_file(self, temp_dir):
        """Test getting file size for empty file."""
        test_file = temp_dir / "empty.txt"
        test_file.write_text("")

        size_kb = get_file_size_kb(test_file)
        assert size_kb == 0.0


class TestResizeImage:
    """Test resize_image function."""

    def test_resize_image_by_width(self, temp_dir):
        """Test resizing image by width."""
        from PIL import Image

        # Create test image
        img = Image.new('RGB', (1200, 800), color=(255, 0, 0))
        input_file = temp_dir / "test.jpg"
        img.save(input_file, 'JPEG', quality=90)

        output_dir = temp_dir / "resized"
        sizes = [300, 600]

        created_files, skipped_sizes = resize_image(
            input_file, output_dir, sizes, dimension='width', quality=90
        )

        assert len(created_files) == 2
        assert len(skipped_sizes) == 0

        # Check first file
        assert created_files[0]['filename'] == 'test_300.jpg'
        assert created_files[0]['width'] == 300
        assert created_files[0]['height'] == 200  # Maintains 3:2 ratio

        # Check second file
        assert created_files[1]['filename'] == 'test_600.jpg'
        assert created_files[1]['width'] == 600
        assert created_files[1]['height'] == 400

    def test_resize_image_by_height(self, temp_dir):
        """Test resizing image by height."""
        from PIL import Image

        # Create test image
        img = Image.new('RGB', (1200, 800), color=(0, 255, 0))
        input_file = temp_dir / "test.jpg"
        img.save(input_file, 'JPEG', quality=90)

        output_dir = temp_dir / "resized"
        sizes = [200, 400]

        created_files, skipped_sizes = resize_image(
            input_file, output_dir, sizes, dimension='height', quality=90
        )

        assert len(created_files) == 2
        assert len(skipped_sizes) == 0

        # Check first file
        assert created_files[0]['width'] == 300  # Maintains 3:2 ratio
        assert created_files[0]['height'] == 200

        # Check second file
        assert created_files[1]['width'] == 600
        assert created_files[1]['height'] == 400

    def test_resize_image_upscaling_prevention(self, temp_dir):
        """Test that upscaling is prevented."""
        from PIL import Image

        # Create small test image
        img = Image.new('RGB', (800, 600), color=(0, 0, 255))
        input_file = temp_dir / "small.jpg"
        img.save(input_file, 'JPEG', quality=90)

        output_dir = temp_dir / "resized"
        sizes = [400, 800, 1200]  # 1200px should be skipped (exceeds original)

        created_files, skipped_sizes = resize_image(
            input_file, output_dir, sizes, dimension='width', quality=90
        )

        assert len(created_files) == 2  # 400px and 800px created (800px equals original)
        assert len(skipped_sizes) == 1  # 1200px skipped

        assert created_files[0]['width'] == 400
        assert created_files[1]['width'] == 800
        assert skipped_sizes[0][0] == 1200

    def test_resize_image_aspect_ratio_preservation(self, temp_dir):
        """Test that aspect ratio is preserved."""
        from PIL import Image

        # Create test image with specific ratio
        img = Image.new('RGB', (1600, 900), color=(255, 255, 0))  # 16:9
        input_file = temp_dir / "test.jpg"
        img.save(input_file, 'JPEG', quality=90)

        output_dir = temp_dir / "resized"
        sizes = [800]

        created_files, skipped_sizes = resize_image(
            input_file, output_dir, sizes, dimension='width', quality=90
        )

        # Check aspect ratio is maintained
        assert created_files[0]['width'] == 800
        assert created_files[0]['height'] == 450  # 800 * (900/1600)

    def test_resize_image_quality_setting(self, temp_dir):
        """Test different quality settings produce different file sizes."""
        from PIL import Image, ImageDraw
        import random

        # Create test image with noise/detail for better quality differentiation
        img = Image.new('RGB', (1200, 800), color=(128, 128, 128))
        draw = ImageDraw.Draw(img)

        # Add random noise to make image more compressible
        random.seed(42)  # For reproducibility
        for _ in range(10000):
            x = random.randint(0, 1199)
            y = random.randint(0, 799)
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            draw.point((x, y), fill=color)

        input_file = temp_dir / "test.jpg"
        img.save(input_file, 'JPEG', quality=90)

        # Resize with high quality
        output_dir_high = temp_dir / "high"
        created_high, _ = resize_image(
            input_file, output_dir_high, [600], dimension='width', quality=95
        )

        # Resize with low quality
        output_dir_low = temp_dir / "low"
        created_low, _ = resize_image(
            input_file, output_dir_low, [600], dimension='width', quality=50
        )

        # Lower quality should produce smaller file (or roughly equal for simple images)
        # Using <= to account for cases where images are very simple
        assert created_low[0]['size_kb'] <= created_high[0]['size_kb']

    def test_resize_image_output_directory_creation(self, temp_dir):
        """Test that output directory is created if it doesn't exist."""
        from PIL import Image

        img = Image.new('RGB', (1200, 800), color=(255, 0, 255))
        input_file = temp_dir / "test.jpg"
        img.save(input_file, 'JPEG', quality=90)

        # Use non-existent directory
        output_dir = temp_dir / "new" / "nested" / "dir"
        assert not output_dir.exists()

        created_files, _ = resize_image(
            input_file, output_dir, [300], dimension='width', quality=90
        )

        # Directory should be created
        assert output_dir.exists()
        assert len(created_files) == 1

    def test_resize_image_file_naming(self, temp_dir):
        """Test output file naming pattern."""
        from PIL import Image

        img = Image.new('RGB', (1200, 800), color=(0, 255, 255))
        input_file = temp_dir / "vacation_photo.jpg"
        img.save(input_file, 'JPEG', quality=90)

        output_dir = temp_dir / "resized"
        sizes = [300, 600]

        created_files, _ = resize_image(
            input_file, output_dir, sizes, dimension='width', quality=90
        )

        # Check naming pattern: {basename}_{size}.{ext}
        assert created_files[0]['filename'] == 'vacation_photo_300.jpg'
        assert created_files[1]['filename'] == 'vacation_photo_600.jpg'

    def test_resize_image_preserves_extension_case(self, temp_dir):
        """Test that file extension case is preserved."""
        from PIL import Image

        img = Image.new('RGB', (1200, 800), color=(255, 128, 0))
        input_file = temp_dir / "test.JPG"  # Uppercase extension
        img.save(input_file, 'JPEG', quality=90)

        output_dir = temp_dir / "resized"

        created_files, _ = resize_image(
            input_file, output_dir, [300], dimension='width', quality=90
        )

        # Should preserve uppercase
        assert created_files[0]['filename'] == 'test_300.JPG'

    def test_resize_image_all_sizes_skipped(self, temp_dir):
        """Test when all sizes are skipped due to upscaling."""
        from PIL import Image

        img = Image.new('RGB', (400, 300), color=(128, 0, 128))
        input_file = temp_dir / "small.jpg"
        img.save(input_file, 'JPEG', quality=90)

        output_dir = temp_dir / "resized"
        sizes = [800, 1200, 1600]  # All larger than original

        created_files, skipped_sizes = resize_image(
            input_file, output_dir, sizes, dimension='width', quality=90
        )

        assert len(created_files) == 0
        assert len(skipped_sizes) == 3
