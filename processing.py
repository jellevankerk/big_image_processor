import os
import time
from PIL import Image
import numpy as np


def apply_threshold(image_path, threshold=128):
    """Apply a simple threshold to the image."""
    try:
        image = Image.open(image_path).convert('L')  # Convert to grayscale
        image_array = np.array(image)
        thresholded_array = (image_array > threshold) * 255  # Apply threshold
        thresholded_image = Image.fromarray(thresholded_array.astype(np.uint8))
        return thresholded_image
    except Exception as e:
        print(f"Error processing image {image_path}: {e}")
        return None

def check_patches_to_be_processed(input_dir):
    """
    Checks which files in the input_data subfolder do not have corresponding processed versions
    in the processed_data subfolder for each session_id folder in input_dir.
    If processed_data folder does not exist, it considers all files in input_data as not processed.

    Parameters:
    input_dir (str): The path to the directory containing session_id folders.

    Returns:
    dict: A dictionary where keys are session_ids and values are lists of files
          that are yet to be processed.
    """
    session_files_to_process = {}

    # Iterate through all session_id folders in the input directory
    for session_id in os.listdir(input_dir):
        session_path = os.path.join(input_dir, session_id)
        if not os.path.isdir(session_path):
            continue

        input_data_path = os.path.join(session_path, "input_data")
        processed_data_path = os.path.join(session_path, "processed_data")

        # Check if input_data folder exists
        if not os.path.exists(input_data_path):
            continue

        # Ensure processed_data folder exists
        if not os.path.exists(processed_data_path):
            continue

        # Get the list of files in input_data and processed_data folders
        input_files = set(os.listdir(input_data_path))
        processed_files = set(os.listdir(processed_data_path))

        # Find files that are not yet processed
        files_to_process = [file for file in input_files if file not in processed_files]

        if files_to_process:
            session_files_to_process[session_id] = files_to_process

    return session_files_to_process

def process_patches(input_dir, threshold=128, batch_size=10, poll_interval=5):
    """Continuously monitor the input directory for new patches and process them."""

    while True:
        session_files_to_process = check_patches_to_be_processed(input_dir)
        
        for session_id, files in session_files_to_process.items():
            input_data_path = os.path.join(input_dir, session_id, "input_data")
            processed_data_path = os.path.join(input_dir, session_id, "processed_data")

            # Process a batch of images
            for file in files[:batch_size]:
                input_path = os.path.join(input_data_path, file)
                output_path = os.path.join(processed_data_path, file)

                # Apply threshold and save the processed image
                thresholded_image = apply_threshold(input_path, threshold)
                if thresholded_image is not None:
                    thresholded_image.save(output_path)
                    print(f"Processed {file} in session {session_id}")
                else:
                    print(f"Skipping {file} due to an error.")
        print('Batch loop done')
        time.sleep(poll_interval)

# Example usage
if __name__ == "__main__":
    input_directory = r"temp"  # Replace with your input directory path
    threshold_value = 128  # Threshold value for processing
    batch_size = 10  # Number of images to process at a time
    polling_interval = 5  # Time in seconds to wait between checks

    process_patches(input_directory, threshold=threshold_value, batch_size=batch_size, poll_interval=polling_interval)

