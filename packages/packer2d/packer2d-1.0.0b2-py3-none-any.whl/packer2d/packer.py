from collections.abc import Callable, Iterable
from typing import Literal

from .qtree import *
from .rect import *

__all__ = ['pack', 'getArrangeFn', 'getRectSortFn', 'NotEnoughSpaceError',
           'GrowDirectionType', 'ArrangeType', 'PlaceOrderType']


class NotEnoughSpaceError(Exception):
    pass


GrowDirectionType = Literal["nowhere", "vertical", "horizontal", "anywhere"]

ArrangeType = Literal["box", "left", "top"]

PlaceOrderType = Literal["smallest_first", "largest_first"]


def getArrangeFn(orientation: ArrangeType, param: float = None) -> Callable:
    """
    Returns a function that finds the best rectangle fit based on the given orientation.
    Usually you won't need to create such function yourself, but instead would call the `getBestRectFn` function to create
    one.

    The function returned traverses all the items in the quadtree and returns the rectangle of the received item, displaced
    to fit in the picked quadtree item.


    Parameters:
        orientation (str): The orientation of the rectangles. Must be either "left", "top" or "box".

    Returns:
        function: A function that takes in two parameters:
            - qt (QuadTree): The quadtree containing the available areas.
            - item (Item): The item to be placed.

    Raises:
        ValueError: If the orientation is not "left" or "top".
        NotEnoughSpaceError: If no suitable area is found.
    """
    if orientation == "top":
        fit_fn = lambda a: (a.item.rect.y1, a.item.rect.x1)
    elif orientation == "left":
        fit_fn = lambda a: (a.item.rect.x1, a.item.rect.y1)
    elif orientation == "box":
        if param is None:
            fit_fn = lambda a: max(a.item.rect.x1, a.item.rect.y1)
        else:
            fit_fn = lambda a: max(a.item.rect.x1, a.item.rect.y1 * param)
    else:
        raise ValueError("Orientation must be either 'left' or 'top'")

    def inner(qt: QTree, item: Item):
        rect = item.rect  # rect is a naked rect (not an Item)
        available_areas = list(qt.items())

        available_areas.sort(key=fit_fn)

        for a in available_areas:
            if fitsIn(rect, a.item.rect):
                arect = a.item.rect
                placed = displaced(rect, arect.x1 - rect.x1, arect.y1 - rect.y1)
                return placed

        raise NotEnoughSpaceError("No suitable area found")

    return inner


def getRectSortFn(order: PlaceOrderType) -> Callable:
    """
    Generate a sorting function based on the given order.

    Args:
        order (str): The order in which to sort the rectangles. Must be either "largest_first"
                     or "smallest_first".

    Returns:
        function: A sorting function that takes an item as input and returns a value based on the
                  given order. If order is 'smallest_first', the function returns the maximum
                  dimension of the item's rectangle. If order is 'largest_first', the function
                  returns the negative maximum dimension of the item's rectangle.

    Raises:
        ValueError: If the order is neither 'largest_first' nor 'smallest_first'.
    """
    if order == 'smallest_first':
        order_fn = lambda item: max(width(item.rect), height(item.rect))
    elif order == 'largest_first':
        order_fn = lambda item: -max(width(item.rect), height(item.rect))
    else:
        raise ValueError("Order must be either 'largest_first' or 'smallest_first'")

    return order_fn




def extendQuadtree(qt: QTree, max_x2: float, max_y2: float):
    # these two don't change when a new root is added
    x1 = qt.region.x1
    y1 = qt.region.y1
    # these two change
    prev_x2 = qt.region.x2
    prev_y2 = qt.region.y2
    qt.addLevelAbove()
    new_x2 = qt.region.x2
    new_y2 = qt.region.y2

    assert (not (max_x2 and max_y2))

    if max_x2:
        qt.insertItem(Item((x1, prev_y2, max_x2, new_y2)))
    elif max_y2:
        qt.insertItem(Item((prev_x2, y1, new_x2, max_y2)))
    else:
        qt.insertItem(Item((x1, prev_y2, new_x2, new_y2)))
        qt.insertItem(Item((prev_x2, y1, new_x2, new_y2)))

    return
    # TODO: check why the code below is not working
    #       the idea is to extend items that are touching the old root edges
    #       to the new root edges


#    to_add_to_root = []
#
#    root = qt.root
#
#    def isBoundary(node: QTreeNode) -> bool:
#        if node == root: return True
#        return node.region.x2 == prev_x2 or node.region.y2 == prev_y2
#
#
#    # only traverse nodes that bound the area which was extended
#    for node, _level in qt.nodes():
#        if not node.items:
#            continue
#        node_items = []
#        for item in node.items:
#            if item.rect.x2 != prev_x2 and item.rect.y2 != prev_y2:
#                node_items.append(item)
#                continue
#            rect = item.rect
#            item.rect = Rect(rect.x1,
#                             rect.y1,
#                             new_x2 if rect.x2 == prev_x2 else rect.x2,
#                             new_y2 if rect.y2 == prev_y2 else rect.y2
#                             )
#            to_add_to_root.append(item)
#        node.items = node_items
#    qt.root.items = to_add_to_root
#


# items is a list of Items
def pack(items: Iterable[Item], max_area: Tuple, arrange: Union[Callable, ArrangeType, None] = None,
         insert_order: Union[Callable, PlaceOrderType, None] = None, smallest_size: Union[int, Tuple[int, int]] = 3,
         max_depth: int = 5,
         int_coords: bool = True, grow_dir: GrowDirectionType = "anywhere") -> QTree:
    """
        Packs a list of 2D items into a given area.
        After the function has been called, the items have been packed into the area and their rect field has been updated.

        Args:
            items (list): A list of Item objects to be packed into the area.
            max_area (tuple): The maximum area to pack the items into. It can be either a (width, height) or
                a (x1, y1, x2, y2) tuple.
            arrange (function or str, optional): How will the items be laid out in the area:
                If not set, or "top", items will be placed from top to bottom.
                If "left", items will be placed from left to right.
            insert_order (function or str, optional): The function to determine the order in which items are
                inserted:
                If not set ot 'largest_first", items will be inserted from biggest to smallest.
                If "smallest_first", items will be inserted from smallest to biggest.
                If it's a function, then it will be used to determine the key while sorting a list of item.
            smallest_size (tuple or int, optional): The smallest size of an item to be considered for packing.
                Defaults to 3 (equivalent to (3, 3)).
            max_depth (int, optional): The maximum depth of the quadtree. Defaults to 5.
            int_coords (bool, optional): Whether to enforce integer coordinates for the item placement.
                Defaults to True.
            grow_dir (str, optional): The direction in which the container can grow if it doesn't have enough
                space to contain the items. If set to "nowhere", no attempt will be made to grow the
                container and an exception will be raised if there's not enough space.
                Defaults to GrowDirection.ANYWHERE.

        Returns:
            QTree: The quadtree containing the available areas.

    """
    if arrange is None:
        arrange = getArrangeFn("box")
    elif isinstance(arrange, str):
        arrange = getArrangeFn(arrange)

    if insert_order is None:
        insert_order = getRectSortFn("largest_first")
    elif isinstance(insert_order, str):
        insert_order = getRectSortFn(insert_order)

    if isinstance(smallest_size, (int, float)):
        smallest_size = (smallest_size, smallest_size)

    qt = QTree(ensureRect(max_area), max_depth=max_depth, int_coords=int_coords)

    qt.insertItem(Item(max_area))

    max_x2 = None
    max_y2 = None
    if grow_dir == "vertical":
        max_x2 = qt.region.x2
    elif grow_dir == "horizontal":
        max_y2 = qt.region.y2

    items = list(items)

    items.sort(key=insert_order)

    for it in items:
        while True:
            try:
                dest_area = arrange(qt, it)
            except NotEnoughSpaceError:
                if grow_dir == GrowDirectionType.NOWHERE:
                    raise
                extendQuadtree(qt, max_x2, max_y2)
                print("Add level above")
            else:
                break

        it.rect = dest_area  # move to the target location

        # find all the rects that intersect the dest_area, and bore a hole through them
        affected = qt.getIntersectingItems(dest_area)

        new_rects = []
        # remove those elements from the qtree and bore a hole through the items
        for a in affected:  # a is an ItemRef
            a.removeFromTree()
            for n in bore(a.item.rect, dest_area, int_coords=int_coords):
                w, h = rectSize(n)
                if w >= smallest_size[0] and h >= smallest_size[1]:  # don't add too small rects
                    new_rects.append(n)

        # insert each item into the qtree, checking we remove all items that are contained inside another
        for n in new_rects:  # these are naked rects
            qt.insertLargestItem(Item(n))

    return qt
