def get(request):
    return {
        'name': 'Job the wealthy'
    }


def post(request):
    user_agent = request.user_agent
    return {
        'user_agent': user_agent
    }
