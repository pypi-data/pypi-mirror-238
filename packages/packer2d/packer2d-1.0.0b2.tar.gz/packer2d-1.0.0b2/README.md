<img alt="Version" src="https://img.shields.io/badge/version-1.0.0--beta-blue.svg?cacheSeconds=604800" />
<a href="https://gitlab.com/felingineer/packer2d/-/blob/master/LICENSE.txt" target="_blank"><img alt="License:BSD" src="https://img.shields.io/badge/License-BSD-yellow.svg" /></a>

# packer2d


# Project Description
  
The primary goal of 2D bin packing is to find an arrangement of items (in this case, rectangles) that utilizes the available container space optimally.

That is what Packer2D does. It takes a list of rectangles and arranges their positions in a specified area attempting to pack them leaving little wasted space.


![](https://gitlab.com/felingineer/packer2d/-/raw/master/images/img1.png)


# Installation

## Using pip

```
pip install packer2d

```

## From sources

The source code is available at [Gitlab](https://gitlab.com/felingineer/packer2d)

# Example

```python

from packer2d import Item, pack

# let's say we have this list with the sizes of the rectangles to pack

sizes = [
    (15,20),
    (7,5),
    (9,18),
    ...
]

# The packer function takes a list of Item objects, so we create it now.
# We can initialize Item objects with 2-tuples that contain the size of the rectangles
# or with 4-tuples that specify the corners of the rectangle like so: (x1, y2, x2, y2).
# In that case, only their size is taken into consideration, as they will be moved around.

items = [Item(size) for size in sizes]

pack(items, (200, 200))

# now the rect propery of each item has been set to a Rect object, which can be seen as
# a 4-tuple with the coordinates (x1, y2, x2, y2). 

for item in items:
    print(item.rect)


```

There's another example in the repository, called `test.py`, which was used to generate the image shown at the top. It requires the package `pillow` to be installed.



# API


## FUNCTIONS

### ➤ function *pack*

```python
pack(
    items: Iterable[Item],
    max_area: Tuple,
    arrange: Optional[Callable, Arrange] = None,
    insert_order: Optional[Callable, PlaceOrder] = None,
    smallest_size: Union[int, Tuple[int, int]] = 3,
    max_depth: int = 5,
    int_coords: bool = True,
    grow_dir: GrowDirection = <GrowDirection.ANYWHERE: 3>
) → QTree
```

Packs a list of 2D items into a given area. After the function has been called, the location of the items has been computed and their rect field has been updated. 



#### Args:

 - **items** (list): A list of Item objects to be packed into the area. 

    Required parameter.


 - **max_area** (tuple): The maximum area to pack the items into. It can be either a (width, height) or a (x1, y1, x2, y2) tuple. Note the area might grow beyond the initial size if `grow_dir` is set.

    Required parameter.


 - **arrange** (function or str, optional): How will the items be laid out in the area:
     
    * If not set, or "top", items will be laid out from top to bottom. 
   
    * If "left", items will be placed from left to right. 
    
    * If it's a function, then it must accept two parameters and must either return a rectangle where the item should be placed, or raise **NotEnoughSpaceError** if a suitable area couldn't be found. Such a function can be created with `getArrangeFn`.

        Args:
        
         - **qt** (QTree): The quadtree containing the available areas.
        
         - **item** (Item): The item to be placed.

    Defaults to "top"


 - **insert_order** (function or str, optional): The function to determine the order in which items are inserted: 
    * If not set to "largest_first", items will be inserted from largest to smallest. 
   
    * If "smallest_first", items will be inserted from smallest to largest. 
    
    * If it's a function, then it must accept an Item as only parameter and must return a value usable as key when sorting a list. Its value will determine the order in which items are considered for placement. Such a function can be created with `rectSortFn`.

       Defaults to "largest_first".

 - **smallest_size** (tuple or int, optional): Free areas smaller than this size won't be considered. Setting this value too low can make the packing slower. Setting it too high may cause too much wasted space. It should match the smallest size of the item to be placed. 

   Defaults to 3 (which is equivalent to (3,3) )
 
 - **max_depth** (int, optional): The maximum depth of the quadtree. Note if growing the area is allowed (by using `grow_dir`), then max_depth automatically increments whenever the area is expanded. 

    Defaults to 5.
 
 - **int_coords** (bool, optional): Whether to enforce integer coordinates for the item placement. 

    Defaults to True. 

 - **grow_dir** (GrowDirection, optional): The direction in which the container can grow if it doesn't have enough space to contain all the items. 
   If set to "nowhere", no attempt will be made to grow the container and an exception will be raised if there's not enough space. 
   
    Defaults to "anywhere". 

#### Returns:
    
 - QTree : An instance of the internal quadtree used to keep track of available areas.

#### Raises:

 - **NotEnoughSpaceError** if not all elements can be placed in *max_area* and grow_dir was set to "nowhere".

</br></br>

### ➤ function *getArrangeFn*

```python
getArrangeFn(orientation: ArrangeType, param: float = None) → Callable
```

Creates and returns a function used to pick the best location to place an item, from all available locations at a given moment.

#### Args:

 - **orientation** (str): The orientation of the rectangles. Must be either "left", "top" or "box". 


 - **param** (float): Used when orientation=="box" to specify the aspect ratio of the placement. If 1 or not specified, then it is a square.


#### Returns:

 - A function (see the parameter `arrange` in the function `pack`)


#### Raises:

 - **ValueError** If the orientation is not "left", "top" or "box".

</br></br>

### ➤ function *getRectSortFn*

```python
getRectSortFn(order: PlaceOrderType) → Callable
```

Creates and returns a function that can be passed as key when sorting a list. It's used to decide the order in which items get placed.



#### Args:
 - **order** (str): The order in which to sort the rectangles. Must be either "largest_first" or "smallest_first". 



#### Returns:

 - A function (see parameter `insert_order` in the function `pack`)


#### Raises:


 - **ValueError** If the order is neither 'biggest_first' or 'smallest_first'. 

</br></br>

## CLASSES

### ➤ class *Item*
Container that holds a rectangle and an optional data field. It is used to pass the rectangles that will be arranged to the function `pack`. It is also used internally by the packer to store the available regions in a QTree.


#### `__init__(self, rect: Union[Tuple, RectType], data: Any = None)`

 - **rect** (tuple or RectType): Can be a 2-tuple with the size of the item (width, height), a 4-tuple with the coordinates of the item (x1, y1, x2, y2) or an object that fulfills the `RectType` requirements.

 - **data** (any): Can be set by the user to anything


#### Properties:

 - **rect** (RectType): This is set from the passed argument of the same name when creating an instance. However, in this case it is guaranteed to be a `RectType` object. If the object passed to the constructor wasn't one, a Rect object is created from it.

 - **data** (any): Whatever was passed in the constructor, or None if not set.
    
</br></br>

### ➤ class *Rect*
A subclass of namedtuple that contains the fields x1, y1, x2, y2.

#### `__init__(self, x1:IntFloatType, y1:IntFloatType, x2:IntFloatType, y2:IntFloatType)`

#### Properties (read only):

 - **x1** (IntFloatType)

 - **y1** (IntFloatType)

 - **x2** (IntFloatType)

 - **y2** (IntFloatType)

</br></br>

## TYPES

### ➤ *FloatIntType*

A type that is either float or int

### ➤ *GrowDirectionType*
One of the following strings: "nowhere", "anywhere", "vertical", "horizontal"

### ➤ *ArrangeType*
One of the following strings: "box", "left", "top"

### ➤ *PlaceOrderType*
One of the following strings: "smallest_first", "largest_first"

###  ➤ *RectType*

A type for an object that has the attributes `x1`, `y2`, `x2`, `y2`, of type either int or float


</br></br>

## EXCEPTIONS


### ➤ *NotEnoughSpaceError*
Raised when there is not enough space in the provided area to pack all the items, and growing of the area was not allowed.


</br></br>

# Licensing and Copyright 

BSD 2-Clause License

Copyright © 2023, Guillermo Romero (Gato)





