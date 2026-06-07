#!/usr/bin/env python3
import math
import os
import random
import struct
import wave

SAMPLE_RATE = 44100
DURATION = 10.0
TWO_PI = math.pi * 2


def clamp(value):
    return max(-1.0, min(1.0, value))


def write_wav(path, samples):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with wave.open(path, "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(SAMPLE_RATE)
        for sample in samples:
            handle.writeframes(struct.pack("<h", int(clamp(sample) * 32767)))


def envelope(t, attack=0.08, release=0.6):
    if t < attack:
        return t / attack
    if t > DURATION - release:
        return max(0.0, (DURATION - t) / release)
    return 1.0


def sine(freq, t):
    return math.sin(TWO_PI * freq * t)


def violet_boundary():
    samples = []
    for i in range(int(SAMPLE_RATE * DURATION)):
        t = i / SAMPLE_RATE
        pulse = 0.5 + 0.5 * sine(0.07, t)
        shimmer = sine(742.0 + 8.0 * sine(0.19, t), t) * 0.045
        drone = sine(55.0, t) * 0.32 + sine(110.0, t) * 0.16
        overtone = sine(220.0 + 3.0 * sine(0.11, t), t) * 0.07
        samples.append((drone + overtone + shimmer * pulse) * envelope(t) * 0.72)
    return samples


def aries_fire():
    samples = []
    notes = [146.83, 196.0, 220.0, 293.66]
    for i in range(int(SAMPLE_RATE * DURATION)):
        t = i / SAMPLE_RATE
        beat = int(t * 2.4)
        note = notes[beat % len(notes)]
        local = (t * 2.4) % 1.0
        hit = math.exp(-local * 8.0)
        low = sine(note, t) * 0.38 * hit
        spark = sine(note * 3.0, t) * 0.09 * math.exp(-local * 14.0)
        breath = sine(73.42, t) * 0.12
        samples.append((low + spark + breath) * envelope(t) * 0.8)
    return samples


def pruning_cadence():
    rng = random.Random(144)
    samples = []
    strikes = {0.8, 1.7, 2.8, 4.1, 5.2, 6.4, 7.1, 8.6}
    for i in range(int(SAMPLE_RATE * DURATION)):
        t = i / SAMPLE_RATE
        body = sine(49.0, t) * 0.22 + sine(98.0, t) * 0.08
        tick = 0.0
        for strike in strikes:
            delta = t - strike
            if 0.0 <= delta < 0.16:
                tick += sine(620.0 + 180.0 * rng.random(), t) * math.exp(-delta * 42.0) * 0.32
        samples.append((body + tick) * envelope(t) * 0.78)
    return samples


def main():
    write_wav("assets/audio/violet-boundary.wav", violet_boundary())
    write_wav("assets/audio/aries-fire.wav", aries_fire())
    write_wav("assets/audio/deadwood-pruning.wav", pruning_cadence())


if __name__ == "__main__":
    main()
