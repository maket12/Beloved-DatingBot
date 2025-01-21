# massive = "[[11, None], [14, None]]" - пример строки


def string_to_list(massive: str, form_index: int):
    try:
        massive = massive[1:-1].replace("[", "")
        if "], " in massive:
            massive_edited = massive.split("], ")
            q = massive_edited[-1]
            massive_edited[-1] = q[:-1]
        else:
            massive_edited = massive.split("]")
            massive_edited.remove("")
        return massive_edited[form_index].split(", ")[0]
    except IndexError:
        return None


print(string_to_list("[[11, None], [14, None]]", 0))
