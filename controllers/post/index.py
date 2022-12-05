def get(request):
    is_authenticated = request.authorization
    if is_authenticated:
        return "You are authenticated", "200 OK"
    return "Hello World", "200 OK"
