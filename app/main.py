import os
from dotenv import load_dotenv
from moviepy.editor import VideoFileClip
from pytube import YouTube
from pydub import AudioSegment
from openai import OpenAI
import glob
import certifi

# Set the SSL_CERT_FILE environment variable
os.environ['SSL_CERT_FILE'] = certifi.where()

# Load environment variables
load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Download Video from YouTube
def download_video(url, path='./downloads/'):
    if not os.path.exists(path):
        os.makedirs(path)
    yt = YouTube(url)
    video = yt.streams.filter(progressive=True, file_extension='mp4').first()
    video.download(output_path=path, filename='downloaded_video.mp4')
    return os.path.join(path, 'downloaded_video.mp4')

# Convert Video to Audio
def convert_video_to_audio(video_path, output_dir='./audio/'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    clip = VideoFileClip(video_path)
    audio_path = os.path.join(output_dir, 'converted_audio.mp3')
    clip.audio.write_audiofile(audio_path)
    clip.close()
    return audio_path

# Split Audio into Chunks
def split_audio(audio_path, segment_length=600, output_dir='./chunks/'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    audio = AudioSegment.from_mp3(audio_path)
    chunks = [audio[i:i + segment_length * 1000] for i in range(0, len(audio), segment_length * 1000)]

    chunk_paths = []
    for i, chunk in enumerate(chunks):
        chunk_path = os.path.join(output_dir, f'chunk_{i}.mp3')
        chunk.export(chunk_path, format='mp3')
        chunk_paths.append(chunk_path)
    return chunk_paths

# Transcribe Audio using Whisper
def transcribe_audio(audio_path):
    try:
        with open(audio_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                file=audio_file,
                model="whisper-1", 
            )
            transcription_text = transcript.text
        return transcription_text
    except Exception as e:
        return f"Error in transcription: {e}"

# Main Function
def perform_transcription(url):
    video_path = download_video(url)
    audio_path = convert_video_to_audio(video_path)
    chunk_paths = split_audio(audio_path)

    transcriptions = []
    for chunk_path in chunk_paths:
        transcription = transcribe_audio(chunk_path)
        transcriptions.append(transcription)

    final_transcription = '\\n'.join(transcriptions)
    output_dir = './transcription/'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_name = 'transcription.txt'
    with open(os.path.join(output_dir, file_name), 'w') as file:
        file.write(final_transcription)
    print(f"Transcription saved to {os.path.join(output_dir, file_name)}")

def process_pre_prompts_and_transcription():
    pre_prompt_dir = './pre-prompt/'
    transcription_path = './transcription/transcription.txt'
    response_dir = './response/'

    if not os.path.exists(response_dir):
        os.makedirs(response_dir)

    # Read the transcription text
    with open(transcription_path, 'r') as file:
        transcription_content = file.read().strip()

    # List all pre-prompt files
    pre_prompt_files = glob.glob(pre_prompt_dir + '*.txt')
    num_requests = len(pre_prompt_files)  # Determine the number of requests based on file count

    # Process each pre-prompt file
    for pre_prompt_path in pre_prompt_files:
        with open(pre_prompt_path, 'r') as file:
            pre_prompt_content = file.read().strip()

        # Determine the base name for output files
        base_name = os.path.basename(pre_prompt_path).replace('.txt', '')

        # Send the request
        output = send_openai_request(pre_prompt_content, transcription_content)
        
        # Save the output in a markdown file
        output_file_path = os.path.join(response_dir, f"{base_name}.md")
        with open(output_file_path, 'w') as file:
            file.write(output)

def send_openai_request(system_message, user_message):
    try:
        response = client.chat.completions.create(
            model="gpt-4-0125-preview",  # Ensure correct model is specified
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ]
        )
        # Extract and return the response content, adjust based on the actual response structure
        return response.choices[0].message.content if response.choices else "No response content"
    except Exception as e:
        print(f"Error sending request: {e}")
        return ""

# Make sure to call process_pre_prompts_and_transcription at the end of your main function
if __name__ == "__main__":
    url = input("Enter the YouTube URL: ")
    perform_transcription(url)
    process_pre_prompts_and_transcription()
