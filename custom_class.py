class Rectangle:
    def __init__(self, length: int, width: int):
        self.length = length
        self.width = width

    # To make the class iterable
    def __iter__(self):
        # Use an iterator that yields first the length, then the width in the specified format
        yield {'length': self.length}
        yield {'width': self.width}

if __name__ == "__main__":
    rectangle = Rectangle(length=10, width=5)
    # Iterating over the instance
    for dimension in rectangle:
        print(dimension)
