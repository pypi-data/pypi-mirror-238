"""This package contains core functionality for the Model Auto Conversion (MAC) service.

Specifically, this package contains the following modules:
- config: This sub-package contains the configuration classes for the MAC service.
- entrypoints: This sub-package contains the entrypoints for the MAC service.
- inference: This sub-package contains the classes and functions for serving inferences.
- io: This sub-package contains the classes and functions for loading models for inference.
- service: This sub-package contains the classes to create services for serving inferences.
- utils: This sub-package contains the utility functions for the Model Auto Conversion (MAC)
    package.
"""

import logging

logging.basicConfig(
    format="%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s: %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    level=logging.DEBUG,
)
