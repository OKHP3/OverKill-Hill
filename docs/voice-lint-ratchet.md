# Voice-lint baseline ratchet

`scripts/lint-voice.py` remains an editorial aid when run without options. The
standard site validator runs it with `scripts/voice-lint-baseline.json`, which
makes new warnings fail validation without turning the current reviewed warning
set into immediate cleanup work.

The baseline stores counts of SHA-256 identities derived from each finding's
page path, rule label, and normalized visible-text excerpt. Line numbers do not
affect the identity, so unrelated edits that shift a warning do not fail the
gate. Counts prevent copying an already-known warning into a second location.

## Normal use

Run the full gate before pushing:

```sh
python3 scripts/validate-site.py
```

To inspect all editorial warnings without enforcing the baseline:

```sh
python3 scripts/lint-voice.py
```

## Intentional baseline updates

Do not regenerate the baseline merely to clear CI. First review the finding,
correct the copy if practical, and confirm that retaining it is intentional.
Then create a candidate and review its diff before committing it:

```sh
python3 scripts/lint-voice.py --write-baseline /private/tmp/voice-lint-baseline.json
diff -u scripts/voice-lint-baseline.json /private/tmp/voice-lint-baseline.json
```

If the new baseline is justified, replace the reviewed file using a normal,
separately reviewed patch. A resolved warning can remain in the baseline; it
does not weaken the gate because only current findings are compared.
