# IntelliRename

IntelliRename is an intelligent image renaming tool that uses AI to analyze image content and generate descriptive filenames. It leverages NVIDIA's Vision Language Model (LLM) for accurate image analysis and creates unique, meaningful names for your image files.

## How it Works

1. **Image Analysis:** `image_name_generator.py` uses Vision LLM to analyze each image and generate a descriptive three-word name following specific rules.
2. **Renaming:** `rename_image.py` uses the generated names to rename images within a specified folder. It handles various image formats, converts them to JPEG if necessary, and avoids overwriting existing files.

## Key Features

- Utilizes NVIDIA's Vision LLM for accurate image analysis
- Generates descriptive three-word names for images
- Handles various image formats (JPG, PNG, GIF, BMP, TIFF, WebP, AVIF)
- Converts non-JPEG images to JPEG format
- Avoids overwriting existing files
- Provides informative progress and error messages

## Setup and Usage

1. **Clone the Repository:**
   ```sh
   git clone https://github.com/ad1tyac0des/IntelliRename
   cd IntelliRename
   ```

2. **Run the Setup Script:**
   - On Linux or macOS:
     ```sh
     ./run.sh
     ```
   - On Windows:
     ```powershell
     .\run.ps1
     ```

   These scripts will:
   - Install necessary dependencies
   - Create a `.env` file (if not present)
   - Prompt for your NVIDIA API key (if not already set)
   - Run the main script

## Obtaining your NVIDIA API Key

To get your NVIDIA API key, visit the [NVIDIA NIM](https://build.nvidia.com), sign in or create an account, and generate a new API key. 

## Requirements

- Python 3.8 or higher
- NVIDIA API key for accessing Vision LLM
- Dependencies listed in `requirements.txt`

## Security

This script uses environment variables to securely store the NVIDIA API key. The `.env` file is not committed to version control, ensuring that your API key remains private.

## Notes

- The script assumes all images are in a single folder.
- For best results, ensure your images are clear and well-lit.
- Processing time may vary depending on the number and size of images.

## Contributing

Contributions to IntelliRename are welcome! Please feel free to submit a Pull Request.
