# audio-explainer

Free core of the Audio Explainer Starter Kit. You write a plain-text outline; `outline_to_script.py` parses it into segments, sentences and
the questions you wrote in advance, and can match a typed phrase to one of your questions by keyword overlap. Python 3.8+, standard library
only, no API key, no model, no network.

Outline format (`topic.md` is a worked example):

```
# Title
## Segment heading
Paragraph text, spoken as that segment.
?? A question the listener might ask :: The answer you wrote.
```

## Quickstart

```
git clone https://github.com/MegaStretch23/audio-explainer
cd audio-explainer
python outline_to_script.py topic.md                              # read-aloud script
python outline_to_script.py topic.md --json -o out.json           # structured JSON
python outline_to_script.py topic.md --ask "does it work when its cold outside"
python outline_to_script.py --selfcheck
```

## Sample output (saved from a real run: `sample/demo-output.txt`, `sample/demo-output.json`, `sample/demo-match.json`)

```
How a heat pump works
=====================

[1] Moving heat instead of making it
  A heat pump does not burn fuel to make heat.
  It moves heat from one place to another, the same way a refrigerator does.
  ...
  ? Does it work when it is cold outside? -> Yes, down to a point. ...
```

`--ask "does it work when its cold outside"` returns the written question "Does it work when it is cold outside?" with 3 shared words. A
phrase that shares no word with any written question matches nothing and gets no answer; nothing is generated.

## Want the interruptible audio page?

This repo has no web page and no speech output. The [Audio Explainer Starter Kit](https://vedovino.gumroad.com/l/dsorqj?utm_source=github)
($9, Gumroad) turns the same outline into one self-contained HTML page that reads each segment aloud with the browser's built-in speech
synthesis, lets the listener interrupt with the Space bar, shows your written questions, and resumes at the sentence it stopped on. Voices
come from the listener's own device, so they differ between devices.

MIT licensed.
