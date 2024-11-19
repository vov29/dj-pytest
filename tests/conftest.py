import pytest
pytest_plugins = ['pytester']

#django_db_setup = True

def pytest_configure(config):
    config.option.django_settings_module = "django_testing.settings"