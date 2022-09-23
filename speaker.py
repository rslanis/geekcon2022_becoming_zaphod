"""Getting Started Example for Python 2.7+/3.3+"""
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import time
import subprocess
from tempfile import gettempdir

import vlc

def play_text(text: str):
    # Create a client using the credentials and region defined in the [adminuser]
    # section of the AWS credentials file (~/.aws/credentials).
    # session = Session(profile_name="adminuser")
    session = Session()
    polly = session.client("polly")

    try:
        # Request speech synthesis
        response = polly.synthesize_speech(Text=text, OutputFormat="mp3",
                                            VoiceId="Brian")
    except (BotoCoreError, ClientError) as error:
        # The service returned an error, exit gracefully
        raise

    # Access the audio stream from the response
    if "AudioStream" in response:
        # Note: Closing the stream is important because the service throttles on the
        # number of parallel connections. Here we are using contextlib.closing to
        # ensure the close method of the stream object will be called automatically
        # at the end of the with statement's scope.
            with closing(response["AudioStream"]) as stream:
               output = os.path.join(gettempdir(), "speech.mp3")

               try:
                # Open a file for writing the output as a binary stream
                    with open(output, "wb") as file:
                       file.write(stream.read())
               except IOError as error:
                  # Could not write to file, exit gracefully
                  raise

    else:
        # The response didn't contain audio data, exit gracefully
        raise Exception("no audio data")

    print(output)
    p = vlc.MediaPlayer(output)
    p.play()
    time.sleep(2)
    p.stop()
    p.release()

if __name__ == '__main__':
    play_text("Hi, I'm Zaphod, and fuck you too")
