# Rnd Logger

A python logger implementation for the Made Tech R&D department

This implementation adds in and out of office hours flexibility and overrides the inherits from the root logger provided
by the python logging module. The log output when using the rnd_logger will be json

## Testing

- run `make test`

## Creating a release

- Commit your changes to main and then create a release on Github.
- This will trigger a Github action that will increment the version with the tag you have chosen and publish that
  version to PyPi
- Please use semantic versioning and version relative to the change you have made

## Usage

1. Use the rnd_logger:
    2. ```python
        from rnd_logger import rnd_logger
        logger = rnd_logger.get_logger()
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error_office_hours_alert("Office hours alert message")
        logger.error_out_of_hours_alert("Out of office hours alert message")
        ```
2. Testing the rnd_logger:
    3. There is a caplog fixture provided by pytest
    4. ```python
        import logging
        def test_use_case_logs_info(caplog, use_case_under_test):
            with caplog.at_level(logging.INFO):
                your_test_code()
                records = iter(caplog.records)
                record = next(records)
                assert record.message == "your test log"
       ```
   