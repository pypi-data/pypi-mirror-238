import io
import ffmpeg
import numpy as np
import whisper
from pytube import YouTube, exceptions as pytube_exceptions

def get_text(link: str, modeltype: str = "base", verbose=False) -> str:
    """
    Extract text from a YouTube video's audio.

    This function takes a YouTube link, extracts the audio using Open's Whisper and returns the text.

    Parameters:
        link (str): The YouTube video URL (str).
        modeltype (str, optional): (Optional) The type of Whisper model. Defaults to "base".
        verbose (bool, optional): (Optional) If set to True, the function prints each step of the process. Defaults to False.

    Returns:
        str: Transcribed text from the video's audio (str). If any error occurs, it returns None.

    Example:
        >>> text = get_text("https://www.youtube.com/watch?v=fLeJJPxua3E", modeltype="base", verbose=True)
        >>> print(text)

    Visit Whisper's GitHub for information about the models:  https://github.com/openai/whisper#available-models-and-languages
    """

    try:
        if verbose: print("-- Loading audio from YouTube link")
        yt = YouTube(link)

        if verbose: print(f"-- Video title: {yt.title}")
        stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()
        buffer = io.BytesIO()
        stream.stream_to_buffer(buffer)
        if verbose: print("-- Loading completed. Now transcribing audio")

    except pytube_exceptions.PytubeError as e:
        print(f"-- Failed to load audio from YouTube: {e}")
        return None

    try:
        out, _ = (
            ffmpeg.input('pipe:', threads=0)
            .output("pipe:", format="s16le", acodec="pcm_s16le", ac=1, ar=16_000)
            .run_async(pipe_stdin=True, pipe_stdout=True, pipe_stderr=True)
        ).communicate(input=buffer.getvalue())

    except ffmpeg.Error as e:
        print(f"-- Failed to process audio: {e.stderr.decode()}")
        return None

    finalaudio = np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0

    try:
        result = whisper.load_model(modeltype).transcribe(finalaudio).get("text")
        if result is None:
            print("-- Transcription failed")
            return None
        if verbose: print("-- Transcription completed successfully\n")
        return result

    except Exception as e:
        print(f"Error during transcription: {e}")
        return None
