def rotate_list(list_to_rotate, rotate_num):
    for x in range(rotate_num):
        list_to_rotate.append(list_to_rotate.pop(0))

    return list_to_rotate
