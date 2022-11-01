

def is_float(f):
    try:
        float(f)
        return True
    except ValueError:
        return False

def is_int(i):
    try:
        int(i)
        return True
    except ValueError:
        return False
