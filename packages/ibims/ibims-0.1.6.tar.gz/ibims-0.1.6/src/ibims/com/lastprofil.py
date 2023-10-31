"""
COM for holding information about lastprofile
"""
from typing import Optional

from bo4e.com.com import COM

from ibims.enum.profiltyp import Profiltyp


class Lastprofil(COM):
    """
    This is not part of the official BO4E standard, but is implemented in the c# and go versions:
    https://github.com/Hochfrequenz/BO4E-dotnet/blob/9bdc151170ddba5c9d7535e863d5a396fe7fec52/BO4E/COM/Lastprofil.cs
    https://github.com/Hochfrequenz/go-bo4e/blob/708b39de0dcea8a9448ed4e7341a2687f6bf7c11/com/lastprofil.go
    Fields, which are not needed for migrations, are omitted and the field "profilart" is modelled as Profiltyp ENUM.
    """

    bezeichnung: Optional[str] = None
    """
    Bezeichnung des Profils, durch DVGW bzw. den Netzbetreiber vergeben
    """
    einspeisung: bool = False
    """
    Einspeisung ist true, falls es sich um Einspeisung handelt
    """
    profilart: Optional[Profiltyp] = None
