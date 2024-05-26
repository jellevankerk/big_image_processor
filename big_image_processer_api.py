import os
import shutil
import uuid

from fastapi import FastAPI, UploadFile, File
from PIL import Image
from pydantic import BaseModel

app = FastAPI()

class StitchRequest(BaseModel):
    session_id: str
    save_path: str

@app.post("/slice/")
async def slice_image(file: UploadFile = File(...), patch_size: int = 1024):
    # Create a unique directory for the session
    session_id = str(uuid.uuid4())
    os.makedirs(os.path.join('temp',session_id, 'input_data'), exist_ok=True)
    os.makedirs(os.path.join('temp',session_id, 'processed_data'), exist_ok=True)
    

    image = Image.open(file.file)
    image_name = os.path.splitext(file.filename)[0]
    width, height = image.size

    # Slice the image into patches
    for i in range(0, width, patch_size):
        for j in range(0, height, patch_size):
            box = (i, j, i + patch_size, j + patch_size)
            patch = image.crop(box)
            patch.save(os.path.join('temp', session_id, "input_data", f"{image_name}_{i}_{j}.png"))
    message = {"session_id": session_id, "message": "Image sliced successfully"}
    print(message)
    return message

@app.post("/stitch/")
async def stitch_image(request: StitchRequest):
    session_id = request.session_id
    save_path = request.save_path
    input_dir = os.path.join('temp', session_id)
    processed_data_path = os.path.join(input_dir, 'processed_data')

    if not os.path.exists(processed_data_path):
        return {"error": "Processed data not found"}

    patches = os.listdir(processed_data_path)
    if not patches:
        return {"error": "No patches to stitch"}

    # Assume patches are named as {image_name}_{i}_{j}.png
    patches.sort()
    image_name = '_'.join(patches[0].split('_')[:-2])
    patch_size = Image.open(os.path.join(processed_data_path, patches[0])).size[0]

    # Find the dimensions of the final stitched image
    x_coords = sorted(set(int(p.split('_')[-2]) for p in patches))
    y_coords = sorted(set(int(p.split('_')[-1].split('.')[0]) for p in patches))
    width = (x_coords[-1] // patch_size + 1) * patch_size
    height = (y_coords[-1] // patch_size + 1) * patch_size

    # Create an empty image to stitch the patches
    stitched_image = Image.new('L', (width, height))

    # Paste each patch into the final image
    for patch in patches:
        x = int(patch.split('_')[-2])
        y = int(patch.split('_')[-1].split('.')[0])
        patch_image = Image.open(os.path.join(processed_data_path, patch))
        stitched_image.paste(patch_image, (x, y))
    
    # Is currently saved locally, but on real system will be save on cloud storage
    stitched_image_path = os.path.join(save_path, f"{image_name}_stitched.png")
    stitched_image.save(stitched_image_path)
    
    # Removes the session_id data
    shutil.rmtree(input_dir)

    message = {"session_id": session_id, "message": "Image stitched successfully", "stitched_image_path": stitched_image_path}
    print(message)
    return message

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
