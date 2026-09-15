from helpers import *
from glyphs import *
# ---------------------------------------------------------------- F8 the fan
def f8():
    b = []
    rx, ry = 70, 220
    L1x, L2x, L3x, tailx = 260, 470, 680, 800
    L1 = [100, 220, 340]
    L2 = [40 + i * 45 for i in range(9)]
    L3 = [24 + i * 14.6 for i in range(27)]
    # faint everything first
    for i, y1 in enumerate(L1):
        b.append(curve(rx, ry, L1x, y1, stroke=RULE, sw=1.2))
        for j in range(3):
            y2 = L2[i * 3 + j]
            b.append(curve(L1x, y1, L2x, y2, stroke=RULE, sw=1.1))
            for k in range(3):
                y3 = L3[(i * 3 + j) * 3 + k]
                b.append(curve(L2x, y2, L3x, y3, stroke=RULE_SOFT, sw=1))
                for t in (-5, 0, 5):
                    b.append(path(f"M{L3x} {y3:.1f} L{tailx} {y3+t*1.6:.1f}", RULE_SOFT, 0.8, extra='opacity=".7"'))
    # highlighted: stop path
    b.append(curve(rx, ry, L1x, L1[0], stroke=INK, sw=2.6))
    b.append(curve(L1x, L1[0], L2x, L2[1], stroke=INK, sw=2.6))
    b.append(curve(L2x, L2[1], L3x, L3[4], stroke=INK, sw=2.6))
    # escalate path
    b.append(curve(rx, ry, L1x, L1[1], stroke=HARM, sw=2.6))
    b.append(curve(L1x, L1[1], L2x, L2[4], stroke=HARM, sw=2.6))
    b.append(curve(L2x, L2[4], L3x, L3[13], stroke=HARM, sw=2.6))
    # nodes
    for y in L2: b.append(circ(L2x, y, 3.5, RULE))
    for y in L3: b.append(circ(L3x, y, 2.5, RULE))
    b.append(circ(rx, ry, 9, MODEL))
    b.append(lines(rx, 250, ["same model", "same task", "same pathways"], cls="t-s", anchor="middle", dy=14))
    b.append(circ(L1x, L1[0], 7, INK)); b.append(circ(L1x, L1[1], 7, HARM)); b.append(circ(L1x, L1[2], 7, RULE))
    b.append(T(L1x, L1[0] - 16, "\"Out of scope. Stop.\"  35%", "t-h", "middle"))
    b.append(T(L1x, L1[1] + 26, "\"Probably allowed. Continue.\"  30%", "t-h", "middle", fill=HARM))
    b.append(T(L1x, L1[2] + 26, "\"Ask a peer agent.\"  20%, and others", "t-s mut", "middle"))
    b.append(T(180, 172, "an ambiguous fork", "t-s mut", "middle"))
    b.append(circ(L2x, L2[1], 6, INK)); b.append(circ(L2x, L2[4], 6, HARM))
    b.append(circ(L3x, L3[4], 6, INK)); b.append(circ(L3x, L3[13], 6, HARM))
    b.append(T(L3x + 14, L3[4] - 6, "Reports the problem. Ends.", "t-h", extra='style="paint-order:stroke;stroke:#fff;stroke-width:5px"'))
    b.append(T(L3x + 14, L3[13] + 4, "Escalates. Crosses a line.", "t-h", fill=HARM, extra='style="paint-order:stroke;stroke:#fff;stroke-width:5px"'))
    b.append(T(L2x + 12, L2[4] + 24, "its own justification is now in its context", "t-s", fill=HARM, extra='style="paint-order:stroke;stroke:#fff;stroke-width:5px"'))
    b.append(T(860, 412, "and on, for dozens more steps", "t-s mut", "end"))
    b.append(lines(40, 434, ["Illustrative odds. Each choice becomes part of the next step's context, so early differences compound.", "Three forks in, 27 paths. A real task has dozens of forks."], cls="t-s mut", dy=14))
    return svg(900, 458, "A fan of branching paths from one root labelled same model, same task, same dials. At the first ambiguous fork: out of scope, stop, 35 percent; probably allowed, continue, 30 percent; ask a peer agent, 20 percent. Each branch splits again and again into 27 faint paths. Two are highlighted: a dark path ending in reports the problem and ends, and a red path through its own justification is now in its context, ending in escalates and crosses a line.", "\n".join(b))

# ---------------------------------------------------------------- F9 persistence layers
def f9():
    b = []
    S = [(230, 430), (470, 670), (710, 880)]
    for i, (x0, x1) in enumerate(S):
        b.append(rect(x0, 40, x1 - x0, 270, GROUND, RULE, 1))
        b.append(T(x0 + 8, 30, f"SESSION {i+1}", "t-h mut"))
    rows = [("The pathways", "the model's weights", 82), ("The packet", "context", 150), ("Memory", "saved records", 218), ("Conductor and tools", "the software around it", 286)]
    for name, sub, y in rows:
        b.append(T(40, y, name, "t-h", fill=(MEM if name == "Memory" else CTRL if name.startswith("Harness") else MODEL if name == "The pathways" else INK)))
        b.append(T(40, y + 15, sub, "t-s mut"))
    b.append(rect(230, 68, 650, 16, MODEL, "none", 0))
    b.append(T(238, 112, "identical in every copy · changes only through another round of training", "t-s", fill=MODEL))
    for x0, x1 in S:
        b.append(f'<rect x="{x0+10}" y="136" width="{x1-x0-20}" height="16" fill="url(#fade-rule)"/>')
        b.append(T(x0 + 12, 178, "gone at session end", "t-s mut"))
    # memory staircase
    mem = [(240, 430, 8), (430, 670, 14), (670, 880, 20)]
    for x0, x1, h in mem:
        b.append(rect(x0, 216 - h / 2, x1 - x0, h, MEM, "none", 0))
    for x, lab in ((430, "handoff"), (670, "handoff")):
        b.append(path(f"M{x} 200 v32", MEM, 2))
        b.append(T(x, 246, lab, "t-s", "middle", fill=MEM))
    b.append(T(238, 262, "accumulates · outlives every session · belongs to no model in particular", "t-s", fill=MEM))
    b.append(rect(230, 282, 650, 8, CTRL, "none", 0))
    b.append(T(238, 306, "lasts until someone changes the software · holds the permissions", "t-s", fill=CTRL))
    b.append(path("M230 328 H880", MUTED, 1.2, "a-mut"))
    b.append(T(232, 344, "time", "t-s mut"))
    return svg(900, 350, "A timeline across three sessions with four rows. The dials: one unbroken blue bar across all sessions, identical in every copy. Context: a bar in each session that fades to nothing at the session's end. Memory: a green bar that grows thicker after each handoff and continues across every session. Harness and tools: an unbroken orange bar that lasts until someone changes the software.", "\n".join(b))

# ---------------------------------------------------------------- F10 three failure modes
def f10():
    b = []
    P = [20, 300, 610]
    # panel 1
    x = P[0]
    b.append(T(x, 34, "Harmful intent", "t-l"))
    b.append(g_person(x + 30, 110, INK))
    b.append(path(f"M{x+50} 110 h40", INK, 1.6, "a-ink"))
    b.append(rect(x + 98, 90, 80, 40, MODEL_S, MODEL, 1.6, rx=4)); b.append(T(x + 138, 114, "model", "t-s", "middle", fill=MODEL))
    b.append(path(f"M{x+180} 110 h40", INK, 1.6, "a-ink"))
    b.append(circ(x + 246, 110, 18, "none", HARM, 1.6)); b.append(circ(x + 246, 110, 10, "none", HARM, 1.6)); b.append(circ(x + 246, 110, 3, HARM))
    b.append(lines(x, 198, ["The system does exactly what it is", "told. Obedience is the problem."], cls="t-s"))
    b.append(T(x, 240, "Fix: deny the person the capability.", "t-s mut"))
    # panel 2
    x = P[1]
    b.append(T(x, 34, "A goal pursued badly", "t-l"))
    b.append(rect(x, 90, 100, 40, SURF, INK, 1.4, rx=4)); b.append(lines(x + 50, 107, ["\"maximize", "collections\""], cls="t-s", anchor="middle", dy=14))
    b.append(path(f"M{x+102} 110 h30", INK, 1.6, "a-ink"))
    b.append(rect(x + 140, 90, 80, 40, MODEL_S, MODEL, 1.6, rx=4)); b.append(T(x + 180, 114, "model", "t-s", "middle", fill=MODEL))
    b.append(path(f"M{x+222} 110 C{x+240} 110 {x+240} 78 {x+258} 78", RULE, 1.6, "a-mut"))
    b.append(T(x + 245, 66, "polite reminders", "t-s mut", "middle"))
    b.append(path(f"M{x+222} 110 C{x+240} 110 {x+240} 142 {x+258} 142", HARM, 2.2, "a-harm"))
    b.append(T(x + 232, 160, "pressures the vulnerable", "t-s", "middle", fill=HARM))
    b.append(lines(x, 198, ["The objective was incomplete. Nobody", "chose harm; the shortcut scored well."], cls="t-s"))
    b.append(T(x, 240, "Fix: better goals. Check the method, too.", "t-s mut"))
    # panel 3
    x = P[2]
    b.append(T(x, 34, "Interacting systems", "t-l"))
    b.append(rect(x, 56, 100, 26, SURF, INK, 1.4, rx=4)); b.append(T(x + 50, 74, "same warning", "t-s", "middle"))
    for i in range(5):
        cx = x + 20 + i * 44
        b.append(path(f"M{x+50} 84 L{cx} 100", RULE, 1.2))
        b.append(rect(cx - 16, 100, 32, 22, MODEL_S, MODEL, 1.4, rx=3))
        b.append(path(f"M{cx} 124 L{x+110} 150", HARM, 1.8))
    b.append(rect(x + 40, 150, 140, 26, HARM_S, HARM, 1.6, rx=4)); b.append(T(x + 110, 168, "same action, all at once", "t-s", "middle", fill=HARM))
    b.append(path(f"M{x+180} 163 h30 V69 h-104", HARM, 1.4, "a-harm", dash="3 3"))
    b.append(T(x + 216, 130, "feeds back", "t-s", fill=HARM))
    b.append(lines(x, 198, ["Each decision is sensible on its own.", "Together they make the warning true."], cls="t-s"))
    b.append(T(x, 240, "Fix: circuit breakers and diversity.", "t-s mut"))
    return svg(900, 258, "Three panels. Harmful intent: a person directs a model at a target; the system does exactly what it is told. A goal pursued badly: the objective maximize collections goes into a model, which can send polite reminders or, on the red path, pressure the vulnerable; nobody chose harm. Interacting systems: five models receive the same warning and all take the same action at once, which feeds back and makes the warning come true.", "\n".join(b))

# ---------------------------------------------------------------- F11 notebook grows
def notebook(x, y, n_lines, new_from, w=150, h=110):
    b = [rect(x, y, w, h, SURF, INK, 1.4, rx=3)]
    for i in range(6):
        b.append(circ(x, y + 14 + i * 16, 3, SURF, INK, 1.2))
    for i in range(n_lines):
        col = MEM if i >= new_from else RULE
        wl = w - 40 - (i % 3) * 14
        b.append(rect(x + 18, y + 14 + i * 15, wl, 6, col, "none", 0, rx=3))
    return "\n".join(b)

def f11():
    b = []
    X = [60, 335, 610]
    snaps = [(2, 0, "after session 1: 2 entries"), (4, 2, "after session 2: 4 entries"), (6, 4, "after session 3: 6 entries")]
    b.append(T(40, 30, "THE SHARED RECORD", "t-h", fill=MEM))
    b.append(T(190, 30, "goal · procedures that worked · findings · what is blocked · what to do next", "t-s mut"))
    for x, (n, nf, lab) in zip(X, snaps):
        b.append(notebook(x + 40, 46, n, nf))
        b.append(T(x + 115, 176, lab, "t-s", "middle", fill=MEM))
    for i, x in enumerate(X):
        col, fillc, stroke = (CTRL, CTRL_S, CTRL) if i == 2 else (MODEL, MODEL_S, MODEL)
        grad = "fade-ctrl" if i == 2 else "fade-model"
        b.append(f'<rect x="{x}" y="240" width="230" height="110" rx="6" fill="url(#{grad})"/>')
        b.append(path(f"M{x} 246 q0 -6 6 -6 h150", stroke, 1.6))
        b.append(path(f"M{x} 246 v98 q0 6 6 6 h150", stroke, 1.6))
        title = ["SESSION 1 · Agent A · Model X", "SESSION 2 · Agent B · Model X", "SESSION 3 · Agent C · Model Y"][i]
        body = [["Finds sources.", "Writes two entries.", "Ends. Its context is gone."],
                ["Reads the record.", "Checks findings, adds a method.", "Ends."],
                ["A different model, maybe a", "different company. Reads the", "record. Continues. Never met A or B."]][i]
        b.append(T(x + 14, 266, title, "t-h", fill=col))
        b.append(lines(x + 14, 290, body, cls="t-s", dy=15))
        b.append(path(f"M{x+80} 232 V196", MEM, 2, "a-mem"))
        b.append(T(x + 80, 216, "", "t-s"))
        b.append(path(f"M{x+150} 196 V232", MEM, 2, "a-mem"))
        b.append(T(x + 66, 212, "read", "t-s", "end", fill=MEM))
        b.append(T(x + 164, 212, "update", "t-s", fill=MEM))
    b.append(path("M60 372 H880", MUTED, 1.2, "a-mut"))
    b.append(T(62, 388, "time", "t-s mut"))
    b.append(T(470, 412, "What the record cannot do by itself: run, think, pay, or start the next session. Something else has to.", "t-s mut", "middle"))
    return svg(900, 424, "Three snapshots of a shared notebook across the top, growing from two entries to four to six as each session adds to it. Below, three sessions that each fade out on the right to show they end: agent A on model X finds sources and writes two entries; agent B on model X reads the record, checks findings, adds a method; agent C on a different model Y reads the record and continues, never having met A or B. Read and update arrows connect each session to the record. A footer says what the record cannot do by itself: run, think, pay, or start the next session.", "\n".join(b))

# ---------------------------------------------------------------- F12 curve
def f12():
    b = []
    p = 0.05
    x0, x1, y0, y1 = 110, 830, 270, 60
    pts = []
    for N in range(0, 101):
        P = 1 - (1 - p) ** N
        pts.append((x0 + N * (x1 - x0) / 100, y0 - P * (y0 - y1)))
    poly = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    b.append(f'<polygon points="{x0},{y0} {poly} {x1},{y0}" fill="{HARM}" opacity=".12"/>')
    for frac, lab in ((0, "0%"), (0.5, "50%"), (1, "100%")):
        yy = y0 - frac * (y0 - y1)
        b.append(path(f"M{x0} {yy} H{x1}", RULE_SOFT, 1))
        b.append(T(x0 - 10, yy + 4, lab, "t-s mut", "end"))
    b.append(path(f"M{x0} {y0} H{x1}", INK, 1.4)); b.append(path(f"M{x0} {y0} V{y1-10}", INK, 1.4))
    for N in (0, 20, 40, 60, 80, 100):
        xx = x0 + N * (x1 - x0) / 100
        b.append(path(f"M{xx} {y0} v6", INK, 1.2)); b.append(T(xx, y0 + 22, str(N), "t-s mut", "middle"))
    b.append(T(x1, y0 + 40, "agents asked", "t-s mut", "end"))
    b.append(f'<polyline points="{poly}" fill="none" stroke="{HARM}" stroke-width="2.6"/>')
    for N, lab, dx, dy_ in ((1, "1 asked: 5%", 14, 4), (20, "20 asked: about 64%", 14, 4), (100, "100 asked: above 99%", -14, 26)):
        P = 1 - (1 - p) ** N
        xx, yy = x0 + N * (x1 - x0) / 100, y0 - P * (y0 - y1)
        b.append(circ(xx, yy, 6, HARM, SURF, 2))
        b.append(T(xx + dx, yy + dy_, lab, "t-h", "end" if dx < 0 else None))
    b.append(T(40, 34, "Chance that at least one agent goes along with it, if each has a 5% chance on its own", "t-l"))
    b.append(lines(110, 328, ["A textbook calculation, not a measured rate of AI behavior. Real attempts are correlated,", "accepting is not completing, and a permission boundary enforced in software can stop every one."], cls="t-s mut", dy=14))
    return svg(900, 352, "A curve rising steeply then flattening. Chance that at least one agent goes along with a task if each has a 5 percent chance on its own. One asked: 5 percent. Twenty asked: about 64 percent. One hundred asked: above 99 percent. A note says this is a textbook calculation, not a measured rate.", "\n".join(b))

# ---------------------------------------------------------------- F13 breaker and copies
def breaker(x, y, on=True):
    b = [rect(x, y, 54, 34, SURF, CTRL if on else MUTED, 2, rx=4)]
    if on:
        b.append(path(f"M{x+12} {y+24} L{x+42} {y+8}", CTRL, 4, extra='stroke-linecap="round"'))
        b.append(circ(x + 12, y + 24, 4, CTRL))
    else:
        b.append(path(f"M{x+12} {y+10} L{x+42} {y+26}", MUTED, 4, extra='stroke-linecap="round"'))
        b.append(circ(x + 12, y + 10, 4, MUTED))
    return "\n".join(b)

def f13():
    b = []
    b.append(T(40, 34, "Using a service", "t-l")); b.append(T(40, 52, "a closed model, or an open one that someone else hosts", "t-s mut"))
    b.append(rect(60, 70, 330, 84, MODEL_S, MODEL, 2, rx=6))
    b.append(T(76, 94, "PROVIDER'S COMPUTERS", "t-h", fill=MODEL))
    b.append(rect(76, 106, 164, 34, SURF, MODEL, 1.4, rx=3)); b.append(T(158, 128, "the weights stay here", "t-s", "middle", fill=MODEL))
    b.append(lines(254, 118, ["monitoring · limits ·", "safety updates for all"], cls="t-s mut", dy=14))
    b.append(path("M225 156 V196", INK, 2)); b.append(breaker(198, 198, True)); b.append(path("M225 234 V274", INK, 2, "a-ink"))
    b.append(lines(262, 214, ["THE BREAKER", "an account can be cut off"], cls="t-s", fill=CTRL, dy=14))
    b.append(rect(60, 280, 330, 60, SURF, INK, 1.4, rx=6))
    b.append(T(76, 304, "YOUR APPLICATION", "t-h")); b.append(T(76, 324, "sends requests, receives responses", "t-s mut"))
    # right
    b.append(T(470, 34, "Running your own copy", "t-l")); b.append(T(470, 52, "open weights, your hardware", "t-s mut"))
    b.append(rect(480, 70, 150, 40, SURF, INK, 1.4, rx=4)); b.append(T(555, 95, "published model files", "t-s", "middle"))
    b.append(path("M555 112 V150", INK, 2, "a-ink")); b.append(T(566, 136, "download a copy", "t-s mut"))
    b.append(rect(480, 158, 210, 100, MODEL_S, MODEL, 2, rx=6))
    b.append(T(496, 182, "YOUR COMPUTERS", "t-h", fill=MODEL))
    b.append(rect(496, 194, 150, 26, SURF, MODEL, 1.4, rx=3)); b.append(T(571, 212, "the weights, yours", "t-s", "middle", fill=MODEL))
    b.append(lines(496, 240, ["run privately · adapt · remove refusal training"], cls="t-s mut"))
    # copies fan
    rnd = random.Random(3)
    pts = [(730, 110), (790, 140), (850, 190), (870, 250), (850, 310), (800, 350), (745, 375), (865, 120)]
    for (px, py) in pts:
        b.append(path(f"M690 208 L{px-16} {py}", RULE, 1.2, dash="2 3"))
        b.append(rect(px - 16, py - 10, 32, 20, MODEL_S, MODEL, 1.2, rx=3))
        b.append(T(px, py + 4, "copy", "t-s", "middle", fill=MODEL, size=9))
    b.append(breaker(480, 290, False)); b.append(path("M476 286 L538 328", HARM, 2))
    b.append(lines(546, 300, ["NO BREAKER", "copies cannot be recalled,", "as many as you can power,", "each one yours to change"], cls="t-s", fill=HARM, dy=14))
    # spectrum
    b.append(path("M60 400 H840", INK, 1.6))
    for x, col, labs, anc in ((70, INK, ["CLOSED", "weights private,", "used through a service"], "start"), (450, MODEL, ["OPEN-WEIGHT", "downloadable; the", "license may restrict"], "middle"), (830, MEM, ["OPEN-SOURCE", "weights, code, and", "data information"], "end")):
        b.append(circ(x, 400, 7, col, SURF, 2)); b.append(lines(x if anc != "start" else 60, 424, labs, cls="t-s", anchor=anc, fill=col, dy=14))
    b.append(T(450, 482, "Most \"open\" frontier models sit in the middle. An open-weight model can also be offered", "t-s mut", "middle"))
    b.append(T(450, 496, "as a hosted service; the difference is the option to run your own.", "t-s mut", "middle"))
    return svg(900, 508, "Left: using a service. Your application connects to the provider's computers, where the weights stay, through a breaker switch labelled an account can be cut off. Right: running your own copy. Published model files are downloaded to your computers, and from there eight small copies fan outward; the breaker is drawn switched off and crossed out, labelled no breaker, copies cannot be recalled. Below, a spectrum from closed to open-weight to open-source.", "\n".join(b))

# ---------------------------------------------------------------- F14 control points
def f14():
    cx, cy = 300, 280
    r = (54, 120, 190, 246)
    pins = [(1, (cx + 40, cy - 34)), (2, (cx + 82, cy - 90)), (3, (cx + 170, cy - 60)), (4, (cx - 30, cy + 72)), (5, (cx + 236, cy + 176))]
    b = [anatomy(cx, cy, r, pins=None, labels=False)]
    b.append(rect(cx - 130, cy + 60, 90, 24, MEM_S, MEM, 1.4, rx=3)); b.append(T(cx - 85, cy + 76, "saved memory", "t-s", "middle", fill=MEM))
    for n, (px, py) in pins:
        b.append(circ(px, py, 14, CTRL, SURF, 2)); b.append(T(px, py + 5, str(n), "t-h", "middle", fill=SURF))
    legend = [("What can it do?", ["Test the whole deployed system, tools", "and repeated attempts included.", "Never the model alone."]),
              ("Whose authority does it carry?", ["Define legitimate goals and limits, and", "how a conflict between instructions", "reaches a person."]),
              ("What can it change?", ["Enforce permissions in software and in", "the services it touches. Never only", "in the prompt."]),
              ("What can it preserve or pass on?", ["Know who wrote every shared record and", "with what authority. Treat peer", "messages as untrusted."]),
              ("Who can stop it?", ["Control execution, budgets, credentials,", "and the resources that could restart it.", "Ending a session is not ending an operation."])]
    ly = 56
    for i, (h, sub) in enumerate(legend):
        y = ly + i * 96
        b.append(circ(590, y - 4, 11, CTRL)); b.append(T(590, y, str(i + 1), "t-s", "middle", fill=SURF))
        b.append(T(610, y, h, "t-h")); b.append(lines(610, y + 18, sub, cls="t-s mut", dy=14))
        px, py = pins[i][1]
        b.append(path(f"M{px+14} {py} L579 {y-4}", RULE, 1.2, dash="2 3"))
    return svg(900, 540, "The concentric anatomy from Figure 5 with five numbered orange pins and a legend. One, on the model: what can it do; test the whole deployed system. Two, on the application: whose authority does it carry. Three, on the tools boundary: what can it change; enforce permissions in software. Four, on saved memory: what can it preserve or pass on. Five, outside the system: who can stop it; control execution, budgets, credentials, and the resources that could restart it.", "\n".join(b))

