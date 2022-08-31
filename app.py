from flask import Flask, render_template, request, send_from_directory

"""Getting Started Example for Python 2.7+/3.3+"""
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir

app = Flask(__name__)

SPEED_RATES = {0: 'x-slow', 25: 'slow', 50: 'medium', 75: 'fast', 100: 'x-fast'}
PITCHES = {0: 'x-low', 25: 'low', 50: 'medium', 75: 'high', 100: 'x-high'}
DEFAULT_ARGS = {'gender': 'Male', 'accent': 'American', 'speed': 50, 'pitch': 50, 'breakTime': 3, 'breakFreq': 3}

VOICES = {
    "American": {
        "Male": "Matthew",
        "Female": "Salli",
        "Child": "Justin"
    },
    "British": {
        "Male": "Brian",
        "Female": "Amy",
        "Child": "Justin"
    },
    "Australian": {
        "Male": "Russell",
        "Female": "Nicole",
        "Child": "Justin"
    }
}


def compose_text(pitch="medium", rate="medium", break1="3", break2="300"):
    with open('transcript.txt', 'r') as file:
        text = file.read().replace('\n', '')
    text = text.replace("%pitch%", pitch)
    text = text.replace("%rate%", rate)
    text = text.replace("%break1%", break1 + "s")
    text = text.replace("%break2%", break2 + "ms")
    return text


@app.route('/')
def index():
    return render_template('index.html', args=DEFAULT_ARGS)


@app.route('/polly')
def polly():
    args = request.args

    # Create a client using the credentials and region defined in the [adminuser]
    # section of the AWS credentials file (~/.aws/credentials).
    session = Session(profile_name="pollyuser")
    polly_cli = session.client("polly")
    # TODO: break time and break freq
    text = compose_text(
        pitch=PITCHES[int(args['pitch'])],
        rate=SPEED_RATES[int(args['speed'])],
        break1=args['breakTime'])
    print(text)

    try:
        # Request speech synthesis
        response = polly_cli.synthesize_speech(
            Text=text,
            TextType="ssml",
            OutputFormat="mp3",
            VoiceId=VOICES[args['accent']][args['gender']])

    except (BotoCoreError, ClientError) as error:
        # The service returned an error, exit gracefully
        print(error)
        return render_template('index.html', args=DEFAULT_ARGS)

    # Access the audio stream from the response
    if "AudioStream" in response:
        # Note: Closing the stream is important because the service throttles on the
        # number of parallel connections. Here we are using contextlib.closing to
        # ensure the close method of the stream object will be called automatically
        # at the end of the with statement's scope.
        with closing(response["AudioStream"]) as stream:
            output = os.path.join(os.path.abspath('./'), "speech_polly.mp3")

            try:
                # Open a file for writing the output as a binary stream
                with open(output, "wb") as file:
                    file.write(stream.read())
            except IOError as error:
                # Could not write to file, exit gracefully
                print(error)
                sys.exit(-1)

    else:
        # The response didn't contain audio data, exit gracefully
        print("Could not stream audio")
        return render_template('index.html', args=DEFAULT_ARGS)

    # Play the audio using the platform's default player
    # if sys.platform == "win32":
    #     os.startfile(output)
    # else:
    #     # The following works on macOS and Linux. (Darwin = mac, xdg-open = linux).
    #     opener = "open" if sys.platform == "darwin" else "xdg-open"
    #     subprocess.call([opener, output])

    # record the setting
    with open("settings.csv", "a+") as output:
        output.write(','.join(
            [args['gender'], args['accent'], args['speed'], args['pitch'], args['breakTime'], args['breakFreq']]))
        output.write('\n')

    return render_template('index.html', args=args)


@app.route('/<path:filename>')
def download_file(filename):
    return send_from_directory('./', filename)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
