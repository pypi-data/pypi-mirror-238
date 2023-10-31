try:
    from PIL import Image, ImageDraw, ImageFont
except:
    Image = None

import random

from packer2d.packer import *
from packer2d.qtree import *


def getImg(qt):
    x1, y1, x2, y2 = qt.region
    w = x2 - x1
    h = y2 - y1

    return Image.new("RGB", (w * 2, h * 2), (255, 255, 255))


def drawRects(qt, img, rects, color_=(255, 255, 255), shift=1, fill=False):
    xz, yz, _x2, _y2 = qt.region
    drw = ImageDraw.Draw(img)

    if not callable(color_):
        color = lambda i: color_
    else:
        color = color_

    for i, r in enumerate(rects):
        area = (
            (r.x1 - xz) * 2 + shift,
            (r.y1 - yz) * 2 + shift,
            (r.x2 - xz) * 2 - shift,
            (r.y2 - yz) * 2 - shift,
        )
        c = color(i)
        assert (isinstance(c, tuple))

        drw.rectangle(area, outline=color(i), fill=fill(i) if fill else None)


def drawQuadtree(qt, img):
    colors = []
    for i in range(qt.max_depth):
        g = 170 - int(127 * (i / (qt.max_depth - 1)))
        colors.append((g, g, g))

    drawRects(qt, img, (nl[0].region for nl in qt.nodes()), (255, 255, 255, 2), shift=0)
    drawRects(qt, img, map(lambda iref: iref.item.rect, qt.items()), (127, 0, 127))


def drawNumbers(qt, img, items):
    xz, yz, _x2, _y2 = qt.region
    drw = ImageDraw.Draw(img)

    for i, item in enumerate(items):
        msg = str(i)
        x = (item.rect.x1 - xz) * 2 + 2
        y = (item.rect.y1 - yz) * 2
        drw.text((x, y), msg, align='center')


def randomColor(seed, light=False):
    # Set the seed for consistent color generation
    random.seed(seed)

    # Generate random values for R, G, and B in the range [0, 1]
    red = random.random()
    green = random.random()
    blue = random.random()

    # Return the color as a 3-tuple
    if light:
        return (int(red * 128) + 128, int(green * 128) + 128, int(blue * 128) + 128)
    else:
        return (int(red * 128), int(green * 128), int(blue * 128))


def main():
    import random

    cfg = dict(
        base_size=(600, 400),
        smallest_size=5,
        largest_size=50,
        count=270,
        show_quadtree=False,
        show_items=True,
        show_numbers=False,
        grow="nowhere",
        arrange="top",
        colors=True,
        fill=True,
        seed=1000
    )

    if cfg['seed']:
        random.seed(cfg['seed'])


    items = []
    for i in range(cfg['count']):
        w = random.randint(cfg['smallest_size'], cfg['largest_size'])
        h = random.randint(cfg['smallest_size'], cfg['largest_size'])
        items.append(Item((w, h), i))

    print()
    print("Before packing:")
    for it in items:
        print(it)

    qt = pack(items, cfg['base_size'], smallest_size=cfg['smallest_size'], grow_dir=cfg['grow'], arrange=cfg['arrange'])

    print()
    print("After packing:")

    print(qt.max_depth)

    for it in items:
        print(it)

    if Image:
        img = getImg(qt)
        if cfg['show_quadtree']:
            drawQuadtree(qt, img)

        if cfg['show_items']:
            fill = False
            if cfg['colors']:
                color = randomColor
                if cfg['fill']:
                    fill = lambda i: randomColor(i, light=True)
            else:
                color = (128, 255, 128)
                if cfg['fill']:
                    fill = (64, 128, 64)
            drawRects(qt, img, (it.rect for it in items), color, fill=fill)

        if cfg['show_numbers']:
            drawNumbers(qt, img, items)

        img.show()
    else:
        print("*"*60)
        print("Skipping drawing of packing, Pillow is not installed")
        print("*"*60)


if __name__ == "__main__":
    main()
