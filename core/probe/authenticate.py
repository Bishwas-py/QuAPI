def authenticate(func):
    print("authenticate")

    # This function is what we "replace" hello with
    def wrapper(*args, **kw):
        print("args", args)
        return func(*args, **kw)  # Call hello

    return wrapper
