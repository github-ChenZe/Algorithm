from Frame.Algorithm import *
from Graphing.Pixel import *


class InsertionSort(Algorithm):
    def __init__(self, arr):
        super(InsertionSort, self).__init__()
        self.array = arr
        self.diagram = SortingDiagram(numbers=arr)
        self.converter = None

    def toXML(self):
        # create XML
        root = etree.Element('table')
        # another child with text
        row = etree.Element('row')
        for e in self.array:
            cell = etree.Element('cell')
            cell.text = '%s' % e
            row.append(cell)
        root.append(row)

        # pretty string
        return etree.tostring(root, pretty_print=True)

    def action(self):
        self.converter = XMLtoImage.XMLtoImage()
        self.pending(description="Algorithm begins.")
        self.insertion_sort(self.array)
        self.pending(description="Algorithm done.")

    def generate_algorithm_diagram(self, **kwargs):
        return self.converter.convert(self.toXML())
        colors = [BLACK] * len(self.array)
        result = []
        if "tested" in kwargs:
            colors[kwargs["tested"][0]] = "Yellow"
            colors[kwargs["tested"][1]] = "Yellow"
            self.diagram.reset_colors(colors)
            result.append(self.diagram.render())
        if "swapped" in kwargs:
            colors[kwargs["swapped"][0]] = "Red"
            colors[kwargs["swapped"][1]] = "Red"
            self.diagram.reset_colors(colors)
            result += ([i for i in self.diagram.animated_swap_iterator(kwargs["swapped"][0], kwargs["swapped"][1], 1/25.0)])
        if "pointer" in kwargs:
            result += ([i for i in self.diagram.animated_moving_iterator(kwargs["pointer"], 1/25.0)])
        if len(result) == 0:
            result.append(self.diagram.render())
        return result, kwargs["description"]

    def swap(self, arr, i, j):
        temp = arr[i]
        arr[i] = arr[j]
        arr[j] = temp
        self.pending(swapped=(i, j), description="Swapped %d (index %d) with %d (index %d)." % (arr[i], i, arr[j], j))

    def accommodate(self, arr, i):
        for j in xrange(i, 0, -1):
            if arr[j] < arr[j - 1]:
                self.pending(tested=(j, j - 1),
                             description="%d (index %d) is less than %d (index %d)." % (arr[j], j, arr[j-1], j-1))
                self.swap(arr, j - 1, j)

    def insertion_sort(self, arr):
        for i in range(0, len(arr)):
            self.pending(pointer=i, description="Handling %d (index %d)." % (arr[i], i))
            self.accommodate(arr, i)


def pr(st):
    st.show()


if __name__ == '__main__':
    toImage = XMLtoImage.XMLtoImage()
    a = [4, 5, 1, 3, 2]
    inS = InsertionSort(a)
    inS.generate_algorithm_diagram(description="")#[0][0].show()
