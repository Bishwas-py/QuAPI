def get(request):
    print("request", request.path)
    if "new" in request.headers:
        return ["Hello World", "200 OK"]
    return {
        "path": request.path
    }
    