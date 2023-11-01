from rhazes.decorator import bean
from django.conf import settings
import os
from parse_it import ParseIt

from django_boot_core.exceptions import MissingConfigurationException


@bean()
class DjangoBootConfiguration:
    """
    Helper bean for reading values from settings.APPLICATION_CONFIGURATION
    """

    def __init__(self):
        self.django_boot_settings: dict = settings.DJANGO_BOOT
        self.application_configuration = self.django_boot_settings.get(
            "APPLICATION_CONFIGURATION", {}
        )

    def get_application_configuration_location(self):
        path = self.application_configuration.get("LOCATION")
        if path is None:
            if hasattr(settings, "BASE_DIR"):
                return os.path.join(settings.BASE_DIR, "application_config")
            raise MissingConfigurationException("APPLICATION_CONFIGURATION.LOCATION")

    def get_application_configuration_type_priority(self):
        return self.application_configuration.get("CONFIG_TYPE_PRIORITY")

    def get_application_configuration_global_default_value(self):
        return self.application_configuration.get("GLOBAL_DEFAULT_VALUE")

    def get_application_configuration_type_estimation(self):
        return self.application_configuration.get("TYPE_ESTIMATE", True)

    def get_application_configuration_recurse(self):
        return self.application_configuration.get("RECURSE", False)

    def get_application_configuration_force_envvars_uppercase(self):
        return self.application_configuration.get("FORCE_ENVVARS_UPPERCASE", True)

    def get_application_configuration_envvar_prefix(self):
        return self.application_configuration.get("ENVVAR_PREFIX")

    def get_application_configuration_suffix_mapping(self):
        return self.application_configuration.get("SUFFIX_MAPPING")

    def get_application_configuration_envvar_divider(self):
        return self.application_configuration.get("ENVVAR_DIVIDER", False)

    def get_application_configuration_none_values(self):
        return self.application_configuration.get("NONE_VALUES", False)


@bean(_for=ParseIt)
class ApplicationConfiguration(ParseIt):
    def __init__(self, django_boot_configuration: DjangoBootConfiguration):
        super(ApplicationConfiguration, self).__init__(
            config_type_priority=django_boot_configuration.get_application_configuration_type_priority(),
            global_default_value=django_boot_configuration.get_application_configuration_global_default_value(),
            type_estimate=django_boot_configuration.get_application_configuration_type_estimation(),
            recurse=django_boot_configuration.get_application_configuration_recurse(),
            force_envvars_uppercase=django_boot_configuration.get_application_configuration_force_envvars_uppercase(),
            config_location=django_boot_configuration.get_application_configuration_location(),
            envvar_prefix=django_boot_configuration.get_application_configuration_envvar_prefix(),
            custom_suffix_mapping=django_boot_configuration.get_application_configuration_suffix_mapping(),
            envvar_divider=django_boot_configuration.get_application_configuration_envvar_divider(),
            none_values=django_boot_configuration.get_application_configuration_none_values(),
        )
