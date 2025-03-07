# PyVideo
This program is a media player where you can add, remove videos, and stream videos to a Chromecast and compatible devices.

The compatible Python version is 3.12.

# Requirements

1. Install Python version 3.12. and IDE in this proyect was used Pycharm Community Edition

2. Install required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. **Install ImageMagick to work with subtitles:**

    - Download the latest version of ImageMagick from [this link](https://imagemagick.org/script/download.php).
    - Example file to download: `ImageMagick-7.1.1-44-Q16-x64-dll.exe`.

4. **Set up environment variables on Windows:**

    - Go to "Environment Variables" in Windows.
    - In the "System variables" section, add a new variable.
    - The name of the variable should be `IMAGEMAGICK_BINARY`.
    - The value of the variable should be the following path:  
      `C:\Program Files\ImageMagick-7.1.1-Q16\magick.exe`.

    This will allow ImageMagick to function properly for subtitle operations.
