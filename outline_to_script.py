#!/usr/bin/env python3
"""outline_to_script.py - free minimal core of the Audio Explainer Starter Kit. Standard library only, Python 3.8+, no network.

Reads a plain-text outline (see topic.md) and writes a read-aloud script: segments split into sentences, plus the questions you wrote.
It also shows the keyword-overlap matcher that picks which written question a typed phrase refers to.

Usage:
  python outline_to_script.py topic.md                       # script on stdout
  python outline_to_script.py topic.md --json -o out.json    # structured JSON
  python outline_to_script.py topic.md --ask "does it work when its cold"   # which written question matches (keyword overlap)
  python outline_to_script.py --selfcheck

The paid kit turns the same outline into ONE self-contained interruptible web page (browser speech synthesis, Space bar to interrupt,
resume at the interrupted sentence). This free core has no web page and no speech output.
"""
import argparse, json, re, sys
from pathlib import Path

def split_sentences(text):
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p]

def parse(md):
    title, segs, cur = "Untitled explainer", [], None
    for raw in md.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("# ") and not line.startswith("## "):
            title = line[2:].strip()
        elif line.startswith("## "):
            cur = {"heading": line[3:].strip(), "text": [], "ask": []}
            segs.append(cur)
        elif line.startswith("??"):
            if cur is None:
                raise SystemExit("a '??' question line must come after a '## ' heading")
            q, sep, a = line[2:].partition("::")
            if not sep or not q.strip() or not a.strip():
                raise SystemExit("question lines need the form: ?? question :: answer  (got: %r)" % line)
            cur["ask"].append({"q": q.strip(), "a": a.strip()})
        else:
            if cur is None:
                raise SystemExit("text must come after a '## ' heading (got: %r)" % line)
            cur["text"].append(line)
    out = []
    for s in segs:
        sents = split_sentences(" ".join(s["text"]))
        if not sents:
            raise SystemExit("segment %r has no text" % s["heading"])
        out.append({"heading": s["heading"], "sentences": sents, "ask": s["ask"]})
    if not out:
        raise SystemExit("no '## ' segments found")
    return title, out


STOP = set("a an the is are was were do does did of to in on it its and or for with how what why when who can i you my me be this that at as by".split())

def words(s):
    return {w for w in re.findall(r"[a-z0-9]+", s.lower()) if w not in STOP}

def match(typed, asks):
    """-> (question dict or None, overlap count). Needs at least one shared non-stopword; ties go to the first written question."""
    t, best, score = words(typed), None, 0
    for q in asks:
        n = len(t & words(q["q"]))
        if n > score:
            best, score = q, n
    return best, score

def render(title, segs):
    out = [title, "=" * len(title)]
    for i, s in enumerate(segs, 1):
        out += ["", "[%d] %s" % (i, s["heading"])] + ["  " + x for x in s["sentences"]]
        for q in s["ask"]:
            out.append("  ? %s -> %s" % (q["q"], q["a"]))
    return "\n".join(out) + "\n"

def selfcheck():
    md = "# T\n## One\nFirst sentence. Second one!\n?? Does it work when cold? :: Yes.\n## Two\nOnly line.\n"
    title, segs = parse(md)
    assert title == "T" and len(segs) == 2 and segs[0]["sentences"] == ["First sentence.", "Second one!"]
    q, n = match("works when its cold", segs[0]["ask"])
    assert q and q["a"] == "Yes." and n >= 1
    assert match("banana", segs[0]["ask"])[0] is None
    for bad in ("text first\n", "## H\n", "## H\ntext\n?? no separator\n"):
        try:
            parse(bad); raise AssertionError("accepted " + repr(bad))
        except SystemExit:
            pass
    print("selfcheck PASS")

def main():
    ap = argparse.ArgumentParser(description="outline -> read-aloud script (free core)")
    ap.add_argument("outline", nargs="?"); ap.add_argument("--json", action="store_true"); ap.add_argument("-o"); ap.add_argument("--ask"); ap.add_argument("--selfcheck", action="store_true")
    a = ap.parse_args()
    if a.selfcheck:
        return selfcheck()
    if not a.outline:
        ap.error("outline file required")
    title, segs = parse(Path(a.outline).read_text(encoding="utf-8"))
    if a.ask is not None:
        allq = [q for s in segs for q in s["ask"]]
        q, n = match(a.ask, allq)
        print(json.dumps({"typed": a.ask, "matched": q, "shared_words": n}, indent=1))
        return
    text = json.dumps({"title": title, "segments": segs}, indent=1) + "\n" if a.json else render(title, segs)
    if a.o:
        Path(a.o).write_text(text, encoding="utf-8"); print("wrote", a.o)
    else:
        sys.stdout.write(text)

if __name__ == "__main__":
    main()
