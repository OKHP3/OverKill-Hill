"""Original, sample-free instruments for the MurderBird programmed demo.

Each call returns a mono float32 note including a short release. Velocity is
linear 0..1 (MIDI velocities 1..127 are also accepted). Note 69 is exactly 440 Hz.
These are deliberately synthetic instruments, not sampled real guitar players.
"""
from __future__ import annotations

import numpy as np
from scipy.signal import butter, sosfilt


def _filter(signal, cutoff, sr, kind="lowpass", order=2):
    nyquist = sr * 0.5
    if isinstance(cutoff, (tuple, list)):
        cutoff = [min(float(v), nyquist * .94) for v in cutoff]
    else:
        cutoff = min(float(cutoff), nyquist * .94)
    return sosfilt(butter(order, cutoff, btype=kind, fs=sr, output="sos"), signal)


def _gate(t, duration, attack, release):
    env = np.minimum(t / max(attack, 1e-5), 1.0)
    release_pos = np.clip((t - duration) / release, 0, 1)
    return env * np.cos(release_pos * np.pi / 2) ** 2


def _guitar(t, f, duration, velocity, sr, rng):
    muted = duration < .30
    pickup = rng.uniform(.13, .20)
    phases = rng.uniform(-.06, .06, 36)
    signal = np.zeros_like(t)
    # Dispersive decay and pickup-position harmonic cancellation give each
    # double track a different pick, while the fundamental remains in tune.
    for h in range(1, min(36, int(sr * .43 / f)) + 1):
        weight = np.sin(np.pi * h * pickup) / h ** .92
        decay = (.075 + .52 / (h ** .56)) if muted else (.30 + 3.7 / h ** .8)
        signal += weight * np.sin(2 * np.pi * f * h * t + phases[h-1]) * np.exp(-t / decay)
    signal /= 1.25
    noise = rng.standard_normal(len(t))
    pick = _filter(noise, (1400, 7000), sr, "bandpass")
    signal += .10 * pick * np.exp(-t / .009)
    if muted:
        signal *= np.exp(-t / max(.085, duration * .80))
    # A shaped preamp and cabinet remove brittle upper partials after drive.
    signal = _filter(signal, 65, sr, "highpass")
    signal = np.tanh(signal * (4.3 + velocity * 1.6)) / 1.25
    signal = _filter(signal, 4700 if muted else 5400, sr, order=3)
    signal = _filter(signal, 75, sr, "highpass")
    return signal * _gate(t, duration, .0015, .075 if muted else .16) * .72


def _bass(t, f, duration, velocity, sr, rng):
    fundamental = np.sin(2 * np.pi * f * t)
    upper = (.40 * np.sin(4 * np.pi * f * t)
             + .23 * np.sin(6 * np.pi * f * t)
             + .10 * np.sin(10 * np.pi * f * t))
    transient = _filter(rng.standard_normal(len(t)), 1600, sr) * np.exp(-t / .009) * .035
    grit = np.tanh((fundamental * .6 + upper) * 2.1)
    grit = _filter(grit, 1900, sr)
    signal = .66 * fundamental + .24 * grit + transient
    signal *= (.73 + .27 * np.exp(-t / .12))
    return signal * _gate(t, duration, .004, .10) * .75


def _lead(t, f, duration, velocity, sr, rng):
    # Rounded triangle body, restrained bright harmonics and an octave bell.
    signal = np.sin(2 * np.pi * f * t)
    for h in (3, 5, 7, 9):
        if h * f < sr * .43:
            signal += ((-1) ** ((h - 1) // 2)) * .7 / h ** 2 * np.sin(2 * np.pi * f * h * t)
    for h in (2, 4, 6):
        if h * f < sr * .43:
            signal += .16 / h * np.sin(2 * np.pi * f * h * t + rng.uniform(-.03, .03))
    bell = .22 * np.sin(2 * np.pi * f * 2 * t) * np.exp(-t / .24)
    signal = np.tanh((signal + bell) * 1.2)
    signal = _filter(signal, min(6500, f * 12), sr)
    signal *= .83 + .17 * np.exp(-t / .20)
    return signal * _gate(t, duration, .007, .20) * .62


def _pad(t, f, duration, velocity, sr, rng):
    signal = np.zeros_like(t)
    for h, amp in ((1, .65), (2, .22), (3, .09), (4, .04)):
        if h * f < sr * .43:
            phase = rng.uniform(0, 2 * np.pi)
            signal += amp * np.sin(2 * np.pi * f * h * t + phase)
    air = _filter(rng.standard_normal(len(t)), (700, 3200), sr, "bandpass")
    signal += .035 * air
    signal *= .94 + .06 * np.sin(2 * np.pi * .31 * t + rng.uniform(0, 6.28))
    signal = _filter(signal, 2600, sr)
    return signal * _gate(t, duration, min(.32, duration * .30), .24) * .45


def render_note(track: str, note: int, duration: float, velocity: float,
                sr: int, seed: int) -> np.ndarray:
    """Render a pitched instrument note; no downloads, samples or global state.

    Track names may contain guitar/rhythm/chug, bass, lead/melody/bell, or
    pad/drone/atmos. Unknown track names raise ValueError rather than silently
    choosing an inappropriate instrument. Different seeds alter guitar pick
    timbre, phase and transient, suitable for independent stereo doubles.
    """
    if not np.isfinite(duration) or duration <= 0:
        raise ValueError("duration must be positive and finite")
    if sr < 8000:
        raise ValueError("sample rate must be at least 8000 Hz")
    if not 0 <= note <= 127:
        raise ValueError("MIDI note must be between 0 and 127")
    velocity = float(velocity)
    if velocity > 1:
        velocity /= 127.0
    velocity = float(np.clip(velocity, 0, 1))
    if not np.isfinite(velocity):
        raise ValueError("velocity must be finite")
    t = np.arange(int(np.ceil((duration + .25) * sr)), dtype=np.float64) / sr
    f = 440.0 * 2 ** ((float(note) - 69) / 12)
    if f >= sr * .43:
        raise ValueError("note is above the useful frequency range at this sample rate")
    rng = np.random.default_rng(int(seed) % (2 ** 64))
    track = track.lower()
    if "bass" in track:
        signal = _bass(t, f, duration, velocity, sr, rng)
    elif any(name in track for name in ("guitar", "rhythm", "chug")):
        signal = _guitar(t, f, duration, velocity, sr, rng)
    elif any(name in track for name in ("lead", "melody", "bell")):
        signal = _lead(t, f, duration, velocity, sr, rng)
    elif any(name in track for name in ("pad", "drone", "atmos")):
        signal = _pad(t, f, duration, velocity, sr, rng)
    else:
        raise ValueError(f"Unknown instrument track: {track}")
    # Preserve velocity and instrument dynamics; no per-note normalization.
    signal *= velocity
    return np.clip(signal, -1.0, 1.0).astype(np.float32)
