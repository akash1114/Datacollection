from django.apps import AppConfig


class CollectionConfig(AppConfig):
    name = 'collection'
    def ready(self):
        from collection.schedular import updater
        updater.start()