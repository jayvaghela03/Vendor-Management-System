from django.apps import AppConfig

class VendorApiConfig(AppConfig):
    """
    Configuration class for the 'vendor_api' app.

    Attributes:
        default_auto_field (str): The default auto field for model creation.
        name (str): The name of the app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vendor_api'

    def ready(self):
        """
        Method called when the app is ready. It registers signals.

        Signals:
            - Registers signals by importing the 'vendor_api.signals' module.
        """
        import vendor_api.signals
