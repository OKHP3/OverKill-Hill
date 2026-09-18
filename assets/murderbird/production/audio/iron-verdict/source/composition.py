"""Original, event-based MurderBird instrumental composition.

No source audio or borrowed melodies. Times and durations are quarter-note beats;
MIDI pitches use C4=60. This module writes no files and needs no dependencies.
"""

import random


def generate_events():
    """Return the 56-bar score; instrumentation/rendering is caller-owned."""
    rng = random.Random(10456)
    events = []
    total_beats = 224.0

    def put(track, start, duration, note, velocity):
        start = max(0.0, float(start))
        duration = min(float(duration), total_beats - start)
        if duration <= 0:
            return
        events.append(dict(track=track, start=round(start, 6),
                           duration=round(duration, 6), note=int(note),
                           velocity=round(max(0.0, min(1.0, velocity)), 4)))

    def guitar(start, duration, note, velocity, opened=False):
        # Stable, small timing differences, separately articulated doubles.
        for track, offset, factor in [('guitar_left', 0.0, 1.0),
                                       ('guitar_right', rng.uniform(.002, .008), .96)]:
            put(track, start + offset, duration, note, velocity * factor)
            if opened:
                put(track, start + offset, duration * .94, note + 7,
                    velocity * factor * .47)

    # Explicit eighth-grid attacks: silence is represented by omitted events.
    # (Beat within bar, MIDI pitch, articulation duration.)
    riff = [
        [(0, 38, .27), (1, 38, .23), (1.5, 38, .31),
         (2.5, 45, .31), (3, 44, .28)],
        [(0, 38, .27), (1, 38, .26), (1.5, 41, .32),
         (2.5, 39, .29), (3, 38, .88)],
        [(0, 38, .22), (.5, 38, .24), (1.5, 38, .29),
         (2.5, 48, .32), (3, 45, .32)],
        [(0, 43, .30), (1, 41, .30), (1.5, 39, .31),
         (2, 38, 1.80)],
    ]
    hook = [
        [(0, 62, 1.5), (1.5, 65, .5), (2, 64, 1)],
        [(0, 68, .5), (.5, 67, 1.5), (2, 62, 2)],
        [(0, 62, 1.5), (1.5, 65, .5), (2, 69, 2)],
        [(0, 67, 1), (1, 64, 1), (2, 62, 2)],
    ]

    def bass_pitch(pitch):
        pitch -= 12
        while pitch < 26:  # Never below D1.
            pitch += 12
        return pitch

    def riff_bar(bar, velocity=.85, pressure=False, sparse=False):
        pattern = riff[bar % 4]
        for n, (pos, pitch, duration) in enumerate(pattern):
            if sparse and n not in (0, len(pattern) - 1):
                continue
            duration = duration * (1.20 if sparse else 1)
            # An intentional breath at the end of each eight-bar phrase.
            if bar % 8 == 7 and pos == 2:
                duration = 1.0
            v = velocity * (1.0 if pos in (0, 2) else .88)
            guitar(bar * 4 + pos, duration, pitch, v, duration > .75)
            put('bass', bar * 4 + pos, max(.26, duration * 1.02),
                bass_pitch(pitch), v * .91)
        if pressure and bar % 2 == 0:
            # One extra low pickup; no borrowed riff or pitch contour.
            guitar(bar * 4 + 3.5, .18, 38, velocity * .67)
            put('bass', bar * 4 + 3.5, .20, 26, velocity * .65)

    chords = {'D': [50, 57, 65], 'Bb': [46, 53, 62],
              'C': [48, 55, 64]}
    roots = {'D': 38, 'Bb': 46, 'C': 48}
    # Map the melody to each harmony while preserving its rhythmic identity.
    # The brief Ab in the original D motif is a passing tension resolving to G.
    melody_map = {
        'D': {62: 62, 65: 65, 64: 64, 68: 68, 67: 67, 69: 69},
        'Bb': {62: 62, 65: 65, 64: 63, 68: 65, 67: 62, 69: 70},
        'C': {62: 60, 65: 64, 64: 62, 68: 65, 67: 64, 69: 67},
    }

    def pad_bar(bar, chord='D', velocity=.28, duration=3.8):
        for note in chords[chord]:
            put('pad', bar * 4, duration, note, velocity)

    def hook_bar(bar, chord='D', velocity=.76, octave=False):
        for pos, note, dur in hook[bar % 4]:
            pitch = melody_map[chord][note]
            put('lead', bar * 4 + pos, max(.18, dur * .94), pitch, velocity)
            if octave:
                put('lead', bar * 4 + pos + .006, max(.18, dur * .89),
                    pitch + 12, velocity * .23)

    # Ignition: distant harmony and isolated, recognizable motive fragments.
    for bar in range(4):
        pad_bar(bar, velocity=.16 + bar * .025)
    put('bass', 0, 3.7, 26, .45)
    guitar(8, .26, 38, .40)
    guitar(9, .24, 38, .42)
    guitar(9.5, .29, 38, .46)
    guitar(14.5, .34, 45, .45)
    guitar(15, .31, 44, .47)

    # Assessment into the first full walking groove.
    for bar in range(4, 8):
        riff_bar(bar, .56, sparse=True)
        pad_bar(bar, velocity=.23)
    for bar in range(8, 16):
        riff_bar(bar, .82)
        if bar % 2 == 0:
            pad_bar(bar, velocity=.23, duration=7.75)
    for bar in range(16, 24):
        riff_bar(bar, .88, pressure=True)
        if bar % 2 == 0:
            pad_bar(bar, velocity=.26, duration=7.75)
        if bar >= 20:
            hook_bar(bar, velocity=.56)

    def wings(start, strongest=False):
        # Two bars each: D minor, Bb major, C major, D minor.
        progression = ['D', 'D', 'Bb', 'Bb', 'C', 'C', 'D', 'D']
        for k, chord in enumerate(progression):
            bar = start + k
            root = roots[chord]
            pad_bar(bar, chord, .36 if strongest else .30)
            hook_bar(bar, chord, .88 if strongest else .77, strongest)
            if chord == 'D':
                riff_bar(bar, .97 if strongest else .89)
            else:
                # Spacious open fifths between clipped root attacks.
                for pos, dur in [(0, 1.22), (1.5, .26), (2.5, .24), (3, .70)]:
                    guitar(bar * 4 + pos, dur, root,
                           .95 if strongest else .87, dur > .6)
                    put('bass', bar * 4 + pos, dur * 1.03,
                        bass_pitch(root), .90 if strongest else .82)

    wings(24)

    # Half-time space: keep the motif's teeth but leave room for heavy drums.
    for bar in range(32, 36):
        riff_bar(bar, .77, sparse=True)
        pad_bar(bar, velocity=.24)
    for bar in range(36, 40):
        riff_bar(bar, .80 + (bar - 36) * .035, pressure=bar >= 38)
        pad_bar(bar, velocity=.27)
    wings(40, strongest=True)

    for bar in range(48, 52):
        riff_bar(bar, .97, pressure=True)
        pad_bar(bar, velocity=.28)

    # Final verdict: two fragments, a synchronized stop, then a long D ending.
    riff_bar(52, .96)
    for pos, pitch in [(0, 43), (1, 41), (1.5, 39), (2, 38)]:
        guitar(53 * 4 + pos, .30, pitch, .92)
        put('bass', 53 * 4 + pos, .33, bass_pitch(pitch), .88)
    guitar(54 * 4, 5.6, 38, .98, opened=True)
    put('bass', 54 * 4, 6.4, 26, .95)
    put('lead', 54 * 4, 4.5, 74, .71)
    pad_bar(54, velocity=.32, duration=7.6)

    events.sort(key=lambda e: (e['start'], e['track'], e['note']))
    return dict(
        bpm=104, bars=56, title='MurderBird - Iron Verdict', events=events,
        sections=[
            dict(name='Ignition', start_bar=0, bars=4),
            dict(name='Assessment', start_bar=4, bars=4),
            dict(name='Stride', start_bar=8, bars=8),
            dict(name='Pressure', start_bar=16, bars=8),
            dict(name='Wings', start_bar=24, bars=8),
            dict(name='Half-time / Rebuild', start_bar=32, bars=8),
            dict(name='Iron Verdict', start_bar=40, bars=8),
            dict(name='Final Approach', start_bar=48, bars=4),
            dict(name='Decisive Ending', start_bar=52, bars=4),
        ])
