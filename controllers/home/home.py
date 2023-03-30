from core.essentials import STATUS

def get(request):
    return ["HELLO"], STATUS.BAD_REQUEST_400, "text/plain"