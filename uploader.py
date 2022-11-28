from uiautomator import device as d
from time import sleep
import os,datetime

APP_NAME = 'com.ss.android.ugc.trill'

TIKTOK_AUDIO = 'lil droptop opp smoker 3'
ORIGINAL_AUDIO = 0
ADDED_AUDIO = 1

DESCRIPTION = 'test'
DRAFT = False

# Kill tiktok app
os.system('adb shell am force-stop %s' % APP_NAME)

# Copy files to device
ITEM_COUNT = len(os.listdir('to_upload'))
UPLOADED_FILES = []
for file in os.listdir('to_upload'):
    # Rename files to a number
    # get date and time with ms
    time_str = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
    new_name = '%s.%s' % (time_str, file.split('.')[-1])
    UPLOADED_FILES.append(new_name)
    os.rename('to_upload/%s' % file, 'to_upload/%s' % new_name)
    os.system('cd to_upload && adb push %s /sdcard/' % new_name)
    # Call the media scanner to add the video to the media content provider
    os.system('adb shell am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///sdcard/%s' % new_name)

# Start tiktok app
os.system('adb shell am start -n %s/com.ss.android.ugc.aweme.splash.SplashActivity' % APP_NAME)

# Click on the upload button
d(resourceId='%s:id/e51' % APP_NAME).click.wait()

# Click on the gallery button
d(resourceId='%s:id/ibr' % APP_NAME).click.wait()

# Click on the first video
for i in range(ITEM_COUNT):
    element = d(resourceId='%s:id/cek' % APP_NAME) \
    .child(index=i) \
    .child(resourceId='%s:id/c2b' % APP_NAME) \
    .child(resourceId='%s:id/csr' % APP_NAME)

    if i == ITEM_COUNT - 1:
        element.click.wait()
    else:
        element.click()

# Press next button (h1s)
d(resourceId='%s:id/h1s' % APP_NAME).click.wait()

if TIKTOK_AUDIO:
    # Click audio button (amo)
    d(resourceId='%s:id/amo' % APP_NAME).click.wait()
    # Click magnifying glass
    d(className='android.widget.ImageView', instance=0).click.wait()
    d(text='Search').set_text(TIKTOK_AUDIO)
    d(text='Search').click.wait()

    # Click on: resource: dyr > TextView
    d(resourceId='%s:id/dyr' % APP_NAME) \
    .child(className='android.widget.TextView').click.wait()

    # Press e0b
    d(resourceId='%s:id/e0b' % APP_NAME).click.wait()

    if ORIGINAL_AUDIO != 1 or ADDED_AUDIO != 1:
        # Press 'Volume' button
        d(text='Volume').click.wait()

        # "android.widget.SeekBar"
        # 0 = original audio
        # 1 = added audio

        def set_seekbar(seekbar, value):
            # drag from left to right
            # seekbar = d(className='android.widget.SeekBar', instance=seekbar)
            print(value)
            drag_to = seekbar.info['bounds']['left'] + ((seekbar.info['bounds']['right']-seekbar.info['bounds']['left']*0.985) * value)
            print(drag_to)
            height = seekbar.info['bounds']['bottom'] - seekbar.info['bounds']['top']
            y = seekbar.info['bounds']['top'] + height / 2

            d.click(drag_to, y)

        # Set original audio volume
        set_seekbar(d(className='android.widget.SeekBar', instance=0), ORIGINAL_AUDIO / 2)

        # Set added audio volume
        set_seekbar(d(className='android.widget.SeekBar', instance=1), ADDED_AUDIO / 2)

        #  Press 'Done' button
        d(text='Done').click.wait()

# Press 'Next' button
d(text='Next').click.wait()

# Description: class="android.widget.EditText"
d(className='android.widget.EditText').set_text(DESCRIPTION)
# Press back button
d.press.back()

if DRAFT:
    # Press 'Save' button
    d(text='Drafts').click.wait()
else:
    # Press 'Post' button
    d(text='Post', instance=1).click.wait()

# Wait until hs2 is gone
d(resourceId='%s:id/hs2' % APP_NAME).wait.gone(timeout=120000)

# Delete files from device
for file in UPLOADED_FILES:
    os.system('adb shell rm /sdcard/%s' % file)

print('Uploaded!')