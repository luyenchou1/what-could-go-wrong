from helpers import *
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

