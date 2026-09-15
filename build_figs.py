#!/usr/bin/env python3
"""Regenerates the 14 inline SVG figures in index.html. Run from this folder."""
import math, random, re

INK = "#171B1C"; MUTED = "#66717A"; RULE = "#C9CFCB"; RULE_SOFT = "#E1E5E1"; GROUND = "#F3F4F1"; SURF = "#FFFFFF"
MODEL = "#1E5A86"; MODEL_S = "#D5E4F0"
CTRL = "#B9771A"; CTRL_S = "#F4E3C4"
HARM = "#A8432E"; HARM_S = "#F1D6CF"
MEM = "#4F7A3A"; MEM_S = "#DCE8D2"

DEFS = """<defs>
<marker id="a-ink" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="%s"/></marker>
<marker id="a-model" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="%s"/></marker>
<marker id="a-ctrl" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="%s"/></marker>
<marker id="a-harm" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="%s"/></marker>
<marker id="a-mem" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="%s"/></marker>
<marker id="a-mut" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="%s"/></marker>
<linearGradient id="fade-model" x1="0" x2="1"><stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s" stop-opacity="0"/></linearGradient>
<linearGradient id="fade-rule" x1="0" x2="1"><stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s" stop-opacity="0"/></linearGradient>
<linearGradient id="fade-ctrl" x1="0" x2="1"><stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s" stop-opacity="0"/></linearGradient>
<pattern id="brick" width="26" height="14" patternUnits="userSpaceOnUse"><rect width="26" height="14" fill="%s"/><path d="M0 7H26M13 0V7M0 7V14M26 7V14" stroke="%s" stroke-width="1.2" fill="none"/></pattern>
</defs>""" % (INK, MODEL, CTRL, HARM, MEM, MUTED, MODEL_S, MODEL_S, RULE, RULE, CTRL_S, CTRL_S, CTRL_S, CTRL)

def svg(w, h, label, body):
    return f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{label}">\n{DEFS}\n{body}\n</svg>'

def T(x, y, s, cls="", anchor=None, fill=None, size=None, extra=""):
    a = []
    if cls: a.append(f'class="{cls}"')
    if anchor: a.append(f'text-anchor="{anchor}"')
    st = []
    if fill: st.append(f"fill:{fill}")
    if size: st.append(f"font-size:{size}px")
    if st: a.append('style="' + ";".join(st) + '"')
    if extra: a.append(extra)
    return f'<text x="{x}" y="{y}" {" ".join(a)}>{s}</text>'

def lines(x, y, items, dy=15, **kw):
    return "\n".join(T(x, y + i * dy, s, **kw) for i, s in enumerate(items))

def rect(x, y, w, h, fill=SURF, stroke=INK, sw=1.4, rx=0, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'

def path(d, stroke=INK, sw=1.4, marker=None, dash=None, fill="none", extra=""):
    m = f' marker-end="url(#{marker})"' if marker else ""
    dsh = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" stroke="{stroke}" stroke-width="{sw}" fill="{fill}"{m}{dsh} {extra}/>'

def circ(cx, cy, r, fill=INK, stroke="none", sw=1.4, extra=""):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'

def curve(x1, y1, x2, y2, **kw):
    mx = (x1 + x2) / 2
    return path(f"M{x1} {y1} C{mx} {y1} {mx} {y2} {x2} {y2}", **kw)

# ---------------------------------------------------------------- F1 grid
def f1():
    gx, gy, cw, ch = 200, 60, 220, 150
    b = []
    b.append(T(gx - 24, gy + ch, "Could AI end humanity?", "t-l", "end"))
    b.append(T(gx - 24, gy + ch + 20, "yes, above · no, below", "t-s mut", "end"))
    b.append(T(gx + cw, gy + 2 * ch + 40, "Should frontier models be open?", "t-l", "middle"))
    b.append(T(gx + cw, gy + 2 * ch + 58, "no, left · yes, right", "t-s mut", "middle"))
    cells = [
        (0, 0, "Lock it down.", ["Only a few labs should", "ever hold the weights."]),
        (1, 0, "Openness is the defence.", ["Concentrated power is", "the bigger danger."]),
        (0, 1, "Business as usual.", ["Let the market decide", "who controls access."]),
        (1, 1, "Nothing to fear.", ["Release everything."]),
    ]
    for cx_, cy_, head, sub in cells:
        x, y = gx + cx_ * cw, gy + cy_ * ch
        b.append(rect(x, y, cw, ch, GROUND, RULE, 1.2))
        b.append(T(x + 18, y + 40, head, "t-xl"))
        b.append(lines(x + 18, y + 64, sub, cls="t-s mut"))
    b.append(rect(gx, gy, 2 * cw, 2 * ch, "none", INK, 1.6))
    # third axis emerging from the centre
    cx, cy = gx + 2 * cw, gy + 2 * ch
    b.append(circ(cx, cy, 7, CTRL))
    b.append(path(f"M{cx} {cy} L{cx + 210} {cy + 120}", CTRL, 5, "a-ctrl", extra='stroke-linecap="round"'))
    b.append(T(cx + 92, cy + 44, "the axis this essay is about", "t-h", fill=CTRL, extra=f'transform="rotate(29.7 {cx+92} {cy+44})"'))
    b.append(lines(cx + 20, cy + 156, ["What is the system allowed to do,", "and who can stop it?"], cls="t-l", fill=CTRL, dy=20))
    return svg(900, 560, "A two-by-two grid. The vertical axis asks whether AI could end humanity. The horizontal asks whether frontier models should be open. Each cell holds the slogan that position produces. A third orange axis emerges from the centre of the grid, labelled: what is the system allowed to do, and who can stop it. That is the axis this essay is about.", "\n".join(b))

# ---------------------------------------------------------------- F2 thousand dots
def f2():
    b = []
    cols, rows, sp, r = 40, 25, 15.4, 5.6
    ox, oy = 40, 46
    for i in range(rows * cols):
        cx = ox + (i % cols) * sp + sp / 2
        cy = oy + (i // cols) * sp + sp / 2
        b.append(circ(cx, cy, r, RULE_SOFT, RULE, 0.8))
    for i in (0, 1):
        cx = ox + i * sp + sp / 2; cy = oy + sp / 2
        b.append(circ(cx, cy, r + 1.5, HARM))
    W = cols * sp
    b.append(T(ox, 30, "1,000 dots. Everyone alive in 2020.", "t-l"))
    lx = ox + W + 36
    b.append(circ(lx + 8, 70, 7, HARM))
    b.append(lines(lx + 24, 74, ["Two dots.", "COVID-19 excess deaths,", "2020 to 2021.", "14.9 million (WHO),", "about 0.2% of humanity."], cls="t-s", dy=15))
    b.append(lines(lx, 170, ["That was a global", "catastrophe. Two dots."], cls="t-h", dy=17))
    b.append(lines(lx, 236, ["Extinction is all", "1,000 dots."], cls="t-h", dy=17))
    b.append(lines(lx, 300, ["The 998 dots in", "between are the", "conversation we", "are not having."], cls="t-h", fill=HARM, dy=17))
    # bracket under grid
    y0 = oy + rows * sp + 14
    b.append(path(f"M{ox + 2*sp} {y0} L{ox + 2*sp} {y0+10} L{ox + W} {y0+10} L{ox + W} {y0}", HARM, 1.6))
    b.append(T(ox + (2 * sp + W) / 2, y0 + 30, "catastrophic, and far short of extinction", "t-s", "middle", fill=HARM))
    return svg(900, 470, "A grid of one thousand small dots representing everyone alive in 2020. Two dots are red, representing the 14.9 million excess deaths associated with COVID-19 in 2020 and 2021, about 0.2 percent of humanity. Extinction would be all one thousand dots. A bracket marks the 998 dots in between as the conversation we are not having.", "\n".join(b))

# ---------------------------------------------------------------- F3 dials
def dial(cx, cy, ang, col, r=13, needle_col=None):
    needle_col = needle_col or col
    a = math.radians(ang)
    x2, y2 = cx + (r - 3) * math.cos(a), cy + (r - 3) * math.sin(a)
    return (circ(cx, cy, r, SURF, col, 1.4) + path(f"M{cx} {cy} L{x2:.1f} {y2:.1f}", needle_col, 2, extra='stroke-linecap="round"') + circ(cx, cy, 2, col))

def f3():
    rnd = random.Random(7)
    b = []
    cols, rows, sp = 6, 4, 38
    panels = [(40, "Before training", "Dials at random. Knows nothing."),
              (330, "After pre-training", "Every dial set. Trillions of nudges."),
              (620, "After post-training", "A few dials nudged again, slightly.")]
    start = [rnd.uniform(0, 360) for _ in range(cols * rows)]
    learned = [rnd.uniform(0, 360) for _ in range(cols * rows)]
    tweak = {3, 8, 14, 17, 21}
    for pi, (px, title, sub) in enumerate(panels):
        b.append(T(px, 34, title, "t-l"))
        b.append(T(px, 52, sub, "t-s mut"))
        b.append(rect(px, 66, cols * sp + 10, rows * sp + 10, GROUND, RULE, 1, rx=6))
        for i in range(cols * rows):
            cx = px + 5 + (i % cols) * sp + sp / 2
            cy = 66 + 5 + (i // cols) * sp + sp / 2
            if pi == 0:
                b.append(dial(cx, cy, start[i], RULE, needle_col=MUTED))
            elif pi == 1:
                b.append(dial(cx, cy, learned[i], MODEL))
            else:
                if i in tweak:
                    a0, a1 = learned[i], learned[i] + 40
                    ra = 16
                    x0, y0 = cx + ra * math.cos(math.radians(a0)), cy + ra * math.sin(math.radians(a0))
                    x1, y1 = cx + ra * math.cos(math.radians(a1)), cy + ra * math.sin(math.radians(a1))
                    b.append(path(f"M{x0:.1f} {y0:.1f} A{ra} {ra} 0 0 1 {x1:.1f} {y1:.1f}", CTRL, 2.4, "a-ctrl"))
                    b.append(dial(cx, cy, a1, MODEL, needle_col=CTRL))
                else:
                    b.append(dial(cx, cy, learned[i], MODEL))
    # loops between panels
    def loop(x, y, col, l1, l2, l3):
        b.append(path(f"M{x} {y} A18 18 0 1 1 {x} {y+0.1}", col, 2.2, extra="opacity='.9'"))
        b.append(circ(x + 18, y, 3, col))
        b.append(lines(x + 30, y - 4, [l1, l2], cls="t-s", fill=col, dy=14))
    loop(70, 268, MODEL, "predict the next word · compare · nudge", "trillions of times", "")
    loop(440, 268, CTRL, "try a task · score it · nudge", "far fewer times", "")
    b.append(path("M296 148 L322 148", MODEL, 2, "a-model"))
    b.append(path("M586 148 L612 148", CTRL, 2, "a-ctrl"))
    b.append(lines(40, 312, ["24 dials shown. A real model has hundreds of billions. Nobody sets one by hand, and nobody can read a fact or a rule off one.", "Using the model afterward turns none of them."], cls="t-s mut", dy=14))
    return svg(900, 336, "Three panels of the same 24 dials. Before training the needles point at random. After pre-training every needle has been set by trillions of small nudges. After post-training the same needles stand, with five of them nudged a little further, marked in orange. Loops between the panels read: predict the next word, compare, nudge, trillions of times; and try a task, score it, nudge, far fewer times.", "\n".join(b))

# ---------------------------------------------------------------- F4 probability flow
def f4():
    b = []
    top, k = 70, 2.5
    L = [("Helpful answer", 25, MODEL), ("Keeps writing an \"article\"", 25, RULE), ("Role-plays a dialogue", 20, RULE), ("Other", 15, RULE), ("Confident fabrication", 15, HARM)]
    R = [("Helpful answer", 85, MODEL), ("Asks a clarifying question", 8, RULE), ("Declines safely", 5, RULE), ("Confident fabrication", 0.8, HARM), ("Other", 1.2, RULE)]
    x0, w0, x1, w1 = 260, 70, 540, 70
    side_i = [0]
    def stack(x, w, segs, side):
        y = top; out = []
        for name, v, col in segs:
            h = max(v * k, 3)
            out.append(rect(x, y, w, h, col, SURF, 1.2))
            if side == "L":
                out.append(T(x - 12, y + h / 2 + 4, f"{name}  {v:g}%", "t-s", "end", fill=(HARM if col == HARM else INK)))
            else:
                lab = f"{v:g}%  {name}" if v >= 1 else "fabrication: still above zero"
                if v >= 50:
                    out.append(T(x + w + 12, y + h / 2 + 4, lab, "t-s", fill=INK))
                else:
                    ly = 236 + side_i[0] * 18; side_i[0] += 1
                    out.append(path(f"M{x+w} {y+h/2:.1f} L{x+w+14} {ly-4}", RULE, 1))
                    out.append(T(x + w + 18, ly, lab, "t-s", fill=(HARM if col == HARM else INK)))
            y += h
        return out, y
    sl, yl = stack(x0, w0, L, "L"); sr, yr = stack(x1, w1, R, "R")
    # flows: first four left segments -> right helpful; fabrication -> the rest
    yL = top; yR = top
    for name, v, col in L[:4]:
        h = v * k
        b.append(path(f"M{x0+w0} {yL} C{(x0+w0+x1)/2} {yL} {(x0+w0+x1)/2} {yR} {x1} {yR} L{x1} {yR+h} C{(x0+w0+x1)/2} {yR+h} {(x0+w0+x1)/2} {yL+h} {x0+w0} {yL+h} Z", "none", 0, fill=MODEL, extra='opacity=".18"'))
        yL += h; yR += h
    fabL0, fabL1 = yL, yL + 15 * k
    fabR0, fabR1 = yR, yr
    b.append(path(f"M{x0+w0} {fabL0} C{(x0+w0+x1)/2} {fabL0} {(x0+w0+x1)/2} {fabR0} {x1} {fabR0} L{x1} {fabR1} C{(x0+w0+x1)/2} {fabR1} {(x0+w0+x1)/2} {fabL1} {x0+w0} {fabL1} Z", "none", 0, fill=HARM, extra='opacity=".22"'))
    b += sl + sr
    b.append(T(x0 + w0 / 2, 40, "Before post-training", "t-l", "middle"))
    b.append(T(x1 + w1 / 2, 40, "After post-training", "t-l", "middle"))
    b.append(T((x0 + w0 + x1) / 2, 40, "same dials, nudged", "t-s mut", "middle"))
    b.append(path(f"M{(x0+w0+x1)/2 - 40} 52 L{(x0+w0+x1)/2 + 40} 52", MUTED, 1.4, "a-mut"))
    b.append(T(40, 350, "Asked something ambiguous, what does the model do? Illustrative numbers; the real distributions are not published.", "t-s mut"))
    b.append(T(40, 366, "The shape is the point. Probability moves. Nothing is switched off.", "t-s mut"))
    return svg(900, 380, "Two stacked bars connected by flows. Before post-training the probability of a helpful answer is 25 percent, with the rest spread across continuing as an article, role-playing, other, and 15 percent confident fabrication. After post-training, 85 percent flows into a helpful answer; the fabrication mass flows mostly into clarifying questions and safe refusals, but a sliver of fabrication remains, labelled still above zero.", "\n".join(b))

# ---------------------------------------------------------------- F5 / F14 concentric anatomy
def ring_item(cx, cy, r, deg, label, col=INK, glyph=None):
    a = math.radians(deg)
    x, y = cx + r * math.cos(a), cy + r * math.sin(a)
    out = []
    if glyph:
        out.append(glyph(x, y - 14, col))
    out.append(T(f"{x:.1f}", f"{y+6:.1f}", label, "t-s", "middle", fill=col))
    return "\n".join(out)

def g_search(x, y, c): return circ(x - 2, y - 2, 6, "none", c, 1.8) + path(f"M{x+2.5} {y+2.5} L{x+8} {y+8}", c, 2.2)
def g_file(x, y, c): return path(f"M{x-6} {y-8} h9 l4 4 v13 h-13 z", c, 1.6, fill=SURF) + path(f"M{x-3} {y} h7 M{x-3} {y+4} h7", c, 1.2)
def g_code(x, y, c): return rect(x - 9, y - 7, 18, 14, SURF, c, 1.6, rx=2) + T(f"{x:.1f}", f"{y+4:.1f}", "&gt;_", "t-s", "middle", fill=c, size=9)
def g_mail(x, y, c): return rect(x - 9, y - 6, 18, 13, SURF, c, 1.6, rx=1) + path(f"M{x-9} {y-6} L{x} {y+1} L{x+9} {y-6}", c, 1.4)
def g_money(x, y, c): return circ(x, y, 8, SURF, c, 1.6) + T(f"{x:.1f}", f"{y+4:.1f}", "$", "t-s", "middle", fill=c, size=11)
def g_agents(x, y, c): return circ(x - 5, y, 5, SURF, c, 1.6) + circ(x + 5, y, 5, SURF, c, 1.6)
def g_globe(x, y, c): return circ(x, y, 8, SURF, c, 1.6) + path(f"M{x-8} {y} h16 M{x} {y-8} v16 M{x-5.5} {y-5.5} q5.5 5.5 0 11 M{x+5.5} {y-5.5} q-5.5 5.5 0 11", c, 1)
def g_person(x, y, c): return circ(x, y - 4, 4, SURF, c, 1.6) + path(f"M{x-7} {y+9} q7 -10 14 0", c, 1.6, fill=SURF)
def g_building(x, y, c): return rect(x - 8, y - 8, 16, 17, SURF, c, 1.6) + path(f"M{x-4} {y-3} h3 M{x+1} {y-3} h3 M{x-4} {y+2} h3 M{x+1} {y+2} h3", c, 1.2)

def anatomy(cx, cy, radii, pins=None, labels=True):
    r0, r1, r2, r3 = radii
    b = []
    b.append(circ(cx, cy, r3, GROUND, RULE, 1.2))
    b.append(circ(cx, cy, r2, CTRL_S, CTRL, 1.6))
    b.append(circ(cx, cy, r1, SURF, INK, 1.4))
    b.append(circ(cx, cy, r0, MODEL_S, MODEL, 2))
    b.append(T(cx, cy - 4, "THE MODEL", "t-l", "middle", fill=MODEL))
    b.append(T(cx, cy + 14, "frozen dials", "t-s", "middle", fill=MODEL))
    b.append(T(cx, cy + 28, "produces only text", "t-s", "middle", fill=MODEL))
    b.append(T(cx, cy - r1 + 24, "THE APPLICATION", "t-h", "middle"))
    b.append(T(cx, cy - r2 + 24, "TOOLS AND PERMISSIONS", "t-h", "middle", fill=CTRL))
    b.append(T(cx, cy - r3 + 22, "THE WORLD", "t-h", "middle", fill=MUTED))
    if labels:
        b.append(T(cx, cy + r0 + 26, "role and rules", "t-s", "middle"))
        b.append(T(cx, cy + r0 + 42, "the conversation so far", "t-s", "middle"))
        b.append(T(cx, cy + r0 + 58, "saved memory", "t-s", "middle", fill=MEM))
        rr = (r1 + r2) / 2 + 10
        items = ((32, "search", g_search), (55, "files", g_file), (78, "code", g_code), (102, "email", g_mail), (125, "money", g_money), (148, "agents", g_agents))
        for deg, lab, g in items:
            b.append(ring_item(cx, cy, rr, deg, lab, CTRL, g))
        rr = (r2 + r3) / 2 + 8
        for deg, lab, g in ((40, "the internet", g_globe), (75, "your systems", g_building), (105, "people", g_person), (140, "other agents", g_agents)):
            b.append(ring_item(cx, cy, rr, deg, lab, MUTED, g))
    if pins:
        for n, (px, py) in pins:
            b.append(circ(px, py, 14, CTRL, SURF, 2))
            b.append(T(px, py + 5, str(n), "t-h", "middle", fill=SURF))
    return "\n".join(b)

def f5():
    cx, cy = 320, 352
    r = (66, 150, 232, 280)
    b = [anatomy(cx, cy, r)]
    # brackets on the right
    bx = 612
    b.append(path(f"M{bx} {cy-150} h10 v300 h-10", INK, 1.4))
    b.append(T(bx + 22, cy - 8, "\"a chatbot\"", "t-l"))
    b.append(lines(bx + 22, cy + 10, ["the model plus", "the application"], cls="t-s mut", dy=14))
    bx2 = 742
    b.append(path(f"M{bx2} {cy-232} h10 v464 h-10", CTRL, 1.8))
    b.append(T(bx2 + 22, cy - 8, "\"an agent\"", "t-l", fill=CTRL))
    b.append(lines(bx2 + 22, cy + 10, ["the chatbot plus", "tools, run in", "a loop"], cls="t-s", fill=CTRL, dy=14))
    b.append(path(f"M{cx} {cy-r[3]-2} V{cy-r[3]-40}", MUTED, 1.2, dash="3 4"))
    b.append(T(cx, cy - r[3] - 46, "words", "t-s mut", "middle"))
    b.append(path(f"M{cx} {cy+r[3]+2} V{cy+r[3]+40}", MUTED, 1.2, "a-mut", dash="3 4"))
    b.append(T(cx, cy + r[3] + 56, "actions", "t-s mut", "middle"))
    return svg(900, 700, "Four concentric rings. At the centre, the model: frozen dials that produce only text. Around it, the application: role and rules, the conversation, saved memory. Around that, tools and permissions with icons for search, files, code, email, money, and other agents. The outer ring is the world: the internet, your systems, people, other agents. Brackets on the right mark the model plus application as a chatbot, and the chatbot plus tools run in a loop as an agent. A dashed arrow runs from words at the top to actions at the bottom.", "\n".join(b))

# ---------------------------------------------------------------- F6 context window
def f6():
    b = []
    tiles = [("Your message", "\"Prepare a briefing on this company.\"", INK, SURF, "M"),
             ("The app's instructions", "role, rules, which tools exist", INK, SURF, "!"),
             ("Saved memory", "\"prefers a one-page brief\" (from May)", MEM, MEM_S, "m"),
             ("Documents and search", "the attached report, a news hit", INK, SURF, "D")]
    ys = [50, 120, 190, 260]
    vx, vy, vw, vh = 400, 40, 180, 330
    # vessel
    b.append(path(f"M{vx} {vy} V{vy+vh-16} q0 16 16 16 h{vw-32} q16 0 16 -16 V{vy}", INK, 1.8, fill=SURF))
    b.append(T(vx + vw / 2, vy - 14, "CONTEXT WINDOW", "t-h", "middle"))
    for frac, lab in ((0, "0"), (0.5, "half"), (1, "full")):
        yy = vy + vh - frac * vh
        b.append(path(f"M{vx-8} {yy:.1f} h8", INK, 1.2))
        b.append(T(vx - 12, yy + 4, lab, "t-s mut", "end"))
    layers = [("instructions", 44, RULE, INK), ("conversation so far", 92, RULE_SOFT, INK), ("memory note", 30, MEM_S, MEM), ("report excerpts", 78, RULE_SOFT, INK), ("news hit", 30, RULE, INK)]
    y = vy + vh
    for name, h, col, tc in layers:
        y -= h
        b.append(rect(vx + 2, y, vw - 4, h - 2, col, "none", 0))
        b.append(T(vx + vw / 2, y + h / 2 + 4, name, "t-s", "middle", fill=tc))
    b.append(T(vx + vw / 2, y - 14, "room left: a little", "t-s mut", "middle"))
    for (t, s, tc, fill, gl), ty in zip(tiles, ys):
        b.append(rect(40, ty, 250, 54, fill, tc, 1.4, rx=4))
        b.append(rect(50, ty + 12, 30, 30, SURF, tc, 1.4, rx=3))
        b.append(T(65, ty + 32, gl, "t-h", "middle", fill=tc))
        b.append(T(90, ty + 22, t, "t-h", fill=tc))
        b.append(T(90, ty + 40, s, "t-s mut"))
        col = MEM if tc == MEM else INK
        b.append(curve(292, ty + 27, vx - 2, 200 + (ty - 50) * 0.25, stroke=col, sw=1.4, marker=("a-mem" if col == MEM else "a-ink")))
    # dropped tile
    b.append(path(f"M{vx+vw/2} {vy+vh+2} v26", MUTED, 1.4, "a-mut", dash="3 3"))
    b.append(rect(vx - 20, vy + vh + 34, vw + 40, 34, "none", MUTED, 1.2, rx=4, extra='stroke-dasharray="4 3"'))
    b.append(T(vx + vw / 2, vy + vh + 49, "an earlier exchange, summarized or dropped", "t-s mut", "middle"))
    b.append(T(vx + vw / 2, vy + vh + 62, "when the window is full", "t-s mut", "middle"))
    # model and output
    b.append(path(f"M{vx+vw+4} 200 h40", INK, 1.6, "a-ink"))
    b.append(rect(630, 160, 110, 80, MODEL_S, MODEL, 2, rx=6))
    b.append(T(685, 196, "MODEL", "t-l", "middle", fill=MODEL))
    b.append(T(685, 216, "reads the packet", "t-s", "middle", fill=MODEL))
    b.append(path("M744 200 h40", INK, 1.6, "a-ink"))
    b.append(rect(790, 150, 100, 100, SURF, INK, 1.4, rx=4))
    b.append(T(840, 180, "OUTPUT", "t-h", "middle"))
    b.append(lines(840, 202, ["an answer, or", "a request to", "use a tool"], cls="t-s mut", anchor="middle"))
    b.append(lines(40, 346, ["Memory lives outside the model, in the app's", "storage. It changes an answer only when the app", "retrieves it and puts it in the packet. Stored", "somewhere is different from in front of the", "model right now."], cls="t-s", fill=MEM, dy=15))
    return svg(900, 460, "Four tiles on the left, your message, the app's instructions, saved memory, and documents and search, feed into a vessel labelled context window that is nearly full, with layers stacked inside and a scale from empty to full. A dashed tile below the vessel shows an earlier exchange that was summarized or dropped when the window filled. The model reads the packet and produces an output: an answer or a request to use a tool.", "\n".join(b))

# ---------------------------------------------------------------- F7 the wall
def f7():
    b = []
    b.append(T(40, 34, "Your task: \"Prepare a briefing on this company for my 3pm.\"", "t-s mut"))
    b.append(rect(40, 90, 250, 120, MODEL_S, MODEL, 2, rx=6))
    b.append(T(56, 116, "1 · THE MODEL PROPOSES", "t-h", fill=MODEL))
    b.append(lines(56, 140, ["\"Search for the company's", "latest annual report.\""], cls="t-h"))
    b.append(T(56, 194, "It can only write the request.", "t-s mut"))
    b.append(path("M292 150 h108", INK, 2, "a-ink"))
    # wall
    wx, wy, ww, wh = 410, 50, 44, 190
    b.append(rect(wx, wy, ww, wh, "url(#brick)", CTRL, 1.6))
    gy = 128
    b.append(rect(wx - 2, gy, ww + 4, 44, SURF, CTRL, 2.2))
    b.append(path(f"M{wx+6} {gy+22} h{ww-12}", CTRL, 1.6, "a-ctrl", dash="3 3"))
    b.append(T(wx + ww / 2, wy + wh + 24, "2 · PERMISSION BOUNDARY", "t-h", "middle", fill=CTRL))
    b.append(lines(wx + ww / 2, wy + wh + 42, ["The application checks:", "this tool? this action? this budget?", "A wall in software, outside the model."], cls="t-s mut", anchor="middle", dy=14))
    # tools
    b.append(path(f"M{wx+ww+4} 150 h60", INK, 2, "a-ink"))
    tx = 530
    b.append(rect(tx, 60, 240, 180, SURF, INK, 1.4, rx=6))
    b.append(T(tx + 16, 86, "3 · A TOOL RUNS", "t-h"))
    tools = [("search", g_search), ("files", g_file), ("code", g_code), ("email", g_mail), ("money", g_money)]
    for i, (lab, g) in enumerate(tools):
        x = tx + 32 + i * 46
        b.append(g(x, 116, INK))
        b.append(T(x, 142, lab, "t-s", "middle"))
    b.append(lines(tx + 16, 174, ["Only what the gate allowed.", "The result comes back as text."], cls="t-s mut"))
    b.append(T(tx + 16, 222, "4 · Result enters context; go again", "t-s"))
    # loop back
    b.append(path(f"M{tx+240} 150 h30 q20 0 20 20 V330 q0 20 -20 20 H185 q-20 0 -20 -20 V214", INK, 2.2, "a-ink"))
    b.append(T(300, 344, "repeat until the task ends or a limit is hit", "t-s mut", "middle"))
    b.append(rect(600, 366, 290, 60, CTRL_S, CTRL, 1.6, rx=4))
    b.append(lines(616, 390, ["Drafting an email and sending one", "are two different permissions."], cls="t-h", fill=CTRL, dy=18))
    return svg(900, 440, "The model on the left proposes a step: search for the company's latest annual report. The request runs into a brick wall with a gate labelled permission boundary, where the application checks the tool, the action, and the budget. Beyond the wall, a tool runs: icons for search, files, code, email, money. The result loops back into the model's context and the cycle repeats. A callout says drafting an email and sending one are two different permissions.", "\n".join(b))

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
    b.append(lines(rx, 250, ["same model", "same task", "same dials"], cls="t-s", anchor="middle", dy=13))
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
    rows = [("The dials", "the model's weights", 82), ("Context", "the packet", 150), ("Memory", "saved records", 218), ("Harness and tools", "the software around it", 286)]
    for name, sub, y in rows:
        b.append(T(40, y, name, "t-h", fill=(MEM if name == "Memory" else CTRL if name.startswith("Harness") else MODEL if name == "The dials" else INK)))
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
    b.append(rect(x, 90, 100, 40, SURF, INK, 1.4, rx=4)); b.append(lines(x + 50, 108, ["\"maximize", "collections\""], cls="t-s", anchor="middle", dy=13))
    b.append(path(f"M{x+102} 110 h30", INK, 1.6, "a-ink"))
    b.append(rect(x + 140, 90, 80, 40, MODEL_S, MODEL, 1.6, rx=4)); b.append(T(x + 180, 114, "model", "t-s", "middle", fill=MODEL))
    b.append(path(f"M{x+222} 110 C{x+240} 110 {x+240} 78 {x+258} 78", RULE, 1.6, "a-mut"))
    b.append(T(x + 245, 66, "polite reminders", "t-s mut", "middle"))
    b.append(path(f"M{x+222} 110 C{x+240} 110 {x+240} 142 {x+258} 142", HARM, 2.2, "a-harm"))
    b.append(T(x + 245, 160, "pressures the vulnerable", "t-s", "middle", fill=HARM))
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
    b.append(rect(76, 106, 120, 34, SURF, MODEL, 1.4, rx=3)); b.append(T(136, 128, "the weights stay here", "t-s", "middle", fill=MODEL))
    b.append(lines(214, 118, ["monitoring · limits ·", "safety updates for everyone"], cls="t-s mut", dy=14))
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
    b.append(rect(496, 194, 120, 26, SURF, MODEL, 1.4, rx=3)); b.append(T(556, 212, "the weights, yours", "t-s", "middle", fill=MODEL))
    b.append(lines(496, 240, ["run privately · adapt · remove refusal training"], cls="t-s mut"))
    # copies fan
    rnd = random.Random(3)
    pts = [(730, 120), (790, 150), (840, 200), (860, 260), (830, 320), (770, 350), (710, 330), (860, 130)]
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
    b.append(T(450, 482, "Most \"open\" frontier models sit in the middle. An open-weight model can also be offered as a hosted service; the difference is the option to run your own.", "t-s mut", "middle"))
    return svg(900, 496, "Left: using a service. Your application connects to the provider's computers, where the weights stay, through a breaker switch labelled an account can be cut off. Right: running your own copy. Published model files are downloaded to your computers, and from there eight small copies fan outward; the breaker is drawn switched off and crossed out, labelled no breaker, copies cannot be recalled. Below, a spectrum from closed to open-weight to open-source.", "\n".join(b))

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

FIGS = [f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12, f13, f14]

def main():
    s = open("index.html").read()
    parts = re.split(r'(<div class="art">\s*<svg.*?</svg>\s*</div>)', s, flags=re.S)
    blocks = [i for i, p in enumerate(parts) if p.startswith('<div class="art">')]
    assert len(blocks) == 14, len(blocks)
    for idx, fn in zip(blocks, FIGS):
        parts[idx] = '<div class="art">\n' + fn() + '\n  </div>'
    open("index.html", "w").write("".join(parts))
    print("rebuilt", len(blocks), "figures")

if __name__ == "__main__":
    main()
