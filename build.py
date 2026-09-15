#!/usr/bin/env python3
"""Builds index.html (page body, artifact source) and docs/index.html (full document for GitHub Pages)
from src.html by replacing <!-- FIG:key --> placeholders with numbered figure blocks."""
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from helpers import *
from glyphs import *
import newfigs
import keptfigs

FIGS = {
    "network":   ("One small network learns cat from dog",
                  "Nobody writes a rule about whiskers. The network guesses, gets corrected, and the connections that helped get a little stronger. Do it a few hundred thousand times and pathways form.",
                  newfigs.fig_network),
    "worldmodel": ("Now do it for everything humans have written",
                  "A language model plays the same game with words, at a scale of hundreds of billions of connections. The pathways it forms for grammar, facts, and reasoning are its world model. It forms pathways for persuasion and deception by the same process, because they are in the text too.",
                  newfigs.fig_worldmodel),
    "habits":    ("Post-training teaches habits",
                  "The same question, before and after. Post-training makes the helpful answer the strong default. The other continuations are dimmed, not deleted.",
                  newfigs.fig_habits),
    "packet":    ("What you typed, and what the model read",
                  "Your line is a small slice of the packet. The hidden instructions, the saved memory, and the document the app added are all read as part of the same request. Word counts are illustrative.",
                  newfigs.fig_packet),
    "conductor": ("One task, step by step",
                  "The model only ever writes a request. The conductor decides whether to run it. Step 4 is the gate doing its job: drafting the email and sending it are different permissions.",
                  newfigs.fig_conductor),
    "stack":     ("The whole system, assembled",
                  "A model is the bottom two layers. A chatbot adds instructions and a packet. An agent adds tools and a conductor. The open-versus-closed debate is about the bottom layer only.",
                  newfigs.fig_stack),
    "fan":       ("Same pathways, different paths",
                  "Testing a model once and finding that it refuses tells you about one path through this tree. Safety is a distribution, and long-running agents with tools, memory, and peers sample its tails.",
                  keptfigs.f8),
    "persist":   ("Persistence, layer by layer",
                  "The pathways outlast everything and never move on their own. The packet is gone in an hour. Memory and the conductor are the durable layers, and neither is tied to a particular model.",
                  keptfigs.f9),
    "threeways": ("Three ways control fails",
                  "Stopping a malicious user, specifying a task properly, and preventing a cascade are three different control problems. The pathways overlap, and none requires the AI to want anything.",
                  keptfigs.f10),
    "notebook":  ("The project survives the session",
                  "What survives is a record of the work, not the model's intelligence. The record is tiny, portable, and indifferent to which model reads it.",
                  keptfigs.f11),
    "curve":     ("Refusal as a delay",
                  "If a system can keep sampling new agents, a refusal becomes a delay rather than a barrier. The notebook then tends to preserve what worked, so the collective gets better at crossing the line without anyone retraining anything.",
                  keptfigs.f12),
    "breaker":   ("What changes when a copy leaves the provider",
                  "\"Closed\" does not mean nobody can use it, and \"open\" does not mean it is free to run. The difference that matters is the breaker.",
                  keptfigs.f13),
    "control":   ("Five control points on the assembled system",
                  "Open versus closed is a question about the bottom layer. Four of the five control points sit above it.",
                  newfigs.fig_control),
}

HEAD_EXTRA = """<meta name="description" content="A visual guide to how modern AI systems are put together, how they could cause catastrophic harm, and where control actually lives.">
<meta property="og:type" content="article">
<meta property="og:title" content="What Could Go Wrong?">
<meta property="og:description" content="A visual guide to how modern AI systems are put together, how they could cause catastrophic harm, and where control actually lives.">
<meta property="og:url" content="https://luyenchou1.github.io/what-could-go-wrong/">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="What Could Go Wrong?">
<meta name="twitter:description" content="A visual guide to how modern AI systems are put together, how they could cause catastrophic harm, and where control actually lives.">
<style>body{margin:0} img{max-width:100%} [hidden]{display:none!important}</style>"""

def main():
    src = open("src.html").read()
    n = [0]
    def sub(m):
        key = m.group(1)
        title, cap, fn = FIGS[key]
        n[0] += 1
        return (f'<figure class="fig" id="fig-{key}">\n  <div class="fighead"><span class="eyebrow">Figure {n[0]}</span><span class="ftitle">{title}</span></div>\n'
                f'  <div class="art">\n{fn()}\n  </div>\n  <figcaption>{cap}</figcaption>\n</figure>')
    body = re.sub(r"<!-- FIG:(\w+) -->", sub, src)
    open("index.html", "w").write(body)
    t_end = body.index("</title>") + len("</title>")
    doc = ("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
           + body[:t_end] + "\n" + HEAD_EXTRA + "\n</head>\n<body>\n" + body[t_end:] + "\n</body>\n</html>\n")
    os.makedirs("docs", exist_ok=True)
    open("docs/index.html", "w").write(doc)
    print(f"built {n[0]} figures; index.html {len(body)} bytes; docs/index.html {len(doc)} bytes")

if __name__ == "__main__":
    main()
