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
    '-l', '--lista-urzadzen', action='store_true',
    help='pokaz liste urzadzen i wyjdz')

args, remaining = parser.parse_known_args()

if args.lista_urzadzen:

    print(sd.query_devices())
    parser.exit(0)

parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])

parser.add_argument(
    '-i', '--inputowe', type=int_or_str,
    help='urzadzenie wejscia (numeryczne ID lub substring)')

parser.add_argument(
    '-o', '--outputowe', type=int_or_str,
    help='urzadzenie wyjscia (numeryczne ID lub substring)')

parser.add_argument(
    '-k', '--kanaly', type=int, default=2,
    help='ile kanalow (meh)')

parser.add_argument('--typ', help='typ danych audio (meh)')
parser.add_argument('--czest', type=float, help='czestotliwosc probkowania (meh)')
parser.add_argument('--blok', type=int, help='rozmiar bloku (meh)')
parser.add_argument('--opoznienie', type=float, default=.3, help='opoznienie w sekundach (YEAH BABY! [>.4 is evil])')
parser.add_argument('--max-glosnosc', type=float, default=.15, help='maksymalna glosnosc zanim zaskoczy (0-1)')
parser.add_argument('--rage', action='store_true', help='sproboj, co ci szkodzi?')

args = parser.parse_args(remaining)

def callback(indata, outdata, frames, time, status):

    if status:

        print(status)

    if numpy.max(indata) > args.max_glosnosc:  # change for calibration and more funs

        outdata[:] = indata

    else:

        if not args.rage:

            outdata[:] = 0  # delete for funs!


try:

    with sd.Stream(device=(args.inputowe, args.outputowe),
                   samplerate=args.czest, blocksize=args.blok,
                   dtype=args.typ, latency=args.opoznienie,
                   channels=args.kanaly, callback=callback):

        print('#' * 19)
        print('wdus enter by wyjsc')
        print('#' * 19)
        input()

except KeyboardInterrupt:

    parser.exit('')

except Exception as e:

    parser.exit(type(e).__name__ + ': ' + str(e))
