import api.uploader as uploader
import pytube,os

VIDEO_URL = 'https://www.youtube.com/watch?v=MVu496LdCko'

def main():
    if not os.path.exists('to_upload'):
        os.mkdir('to_upload')
        
    print('🧹 Cleaning up...')
    for file in os.listdir('to_upload'):
        os.remove('to_upload/%s' % file)

    print('📥 Downloading video...')
    youtube = pytube.YouTube(VIDEO_URL)
    video = youtube.streams.first()
    video.download('to_upload')

    print('📤 Uploading video...')
    uploader.upload_tiktok(description='I stole this video from YouTube')
    print('🥳 You\'re a thief!')

if __name__ == '__main__':
    main()