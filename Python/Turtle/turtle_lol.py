from turtle import penup, pendown, forward, setheading, right, left, done
from math import sin, pi

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

def _draw_clock(side):
    angle = 360//12
    penup()
    left(90)
    forward(side*2)
    right(105)
    pendown()
    for _ in range(12):
        forward(side)
        right(angle)


def _draw_clock_arm(angle, side, version):
    penup()
    if version is 0:    # seconds
        sec_len = 1.8*side
        setheading(90 - angle)
        pendown()
        forward(sec_len)
    elif version is 1:  # minites
        min_len = side*1.6
        min_width = side/20
        setheading(90-angle)
        right(180)
        forward(min_width/2.0)
        pendown()
        left(90)
        forward(min_width/2.0)
        left(90)
        forward(min_len)
        left(90)
        forward(min_width)
        left(90)
        forward(min_len)
        left(90)
        forward(min_width/2.0)
        penup()
        left(90)
        forward(min_width/2.0)
        pendown()
    elif version is 2:  # hours
        hs_len = side*1.4
        hs_width = side/10
        setheading(90-angle)
        right(180)
        forward(hs_width/2.0)
        pendown()
        left(90)
        forward(hs_width/2.0)
        left(90)
        forward(hs_len)
        left(90)
        forward(hs_width)
        left(90)
        forward(hs_len)
        left(90)
        forward(hs_width/2.0)
        penup()
        left(90)
        forward(hs_width/2.0)
        pendown()
        


def _calculate_clock_angles(epoch_time):
    hour_angle = (epoch_time % 43200) * (360 / 43200.0)
    minute_angle = (epoch_time % 3600) * (360 / 3600.0)
    second_angle = (epoch_time % 60) * (360 / 60.0)

    return hour_angle, minute_angle, second_angle


def clock(epoch_time, side):
    _draw_clock(side)
    rad = side / (2 * (sin(pi / 12)))
    penup()
    right(75)
    forward(rad)
    left(90)
    pendown()

    hour_angle, minute_angle, second_angle = _calculate_clock_angles(epoch_time)

    print(hour_angle, minute_angle, second_angle)
    
    _draw_clock_arm(hour_angle, side, 2)
    _draw_clock_arm(minute_angle, side, 1)
    _draw_clock_arm(second_angle, side, 0)

    done()


def main():
    clock(1661081862, 150.0)
    done()


if __name__ == '__main__':
    main()
