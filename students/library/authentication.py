def auth(func):

    def wrapper_func():
        # Do something before the function.
        resp  = func()
        # Do something after the function.
    return wrapper_func