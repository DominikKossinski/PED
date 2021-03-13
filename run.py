import pandas as pd
import json
import os
from categories import get_categories_dict
import string
from tokenizers import Tokenizer
import nltk

def main():
    stemmer = nltk.SnowballStemmer("english", ignore_stopwords=True)
    print(stemmer.stem("can't"))
    gb_videos = pd.read_csv(os.path.join("youtube_data", "GB_videos_5p.csv"), sep=";")
    # for i in range(len(gb_videos)):
    #     print(i)
    #     text = gb_videos["description "].iloc[i]
    # text = "Click here to continue the story and make your own monster:\nhttp://bit.ly/2mboXgj\n\nJoe befriends a noisy Monster under his bed but the two have so much fun together that he can't get to sleep, leaving him tired by day. For Christmas Joe receives a gift to help him finally get a good night’s sleep.\n\nShop the ad\nhttp://bit.ly/2hg04Lc\n\nThe music is Golden Slumbers performed by elbow, the original song was by The Beatles. \nFind the track:\nhttps://Elbow.lnk.to/GoldenSlumbersXS\n\nSubscribe to this channel for regular video updates\nhttp://bit.ly/2eU8MvW\n\nIf you want to hear more from John Lewis:\n\nLike John Lewis on Facebook\nhttp://www.facebook.com/johnlewisretail\n\nFollow John Lewis on Twitter\nhttp://twitter.com/johnlewisretail\n\nFollow John Lewis on Instagram\nhttp://instagram.com/johnlewisretail"
    text = "Today I show you how to completely dry a shirt or any other piece of clothing in 30 seconds or less. I recently discovered this amazing trick that can dry any piece of clothing incredibly fast! I didn't believe my eyes as my shirt magically became bone dry in a matter of seconds. I thought this method was too good to keep to myself, so I decided to make this video to share it with the world. Sick of waiting for your clothes to dry? Simply follow the step by step instructions in this video.\\n\\nDon't keep this lightning fast clothes drying technique to yourself! SHARE IT: \\nTWEET IT► https://ctt.ec/89bMT \\nEGGBOOK IT► http://bit.ly/ShirtDryLifeHack \\n\\nClick Here To Eggscribe! --►\\n\u202ahttp://bit.ly/Eggscribe\\n\\nHave a video Suggestion? Post it in the Comments Section, Contact me through my Facebook page or Tweet me!\\n\\nConnect with me!\\nFacebook ► \u202ahttp://www.facebook.com/HowToBasic\u202c\\nTwitter ► \u202ahttp://www.twitter.com/HowToBasic\u202c\\nInstagram ► \u202ahttp://instagram.com/HowToBasic\u202c\\n2ND Channel ► \u202ahttp://www.youtube.com/HowToBasic2\u202c\\n \\nT-Shirts & Eggy Merchandise ► \u202ahttp://howtobasic.spreadshirt.com/\\n\\nKnow someone that would be interested in this life hack? Link them to this video!"
    # text = "Trust us, there's nowhere else in the universe that you'll see something like this. GMM #1217\nWatch GMMore: https://youtu.be/qfBLDHxHb6Q | Part 3: https://youtu.be/BsfhHKx6ajA\nWatch today's episode from the start: http://bit.ly/GMM1217\n\nPick up all of the official GMM merch only at https://mythical.store\n\nFollow Rhett & Link: \nInstagram: https://instagram.com/rhettandlink\nFacebook: https://facebook.com/rhettandlink\nTwitter: https://twitter.com/rhettandlink\nTumblr: https://rhettandlink.tumblr.com\nSnapchat: @realrhettlink\nWebsite: https://mythical.co/\n\nCheck Out Our Other Mythical Channels:\nGood Mythical MORE: https://youtube.com/goodmythicalmore\nRhett & Link: https://youtube.com/rhettandlink\nThis Is Mythical: https://youtube.com/thisismythical\nEar Biscuits: https://applepodcasts.com/earbiscuits\n\nWant to send us something? https://mythical.co/contact\nHave you made a Wheel of Mythicality intro video? Submit it here: https://bit.ly/GMMWheelIntro\n\nIntro Animation by Digital Twigs: https://www.digitaltwigs.com\nIntro & Outro Music by Jeff Zeigler & Sarah Schimeneck https://www.jeffzeigler.com\nWheel of Mythicality theme: https://www.royaltyfreemusiclibrary.com/\nAll Supplemental Music fromOpus 1 Music: https://opus1.sourceaudio.com/\nWe use ‘The Mouse’ by Blue Microphones https://www.bluemic.com/mouse/\n\nNo alpacas were harmed or found themselves attracted to Abraham Lincoln during the making of this segment."
    print(text)
    print(Tokenizer.tokenize(text))
    print(string.punctuation)
    get_categories_dict()
    exit(-4561)
    gb_videos = pd.read_csv(os.path.join("youtube_data", "GB_videos_5p.csv"), sep=";")
    print(gb_videos.head(20))
    print(gb_videos.shape)
    print(gb_videos.columns)
    print(gb_videos.dtypes)
    with open(os.path.join("youtube_data", "GB_category_id.json"), "r") as file:
        gb_category = json.load(file)
        file.close()
    print(len(gb_category["items"]))


if __name__ == '__main__':
    main()
