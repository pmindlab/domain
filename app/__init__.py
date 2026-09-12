__version__ = "1.7.1"

# Extend the v1.7 curator with a larger, still-curated context pool before
# app.main imports the legacy-named workshop_v16 module.
from . import workshop_v171_expansion as _workshop_v171_expansion

_workshop_v171_expansion.install()
