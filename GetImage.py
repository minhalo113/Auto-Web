from GetTranscript import get_transcript
import requests


def getImage():
    transcripts = get_transcript()
    imagePrompt = transcripts[0]

    S = requests.Session()

    url = "https://en.wikipedia.org/w/api.php"
    PARAMS = {
        "action": "query",
        "format": "json",
        "titles": "Albert Einstein",
        "prop": "images"
    }
    response = S.get(url= url, params=PARAMS)
    data = response.json()

    pages = data['query']['pages']

    for page_id, page_info in pages.items():
        if 'images' in page_info:
            for img in page_info['images']:
                print(img['title'])
    print(imagePrompt)
    #return images

if __name__ == "__main__":
    images = getImage()
