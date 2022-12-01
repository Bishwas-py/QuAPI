from core.probe import authenticate


def get(request):
    print("request", request.path)
    if "new" in request.accepts:
        return ["Hello World", "200 OK"]
    return {
        "path": request.user_agent
    }


@authenticate.authenticate
def post(request):
    return "Hello World", "200 OK"
