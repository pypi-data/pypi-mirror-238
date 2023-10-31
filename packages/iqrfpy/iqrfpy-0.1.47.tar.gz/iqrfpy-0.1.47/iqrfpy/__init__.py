"""iqrfpy

.. include:: ../README.md

.. include:: ../changelog.md
"""
__version__ = '0.1.47'

from typeguard import install_import_hook
with install_import_hook('iqrfpy'):
    from iqrfpy import async_response, confirmation, enums, exceptions, irequest, iresponse, messages, peripherals, \
        transports, utils, response_factory
