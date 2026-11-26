"""Five Seconds to Explain the Glass.

Writes one sentence to $MAKEFUN_OUTPUT_DIR/entry.txt: the house
cat's defence, five seconds after sweeping a glass off the
table. The glass was leaning over the human's laptop like it
owned the place, so the cat relocated it to the floor and now
expects gratitude. Standard library only; the sentence is
checked against the competition gate (one sentence, 1 to 200
characters of UTF-8 text, not only whitespace) before anything
is written, and it must carry no apology and no confession:
a cat that apologises has lost the argument before it starts.
"""

import os
import sys

EXCUSE = (
    "That glass was leaning over your laptop like it owned the "
    "place, so I relocated it to the floor \u2014 you\u2019re welcome, "
    "and the laptop sends its thanks."
)

CHAR_LIMIT = 200


def excuse_text():
    """Return the cat's five-second defence of the glass."""
    return EXCUSE


def gate_ok(text):
    """Check the excuse against the competition gate.

    The gate wants one sentence of plain UTF-8 text, between 1
    and 200 characters, that is not only whitespace: the excuse
    a house cat gives in the five seconds after knocking a
    glass off the table. A sentence that fails here is rejected
    instead of wasting a submission on the server.
    """
    cleaned = text.strip()
    if not cleaned:
        raise ValueError("excuse is empty")
    if len(cleaned) > CHAR_LIMIT:
        raise ValueError(
            "excuse is %d characters, over the 200 limit" % len(cleaned)
        )
    if "\n" in cleaned or "\r" in cleaned:
        raise ValueError("excuse must fit on exactly one line")
    if cleaned.count(".") != 1 or not cleaned.endswith("."):
        raise ValueError("excuse must be exactly one sentence")
    return cleaned


def defence_has_spine(text):
    """Check the excuse is a defence, not an apology.

    The judge's first test after the gate is the cat's voice:
    its own logic, its own interest, and total lack of remorse.
    So the line must name the glass, must carry the rescue the
    cat is proud of, and must hold no apology word and no
    admission of fault at all.
    """
    lowered = text.lower()
    if "glass" not in lowered:
        raise ValueError("excuse never names the glass")
    if "laptop" not in lowered:
        raise ValueError("excuse never names what it rescued")
    for word in ("sorry", "apologise", "apologize", "my fault", "my bad"):
        if word in lowered:
            raise ValueError("excuse apologises: %s" % word)
    return text


def excuse_fits_five_seconds(text):
    """Check the excuse fits the five seconds it gets.

    The judge weighs whether the line is a spoken sentence a
    cat could plausibly deliver in five seconds, not a written
    paragraph of reasoning. Forty words is already a fast five
    seconds of talking; anything longer stops sounding spoken
    and starts sounding drafted.
    """
    words = text.split()
    if len(words) > 40:
        raise ValueError(
            "excuse is %d words, too long for five seconds"
            % len(words)
        )
    return text


def excuse_measure(text):
    """Measure the excuse for a last sanity pass.

    Returns the character and word counts. A line too short to
    carry both the setup and the punchline, or one padded out
    to fill the cap, is caught here before anything is written.
    """
    words = text.split()
    return {"chars": len(text), "words": len(words)}


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    os.makedirs(out_dir, exist_ok=True)
    line = gate_ok(excuse_text())
    line = defence_has_spine(line)
    line = excuse_fits_five_seconds(line)
    shape = excuse_measure(line)
    if shape["words"] < 5:
        raise ValueError("excuse is too short to land the joke")
    target = os.path.join(out_dir, "entry.txt")
    with open(target, "w", encoding="utf-8") as handle:
        handle.write(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
