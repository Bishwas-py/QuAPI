context = {
    'name': 'Job the wealthy'
}


def get(request):
    print("request", request)
    print('context')
    return {
        'name': 'Job the wealthy'
    }
