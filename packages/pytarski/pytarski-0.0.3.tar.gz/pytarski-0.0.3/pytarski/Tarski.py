class TarskiObject:
    def __init__(self, shape, size, col, row):
        if shape not in ['cube', 'dodec', 'tet']:
            raise NameError('Invalid shape')
        if size not in ['small', 'medium', 'large']:
            raise NameError('Invalid size')
        if col not in range(8):
            raise NameError('Invalid column')
        if row not in range(8):
            raise NameError('Invalid row')
        self.shape = shape
        self.size = size 
        self.col = col 
        self.row = row

    def __str__(self):
        return f'{self.shape} {self.size} {self.col} {self.row}'
    
class TarskiBoard:
    def __init__(self):
        self.objects = []

    def __str__(self):
        s = ''
        for obj in self.objects:
            s += str(obj) + ', '
        return s[:-2]

    def add(self, shape, size, col, row):
        for obj in self.objects:
            if obj.col == col and obj.row == row:
                if obj.shape == shape and obj.size == size:
                    return obj
                else:
                    raise NameError(f'Object already exists at column {col} and row {row}')
            elif (obj.size == 'large' or size == 'large'):
                if (obj.col == col + 1 or obj.col == col - 1 or obj.col == col) and (obj.row == row + 1 or obj.row == row - 1 or obj.row == row):
                    raise NameError(f'Cannot place an object in a tile surrounding a large object')
        self.objects.append(TarskiObject(shape, size, col, row))
        return self.objects[-1]
            