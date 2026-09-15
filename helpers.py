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

