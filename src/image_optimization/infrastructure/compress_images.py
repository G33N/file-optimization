from PIL import Image
import os

def transform_to_format(input_path, output_path, format):
    """
    Transforms an image to X format.

    Parameters:
    - input_path (str): Path to the input image file.
    - output_path (str): Path to save the X image.

    Returns:
    - None
    """
    try:

        img = Image.open(input_path)
        rgb_im = img.convert('RGB')
        rgb_im.save(output_path, format=format)

        output_formated_path = os.path.splitext(output_path)[0] + '.' + format.lower()

        print(f"Image transformed to {format} successfully and saved at {output_formated_path}")
        return output_formated_path
    except Exception as e:
        print(f"Error transforming image to {format}: {e}")

import os

def split_aws_key(key):
    """
    Splits the AWS key into UUID and extension.

    Parameters:
    - key (str): AWS key.

    Returns:
    - uuid (str): UUID of the key.
    - extension (str): Extension of the key.
    """
    try:
        filename, _ = os.path.splitext(key)
        uuid = filename.split('/')[-1]
        extension = os.path.splitext(key)[1]
        
        return uuid, extension
    
    except Exception as e:
        print(f"Error splitting AWS key: {e}")

def clean_tmp_files(file):
    """
    Cleans temporary files created during the process.

    Parameters:
    - None

    Returns:
    - None
    """
    try:
        if os.path.exists(file):
            os.remove(file)
        print("Temporary files cleaned successfully")
    except Exception as e:
        print(f"Error trying to remove: {e}")

def remove_output_files(output_path):
    """
    Removes the output files.

    Parameters:
    - output_path (str): Path to the output file.

    Returns:
    - None
    """
    try:
        if os.path.exists(output_path):
            os.remove(output_path)
        print(f"Output files removed successfully")
    except Exception as e:
        print(f"Error trying to remove: {e}")

def compress_image(key,input_path, output_path, quality= 85, format="JPEG"):
    """
    Compresses an image.

    Parameters:
    - input_path (str): Path to the input image file.
    - output_path (str): Path to save the compressed image.
    - quality (int): Compression quality (0 to 100). Higher values mean better quality.

    Returns:
    - None
    """
    try:
        img = Image.open(input_path)
        if img.format != "WEBP":
            uuid, extension = split_aws_key(key)

            img = Image.open(transform_to_format(input_path, 'input/tmp-'+uuid+'.'+format.lower(), format))
            clean_tmp_files(file='input/tmp-'+uuid+'.'+format.lower())

        file_name, _ = os.path.splitext(os.path.basename(input_path))
        output_formated_path = os.path.splitext(output_path)[0] + file_name + '.' + format.lower()
        img.save(output_formated_path, quality=quality, format=format)

        original_size = os.path.getsize(input_path)
        compressed_size = os.path.getsize(output_formated_path)
        optimization_percentage = ((original_size - compressed_size) / original_size) * 100

        print(f"Image compressed successfully and saved at {output_formated_path}")
        print(f"Original Size: {original_size} bytes")
        print(f"Compressed Size: {compressed_size} bytes")
        print(f"Optimization Percentage: {optimization_percentage:.2f}%")

        return file_name + '.' + format.lower()
    except Exception as e:
        print(f"Error compressing image: {e}")