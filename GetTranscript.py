from ScrapeContent import return_videos_list
from youtube_transcript_api import YouTubeTranscriptApi
from huggingface_hub import InferenceClient
from config import API_HUGGINGFACE_KEY

def write_video_ids_to_file(video_id, filename = 'already_use_video.txt'):
    with open(filename, 'a') as f:
        f.write(video_id + "\n")

def test_to_file(video_id, filename = 'test.txt'):
    with open(filename, 'w') as f:
        f.write(video_id + "\n")

def revise_script(text):
    # use model to revise script
    text = "Tell me more about this: " + text
    api_key = API_HUGGINGFACE_KEY

    refined_text =[]
    title = []

    client = InferenceClient(
        "HuggingFaceH4/zephyr-7b-beta",
        token=api_key,
    )

    for message in client.chat_completion(
        messages=[{"role": "user", "content": text}],
        max_tokens=2048,
        stream=True
    ):  
        refined_text.append(message.choices[0].delta.content)
    refined_text = "".join(refined_text)
    
    for message in client.chat_completion(
        messages=[{"role": "user", "content": 
                   "Create only one title for this paragraph, only answer the title, do not add any unnecessary word:" + refined_text}],
        max_tokens=50,
        stream=True,
        temperature=0.1
    ):  
        title.append(message.choices[0].delta.content)
    title = "".join(title)

    return  [refined_text, title]

def get_transcript():
    video = return_videos_list()
    write_video_ids_to_file(video['video_id'])
    script = ""

    # get script through audio
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video['video_id'])

        for entry in transcript:
            script = script + " " + entry["text"]

    except Exception as e:
        print("Error :", e)

    # revise script
    [finalize_script, title] = revise_script(script)
    return [script, finalize_script, title]

if __name__ == "__main__":
    get_transcript()