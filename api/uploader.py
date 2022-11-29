from uiautomator import Device
from time import sleep
import os,datetime,subprocess,json
config = json.loads(open('config.json', 'r').read())

# "Static" config
SD_CARD_INDEX = False
POSSIBLE_APPS = ['com.zhiliaoapp.musically', 'com.ss.android.ugc.trill']
RELATIVE_PATH = 'Pictures/TTUploader' # has to be it's own folder

d = Device(config['device'])
def adb(command):
    proc = subprocess.Popen('adb -s %s %s' % (config['device'], command), stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    return out.decode('utf-8')

device_size = (0,0)
def touch(x, y, relative=True):
    global device_size
    # coords are in percentage
    if device_size[0] == 0:
        device_size = (d.info['displayWidth'], d.info['displayHeight'])

    x = int(x * device_size[0]) if relative else x
    y = int(y * device_size[1]) if relative else y
    d.click(x, y)

    
def upload_tiktok(tiktok_audio=None, original_audio=1, added_audio=1, draft=False, description=None, photo_mode=False):
    # Find app
    packages = adb('shell pm list packages')
    for package in POSSIBLE_APPS:
        if package in packages:
            APP_NAME = package
            break

    if not APP_NAME:
        print('😵 TikTok not found')
        return

    # Kill tiktok app
    adb('shell am force-stop %s' % APP_NAME)

    # Delete old files on device
    adb('shell rm -rf /sdcard/%s' % RELATIVE_PATH)

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
        adb('push to_upload/%s /sdcard/%s/%s' % (new_name, RELATIVE_PATH, new_name))
        # Call the media scanner to add the video to the media content provider
        # I don't know why it's like this, but for some reason the first one only works on my emulator
        if SD_CARD_INDEX:
            adb('shell am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///sdcard/%s/%s' % (RELATIVE_PATH, new_name))
        else:
            adb('shell am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///storage/emulated/0/%s/%s' % (RELATIVE_PATH, new_name))
    
    # Start tiktok app
    start = adb('shell am start -n %s/com.ss.android.ugc.aweme.splash.SplashActivity' % APP_NAME)
    if 'does not exist.' in start:
        print('😵 Failed to start app')
        return

    # Click on the upload button
    d(text='Profile').wait.exists(timeout=10000)
    touch(0.5, 0.99)

    # Click on the gallery button
    d(text='Upload').click.wait()

    select_multiple = d(text='Select multiple')
    if select_multiple and not d(className='android.widget.CheckBox').info['checked']:
        select_multiple.click.wait()

    # Click on the first video
    for i in range(ITEM_COUNT):
        element = d(className="androidx.recyclerview.widget.RecyclerView") \
            .child(index=i).child(className="android.widget.FrameLayout").child(className="android.widget.TextView")
        

        if i == ITEM_COUNT - 1:
            element.click.wait()
        else:
            element.click()

    # Press Next
    next_button = d(text='Next')
    if not next_button:
        next_button = d(text='Next (%s)' % ITEM_COUNT)
    if not next_button:
        for text_view in d(className='android.widget.TextView'):
            if 'Next' in text_view.text:
                text_view.click.wait()
                break
    else:
        next_button.click.wait()

    if photo_mode:
        if not d(text='Switch to video mode'):
            # Press "Switch to photo mode" button
            d(text='Switch to photo mode').click.wait()

    if tiktok_audio:
        # Click audio button
        for layout in d(className="android.widget.LinearLayout"):
            if layout.info['clickable']:
                layout.click.wait()
                break
        # Click magnifying glass
        d(className='android.widget.ImageView')[0].click.wait()
        d(text='Search').set_text(tiktok_audio)
        d(text='Search').click.wait()

        # Click first result
        first_result = d(className="androidx.recyclerview.widget.RecyclerView") \
            .child(className="android.widget.LinearLayout")
        first_result.child(index=0).click()

        sleep(0.2)

        # Press check button
        first_result.child(className="android.widget.LinearLayout") \
            .child(className="android.widget.LinearLayout").click.wait()

        if original_audio != 1 or added_audio != 1:
            # Press 'Volume' button
            d(text='Volume').click.wait()

            # "android.widget.SeekBar"
            # 0 = original audio
            # 1 = added audio

            def set_seekbar(seekbar, value):
                target = seekbar.info['bounds']['left'] + ((seekbar.info['bounds']['right']-seekbar.info['bounds']['left']*0.985) * value)
                height = seekbar.info['bounds']['bottom'] - seekbar.info['bounds']['top']
                y = seekbar.info['bounds']['top'] + height / 2

                d.click(target, y)

            # Set original audio volume
            set_seekbar(d(className='android.widget.SeekBar', instance=0), original_audio / 2)

            # Set added audio volume
            set_seekbar(d(className='android.widget.SeekBar', instance=1), added_audio / 2)

            #  Press 'Done' button
            d(text='Done').click.wait()
        else:
            # Press the back button
            d.press.back()

    # Press 'Next' button
    d(text='Next').click.wait()

    if description:
        # Description
        d(className='android.widget.EditText').set_text(description)
        # Press back button
        d.press.back()

    if draft:
        # Press 'Save' button
        d(text='Drafts').click.wait()
    else:
        # Press 'Post' button
        d(text='Post', instance=1).click.wait()

    # Check if we got a prompt
    try:
        d(text='Post Now').click.wait(timeout=5000)
    except:
        pass

    # Wait until the upload is done
    d(resourceId='%s:id/hs0' % APP_NAME).wait.gone(timeout=1000*60*60*2)
    #                  ^^^^^ THIS (maybe) NEEDS TO BE UPDATED
    # I can't find a quick and reliable way to check if the upload is done, feel free to make a PR