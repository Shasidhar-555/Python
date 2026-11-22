
# Task 7 - Python Modules

import milkrate imports the module and uses calls such as
milkrate.payout(...).

from milkrate import payout imports the payout function directly.

import milkrate as mr imports the module with the shorter alias mr.

The if __name__ == "__main__": block runs the demonstration table
only when milkrate.py is executed directly. During import,
__name__ is "milkrate", so the table is not printed.

Python searches for modules using sys.path, including relevant
script directories and configured import locations.

The standard library provides modules such as decimal and math.

Copying calculation functions into every script creates repeated
code. A shared module provides one source of truth for rates and
calculations. Python caches imported modules in sys.modules, so
the module normally executes once per interpreter.

Importing has a one-time startup cost. Subsequent calls reuse
the imported functions. Processing n entries remains O(n).
