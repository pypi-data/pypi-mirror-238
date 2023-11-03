def cube(object): # check if the object is a cube
    if object.shape == 'cube':
        return True
    return False
    
def dodec(object): # check if the object is a dodecahedron
    if object.shape == 'dodec':
        return True
    return False

def tet(object): # check if the object is a tetrahedron
    if object.shape == 'tet':
        return True
    return False

def small(object): # check if the object is small
    if object.size == 'small':
        return True
    return False
    
def medium(object): # check if the object is medium
    if object.size == 'medium':
        return True
    return False

def large(object): # check if the object is large
    if object.size == 'large':
        return True
    return False

def sameShape(object1, object2): # check of objects are the same shape
    if object1.shape == object2.shape:
        return True
    return False

def sameSize(object1, object2): # check of objects are the same size
    if object1.size == object2.size:
        return True
    return False

def sameCol(object1, object2): # check of objects are in the same column
    if object1.col == object2.col:
        return True
    return False

def sameRow(object1, object2): # check of objects are in the same row
    if object1.row == object2.row:
        return True
    return False

def sameDiagonal(object1, object2): # check if the objects are along the same diagonal
    if not sameCol(object1, object2) and not sameRow(object1, object2):
        if abs((object1.row - object2.row) / (object1.col - object2.col)) == 1.0:
            return True
    return False

def smaller(object1, object2): # check if object1 is smaller than object2
    if object1.size == 'small' and (object2.size == 'medium' or object2.size == 'large'):
        return True
    if object1.size == 'medium' and object2.size == 'large':
        return True
    return False

def larger(object1, object2): # check if object1 is larger than object2
    if object1.size == 'large' and (object2.size == 'medium' or object2.size == 'small'):
        return True
    if object1.size == 'medium' and object2.size == 'small':
        return True
    return False

def leftOf(object1, object2): # check if object1 is to the left of object2
    if object1.col < object2.col:
        return True
    return False

def rightOf(object1, object2): # check if object1 is to the right of object2
    if object1.col > object2.col:
        return True
    return False

def frontOf(object1, object2): # check if object1 is in front of object2
    if object1.row < object2.row:
        return True
    return False

def backOf(object1, object2): # check if object1 is in back of object2
    if object1.row > object2.row:
        return True
    return False

def between(object1, object2, object3): # check if object1 is between object2 and object3
    if sameRow(object1, object2) and sameRow(object2, object3):
        if (object2.col < object1.col and object1.col < object3.col) or (object3.col < object1.col and object1.col < object2.col):
            return True
    if sameCol(object1, object2) and sameCol(object2, object3):
        if (object2.row < object1.row and object1.row < object3.row) or (object3.row < object1.row and object1.row < object2.row):
            return True
    if sameDiagonal(object1, object2) and sameDiagonal(object2, object3):
        if (object2.col < object1.col and object1.col < object3.col) and (object2.row < object1.row and object1.row < object3.row):
            return True
        if (object2.col < object1.col and object1.col < object3.col) and (object2.row > object1.row and object1.row > object3.row):
            return True
        if (object2.col > object1.col and object1.col > object3.col) and (object2.row < object1.row and object1.row < object3.row):
            return True
        if (object2.col > object1.col and object1.col > object3.col) and (object2.row > object1.row and object1.row > object3.row):
            return True
    return False

def adjoins(object1, object2): # check if object1 adjoins object2
    if not large(object1) and not large(object2):
        if sameRow(object1, object2):
            if object1.col == (object2.col - 1) or object1.col == (object2.col + 1):
                return True
        if sameCol(object1, object2):
            if object1.row == (object2.row - 1) or object1.row == (object2.row + 1):
                return True
    return False