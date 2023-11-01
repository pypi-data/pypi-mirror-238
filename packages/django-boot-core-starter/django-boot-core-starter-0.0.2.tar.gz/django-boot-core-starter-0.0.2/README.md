# Django Boot Core - Starter

Core starter library for Django Boot.

This library will initialize [Rhazes](https://github.com/django-boot/Rhazes) `ApplicationContext` by default and registers some beans on it.


## Usage

First, add Django Boot Starter to `INSTALLED_APPS`:


```python
INSTALLED_APPS = [
    ...,
    "django_boot_core",
]
```

Then assure you have these two settings in your `settings.py`:

```python
DI_PACKAGES = []  # beans you want to be scanned in your project

DJANGO_BOOT = {
    "APPLICATION_CONFIGURATION": {
        ... # Configuration for ApplicationConfiguration. Read below
    }
}
```

### Application Configuration Parser

Main benefit of using this library is that you will have `ApplicationConfiguration` bean registered for you.

This bean allows you to use configuration files for different services (beans) in your project easily.

`django_boot_core.services.ApplicationConfiguration` is an autoconfigured extension on top of [parse_it](https://github.com/naorlivne/parse_it) library.

To configure `ApplicationConfiguration` (and `ParseIt` class) try changing these values in the settings.

```python
# settings.py

DJANGO_BOOT = {
    "APPLICATION_CONFIGURATION": {
        # Read what blow items do in `parse_it` documentation.
        "LOCATION": os.path.join(BASE_DIR, "application_config"), # Optional, Location to read configuration files from
        "CONFIG_TYPE_PRIORITY": ..., # optional
        "GLOBAL_DEFAULT_VALUE": ..., # optional
        "TYPE_ESTIMATE": ..., # optional
        "RECURSE": ..., # optional
        "FORCE_ENVVARS_UPPERCASE": ..., # optional
        "ENVVAR_PREFIX": ..., # optional
        "SUFFIX_MAPPING": ..., # optional
        "ENVVAR_DIVIDER": ..., # optional
        "NONE_VALUES": ..., # optional
    }
}
```

Default configuration location (directory) (in case `BASE_DIR` is set in `settings.py`) would be `{BASE_DIR}/application_config`.
