# MurderBird - Iron Verdict

**Original instrumental entrance-theme demo · Version 1 · 2:10 · 104 BPM · 4/4**

Created for Jamie's MurderBird: weathered metal, an assessing orange optic, heavy deliberate steps, compact wings opening into an intimidation display. The character's capacity for judgment shapes the pauses and controlled movement. Working title, not a change to the character's canon.

This is a newly composed and programmed recording made with original sound synthesis. It is an industrial-rock demo with synthesized guitar-like instruments, bass, drums, metallic lead and mechanical textures. It is not a recording of a live band, a mashup, a stem separation, an artist voice clone, or a GarageBand-rendered session.

## Listen and edit

- `murderbird-iron-verdict.mp3`: convenient listening copy, 320 kbps stereo.
- `murderbird-iron-verdict.wav`: finished demo mix, 44.1 kHz / 24-bit stereo.
- `iron-verdict-premaster.wav`: mix before final loudness processing.
- `iron-verdict-editable.mid`: Type 1 MIDI with six performance tracks plus tempo/section metadata. Assign instruments to taste; the custom synthesized sounds are not embedded in MIDI.
- `stems/`: seven aligned stereo WAVs, all starting at time zero, preserving silence before each instrument enters. They sum at unity to the premaster within 24-bit rounding tolerance. They do not sum to the loudness-processed listening master.
- `composition-and-arrangement.json`: exact note timings, velocities and section map.
- `audio-validation.json`: render measurements and export checks.
- `source/`: composition, original synthesis and rendering source for reproducibility. This is supporting material; no coding is required to listen or import the WAVs/MIDI.

## Entrance map

| Time | Section | Character cue |
|---|---|---|
| 0:00 | Ignition | Darkness and a first glint from the optic; a low resonance establishes mass. |
| 0:09 | Assessment | Head movement and short, testing musical phrases. |
| 0:18 | Stride | Full rhythm section; the original low-register riff becomes the walking identity. |
| 0:37 | Pressure | More activity, with the melodic hook introduced later in the section. |
| 0:55 | Wings | Harmony widens; the compact wings open and the full hook speaks. |
| 1:14 | Half-time / rebuild | The creature pauses to assess. Percussion and texture rebuild the tension. |
| 1:32 | Iron Verdict | The strongest melodic statement, with octave reinforcement. |
| 1:51 | Final approach | Return to the core riff. |
| 2:00 | Decisive ending | Short final gestures, a sustained D-based hit and controlled decay. |

Times are rounded scene cues. The musical score is 56 bars (129.23 seconds); the file includes a short final decay/fade and totals approximately 129.83 seconds.

## Musical identity

The low riff is centered on D. Its signature uses separated low-D attacks, an A-A-flat descent, and a later F-E-flat-D return. Rests are part of the design: the character has time to look, decide and move. A contrasting lead hook expands the same atmosphere into a singable phrase. The wider passages move through D minor, B-flat, C and D minor; the lead is adapted to each harmony.

The reference songs informed broad preferences: force, melody, dramatic arrivals, rhythmic weight and the contrast between restraint and impact. No audio from Shinedown, Five Finger Death Punch, In This Moment or any other artist was downloaded, extracted, sampled or incorporated. No existing lyrics were used. The note patterns were newly written for this project rather than transcribed from the reference recordings.

## GarageBand project

`murderbird-iron-verdict.band` is the native project, saved through GarageBand on 2026-09-17. It contains six editable MIDI instrument tracks at 104 BPM, with Count In and Metronome disabled. The instruments assigned by GarageBand are two Hard Rock guitars, Picked Bass, Soft Saw Lead, Classic Analog Pad and SoCal drums. The note score is centered on D minor; the imported project's key-signature display remains C Major. Track gains and instrument voicing are initial import defaults and need an audition/mix pass. The MIDI pan messages set the two guitars left/right during playback.

The native project is an editable instrument interpretation of the score. The WAV/MP3 demo and seven audio stems preserve the original custom-synthesis mix, including the separate mechanical-effects track that is not represented in MIDI. They were rendered outside GarageBand.

The owner approved the macOS installation password prompt locally. After that approval, the pending export finalized as `murderbird-iron-verdict-garageband-preview.wav`: 44.1 kHz, 24-bit stereo PCM, 136.635 seconds including the native effect tail, with a sample peak of 0.9885. GarageBand was responsive and its playhead advanced from bar 1 to bar 7 without another content prompt before playback was stopped. These are file and transport checks, not a human auditory audition or a reopened-project test. The native preview has a different instrument sound and tail from the custom-synthesis demo. Downloading all available sounds was resumed, but completion of the entire optional library remains unverified.

For the closest match to this demo:

1. Create an empty GarageBand project at **104 BPM**, **4/4**. Turn off the metronome for listening/export.
2. Import the seven WAV files from `stems/`, putting each on a separate audio track and aligning all left edges at bar 1. Keep the original leading silence.
3. Start with track volume at 0 dB, stereo pan centered, and additional effects off: the stereo placements and sound processing are already rendered into the stems. Add master processing only if you want to change the mix.

For note-level changes, use a separate project or mute the corresponding audio stems before importing `iron-verdict-editable.mid`. Set the project to 104 BPM if the tempo is not adopted automatically. Choose distorted electric guitar sounds for the two guitar tracks, bass for Bass, a melodic metallic synth for Lead, a subdued pad for Pad, and a drum kit for the channel-10 Drums track. The standalone mechanical-effects stem is audio-only. Different instruments will produce a different performance; the General MIDI patch numbers are starting hints, not guaranteed GarageBand patch assignments.

Do not run both all MIDI instruments and all corresponding audio stems together unless intentional doubling is wanted.

## Sound provenance and rights boundary

Every sound in the original custom-synthesis demo (the demo WAV/MP3, premaster and seven stems) was synthesized locally from oscillators, mathematical envelopes and generated noise. No third-party audio loops, commercial recordings, speech models or paid generation services were used. The rendering libraries were NumPy, SciPy, SoundFile and Mido; FFmpeg produced the listening formats. No artist sample license was purchased or used.

The separate `murderbird-iron-verdict-garageband-preview.wav` was rendered in GarageBand using its native instrument patches and the original MIDI score. Its sounds were not generated by the custom-synthesis pipeline. The no-third-party-audio statement above applies only to the original demo; it does not describe the GarageBand instrument content or establish separate rights in that content.

Actual sampling can implicate separate rights in a recording and in its underlying composition; transforming a sample does not by itself establish permission. The [U.S. Copyright Office's musician guidance](https://www.copyright.gov/engage/musicians/) explains that distinction and that there is no universal safe minimum sample length. Apple's [GarageBand loop guidance](https://support.apple.com/en-ca/102034) permits covered loops in original compositions under its stated terms, but the original custom-synthesis demo did not use them.

This provenance record describes what was made and used. It is not a worldwide legal clearance, an exhaustive similarity search against existing music, or a guarantee of exclusive copyright in AI-assisted material.

## Verification and listening limits

The exported audio was checked for finite samples, duration, clipping, channel count, aligned stems and final decay. The MIDI was checked for parsing, tempo, event balance and same-pitch note overlaps. An independent subagent reviewed the score and exports and identified headroom and MIDI issues that were corrected before delivery.

The assistant did not perform a human auditory audition. Musical character and instrument realism therefore need Jamie's listening judgment. This is a complete first demo suitable for evaluating the theme, not a claim of a live-band or studio-finished production.

## Rebuild

With Python and the packages in `source/requirements.txt`, run `source/render-theme.py`. It writes a fresh `rebuild/` folder and leaves the delivered mix untouched. That generates the premaster, stems, MIDI and note data; final listening-master processing is described in `source/mastering.txt`. The deterministic random seeds preserve the programmed performance and sound design.
