import os
import requests
import time

# Set the server URL
base_url = "http://127.0.0.1:8000"

def upload_image(file_path):
    """Upload an image to the slice API."""
    with open(file_path, "rb") as file:
        response = requests.post(f"{base_url}/slice/", files={"file": file})
    response_data = response.json()
    session_id = response_data.get("session_id")
    if not session_id:
        raise Exception("Failed to get session_id from the response")
    return session_id

def check_processing_complete(session_id):
    """Check if processing is complete by comparing input and processed patches."""
    input_dir = os.path.join('temp', session_id, 'input_data')
    processed_dir = os.path.join('temp', session_id, 'processed_data')
    
    input_files = set(os.listdir(input_dir))
    processed_files = set(os.listdir(processed_dir))
    
    return len(input_files) == len(processed_files)

def request_stitch(session_id, save_path):
    """Request the stitched image."""
    response = requests.post(f"{base_url}/stitch/", json={"session_id": session_id, "save_path":save_path})
    response_data = response.json()
    stitched_image_path = response_data.get("stitched_image_path")
    if not stitched_image_path:
        raise Exception("Failed to get stitched_image_path from the response")
    return stitched_image_path

if __name__ == "__main__":
    # Path to the image to be uploaded
    image_path = r"images\test_image.jpg" 
    save_path = r"big_image_result"
    
    try:
        # Step 1: Upload the image to slice API
        session_id = upload_image(image_path)
        print(f"Image uploaded successfully. Session ID: {session_id}")
        
        # Step 2: Wait for the processing to complete
        print("Waiting for processing to complete...")
        while not check_processing_complete(session_id):
            time.sleep(5)  # Wait for 5 seconds before checking again
        
        # Step 3: Request the stitched image
        stitched_image_path = request_stitch(session_id, save_path)
        print(f"Stitched image path: {stitched_image_path}")
    
    except Exception as e:
        print(f"An error occurred: {e}")
