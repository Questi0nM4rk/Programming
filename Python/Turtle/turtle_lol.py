import turtle as t
from datetime import datetime

# Napište proceduru ‹clock›, která pomocí želví grafiky vykreslí ciferník
# hodin s ručičkami v následující podobě:
#
# • ciferník má tvar dvanáctiúhelníku postaveného „na špičku“ s délkou
#   strany rovnou ‹side›, vrcholy dvanáctiúhelníku tedy odpovídají číslicím;
# • ručičky ukazují čas zadaný ve formátu UNIX Epoch Time, tj. jako
#   počet sekund od 1. 1. 1970, 0.00:00, v parametru ‹epoch_time›;
# • sekundová ručička je znázorněna čarou o délce 1,8násobku ‹side›;
# • minutová ručička je znázorněna prázdným obdélníkem o délce
#   1,6násobku ‹side› a šířce dvacetiny ‹side›;
# • hodinová ručička je znázorněna prázdným obdélníkem o délce
#   1,4násobku ‹side› a šířce desetiny ‹side›;
# • pro ručičky ve tvaru obdélníku platí, že vzdálenost mezi středem ciferníku
#   a kratší stranou obdélníku je polovina jeho šířky.
#
# Parametr ‹epoch_time› je vždy celé číslo, parametr ‹side› je kladné „reálné“
# číslo (typu ‹float›).
#
# Minutová a hodinová ručička se neposunují skokově, ale (v rámci možností)
# spojitě, tj. například v čase 13.30:00 je hodinová ručička přesně
# v polovině úhlu mezi jedničkou a dvojkou.
#
# Testovací prostředí želví grafiky podporuje pouze procedury ‹forward›,
# ‹backward›, ‹right›, ‹left›, ‹penup›, ‹pendown›, ‹setheading›.
# Použití procedur ‹speed›, ‹delay› a ‹done› se sice nepovažuje za chybu,
# ale budou v testech ignorovány, tj. «nebudou mít žádný efekt».


"""
move it to the ib111
how to make the clock arms so they are moved from the center

"""

def _draw_clock(side):
    angle = 360//12
    t.penup()
    t.left(90)
    t.forward(side*2)
    t.right(105)
    t.pendown()
    for _ in range(12):
        t.forward(side)
        t.right(angle)


def _draw_clock_arm(angle, side, version):
    t.penup()
    t.goto(0, 0)
    if version is 0:    # seconds
        sec_len = 1.8*side
        t.setheading(90 - angle)
        t.pendown()
        t.forward(sec_len)
    elif version is 1:  # minites
        min_len = side*1.6
        min_width = side/20
        t.setheading(90-angle)
        t.pendown()
        t.right(90)
        t.forward(min_width/2.0)
        t.left(90)
        t.forward(min_len)
        t.left(90)
        t.forward(min_width)
        t.left(90)
        t.forward(min_len)
        t.left(90)
        t.forward(min_width/2.0)
    elif version is 2:  # hours
        hs_len = side*1.4
        hs_width = side/10
        t.setheading(90-angle)
        t.pendown()
        t.right(90)
        t.forward(hs_width/2.0)
        t.left(90)
        t.forward(hs_len)
        t.left(90)
        t.forward(hs_width)
        t.left(90)
        t.forward(hs_len)
        t.left(90)
        t.forward(hs_width/2.0)


def _calculate_clock_angles():
    now = datetime.now()
    hour = now.hour
    minute = now.minute
    second = now.second

    hour_angle = (hour % 12) * 30 + (minute / 2) + (second / 120)
    minute_angle = (minute % 60) * 6 + (second / 10)
    second_angle = (second % 60) * 6

    return hour_angle, minute_angle, second_angle


def clock(epoch_time, side):
    _draw_clock(side)

    t.penup()
    t.right(90)
    t.forward(2*side)
    t.left(90)
    t.pendown()

    hour_angle, minute_angle, second_angle = _calculate_clock_angles()

    _draw_clock_arm(hour_angle, side, 2)
    _draw_clock_arm(minute_angle, side, 1)
    _draw_clock_arm(second_angle, side, 0)

    t.done()


def main():
    clock(1661081862, 150.0)
    t.done()


if __name__ == '__main__':
    main()
