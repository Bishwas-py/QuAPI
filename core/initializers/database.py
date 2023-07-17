# import os
# import pathlib

# import yaml
# import logging
# from pony import orm
# from pony.orm import commit
#
# from core.constants import ENV
#
# CURRENT_DIR = pathlib.Path(os.getcwd())
#
# db = orm.Database()
#
# if os.path.exists(CURRENT_DIR / "db.yaml"):
#     db_config = yaml.load(open(CURRENT_DIR / "db.yaml", "r"), Loader=yaml.FullLoader)
#     if ENV == "development":
#         dev_db = db_config.get("development")
#         if dev_db:
#             db = orm.Database()
#             filename = dev_db.get("filename")
#             provider = dev_db.get("provider")
#             if provider == "sqlite":
#                 if filename:
#                     if not os.path.exists(CURRENT_DIR / filename):
#                         open(CURRENT_DIR / filename, 'a').close()
#                     dev_db.update({"filename": str(CURRENT_DIR / filename)})
#
#             db.bind(**dev_db)
#             orm.set_sql_debug(True)
#             db.generate_mapping(create_tables=True)
#             print("Dev Database initialized")
#         else:
#             logging.warning("No development database found in db.yaml")
#     elif ENV == "production":
#         prod_db = db_config.get("production")
#         if prod_db:
#             db = orm.Database()
#             db.bind(**prod_db)
#             db.generate_mapping(create_tables=True)
#
#         else:
#             logging.warning("No production database found in db.yaml")
#
# else:
#     logging.warning("No db.yaml found, skipping database initialization")
# #
