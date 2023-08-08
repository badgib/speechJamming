#!/usr/bin/env python3
import argparse
import sounddevice as sd
import numpy
assert numpy

def int_or_str(text):

    try:

        return int(text)

    except ValueError:

        return text

parser = argparse.ArgumentParser(add_help=False)

parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')

args, remaining = parser.parse_known_args()

if args.list_devices:

    print(sd.query_devices())
    parser.exit(0)

parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])

parser.add_argument(
    '-i', '--input-device', type=int_or_str,
    help='input device (numeric ID or substring)')

parser.add_argument(
    '-o', '--output-device', type=int_or_str,
    help='output device (numeric ID or substring)')

parser.add_argument(
    '-c', '--channels', type=int, default=2,
    help='number of channels (meh)')

parser.add_argument('--dtype', help='audio data type (meh)')
parser.add_argument('--samplerate', type=float, help='sampling rate (meh)')
parser.add_argument('--blocksize', type=int, help='block size (meh)')
parser.add_argument('--latency', type=float, default=.3, help='latency in seconds (>.4 is evil)')
parser.add_argument('--max-volume', type=float, default=.15, help='max volume before execution (0-1)')
parser.add_argument('--rage', action='store_true', help='try it! it is fun!')

args = parser.parse_args(remaining)

def callback(indata, outdata, frames, time, status):

    if status:

        print(status)

    if numpy.max(indata) > args.max_volume:  # change for calibration and more funs

        outdata[:] = indata

    else:

        if not args.rage:

            outdata[:] = 0  # delete for funs!


try:

    with sd.Stream(device=(args.input_device, args.output_device),
                   samplerate=args.samplerate, blocksize=args.blocksize,
                   dtype=args.dtype, latency=args.latency,
                   channels=args.channels, callback=callback):

        print('#' * 20)
        print('press Return to quit')
        print('#' * 20)
        input()

except KeyboardInterrupt:

    parser.exit('')

except Exception as e:

    parser.exit(type(e).__name__ + ': ' + str(e))
