"""
the Hochfrequenz Bilanzierungsobjekt
"""
from datetime import datetime
from typing import Optional

from bo4e.bo.geschaeftsobjekt import Geschaeftsobjekt

from ibims.com.lastprofil import Lastprofil
from ibims.enum import BoTypErweitert
from ibims.enum.aggregationsverantwortung import Aggregationsverantwortung
from ibims.enum.profiltyp import Profiltyp
from ibims.enum.prognosegrundlage import Prognosegrundlage


class Bilanzierung(Geschaeftsobjekt):
    """
    Bilanzierung is a business object used for balancing. This object is no BO4E standard and a complete go
    implementation can be found at
    https://github.com/Hochfrequenz/go-bo4e/blob/3414a1eac741542628df796d6beb43eaa27b0b3e/bo/bilanzierung.go
    """

    bo_typ: BoTypErweitert = BoTypErweitert.BILANZIERUNG  # type: ignore[assignment]

    bilanzierungsbeginn: datetime
    """
    inclusive start date of balancing
    """
    bilanzierungsende: datetime
    """
    exclusive end date of balancing
    """

    bilanzkreis: Optional[str] = None

    aggregationsverantwortung: Optional[Aggregationsverantwortung] = None

    lastprofile: Optional[list[Lastprofil]] = None

    prognosegrundlage: Optional[Prognosegrundlage] = None

    details_prognosegrundlage: Optional[Profiltyp] = None
