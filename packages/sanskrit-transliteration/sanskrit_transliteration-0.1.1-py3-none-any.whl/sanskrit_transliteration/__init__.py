from .hk_and_skt import HkAndSkt
from .velthius_and_hk import VelthiusHk
from .wx_slp1_hk import WxSlp1Hk
from .from_skt import FromSkt
from .velthius_and_skt import VelSkt
from .wx_slp1_skt import WxSlp1Skt
from .wx_slp1_vel import WxSlp1Vel
from .wx_slp1 import WxSlp1


def transliterate(text, from_scheme, to_scheme):
    if from_scheme == to_scheme:
        raise KeyError("Input and output shouldn't belong to the same scheme.")
    if from_scheme == "HK":
        if to_scheme == "SKT":
            return HkAndSkt.hk_to_skt(text)
        elif to_scheme == "VELTHIUS":
            return VelthiusHk.hk_to_velthius(text)
        elif to_scheme == "SLP1":
            return WxSlp1Hk.hk_to_wx_or_slp1(
                text=text,
                to_scheme="SLP1"
            )
        elif to_scheme == "WX":
            return WxSlp1Hk.hk_to_wx_or_slp1(
                text=text,
                to_scheme=to_scheme
            )
        else:
            raise KeyError(f"{to_scheme} does not exist.")
    elif from_scheme == "SKT":
        return FromSkt.transliterate_from_skt(scheme=to_scheme, text=text)
    elif from_scheme == "VELTHIUS":
        if to_scheme == "SKT":
            return VelSkt.vel_to_skt(text=text)
        if to_scheme == "HK":
            return VelthiusHk.velthius_to_hk(text)
        elif to_scheme == "SLP1":
            return WxSlp1Vel.vel_to_wx_or_slp1(text=text, to_scheme="SLP1")
        elif to_scheme == "WX":
            return WxSlp1Vel.vel_to_wx_or_slp1(text=text, to_scheme="WX")
        else:
            raise KeyError(f"{to_scheme} does not exist.")
    elif from_scheme == "SLP1":
        if to_scheme == "SKT":
            return WxSlp1Skt.wx_slp1_to_skt(text=text, from_scheme="SLP1")
        elif to_scheme == "VELTHIUS":
            return WxSlp1Vel.slp1_to_vel(text=text)
        elif to_scheme == "HK":
            return WxSlp1Hk.slp1_to_hk(text=text)
        elif to_scheme == "WX":
            return WxSlp1.slp1_to_wx(text=text)
        else:
            raise KeyError(f"{to_scheme} does not exist.")
    elif from_scheme == "WX":
        if to_scheme == "SKT":
            return WxSlp1Skt.wx_slp1_to_skt(text, from_scheme="WX")
        elif to_scheme == "VELTHIUS":
            return WxSlp1Vel.wx_to_vel(text=text)
        elif to_scheme == "HK":
            return WxSlp1Hk.wx_to_hk(
                text=text
            )
        elif to_scheme == "SLP1":
            return WxSlp1.wx_to_slp1(text=text)
        else:
            raise KeyError(f"{to_scheme} does not exist.")
    else:
        raise KeyError(f"{from_scheme} does not exist.")
