# QuAPI [pronounced "quappy"]

QuAPI is a simple, lightweight, and fast API for querying,
manipulating, and analyzing data. It is designed to be used
fast in development and production environments; with better
DX [Developer Experience].

## Plans

- [x] Add a generator for creating new controllers
- [x] Restrict or allow certain methods for a controller
- [x] Add a feature for tweaking URL/routes; for example, developers can
      send / to `home.index` or `home.myapp` controller.
- [x] Add a feature for tweaking the default controller
- [x] Add a feature for tweaking paths
- [ ] Dynamic routing; /users/:id
- [ ] Add support for more databases; ORM
- [ ] Add a generator for creating new models
- [ ] Add authentication and authorization abilities; as decorators
- [ ] Add testing abilities and environment

## How to use?

- Git clone this repository
- Install dependencies; `pip install -r requirements.txt`
- Run `./core/generate.py -c <controller_name> <action_name>` to generate a new controller
- Add a `get` function [or your preferred method] in the `controllers/<controller_name>.py` file
- Add `<controller_name>` to the `routes.yaml` file
- Run `make start` to start the server in the project directory;
- Open your browser and go to `localhost:8080/<controller_name>/<action_name>`

### How to use `/<controller_name>/` as URL?

- Create a `index.py` file in `controllers/<controller_name>/` directory
- Add a `get` function [or your preferred method] in the `controllers/<controller_name>.py` file
- Add `<controller_name>` to the `routes.yaml` file
- Run `./core/server.py` to start the server in the project directory; be sure you are
  in the project directory
- Open your browser and go to `localhost:8080/<controller_name>/`

### How to use `/` as URL?

- Create a controller with its action and method; for example, `home.index`
- Add `home.index` to the `routes.yaml` file; as `root: home.index` on the first line
- Run `./core/server.py` to start the server in the project directory; be sure you are
  in the project directory
- Open your browser and go to `localhost:8080/`
- You can also use `/home/index` as URL

## How to contribute?

- Fork this repository
- Make changes
- Create a pull request
- Wait for review
- Merge
- Celebrate :tada:
- Repeat :repeat:

## License

BSD 3-Clause License
