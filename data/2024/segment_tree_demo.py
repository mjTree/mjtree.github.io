import math


class Area:
    __slots__ = (
        "x",
        "y",
        "width",
        "height",
    )

    def __init__(self, x: float, y: float, width: float, height: float):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @property
    def left(self):
        return self.x

    @property
    def top(self):
        return self.y

    @property
    def bottom(self):
        return self.y + self.height

    @property
    def right(self):
        return self.x + self.width

    @property
    def size(self):
        return self.width * self.height


class SegmentArea(Area):
    __slots__ = (
        "mid_x",
        "mid_y",
    )

    def __init__(self, left: float, top: float, right: float, bottom: float):
        Area.__init__(self, left, top, right - left, bottom - top)
        self.mid_x = int((right - left) / 2)
        self.mid_y = int((bottom - top) / 2)

    @property
    def up_left(self):
        return SegmentArea(self.left, self.top, self.mid_x, self.mid_y)

    @property
    def up_right(self):
        return SegmentArea(self.mid_x + 1, self.top, self.right, self.mid_y)

    @property
    def bottom_left(self):
        return SegmentArea(self.left, self.mid_y + 1, self.mid_x, self.bottom)

    @property
    def bottom_right(self):
        return SegmentArea(self.mid_x + 1, self.mid_y + 1, self.right, self.bottom)

    def has_same_border(self, item):
        return (
            self.left == item.left
            or self.right == item.right
            or self.top == item.top
            or self.bottom == item.bottom
        )

    def __contains__(self, item):
        return (
            item.left >= self.left
            and item.right <= self.right
            and item.top >= self.top
            and item.bottom <= self.bottom
        )


class SegmentTreeNode:
    def __init__(self, node_data_list: list, idx: int = 0):
        self._node_data_list = node_data_list
        self._idx = idx

    @property
    def idx(self):
        return self._idx

    @property
    def data(self):
        return self._node_data_list[self._idx]

    @property
    def up_left_node(self):
        return SegmentTreeNode(self._node_data_list, 4 * self._idx + 1)

    @property
    def bottom_right_node(self):
        return SegmentTreeNode(self._node_data_list, 4 * self._idx + 4)

    @property
    def bottom_left_node(self):
        return SegmentTreeNode(self._node_data_list, 4 * self._idx + 3)

    @property
    def up_right_node(self):
        return SegmentTreeNode(self._node_data_list, 4 * self._idx + 2)


class SegmentTree2Dim:
    def __init__(
        self,
        data_list: list,
        width: float = None,
        height: float = None,
        x_segment_num: int = None,
        y_segment_num: int = None,
    ):
        self._data_list = data_list
        self._init_area_size(width, height)
        self._init_segment_num(x_segment_num, y_segment_num)
        self._segment_matrix = [
            [[] for _ in range(self._x_segment_num)] for _ in range(self._y_segment_num)
        ]
        self._group_node_list()
        self._tree_node_data_list = [
            [] for _ in range(16 * self._x_segment_num * self._y_segment_num)
        ]
        segment_area = SegmentArea(
            0, 0, self._x_segment_num - 1, self._y_segment_num - 1
        )
        self._root_node = SegmentTreeNode(self._tree_node_data_list, 0)
        self._build(segment_area, self._root_node)

    def add_data(self, data: Area) -> None:
        x_interval_length = self._width / self._x_segment_num
        y_interval_length = self._height / self._y_segment_num
        x_index = int(data.x / x_interval_length)
        y_index = int(data.y / y_interval_length)
        self._segment_matrix[y_index][x_index].append(data)

    def update_data(self, original_data: Area, new_data: Area) -> bool:
        if not self.delete_data(original_data):
            return False
        self.add_data(new_data)
        return True

    def delete_data(self, data: Area) -> bool:
        x_interval_length = self._width / self._x_segment_num
        y_interval_length = self._height / self._y_segment_num
        x_index = int(data.x / x_interval_length)
        y_index = int(data.y / y_interval_length)
        if data not in self._segment_matrix[y_index][x_index]:
            return False
        self._segment_matrix[y_index][x_index].remove(data)
        return True

    def get_combine_data_within_area(self, area: Area) -> list:
        clean_list = []
        rough_list = []
        x_interval_length = self._width / self._x_segment_num
        y_interval_length = self._height / self._y_segment_num
        segment_area = SegmentArea(
            int(area.left / x_interval_length),
            int(area.top / y_interval_length),
            int(area.right / x_interval_length),
            int(area.bottom / y_interval_length),
        )
        sub_segment_area = SegmentArea(
            0, 0, self._x_segment_num - 1, self._y_segment_num - 1
        )
        self._clean_interval(
            segment_area, sub_segment_area, self._root_node, clean_list, rough_list
        )
        data_list = self._get_chars_from_list(clean_list, rough_list, area)
        return data_list

    def _group_node_list(self):
        for node in self._data_list:
            x_index = int(node.x * self._x_segment_num / self._width)
            y_index = int(node.y * self._y_segment_num / self._height)
            self._segment_matrix[y_index][x_index].append(node)

    def _clean_interval(
        self,
        segment_area: SegmentArea,
        sub_segment_area: SegmentArea,
        tree_node: SegmentTreeNode,
        clean_list: list,
        rough_list: list,
    ) -> None:
        if sub_segment_area in segment_area:
            if segment_area.has_same_border(sub_segment_area):
                rough_list.append(tree_node)
            else:
                clean_list.append(tree_node)
            return
        if segment_area.left <= sub_segment_area.mid_x:
            if segment_area.top <= sub_segment_area.mid_y:
                self._clean_interval(
                    segment_area,
                    sub_segment_area.up_left,
                    tree_node.up_left_node,
                    clean_list,
                    rough_list,
                )
            if segment_area.bottom > sub_segment_area.mid_y:
                self._clean_interval(
                    segment_area,
                    sub_segment_area.bottom_left,
                    tree_node.bottom_left_node,
                    clean_list,
                    rough_list,
                )
        if segment_area.right > sub_segment_area.mid_x:
            if segment_area.top <= sub_segment_area.mid_y:
                self._clean_interval(
                    segment_area,
                    sub_segment_area.up_right,
                    tree_node.up_right_node,
                    clean_list,
                    rough_list,
                )
            if segment_area.bottom > sub_segment_area.mid_y:
                self._clean_interval(
                    segment_area,
                    sub_segment_area.bottom_right,
                    tree_node.bottom_right_node,
                    clean_list,
                    rough_list,
                )

    def _get_chars_from_list(self, clean_list, rough_list, area):
        char_list = []
        for tree_node_position in clean_list:
            if self._tree_node_data_list[tree_node_position.idx] is not None:
                for segment_list in self._tree_node_data_list[tree_node_position.idx]:
                    char_list.extend(segment_list)
        for tree_node_position in rough_list:
            if self._tree_node_data_list[tree_node_position.idx] is not None:
                for segment_list in self._tree_node_data_list[tree_node_position.idx]:
                    for char in segment_list:
                        center_x, center_y = (
                            char.x + char.width / 2.0,
                            char.y - char.height / 2.0,
                        )
                        if (
                            area.left <= center_x <= area.right
                            and area.top <= center_y <= area.bottom
                        ):
                            char_list.append(char)
        return char_list

    def _build(self, segment_area: SegmentArea, tree_node: SegmentTreeNode):
        if not segment_area.width and not segment_area.height:
            self._tree_node_data_list[tree_node.idx] = [
                self._segment_matrix[segment_area.top][segment_area.left]
            ]
            return
        elif not segment_area.height:
            # only put char into lu and ru
            self._build(segment_area.up_left, tree_node.up_left_node)
            self._build(segment_area.up_right, tree_node.up_right_node)
            # use empty recursion for lb and rb
            self._build_empty(segment_area.bottom_left, tree_node.bottom_left_node)
            self._build_empty(segment_area.bottom_right, tree_node.bottom_right_node)
        elif not segment_area.width:
            # only put char into lu and lb
            self._build(segment_area.up_left, tree_node.up_left_node)
            self._build(segment_area.bottom_left, tree_node.bottom_left_node)
            # use empty recursion for ru and rb
            self._build_empty(segment_area.up_right, tree_node.up_right_node)
            self._build_empty(segment_area.bottom_right, tree_node.bottom_right_node)
        else:
            self._build(segment_area.up_left, tree_node.up_left_node)
            self._build(segment_area.up_right, tree_node.up_right_node)
            self._build(segment_area.bottom_left, tree_node.bottom_left_node)
            self._build(segment_area.bottom_right, tree_node.bottom_right_node)
        self._combine_children(tree_node)

    def _build_empty(
        self, segment_area: SegmentArea, tree_node: SegmentTreeNode
    ) -> None:
        if not segment_area.size:
            self._tree_node_data_list[tree_node.idx] = []
        else:
            # doesn't matter which half correspond to which list_position
            # they are all empty
            self._build_empty(segment_area.up_left, tree_node.up_left_node)
            self._build_empty(segment_area.bottom_left, tree_node.bottom_left_node)
            self._build_empty(segment_area.up_right, tree_node.up_right_node)
            self._build_empty(segment_area.bottom_right, tree_node.bottom_right_node)
            self._combine_children(tree_node)

    def _combine_children(self, tree_node: SegmentTreeNode) -> None:
        combined_data_list = []
        combined_data_list.extend(tree_node.up_left_node.data)
        combined_data_list.extend(tree_node.up_right_node.data)
        combined_data_list.extend(tree_node.bottom_left_node.data)
        combined_data_list.extend(tree_node.bottom_right_node.data)
        if combined_data_list:
            self._tree_node_data_list[tree_node.idx] = combined_data_list

    def _init_area_size(self, width, height):
        if width is None or width <= 0 or height is None or height <= 0:
            width = self._data_list[0].right
            height = self._data_list[0].bottom
            for data in self._data_list[1:]:
                width = max((data.right, width))
                height = max((data.bottom, height))
        self._width = width + 1
        self._height = height + 1

    def _init_segment_num(self, x_segment_num, y_segment_num):
        if (
            x_segment_num is None
            or x_segment_num <= 0
            or y_segment_num is None
            or y_segment_num <= 0
        ):
            segment_split_num = int(math.sqrt(len(self._data_list) / 34)) + 1
            x_segment_num = segment_split_num
            y_segment_num = segment_split_num
        self._x_segment_num = x_segment_num
        self._y_segment_num = y_segment_num
