

def is_float(f)->bool:
    try:
        float(f)
        return True
    except ValueError:
        return False

def is_int(i)->bool:
    try:
        int(i)
        return True
    except ValueError:
        return False
