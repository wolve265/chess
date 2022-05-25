def row_int2str(row_i: int) -> str:
    """
    Converts row index to string\n
    e.g 0 -> '1'
    """
    return chr(row_i + ord('1'))

def row_str2int(row_str: str) -> int:
    """
    Converts row string to index\n
    e.g '1' -> 0
    """
    return ord(row_str) - ord('1')

def col_int2str(col_i: int) -> str:
    """
    Converts column index to string\n
    e.g 0 -> 'a'
    """
    return chr(col_i + ord('a'))

def col_str2int(col_str: str) -> int:
    """
    Converts column string to index\n
    e.g 'a' -> 0
    """
    return ord(col_str) - ord('a')


if __name__ == "__main__":
    print(col_str2int('d'), row_str2int('5'))
