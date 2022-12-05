import os
import pathlib
import yaml
import logging
from pony import orm

CURRENT_DIR = pathlib.Path(os.getcwd())
ENV = os.environ.get("ENV", "development")

db = orm.Database()

if os.path.exists(CURRENT_DIR / "db.yaml"):
    db_config = yaml.load(open(CURRENT_DIR / "db.yaml", "r"), Loader=yaml.FullLoader)
    if ENV == "development":
        dev_db = db_config.get("development")
        if dev_db:
            db = orm.Database()
            db.bind(provider=dev_db.get("provider"), filename=dev_db.get("filename"))
            orm.set_sql_debug(True)
        else:
            logging.warning("No development database found in db.yaml")
    elif ENV == "production":
        prod_db = db_config.get("production")
        if prod_db:
            db = orm.Database()
            db.bind(**prod_db)
        else:
            logging.warning("No production database found in db.yaml")

else:
    logging.warning("No db.yaml found, skipping database initialization")
