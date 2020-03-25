import argparse
import tempfile
import queue
import sys
from pynput import keyboard
import sounddevice as sd
import soundfile as sf
import numpy  


def inttext(text):  
        return int(text)

parser = argparse.ArgumentParser(add_help=False)
args, remaining = parser.parse_known_args()

#passing argument
parser.add_argument(
    'filename', nargs='?', metavar='FILENAME')
parser.add_argument(
    '-d', '--device', type=inttext)
parser.add_argument(
    '-r', '--samplerate', type=int)
parser.add_argument(
    '-c', '--channels', type=int, default=1)
parser.add_argument(
    '-t', '--subtype', type=str)
args = parser.parse_args(remaining)

q = queue.Queue()

#record function
def record_voice():
    try:
        if args.filename is None:
            args.filename = tempfile.mktemp(prefix='sentence',
                                            suffix='.wav', dir='')
        file_record= tempfile.mktemp(prefix='sentence',suffix='.wav', dir='')
       
        with sf.SoundFile(file_record, mode='x', samplerate=44100,
                          channels=args.channels, subtype=args.subtype) as file:
            with sd.InputStream(samplerate=44100, device=args.device,
                                channels=1, callback=call_back):              
                print('press Ctrl+C to stop the recording')         
                while True:
                    file.write(q.get())
    except KeyboardInterrupt:
        print('\nRecording finished: ' + repr(file_record))
#call_back for record 
def call_back(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(indata.copy())

def record():
    iterator = 0
    while True:
        choose=input("Start recording? y/n? ")
        if choose=='y':
            print("recording...")
            record_voice()
        if choose=='n':
            return
        iterator += 1
if __name__=='__main__':
    record()