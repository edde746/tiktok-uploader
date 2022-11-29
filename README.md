# tiktok-uploader

Uses adb to automatically upload videos to TikTok. For educational purposes only.

## Running
```bash
# First time
brew install --cask android-sdk android-platform-tools
# Other OS: https://www.xda-developers.com/install-adb-windows-macos-linux/
pip install -r requirements.txt

# Run, it is recommended to write your own scripts
# Or you can use these examples
python greentext_slideshow.py
python youtube_reupload.py
```

## Script doesn't complete

You most likely need to update the resource ID at the end of `uploader.py` (see comment).
Find the resource ID by running `dump.py` while a video is uploading (progress bar in top left) and then searching for `%` in the `dump.xml` file.

## Why is this better than using web app with selenium?

Ability to add audio and upload slideshows, it is also less likely to be blocked and/or be obsolete.