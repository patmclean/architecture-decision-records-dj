"""Initial testing of cli.py"""

from architecture_decision_records.core import cli


class TestCli:
    def test_cli_setting_monkey_patch_return_value(self):
        """Validate _setting works provides the expected return value."""
        storages_config = {
            "AWS_ACCESS_KEY_ID": "ASF4WDA4MWW4OQ44M44E4O4Q4M4W4PMaDA<W4PDA",
            "AWS_SECRET_ACCESS_KEY": "ASaFK44MWA44DM444s4ac4as4daw/da4wrt1231541231231",
            "AWS_STORAGE_BUCKET_NAME": "adr-test-bucker",
            "AWS_S3_REGION_NAME": "us-west-1",
        }
        global_config = {"USE_TZ": True}
        configs = storages_config.update(global_config)
        for setting, value in configs.items():
            result = cli._configure_settings._setting(setting)
            assert result == value

    def test_cli_setting_monkey_patch_return_none(self):
        """Validate _setting returns none for non-existent setting."""
        configs = ("AWS_NON_EXISTENT_KEY", "STORAGE_NON_EXISTENT_KEY")
        for setting in configs:
            assert not cli._configure_settings._setting(setting)