"""
New ENUM to differentiate note types.
"""
from bo4e.enum.strenum import StrEnum


class Regelzone(StrEnum):
    """
    a strenum where the str-value of each member is the ILN of the Regelzone for electricity
    """

    TRANSNETBW = "10YDE-ENBW-----N"
    TENNETDE = "10YDE-EON------1"
    AMPRION = "10YDE-RWENET---I"
    FUENFZIGHERTZ = "10YDE-VE-------2"


class Marktgebiet(StrEnum):
    """
    a strenum where the str-value of each member is the ILN of the Regelzone for Gas
    Also known as: Marktgebietscode
    """

    TRADINGHUBEUROPE = "37Y005053MH0000R"
    THE_H_GAS = "THE0BFH027950000"
    THE_L_GAS = "THE0BFL027960000"
