# AI Image Renamer

This script uses an AI model to rename images based on their content. It leverages Vision LLM for image analysis and generates descriptive names.

## How it Works

1. **Image Analysis:** `image_name_generator.py` uses Vision LLM to analyze the image and generate a three-word name following specific rules.
2. **Renaming:**  `rename_image.py` uses the generated names to rename images within a specified folder. It handles various image formats, converts them to JPEG if necessary, and avoids overwriting existing files.

## Usage

1. **Install Dependencies:**  Run `pip install -r requirements.txt` to install the necessary packages.
2. **Set API Key:** Create a `.env` file in the root of your project and add the following line, replacing `your_actual_api_key` with your actual NVIDIA API key:

```NVIDIA_API_KEY=your_actual_api_key```

3. **Set Folder Path:** Modify the `folder_path` variable in `rename_image.py` to point to the folder containing the images you want to rename.
4. **Run:** Execute `python rename_image.py` to start the renaming process.

## Key Features

- Utilizes Vision LLM for accurate image analysis.
- Generates descriptive three-word names.
- Handles various image formats (JPG, PNG, GIF, BMP, TIFF, WebP, AVIF).
- Avoids overwriting existing files.
- Provides informative progress and error messages.

## Security

This script uses environment variables to securely store NVIDIA API key.  The `.env` file is not committed to version control, ensuring that your API key remains private. 

## Notes

- Requires a valid NVIDIA API key for accessing the Vision LLM.
- The script assumes the images are in a single folder.
- For large image files, consider using the assets API. 
- The necessary dependencies are listed in the `requirements.txt` file.