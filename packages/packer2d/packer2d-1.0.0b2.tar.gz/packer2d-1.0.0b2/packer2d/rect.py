from typing import Protocol, Union, Tuple, List, NamedTuple
from math import ceil

FloatIntType = Union[float, int]


class RectType(Protocol):
    x1: FloatIntType
    y1: FloatIntType
    x2: FloatIntType
    y2: FloatIntType


class Rect(NamedTuple):
    x1: FloatIntType
    y1: FloatIntType
    x2: FloatIntType
    y2: FloatIntType

def ensureRect(rect: Union[RectType, Tuple, List]) -> RectType:
    """
    Ensures that the given coordinates satisfy `RectProtocol` requirements (it has the properties x1, y1, x2 and y2),
    if it does, it is returned without change. Otherwise, a Rect is constructed and returned.

    Parameters:
        rect: An object to be checked

    Returns:
        RectType: A `RectProtocol` object (maybe a Rect) representing the rectangle.

    Raises:
        ValueError: If the argument is not and cannot be made into a RectProtocol object

    Example:
        ensureRect((1, 2, 3, 4))  # Returns: Rect(1, 2, 3, 4)

    Note:
        This function can accept coordinates in different formats:
        - A `RectProtocol` object.
        - A tuple or list with four elements representing the rectangle's coordinates.
        - A tuple or list with two elements representing the width and height of the rectangle.
    """
    try:
        _ = rect.x1
        _ = rect.x2
        _ = rect.y1
        _ = rect.y2
        return rect
    except:
        pass
    try:
        if len(rect) == 4:
            return Rect(*rect)
        else:
            assert(len(rect) == 2)
            return Rect(0, 0, rect[0], rect[1])
    except:
        raise ValueError("Argument to ensureRect must be one of: (width,height), (x1,y1,x2,y2), or a Rect instance")

# returns a series of rectangles that span rect - othe
def bore(rect: RectType, other: RectType, overlapping=True, int_coords=False) -> List[Rect]:
    """
    Generates a list of rectangles that represent the non-overlapping slabs
    created by subtracting the 'other' rectangle from the 'rect' rectangle.
    The resulting rectangles are returned in a list.

    Parameters:
        rect (RectType): The main rectangle from which the slabs are generated.
        other (RectType): The rectangle that is subtracted from the main rectangle.
        overlapping (bool, optional): A flag indicating whether to allow slabs to overlap.
            Defaults to True.

    Returns:
        - List[Rect]: A list of rectangles representing the non-overlapping slabs.
    """
    rects = []

    if int_coords and any(isinstance(f,float) for f in (rect.x1,rect.y1,rect.x2,rect.y2)):
        rect = makeInt(rect, True)

    if other.y1 > rect.y1:  # top slab
        rects.append(Rect(rect.x1, rect.y1, rect.x2, other.y1))
    if other.y2 < rect.y2:  # bottom slab
        rects.append(Rect(rect.x1, other.y2, rect.x2, rect.y2))

    if overlapping:
        if other.x1 > rect.x1:  # left slab
            rects.append(Rect(rect.x1, rect.y1, other.x1, rect.y2))
        if other.x2 < rect.x2:  # right slab
            rects.append(Rect(other.x2, rect.y1, rect.x2, rect.y2))
    else:
        if other.x1 > rect.x1:  # left slab
            rects.append(Rect(rect.x1, other.y1, other.x1, other.y2))
        if other.x2 < rect.x2:  # right slab
            rects.append(Rect(other.x2, other.y1, rect.x2, other.y2))

    return rects


def makeInt(rect: RectType, round_out) -> RectType:
    if round_out:
        return Rect(int(rect.x1), int(rect.y1), int(ceil(rect.x2)), int(ceil(rect.y2)))
    else:
        return Rect(int(ceil(rect.x1)), int(ceil(rect.y1)), int(rect.x2), int(rect.y2))

def intersects(rect: RectType, other: RectType) -> bool:
    """
    Check if two rectangles intersect.

    Parameters:
        rect (RectType): The first rectangle.
        other (RectType): The second rectangle.

    Returns:
        bool: True if the rectangles intersect, False otherwise.
    """
    if other.x1 >= rect.x2: return False
    if other.y1 >= rect.y2: return False
    if rect.x1 >= other.x2: return False
    if rect.y1 >= other.y2: return False
    return True

def contains(rect: RectType, other: RectType) -> bool:
    """
    Check if the given rectangle `other` is completely contained within the rectangle `rect`.

    Args:
        rect: A `RectProtocol` object representing the outer rectangle.
        other: A `RectProtocol` object representing the inner rectangle.

    Returns:
        A boolean indicating whether `other` is contained within `rect`.
    """
    if other.x1 < rect.x1: return False
    if other.y1 < rect.y1: return False
    if other.x2 > rect.x2: return False
    if other.y2 > rect.y2: return False
    return True

def rectCenter(rect: RectType, int_coords: bool = True) -> Tuple[FloatIntType, FloatIntType]:
    """
    Calculate the center coordinates of a rectangle.

    Parameters:
        rect (RectType): The rectangle object.
        int_coords (bool, optional): Whether to enforce integer coordinates. Defaults to True.

    Returns:
        Tuple[FloatInt, FloatInt]: The x and y coordinates of the center point of the rectangle.
    """
    if int_coords:
        return (rect.x1 + rect.x2) // 2, (rect.y1 + rect.y2) // 2
    else:
        return (rect.x1 + rect.x2) / 2, (rect.y1 + rect.y2) / 2

def rectSize(rect: RectType) -> Tuple[FloatIntType, FloatIntType]:
    """
    Calculate the size of a rectangle.

    Args:
        rect (RectType): The rectangle object.

    Returns:
        Tuple[FloatInt, FloatInt]: A tuple containing the width and height of the rectangle.
    """
    return rect.x2 - rect.x1, rect.y2 - rect.y1

def width(rect: RectType) -> FloatIntType:
    """
    Calculate the width of a rectangle.

    Parameters:
        rect (RectType): The rectangle object for which to obtain the width

    Returns:
        FloatInt: A number representing the width of the rectangle
    """
    return rect.x2 - rect.x1


def height(rect: RectType) -> FloatIntType:
    """
    Calculate the height of a rectangle.

    Parameters:
        rect (RectType): The rectangle object for which to obtain the height

    Returns:
        FloatInt: A number representing the height of the rectangle
    """
    return rect.y2 - rect.y1

def displaced(rect: RectType, dx, dy) -> Rect:
    """
    Generate a new rectangle by displacing an existing rectangle.

    Parameters:
        rect (RectType): The original rectangle to be displaced.
        dx (int): The displacement in the x-direction.
        dy (int): The displacement in the y-direction.

    Returns:
        Rect: The displaced rectangle.
    """
    return Rect(rect.x1 + dx, rect.y1 + dy, rect.x2 + dx, rect.y2 + dy)


def fitsIn(rect: RectType, other: RectType) -> bool:
    """
    Check if the given rectangle `rect` can fit inside the other rectangle `other`.
    Note unlike `contains`, this does not check if the rectangles intersect.

    Parameters:
        rect (RectType): The rectangle to check if it fits inside `other`.
        other (RectType): The other rectangle to compare with `rect`.

    Returns:
        bool: True if `rect` can fit inside `other`, False otherwise.
    """
    if rect.x2 - rect.x1 > other.x2 - other.x1: return False
    if rect.y2 - rect.y1 > other.y2 - other.y1: return False
    return True


def intersect(rect: RectType, other: RectType):
    """
    Changes rect to the intersection of rect and other

    Parameters:
        rect (RectType): The first rectangle.
        other (RectType): The second rectangle.

    Returns:
        None
    """
    rect.x1 = max(rect.x1, other.x1)
    rect.y1 = max(rect.y1, other.y1)
    rect.x2 = min(rect.x2, other.x2)
    rect.y2 = min(rect.y2, other.y2)


def copy(rect: RectType) -> Rect:
    """
    Copy the given rectangle.

    Args:
        rect (RectType): The rectangle to be copied.

    Returns:
        Rect: A new rectangle with the same coordinates as the input rectangle.
    """
    return Rect(rect.x1, rect.y1, rect.x2, rect.y2)


