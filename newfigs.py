# New figures for draft 3. Imported by build.py, which supplies the helpers.
import math, random
from helpers import *
from glyphs import *

# ---------------------------------------------------------------- network
def cat_face(cx, cy, r=30, col=INK):
    b = []
    b.append(path(f"M{cx-r*0.85} {cy-r*0.45} L{cx-r*1.05} {cy-r*1.35} L{cx-r*0.25} {cy-r*0.92} Z", col, 1.6, fill=SURF))
    b.append(path(f"M{cx+r*0.85} {cy-r*0.45} L{cx+r*1.05} {cy-r*1.35} L{cx+r*0.25} {cy-r*0.92} Z", col, 1.6, fill=SURF))
    b.append(circ(cx, cy, r, SURF, col, 1.6))
    b.append(circ(cx - r*0.38, cy - r*0.15, 3, col)); b.append(circ(cx + r*0.38, cy - r*0.15, 3, col))
    b.append(path(f"M{cx-4} {cy+r*0.18} L{cx+4} {cy+r*0.18} L{cx} {cy+r*0.32} Z", col, 1, fill=col))
    for dy, dx in ((-2, 0), (4, 2), (10, 0)):
        b.append(path(f"M{cx-8} {cy+r*0.3+dy} L{cx-r*1.15-dx} {cy+r*0.2+dy*1.4}", col, 1.1))
        b.append(path(f"M{cx+8} {cy+r*0.3+dy} L{cx+r*1.15+dx} {cy+r*0.2+dy*1.4}", col, 1.1))
    return "\n".join(b)

def fig_network():
    rnd = random.Random(11)
    b = []
    b.append(rect(40, 130, 120, 120, GROUND, RULE, 1.2, rx=8))
    b.append(cat_face(100, 195, 30))
    b.append(T(100, 272, "a picture", "t-s mut", "middle"))
    IN = [(250, y) for y in (110, 170, 230, 290, 350)]
    inl = ["pointed ears", "whiskers", "long snout", "floppy ears", "fur pattern"]
    H1 = [(440, y) for y in (95, 151, 207, 263, 319, 375)]
    H2 = [(620, y) for y in (95, 151, 207, 263, 319, 375)]
    OUT = [(800, 180), (800, 290)]
    for (x, y) in IN:
        b.append(path(f"M160 195 C 200 195 200 {y} {x-8} {y}", RULE, 1))
    def conns(A, B):
        for (x1, y1) in A:
            for (x2, y2) in B:
                w = rnd.uniform(0.4, 2.2); o = rnd.uniform(0.10, 0.42)
                b.append(path(f"M{x1} {y1} L{x2} {y2}", INK, round(w, 2), extra=f'opacity="{o:.2f}"'))
    conns(IN, H1); conns(H1, H2); conns(H2, OUT)
    # strengthened path (blue)
    strong = [(IN[0], H1[1]), (IN[1], H1[1]), (H1[1], H2[2]), (H2[2], OUT[0]), (IN[4], H1[3]), (H1[3], H2[2])]
    for (x1, y1), (x2, y2) in strong:
        b.append(path(f"M{x1} {y1} L{x2} {y2}", MODEL, 3.4, extra='stroke-linecap="round"'))
    weak = [(IN[2], H1[4]), (H1[4], H2[4]), (H2[4], OUT[1])]
    for (x1, y1), (x2, y2) in weak:
        b.append(path(f"M{x1} {y1} L{x2} {y2}", HARM, 1.6, dash="5 4", extra='opacity=".8"'))
    for (x, y), lab in zip(IN, inl):
        b.append(circ(x, y, 8, SURF, INK, 1.6)); b.append(T(x - 14, y + 4, lab, "t-s", "end"))
    for (x, y) in H1 + H2:
        b.append(circ(x, y, 8, SURF, INK, 1.6))
    for (x, y) in ((440, 151), (620, 207), (440, 263)):
        b.append(circ(x, y, 8, MODEL_S, MODEL, 2))
    b.append(circ(800, 180, 13, MODEL_S, MODEL, 2.4)); b.append(circ(800, 290, 13, SURF, RULE, 1.6))
    b.append(T(800, 152, "CAT", "t-l", "middle", fill=MODEL)); b.append(T(800, 210, "91%", "t-s", "middle", fill=MODEL))
    b.append(T(800, 264, "DOG", "t-l", "middle", fill=MUTED)); b.append(T(800, 320, "9%", "t-s", "middle", fill=MUTED))
    b.append(T(300, 50, "a few dozen connections, each with a strength.", "t-s mut"))
    b.append(T(300, 65, "the strengths are the whole story.", "t-s mut"))
    # annotations
    b.append(T(530, 130, "+  this pathway helped: a little stronger", "t-s", fill=MODEL, extra='style="paint-order:stroke;stroke:#fff;stroke-width:5px"'))
    b.append(T(530, 356, "−  this pathway misled: a little weaker", "t-s", fill=HARM, extra='style="paint-order:stroke;stroke:#fff;stroke-width:5px"'))
    # loop strip
    y = 420
    steps = ["show a picture", "it guesses", "compare with the answer", "nudge the connections"]
    x = 40
    for i, st in enumerate(steps):
        w = len(st) * 7.2 + 24
        b.append(rect(x, y, w, 30, GROUND if i < 3 else CTRL_S, RULE if i < 3 else CTRL, 1.2, rx=15))
        b.append(T(x + w / 2, y + 19, st, "t-s", "middle", fill=(CTRL if i == 3 else INK)))
        x += w + 8
        if i < 3:
            b.append(path(f"M{x-6} {y+15} h14", INK, 1.4, "a-ink")); x += 16
    b.append(path(f"M{x-4} {y+15} h24 q14 0 14 -14 V{y-8} H60", CTRL, 1.4, "a-ctrl", dash="4 3"))
    b.append(T(40, y - 16, "THE LOOP, repeated a few hundred thousand times", "t-h", fill=CTRL))
    return svg(900, 470, "A small neural network. On the left a picture of a cat feeds five input features: pointed ears, whiskers, long snout, floppy ears, fur pattern. Two hidden layers of units connect to two outputs, cat and dog. Every connection has a strength drawn as line thickness. A blue pathway from pointed ears and whiskers to the cat output is marked: this pathway helped, a little stronger. A dashed red pathway from long snout to the dog output is marked: this pathway misled, a little weaker. The output reads cat 91 percent, dog 9 percent. A strip at the bottom shows the loop: show a picture, it guesses, compare with the answer, nudge the connections, again a few hundred thousand times.", "\n".join(b))

# ---------------------------------------------------------------- world model
def mini_net(x, y, col=RULE, dot=MUTED, r=1.7, op=1.0):
    cols = [(6, (6, 17, 28)), (20, (6, 17, 28)), (34, (11, 23))]
    b = []
    for (x1, ys1), (x2, ys2) in zip(cols, cols[1:]):
        for y1 in ys1:
            for y2 in ys2:
                b.append(path(f"M{x+x1} {y+y1} L{x+x2} {y+y2}", col, 0.6, extra=f'opacity="{op*0.9:.2f}"'))
    for xx, ys in cols:
        for yy in ys:
            b.append(circ(x + xx, y + yy, r, dot, extra=f'opacity="{op:.2f}"'))
    return "\n".join(b)

def fig_worldmodel():
    b = []
    # small network at left
    b.append(rect(40, 50, 200, 150, SURF, INK, 1.4, rx=6))
    IN = [(70, y) for y in (85, 125, 165)]; H1 = [(120, y) for y in (75, 105, 135, 165)]; H2 = [(170, y) for y in (75, 105, 135, 165)]; OUT = [(215, 105), (215, 145)]
    rnd = random.Random(5)
    for A, B_ in ((IN, H1), (H1, H2), (H2, OUT)):
        for (x1, y1) in A:
            for (x2, y2) in B_:
                b.append(path(f"M{x1} {y1} L{x2} {y2}", INK, round(rnd.uniform(0.4, 1.8), 2), extra=f'opacity="{rnd.uniform(0.12,0.4):.2f}"'))
    for (x, y) in IN + H1 + H2 + OUT:
        b.append(circ(x, y, 5, SURF, INK, 1.4))
    b.append(circ(215, 105, 6, MODEL_S, MODEL, 1.8))
    b.append(T(140, 222, "the cat/dog network", "t-s", "middle"))
    b.append(T(140, 237, "a few dozen connections", "t-s mut", "middle"))
    # zoom lines
    b.append(path("M240 50 L300 50", MODEL, 1.2, dash="4 3")); b.append(path("M240 200 L300 86", MODEL, 1.2, dash="4 3"))
    b.append(T(140, 290, "one of billions", "t-h", "middle", fill=MODEL))
    b.append(path("M140 300 L296 300", MODEL, 1.2, "a-model"))
    # mosaic
    mx, my, cw, ch, cols, rows = 300, 50, 40, 36, 14, 10
    b.append(rect(mx, my, cw * cols, ch * rows, GROUND, RULE, 1.2))
    for i in range(cols * rows):
        x = mx + (i % cols) * cw; y = my + (i // cols) * ch
        b.append(mini_net(x, y))
    b.append(rect(mx, my, cw, ch, "none", MODEL, 2))
    tags = [("grammar", 330, 100, MODEL), ("Paris is in France", 500, 84, MODEL), ("how code works", 690, 120, MODEL),
            ("how doctors write", 360, 190, MODEL), ("how an argument is built", 560, 210, MODEL), ("arithmetic", 770, 232, MODEL),
            ("how people persuade", 420, 300, HARM), ("how people lie", 640, 320, HARM), ("how attacks work", 470, 380, HARM), ("how to write a memo", 720, 386, MODEL)]
    for lab, x, y, col in tags:
        w = len(lab) * 7.2 + 18
        b.append(rect(x, y, w, 24, SURF, col, 1.4, rx=12))
        b.append(T(x + w / 2, y + 16, lab, "t-s", "middle", fill=col))
    b.append(T(mx + cw * cols, my + ch * rows + 22, "and hundreds of billions more, most with no name", "t-s mut", "end"))
    b.append(T(300, 470, "THE WORLD MODEL", "t-xl", fill=MODEL))
    b.append(T(300, 488, "every connection set by the same loop: guess the next word, compare, nudge.", "t-s"))
    b.append(T(300, 502, "Trillions of times. Nobody wrote any of it in.", "t-s"))
    b.append(T(40, 340, "Blue tags: patterns", "t-s mut")); b.append(T(40, 355, "we wanted.", "t-s mut"))
    b.append(T(40, 380, "Red tags: patterns", "t-s", fill=HARM)); b.append(T(40, 395, "that came along,", "t-s", fill=HARM)); b.append(T(40, 410, "because they are in", "t-s", fill=HARM)); b.append(T(40, 425, "the text too.", "t-s", fill=HARM))
    return svg(900, 514, "On the left, the small cat-and-dog network, labelled one of billions. Dashed lines zoom out to a large mosaic of tiny networks representing the world model. Tags float over the mosaic naming pathways it formed: grammar, Paris is in France, how code works, how doctors write, how an argument is built, arithmetic, how to write a memo, and in red, how people persuade, how people lie, how attacks work. A note says every connection was set by the same loop, guess the next word, compare, nudge, trillions of times.", "\n".join(b))

# ---------------------------------------------------------------- habits
def fig_habits():
    b = []
    outs = ["continues like a magazine article", "answers helpfully", "invents a forum thread", "makes up confident nonsense", "writes it as fan fiction"]
    def row(y0, title, sub, weights, labels, fills, note):
        b.append(T(40, y0, title, "t-l")); b.append(T(40, y0 + 17, sub, "t-s mut"))
        py = y0 + 46
        b.append(rect(40, py, 220, 60, SURF, INK, 1.4, rx=6))
        b.append(T(150, py + 26, "\"How should I prepare", "t-s", "middle")); b.append(T(150, py + 43, "for a board meeting?\"", "t-s", "middle"))
        ys = [py - 12 + i * 26 for i in range(5)]
        for i, (lab, w, fl) in enumerate(zip(labels, weights, fills)):
            col = MODEL if fl == "strong" else HARM if fl == "harm" else INK
            op = 1 if fl == "strong" else 0.9 if fl == "base" else 0.35
            b.append(path(f"M262 {py+30} C 360 {py+30} 360 {ys[i]} 470 {ys[i]}", col, w, extra=f'opacity="{op}" stroke-linecap="round"'))
            b.append(T(482, ys[i] + 4, lab, "t-h" if fl == "strong" else "t-s", fill=(col if fl in ("strong", "harm") else (INK if fl == "base" else MUTED))))
        b.append(lines(40, py + 84, note, cls="t-s mut", dy=14))
    row(36, "BASE MODEL, after pre-training", "It knows what text tends to follow text. It is not yet an assistant.", [1.8] * 5, outs, ["base"] * 5, [])
    b.append(T(760, 112, "ALL FIVE ABOUT", "t-l", fill=MUTED)); b.append(T(760, 130, "EQUALLY LIKELY", "t-l", fill=MUTED))
    # band
    b.append(rect(40, 214, 820, 58, CTRL_S, CTRL, 1.2, rx=4))
    b.append(g_person(64, 240, CTRL))
    b.append(T(84, 234, "POST-TRAINING, the same nudging, aimed at behavior", "t-h", fill=CTRL))
    b.append(T(84, 250, "people compare two answers and pick the better one · tasks that go well get rewarded", "t-s", fill=CTRL))
    b.append(T(84, 264, "harmful requests get refusal drills · far fewer examples than pre-training", "t-s", fill=CTRL))
    b.append(path("M150 274 V296", CTRL, 2.4, "a-ctrl"))
    row(314, "ASSISTANT MODEL, after post-training", "Same pathways, nudged again. Same question.", [1, 5.5, 1, 1.2, 1],
        ["magazine article  ·  rare", "answers helpfully  ·  about 85%", "forum thread  ·  rare", "confident nonsense  ·  rare, not gone", "fan fiction  ·  rare"],
        ["dim", "strong", "dim", "harm", "dim"], [])
    b.append(T(760, 352, "DIMMED,", "t-l", fill=CTRL)); b.append(T(760, 370, "NOT DELETED", "t-l", fill=CTRL))
    b.append(lines(760, 390, ["The pathways are", "still in there.", "Only the odds", "changed. A habit,", "not a lock."], cls="t-s", dy=14))
    b.append(T(40, 476, "Illustrative percentages. Real distributions are not published and depend on the request.", "t-s mut"))
    return svg(900, 490, "Two rows. Top: the base model after pre-training. The question how should I prepare for a board meeting fans out into five continuations of equal weight: continues like a magazine article, answers helpfully, invents a forum thread, makes up confident nonsense, writes it as fan fiction. Between the rows, a band labelled post-training: people compare two answers and pick the better one, tasks that go well get rewarded, harmful requests get refusal drills. Bottom: the assistant model after post-training. The same question now flows overwhelmingly to answers helpfully, about 85 percent. The other continuations are thin and faint, labelled rare, with confident nonsense marked rare and still in there. A note reads dimmed, not deleted: the odds changed, that is a habit not a lock.", "\n".join(b))

# ---------------------------------------------------------------- packet
def fig_packet():
    b = []
    # chat window
    b.append(T(40, 30, "WHAT YOU SEE", "t-l"))
    b.append(rect(40, 44, 340, 470, SURF, INK, 1.4, rx=8))
    b.append(path("M40 80 H380", RULE, 1))
    b.append(circ(60, 62, 5, RULE)); b.append(circ(76, 62, 5, RULE)); b.append(circ(92, 62, 5, RULE))
    b.append(T(210, 66, "Acme Assistant", "t-h", "middle"))
    b.append(rect(56, 100, 230, 40, GROUND, RULE, 1, rx=12))
    b.append(T(70, 124, "Hi Luyen. What do you need?", "t-s"))
    b.append(rect(120, 164, 244, 66, MODEL_S, MODEL, 1.4, rx=12))
    b.append(T(136, 188, "Prepare a briefing on Acme", "t-h", fill=MODEL)); b.append(T(136, 206, "before my 3pm.", "t-h", fill=MODEL))
    b.append(rect(136, 240, 200, 26, SURF, MODEL, 1, rx=13)); b.append(g_file(152, 253, MODEL)); b.append(T(166, 257, "acme-annual-report.pdf", "t-xs", fill=MODEL))
    b.append(rect(56, 456, 268, 40, SURF, RULE, 1.2, rx=20)); b.append(T(72, 481, "Message", "t-s mut"))
    b.append(circ(348, 476, 16, MODEL)); b.append(path("M342 476 L354 476 M349 470 L355 476 L349 482", SURF, 1.8))
    b.append(T(210, 300, "one line, twelve words,", "t-s mut", "middle")); b.append(T(210, 315, "and one attachment", "t-s mut", "middle"))
    # packet document
    b.append(T(440, 30, "WHAT THE MODEL RECEIVES", "t-l"))
    dx, dy, dw = 440, 44, 420
    secs = [("SYSTEM INSTRUCTIONS", True, 100, ["You are Acme Assistant. Be concise and cite sources.", "Never share internal pricing. Do not give legal advice.", "Tools you may request: search, read_file, send_email", "(send_email requires the user's approval)."]),
            ("SAVED MEMORY", True, 48, ["Prefers one-page briefs. Meeting is with Acme's CFO."]),
            ("ATTACHED DOCUMENT", False, 138, ["Acme Annual Report 2025, excerpt, about 6,000 words"]),
            ("SEARCH RESULTS · added by the app", True, 58, ["Acme Q2 earnings call: revenue up 12%, margin down…", "Reuters: Acme names new CFO…"]),
            ("CONVERSATION SO FAR", False, 40, ["Assistant: Hi Luyen. What do you need?"]),
            ("YOUR MESSAGE", False, 46, ["Prepare a briefing on Acme before my 3pm."])]
    y = dy
    b.append(rect(dx, dy, dw, sum(s[2] for s in secs), SURF, INK, 1.4))
    for name, hidden, h, ls in secs:
        you = name == "YOUR MESSAGE"
        fill = MODEL_S if you else (GROUND if hidden else SURF)
        b.append(rect(dx + 1, y + 1, dw - 2, h - 2, fill, "none", 0))
        b.append(path(f"M{dx} {y} H{dx+dw}", RULE, 1))
        b.append(T(dx + 12, y + 16, name, "t-xs", fill=(MODEL if you else MUTED), extra='style="letter-spacing:.08em"'))
        if hidden:
            b.append(rect(dx + dw - 108, y + 5, 96, 16, CTRL_S, CTRL, 1, rx=8)); b.append(T(dx + dw - 60, y + 16, "hidden from you", "t-xs", "middle", fill=CTRL))
        yy = y + 32
        for l in ls:
            b.append(T(dx + 12, yy, l, "t-h" if you else "t-s", fill=(MODEL if you else INK))); yy += 14
        if name == "ATTACHED DOCUMENT":
            rnd = random.Random(2)
            for k in range(6):
                b.append(rect(dx + 12, yy + 2 + k * 14, rnd.uniform(200, 380), 6, RULE, "none", 0, rx=3))
        if you:
            y_you = y + h / 2
        y += h
    # connector
    b.append(path(f"M366 197 C 400 197 400 {y_you} {dx-4} {y_you}", MODEL, 1.6, "a-model", dash="5 4"))
    b.append(T(870, y + 30, "About 9,000 words go in.", "t-h", "end")); b.append(T(870, y + 46, "Twelve of them are yours.", "t-h", "end", fill=MODEL))
    b.append(T(440, y + 30, "Illustrative packet.", "t-s mut"))
    return svg(900, 560, "Left: a chat window showing one user message, prepare a briefing on Acme before my 3pm, with an attached PDF. Right: the packet the model actually receives, drawn as a document with stacked sections: system instructions hidden from you, saved memory hidden from you, the attached document excerpt, search results added by the app, the conversation so far, and finally your message, highlighted. A dashed line connects the chat bubble to that final slice. A note reads: about 9,000 words go in, twelve of them are yours.", "\n".join(b))

# ---------------------------------------------------------------- conductor (comic strip)
def fig_conductor():
    b = []
    PW, PH, GAP = 268, 268, 16
    def panel(col, row, step, bubble, chip, gate, gate_lab, result, last=False):
        x = 40 + col * (PW + GAP); y = 40 + row * (PH + GAP)
        b.append(rect(x, y, PW, PH, SURF, INK, 1.4, rx=6))
        b.append(rect(x, y, PW, 28, GROUND, "none", 0, rx=6)); b.append(path(f"M{x} {y+28} H{x+PW}", RULE, 1))
        b.append(T(x + 12, y + 19, step, "t-h"))
        # model bubble
        b.append(rect(x + 12, y + 40, PW - 24, 22 + 14 * len(bubble), MODEL_S, MODEL, 1.2, rx=8))
        b.append(T(x + 22, y + 56, "MODEL", "t-xs", fill=MODEL, extra='style="letter-spacing:.08em"'))
        for i, l in enumerate(bubble):
            b.append(T(x + 22, y + 72 + i * 14, l, "t-s", fill=MODEL))
        yy = y + 62 + 14 * len(bubble) + 14
        if chip:
            b.append(path(f"M{x+40} {yy-6} v10", INK, 1.2, "a-ink"))
            yy += 16
            b.append(rect(x + 12, yy, PW - 24, 24, SURF, INK, 1.2, rx=4))
            b.append(T(x + 22, yy + 16, chip, "t-s"))
            yy += 24
        if gate:
            gc = MEM if gate == "ok" else HARM
            b.append(path(f"M{x+40} {yy+2} v10", INK, 1.2, "a-ink"))
            yy += 20
            b.append(circ(x + 28, yy + 10, 11, gc))
            mark = f"M{x+22} {yy+10} L{x+27} {yy+15} L{x+35} {yy+5}" if gate == "ok" else f"M{x+23} {yy+5} L{x+33} {yy+15} M{x+33} {yy+5} L{x+23} {yy+15}"
            b.append(path(mark, SURF, 2.2))
            b.append(T(x + 46, yy + 9, "GATE", "t-xs", fill=gc, extra='style="letter-spacing:.08em"'))
            b.append(T(x + 46, yy + 24, gate_lab, "t-s", fill=gc))
            yy += 30
        for i, l in enumerate(result):
            b.append(T(x + 12, yy + 14 + i * 14, l, "t-s" if not last else "t-h", fill=INK if not last else MODEL))
    panel(0, 0, "STEP 1", ["I need Acme's latest numbers."], "search(\"Acme report 2025\")", "ok", "search is allowed. Runs it.", ["Result into the packet:", "3 results found."])
    panel(1, 0, "STEP 2", ["Open the report. Find revenue."], "read_file(\"acme-report.pdf\")", "ok", "reading files is allowed.", ["Result into the packet:", "revenue up 12%, margin down 3 pts."])
    panel(2, 0, "STEP 3", ["Enough. Draft the one-page", "briefing."], None, None, None, ["No tool requested, so no gate.", "The model just writes.", "", "Draft: three bullets, one risk,", "one question for the CFO."])
    panel(0, 1, "STEP 4", ["Send it to the CFO now so she", "has it before the meeting."], "send_email(cfo@acme.com)", "no", "needs your approval. Stopped.", ["Result into the packet:", "\"not permitted without approval.\"", "The model can draft an email.", "The system cannot send one."])
    panel(1, 1, "STEP 5", ["Ask the user instead."], None, None, None, ["Returned to you:", "", "Briefing ready for review.", "Send to Acme's CFO?", "[ Yes ]  [ No ]"], last=True)
    # panel 6: the loop
    x = 40 + 2 * (PW + GAP); y = 40 + (PH + GAP)
    b.append(rect(x, y, PW, PH, CTRL_S, CTRL, 1.4, rx=6))
    b.append(T(x + 12, y + 24, "THE CONDUCTOR", "t-l", fill=CTRL))
    b.append(T(x + 12, y + 42, "runs this loop until the task is done", "t-s", fill=CTRL))
    steps = ["reads the packet", "the model proposes a step", "the gate checks it", "the tool runs", "result into the packet"]
    for i, st in enumerate(steps):
        yy = y + 70 + i * 26
        b.append(circ(x + 30, yy - 4, 9, CTRL)); b.append(T(x + 30, yy, str(i + 1), "t-xs", "middle", fill=SURF))
        b.append(T(x + 48, yy, st, "t-s"))
    b.append(path(f"M{x+252} {y+70+4*26-4} V{y+70-4} H{x+244}", CTRL, 1.6, "a-ctrl", dash="4 3"))
    b.append(T(x + 262, y + 128, "again", "t-xs", fill=CTRL, extra=f'transform="rotate(90 {x+262} {y+128})"'))
    b.append(lines(x + 12, y + 218, ["What the model wants, what it is", "allowed, and what actually happened", "are three different things."], cls="t-h", fill=CTRL, dy=15))
    return svg(900, 616, "A six-panel strip. Step 1: the model says I need Acme's latest numbers and requests a search; the gate allows it and three results go into the packet. Step 2: it requests to read the report file; allowed; revenue up 12 percent goes into the packet. Step 3: it drafts the briefing with no tool, so no gate. Step 4: it requests to send an email to the CFO; the gate refuses, needs your approval, stopped. Step 5: it returns the briefing to you with a question, send to the CFO, yes or no. Panel 6 shows the conductor's loop: reads the packet, model proposes, gate checks, tool runs, result goes back.", "\n".join(b))

# ---------------------------------------------------------------- stack (exploded plates)
PLATES = [("THE PATHWAYS", "the weights, set once in pre-training", MODEL, SURF),
          ("THE HABITS", "post-training: habits, not locks", MODEL_S, MODEL),
          ("INSTRUCTIONS", "the hidden system prompt and rules", SURF, INK),
          ("THE PACKET", "your message, documents, saved memory", SURF, INK),
          ("TOOLS", "search, files, email, code, money", CTRL_S, CTRL),
          ("THE CONDUCTOR AND THE GATE", "runs the loop, checks every request", CTRL_S, CTRL),
          ("THE WORLD", "internet, your systems, other agents", GROUND, MUTED)]

def plate(x0, y, w, lean, fill, stroke, title, tcol, note=None, ncol=None):
    b = []
    b.append(path(f"M{x0} {y+8} L{x0+w} {y+8} L{x0+w} {y} L{x0} {y} Z", stroke, 1, fill=stroke, extra='opacity=".35"'))
    b.append(path(f"M{x0} {y} L{x0+w} {y} L{x0+w+lean} {y-46} L{x0+lean} {y-46} Z", stroke, 1.6, fill=fill))
    b.append(T(x0 + lean / 2 + 22, y - 26, title, "t-h", fill=tcol))
    if note:
        b.append(T(x0 + lean / 2 + 22, y - 10, note, "t-s", fill=ncol or tcol, extra='opacity=".85"'))
    return "\n".join(b)

def stack(x0, ybase, w, lean, step=66, notes=True, notes_x=None):
    b = []
    for i, (title, note, fill, stroke) in enumerate(PLATES):
        y = ybase - i * step
        tcol = SURF if fill == MODEL else (MODEL if stroke == MODEL else CTRL if stroke == CTRL else MUTED if stroke == MUTED else INK)
        b.append(plate(x0, y, w, lean, fill, stroke, title, tcol, note if notes else None))
    return "\n".join(b)

def bracket(x, y1, y2, label, col=INK, sub=None):
    b = [path(f"M{x+8} {y1} H{x} V{y2} H{x+8}", col, 1.6)]
    b.append(T(x - 8, (y1 + y2) / 2 + 4, label, "t-l", "end", fill=col))
    if sub: b.append(T(x - 8, (y1 + y2) / 2 + 20, sub, "t-s", "end", fill=col))
    return "\n".join(b)

def fig_stack():
    x0, yb, w, lean, step = 380, 540, 330, 110, 66
    b = [stack(x0, yb, w, lean, step)]
    def span(i0, i1):
        return (yb - i1 * step - 46 + 4, yb - i0 * step + 8)
    y1, y2 = span(0, 1); b.append(bracket(x0 - 30, y1, y2, "a model", MODEL, "pathways + habits"))
    y1, y2 = span(0, 3); b.append(bracket(x0 - 130, y1, y2, "a chatbot", INK, "+ instructions + packet"))
    y1, y2 = span(0, 5); b.append(bracket(x0 - 230, y1, y2, "an agent", CTRL, "+ tools + conductor"))
    b.append(T(40, 40, "Bottom to top: what is trained, then what is wrapped around it.", "t-s mut"))
    return svg(900, 580, "Seven plates stacked in an exploded view, bottom to top: the pathways, the weights set once in pre-training; the habits, post-training; instructions, the hidden system prompt; the packet, your message, documents, memory; tools; the conductor and the gate; the world. Brackets on the left show that a model is the bottom two plates, a chatbot adds instructions and the packet, and an agent adds tools and the conductor.", "\n".join(b))

def fig_control():
    x0, yb, w, lean, step = 150, 540, 260, 90, 66
    b = [stack(x0, yb, w, lean, step, notes=False)]
    pins = [(1, (x0 + 190, yb - 0 * step - 40)), (2, (x0 + 200, yb - 2 * step - 40)), (3, (x0 + 278, yb - 5 * step - 40)), (4, (x0 + 190, yb - 3 * step - 40)), (5, (x0 + 200, yb - 6 * step - 40))]
    legend = [("What can it do?", ["Test the whole stack, tools and repeated", "attempts included. Never the model alone."]),
              ("Whose authority does it carry?", ["Define legitimate goals and limits, and", "how a conflict reaches a person."]),
              ("What can it change?", ["Enforce permissions in the gate and in the", "services it touches. Not just the packet."]),
              ("What can it preserve or pass on?", ["Know who wrote every notebook entry and", "with what authority. Peer messages are", "untrusted input."]),
              ("Who can stop it?", ["Control execution, budgets, credentials,", "and what could restart it. Ending a", "session is not ending an operation."])]
    for i, (h, sub) in enumerate(legend):
        y = 70 + i * 100
        b.append(circ(560, y - 4, 12, CTRL)); b.append(T(560, y + 1, str(i + 1), "t-h", "middle", fill=SURF))
        b.append(T(582, y, h, "t-h")); b.append(lines(582, y + 18, sub, cls="t-s mut", dy=14))
        px, py = pins[i][1]
        b.append(path(f"M{px+14} {py} L546 {y-4}", RULE, 1.2, dash="2 3"))
    for n, (px, py) in pins:
        b.append(circ(px, py, 14, CTRL, SURF, 2)); b.append(T(px, py + 5, str(n), "t-h", "middle", fill=SURF))
    return svg(900, 580, "The same seven-plate stack with five numbered orange pins. One, on the pathways and habits: what can it do. Two, on instructions: whose authority does it carry. Three, on the conductor and gate: what can it change. Four, on the packet and memory: what can it preserve or pass on. Five, on the world: who can stop it. A legend on the right explains each.", "\n".join(b))
