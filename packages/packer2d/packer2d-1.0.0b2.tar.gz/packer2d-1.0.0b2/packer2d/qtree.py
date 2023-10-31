from enum import IntEnum
from typing import Any, Iterator, Optional

from .rect import *

__all__ = [
    'QTreeNode',
    'QTree',
    'ItemRef',
    'Item',
    'OutOfBoundsError'
]


class OutOfBoundsError(Exception):
    pass


class Quadrant(IntEnum):
    TOP_RIGHT: int = 0
    TOP_LEFT: int = 1
    BOTTOM_LEFT: int = 2
    BOTTOM_RIGHT: int = 3


class QTreeNode:
    __slots__ = ['items', '_children', '_region']

    def __init__(self, area: RectType):
        self.items = None  # set of contained rects
        self._children = None
        self._region = area

    @property
    def region(self) -> RectType:
        """
        Get the region of the quadtree.

        Returns:
            float: The area of the object.
        """
        return self._region

    @classmethod
    def fromQuadrant(cls, parent_area: RectType, quadrant: int, center: Optional[Tuple] = None,
                     int_coords: bool = True) -> 'QTreeNode':
        if not center:
            center = rectCenter(parent_area, int_coords)

        if quadrant == Quadrant.TOP_RIGHT:  # top right
            area = Rect(center[0], parent_area.y1, parent_area.x2, center[1])
        elif quadrant == Quadrant.TOP_LEFT:  # top left
            area = Rect(parent_area.x1, parent_area.y1, center[0], center[1])
        elif quadrant == Quadrant.BOTTOM_LEFT:  # bottom left
            area = Rect(parent_area.x1, center[1], center[0], parent_area.y2)
        elif quadrant == Quadrant.BOTTOM_RIGHT:  # bottom right
            area = Rect(center[0], center[1], parent_area.x2, parent_area.y2)
        else:
            raise ValueError(f"Invalid quadrant {quadrant}")

        return cls(area)

    def add(self, item: 'Item'):
        try:
            self.items.add(item)
        except:
            self.items = {item}

    def remove(self, item: 'Item') -> bool:
        if item in self.items:
            self.items.remove(item)
            return True
        return False

    def __repr__(self) -> str:
        return "<Node %s %s>" % (id(self), self._region)


class ItemRef:
    __slots__ = ['item', 'node']

    def __init__(self, item: 'Item', node: QTreeNode):
        self.item = item
        self.node = node

    def removeFromTree(self):
        if (self.node.remove(self.item)):
            self.item.onRemove()

    def __repr__(self) -> str:
        return "<ItemRef %s : %s>" % (self.node, self.item)


# we use Item objects for two things:
# 1) what we insert in the QTree are items, they have an area and a (currently unused) payload
# 2) the rectangles we try to pack are items, they contain their dimensions 
#	(and after placement, their location) and the related data
class Item:
    __slots__ = ['rect', 'data']

    def __init__(self, rect: Union[Tuple, RectType], data: Any = None):
        self.rect = ensureRect(rect)
        self.data = data

    def onRemove(self):
        pass

    def __repr__(self) -> str:
        if self.data:
            return "<Item %s : %s>" % (self.rect, self.data)
        else:
            return "<Item %s>" % (self.rect,)


class QTree:
    def __init__(self, area_rect: RectType, int_coords: bool = True, max_depth: int = 5):
        area_rect = ensureRect(area_rect)
        self._int_coords = int_coords
        if int_coords:
            if not (isinstance(area_rect.x1, int) or not isinstance(area_rect.y1, int)
                    or not isinstance(area_rect.x2, int) or not isinstance(area_rect.y2, int)):
                raise TypeError("All coordinates must be integers")
        self._root = QTreeNode(area_rect)
        self._max_depth = max_depth

    @property
    def region(self) -> RectType:
        return self._root.region

    @property
    def max_depth(self) -> int:
        return self._max_depth

    @property
    def has_int_coords(self) -> bool:
        return self._int_coords

    @property
    def root(self) -> QTreeNode:
        return self._root

    def findDeepestContainingNode(self, rect: RectType, create_if_missing: bool = True) -> QTreeNode:
        node = self._root
        max_depth = self._max_depth

        while True:
            max_depth -= 1
            c = rectCenter(node._region, self._int_coords)

            if ((rect.x1 < c[0] < rect.x2) or
                    (rect.y1 < c[1] < rect.y2)):
                return node  # rect straddles between nodes

            # identify quadrant
            if rect.x1 >= c[0]:
                if rect.y2 <= c[1]:
                    q = 0
                else:
                    q = 3
            else:
                if rect.y2 <= c[1]:
                    q = 1
                else:
                    q = 2

            if node._children and node._children[q]:
                node = node._children[q]
            else:
                if create_if_missing and max_depth > 0:
                    if not node._children:
                        node._children = [None, None, None, None]
                    child = QTreeNode.fromQuadrant(node._region, q, c, self._int_coords)
                    node._children[q] = child
                    node = child
                else:
                    return node

    def insertItem(self, item: Item) -> ItemRef:
        area = self._root._region

        if not intersects(item.rect, area):
            raise OutOfBoundsError("Rect outside qtree area")

        node = self.findDeepestContainingNode(item.rect)

        node.add(item)

        return ItemRef(item, node)

    # insert item if there's not another item already spanning what item spans
    # also, remove any other item that is spanned by item
    def insertLargestItem(self, item: Item):
        area = self._root._region

        if not intersects(item.rect, area):
            raise OutOfBoundsError("Rect outside qtree area")

        containing, contained = self.getContainItems(item.rect)

        if containing:
            return  # no need to add rect, it's already spanned by another rect

        # if there are elements contained in the new rect, remove them
        for a in contained:
            a.removeFromTree()

        # add the new item
        self.insertItem(item)

    # return two lists:
    #  -- items that contain rect (containing list)
    #  -- items containined inside rect (contained list)
    # if item's rect is equal to rect, it is returned in the first list
    def getContainItems(self, rect: RectType) -> Tuple[List[ItemRef], List[ItemRef]]:
        node_stack = [self._root]
        contained = []
        containing = []

        while node_stack:
            node = node_stack.pop(-1)
            if intersects(node._region, rect):
                if node.items:
                    for it in node.items:
                        if contains(it.rect, rect):
                            containing.append(ItemRef(it, node))
                        elif contains(rect, it.rect):
                            contained.append(ItemRef(it, node))
                if node._children:
                    for ch in node._children:
                        if ch is not None:
                            node_stack.append(ch)
        return containing, contained

    def getIntersectingItems(self, rect: RectType):
        node_stack = [self._root]
        matches = []

        while node_stack:
            node = node_stack.pop(-1)
            if intersects(node._region, rect):
                if node.items:
                    for it in node.items:
                        if intersects(it.rect, rect):
                            matches.append(ItemRef(it, node))
                if node._children:
                    for ch in node._children:
                        if ch is not None:
                            node_stack.append(ch)
        return matches

    def items(self) -> Iterator[ItemRef]:
        node_stack = [self._root]

        while node_stack:
            node = node_stack.pop(-1)
            if node.items:
                for it in node.items:
                    yield ItemRef(it, node)
            if node._children:
                for ch in node._children:
                    if ch is not None:
                        node_stack.append(ch)

    def nodes(self, pred=None) -> Iterator[Tuple[QTreeNode, int]]:
        node_stack = [(self._root, 0)]

        while node_stack:
            node, level = node_stack.pop(-1)
            if pred and not pred(node):
                continue
            yield node, level
            if node._children:
                for ch in node._children:
                    if ch is not None:
                        node_stack.append((ch, level + 1))

    # quadrant is the quadrant on which the previous root will en up in the
    # new root
    def addLevelAbove(self, quadrant=Quadrant.TOP_LEFT):
        r = self._root.region
        w = width(r)
        h = height(r)

        if quadrant == Quadrant.TOP_RIGHT:
            rect = Rect(r.x1 - w, r.y1, r.x2, r.y2 + h)
        elif quadrant == Quadrant.TOP_LEFT:
            rect = Rect(r.x1, r.y1, r.x2 + w, r.y2 + h)
        elif quadrant == Quadrant.BOTTOM_LEFT:
            rect = Rect(r.x1, r.y1 - h, r.x2 + w, r.y2)
        elif quadrant == Quadrant.BOTTOM_RIGHT:
            rect = Rect(r.x1 - w, r.y1 - h, r.x2, r.y2)
        else:
            raise ValueError(f"Invalid quadrant {quadrant}")

        new_root = QTreeNode(rect)
        new_root._children = [None, None, None, None]
        new_root._children[quadrant] = self._root
        new_root.items = []
        self._root = new_root
        self._max_depth += 1
