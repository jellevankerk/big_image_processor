# Large Image Processor for Machine Learning

This project involves creating a processing unit for machine learning models to efficiently handle very large images. This is particularly useful for tasks such as segmentation on satellite images or pathological slide images. These images are typically too large (greater than 1 GB and 10k x 10k pixels) to process at once.

## Getting Started

### Prerequisites

1. Python 3.8 or higher
2. Virtual environment (venv)
3. The following directories created manually:
   - `big_image_result`
   - `temp`

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-repo/large-image-processor.git
    cd large-image-processor
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

### Running the Project

Run the following scripts in separate terminal windows, in this order:

1. **Processing Script:**

    ```bash
    python processing.py
    ```

2. **API Script:**

    ```bash
    python big_image_processor_api.py
    ```

3. **Client Script:**

    ```bash
    python client.py
    ```

### Test Image

You can use the following test image for the project:
[Download Test Image](https://www.pexels.com/search/big%20size/)

## Project Structure

- **big_image_processor_api.py:** Handles slicing and stitching of large images.
- **processing.py:** Processes image patches using a simple thresholding algorithm.
- **client.py:** Client script to upload images, monitor processing, and request stitched images.

## How It Works

1. **Slicing:** The image is sliced into smaller patches.
2. **Processing:** Each patch is processed independently.
3. **Stitching:** The processed patches are stitched back together to form the final image.

## Current Limitations and Future Enhancements

### Limitations

- **Lack of Parallel Processing:** Currently processes patches sequentially.
- **Manual Orchestration:** Requires manual setup and monitoring.
- **Basic Segmentation Algorithm:** Uses a simple thresholding method.
- **Single Machine Limitation:** Designed to run on a single machine.

### Future Enhancements

- **Parallel Processing:** Implement parallel processing using multi-threading or multi-processing.
- **Distributed Processing:** Leverage distributed computing frameworks.
- **Advanced Machine Learning Models:** Integrate models like UNet or Mask R-CNN.
- **Containerization and Orchestration:** Use Docker and Kubernetes for better deployment.
- **Cloud Integration:** Store images and results in cloud storage solutions.


