class Variables:
    title = 'Maze'
    img_height = 300
    width, height = 20, 20
    more_than_one_path = True

    search_methods = [0]
    search_methods_name = ['']
    active_search_methodIndex = 0
    active_search_method = search_methods[active_search_methodIndex]
    end = False
    n_moves = 0

    def __init__(self):
        return None