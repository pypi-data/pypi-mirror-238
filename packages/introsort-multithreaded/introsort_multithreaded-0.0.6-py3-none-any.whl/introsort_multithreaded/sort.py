from platform import python_version
version = python_version().split(".")[1]
if version == "11":
    from introsort_multithreaded.sorting_eleven import sorting
elif version == "12":
    from introsort_multithreaded.sorting_twelve import sorting

def sort_unstable(lst):
    if type(lst[0]) is int:
        return sorting.sort_unstable_int(lst)
    elif type(lst[0]) is float:
        return sorting.sort_unstable_frac(lst)
    elif type(lst[0]) is str:
        return sorting.sort_unstable_str(lst)
    else:
        print("Unknown type")
        return

def sort_stable(lst):
    if type(lst[0]) is float:
        return sorting.sort_stable_frac(lst)
    elif type(lst[0]) is str:
        return sorting.sort_stable_str(lst)
    else:
        print("Unknown type")
        return
