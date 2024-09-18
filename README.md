
# Discord Photo Storage Bot

This Python project automates the process of uploading images to a Discord channel for long-term storage, leveraging Discord's free user limit of 25MB per file. It filters through a specified image folder and uploads all supported image formats to the channel while ensuring no duplicate uploads using SHA256 hashing.

## Features
- **Uploads images**: Automatically uploads images from a local folder to a designated Discord channel.
- **Supported file formats**: `.heic`, `.jpeg`, `.jpg`, `.png`, `.bmp`, `.dng`, `.cr3`.
- **Batch uploading**: Uploads images in batches, respecting Discord’s file size limit of 25MB for free users.
- **SHA256 hashing**: Ensures no duplicate uploads by comparing the SHA256 hash of each file.
- **Resumable uploads**: Keeps track of uploaded images to avoid re-uploading the same files.

## Prerequisites
- Python 3.x
- `discord.py` library
- `tqdm` library for progress bar
- Discord bot token (see below for token setup)

## Installation

1. Clone this repository.
2. Install the required Python libraries:
    ```bash
    pip install discord tqdm
    ```
3. Set up a Discord bot and add it to your server. You can follow [this guide](https://discordpy.readthedocs.io/en/stable/discord.html) to get a bot token and invite the bot to your server.

## Configuration

- **TOKEN**: Replace the placeholder token in `main.py` with your actual Discord bot token. **Note: The token provided in this repository is a dummy token and won't work**.
- **CHANNEL_ID**: Replace the `CHANNEL_ID` in the script with the ID of the Discord channel where you want to upload the images.
- **MAIN_IMAGE_FOLDER**: Specify the path to the folder that contains the images you want to upload.

```python
TOKEN = 'YOUR_DISCORD_BOT_TOKEN'  # Replace with your actual bot token
CHANNEL_ID = 123456789012345678  # Replace with your Discord channel ID
MAIN_IMAGE_FOLDER = r'path_to_your_image_folder'  # Replace with your folder path
```

## Usage

1. Run the script:
    ```bash
    python main.py
    ```
2. The bot will log in to Discord and start uploading images from the specified folder to the designated channel in batches.
3. The progress of the upload will be displayed using the `tqdm` progress bar.

## Notes
- The **Discord bot token** provided in this repository is a **dummy token**. You must replace it with your actual bot token from Discord Developer Portal.
- The script filters images based on file size and supported formats and uploads only files smaller than 25MB, respecting Discord's free user limits.

## Future Enhancements
- Add support for more file formats.
- Implement better error handling and retries for failed uploads.

## License
This project is licensed under the MIT License.
