import logging

from importlib import metadata



# Primary package version
__version__ = metadata.version(__name__)

# Sentinel to make sure we only initialize once.
__initialized = False

logger = logging.getLogger(__name__)


def setup():
    """
    Used to configure the settings for adr so the app may run.
    This should be called before any settings are loaded as it handles all of
    the file loading, conditional settings, and settings overlays required to
    load adr settings from anywhere using environment or config path.
    This pattern is inspired by `django.setup()`.
    """
    global __initialized

    if __initialized:
        logger.info("adr NOT initialized (because it already was)!")
        return

    from architecture_decision_records.core import cli
    from architecture_decision_records.core.runner import configure_app

    configure_app(
        project="adr",
        default_config_path=cli.DEFAULT_CONFIG_PATH,
        default_settings=cli.DEFAULT_SETTINGS,
        settings_initializer=cli.generate_settings,
        settings_envvar=cli.SETTINGS_ENVVAR,
        initializer=cli._configure_settings,
    )
    logger.info("adr initialized!")

    __initialized = True