import api.reddit as reddit,api.uploader as uploader,random,os,pytesseract

CHARACTER_LIMIT = 1000
AUDIOS = ['gracies abc yssn nino','lil droptop opp smoker 3']
DESCRIPTIONS = [
    '🥬',
    'green text',
    'i love green text',
    'green text is the best',
    'i want to be a green text',
    'green text is my favorite',
    'i made this green text',
    'green text is my life',
    'green text is my passion',
    'green text is my religion',
    'green text is my everything',
    'copilot wrote this',
    'green text is my favorite color',
    'green text is my favorite food',
    'green text is my favorite drink',
    'green text is my favorite animal',
    'text can be green',
    'when i grow up i want to be a green text',
    'what is green text',
    'where is green text',
    'where is text green',
    'how do i make text green',
    'how to make text green',
    'when the text is green',
]

def main():
    if not os.path.exists('to_upload'):
        os.mkdir('to_upload')

    print('🧹 Cleaning up...')
    for file in os.listdir('to_upload'):
        os.remove('to_upload/%s' % file)

    print('📂 Getting posts from reddit...')
    json = reddit.get_posts(subreddit='newgreentexts', time='year', limit=10)
    if not json:
        print('😵 Failed to get posts')
        return

    print('📸 Downloading images...')
    reddit.download_images(json)

    print('🔍 Checking font sizes...')
    for file in os.listdir('to_upload'):
        characters = pytesseract.image_to_boxes('to_upload/%s' % file)
        if characters.count('\n') > CHARACTER_LIMIT:
            print('🔥 %s is too big' % file)
            os.remove('to_upload/%s' % file)

    print('📤 Uploading images...')
    uploader.upload_tiktok(tiktok_audio=random.choice(AUDIOS), description=random.choice(DESCRIPTIONS), photo_mode=True)
    print('🎉 Done!')

if __name__ == '__main__':
    main()
