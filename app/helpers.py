def mask_string(string, visible=4):
    size = len(string) - visible
    return string[0:visible + 1] + ('*' * size)