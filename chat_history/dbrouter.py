# from typing import Final
#
#
# class MultiDbRouter:
#     app_labels: Final[str] = "chat_history"
#     db_name: Final[str] = "mongo"
#
#     def db_for_read(self, model, **hints):
#         if model._meta.app_label in self.app_labels:
#             return self.db_name
#         return None
#
#     def db_for_write(self, model, **hints):
#         if model._meta.app_label in self.app_labels:
#             return self.db_name
#         return None
#
#     def allow_relation(self, obj1, obj2, **hints):
#         """
#         Allow relations if a model in the obj1 or obj2 apps is
#         involved.
#         """
#         if (
#             obj1._meta.app_label in self.app_labels
#             or obj2._meta.app_label in self.app_labels
#         ):
#             return True
#         return None
#
#     def allow_migrate(self, db, app_label, model_name=None, **hints):
#         """
#         Make sure the auth and contenttypes apps only appear in the
#         'log_db' database.
#         """
#         if app_label in self.app_labels:
#             return self.db_name
#         return None
