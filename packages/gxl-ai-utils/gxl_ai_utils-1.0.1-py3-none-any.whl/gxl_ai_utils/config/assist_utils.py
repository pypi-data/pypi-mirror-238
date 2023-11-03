def indent(s_, num_spaces):
    """
    第一行前不加空格, 后面的行均加num个空格
    """
    s = s_.split("\n")
    if len(s) == 1:
        return s_
    first = s.pop(0)
    s = [(num_spaces * " ") + line for line in s]
    s = "\n".join(s)
    s = first + "\n" + s
    return s