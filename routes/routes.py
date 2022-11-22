class Routes:
    root = 'posts.index'
    resources = ['posts', 'comments', 'home']
    tweaked_routes = {
        'home.home': '/home',
        'posts.index': {
            'path': '/zz',
            'only-methods': ['get']
        }
    }
    cooked_routes = {}
