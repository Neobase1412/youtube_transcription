# Video Transcription and Prompt Processing

This project provides a Python script that downloads a video from YouTube, extracts its audio, transcribes the audio using OpenAI's Whisper model, and then processes pre-defined prompts with the transcription content using OpenAI's GPT model. The responses are saved in markdown format.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.11+
- pip (Python package installer)
- Virtual environment (recommended for Python package management)

## Setting Up the Project

Follow these steps to get your development environment set up:

1. **Clone the repository:**

   ```sh
   git clone https://github.com/Neobase1412/youtube_transcription.git
   cd youtube_transcription
   ```

2. **Create and activate a virtual environment:**

   - On macOS/Linux:

     ```sh
     python -m venv myenv
     source myenv/bin/activate
     ```

   - On Windows:

     ```sh
     python -m venv myenv
     .\myenv\Scripts\activate
     ```

3. **Install the required packages:**

   ```sh
   pip install -r requirements.txt
   ```

## Configuration

- Create a `.env` file in the project root directory and add your OpenAI API key:

  ```plaintext
  OPENAI_API_KEY=your_api_key_here
  ```

- Ensure the SSL certificates are correctly set up by the script (using `certifi`).

## Running the Script

To run the script, use the following command:

```sh
python main.py
```

You will be prompted to enter a YouTube URL. After the process completes, check the `./transcription/` directory for the transcription text file and the `./response/` directory for the markdown files containing the processed prompts.

## Adding Pre-Prompts

- Add your pre-prompt text files to the `./pre-prompt/` directory. The script will process each file with the transcription content and generate a response for each pre-prompt.

## Contributing

Contributions to this project are welcome. Please feel free to fork the repository, make your changes, and submit a pull request.