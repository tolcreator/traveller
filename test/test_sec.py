""" For testing src/uwp/sec.py """

from contextlib import nullcontext
import pytest
import src.uwp.sec as sec


@pytest.mark.parametrize("line, expected",
    [
        ("Zeycude       0101 C430698-9    De Na Ni Po        613 Zh K9 V",
            nullcontext({
                "name": "Zeycude",
                "hex": "0101",
                "uwp": "C430698-9",
                "bases": "",
                "codes": "De Na Ni Po",
                "pbg": "613",
                "allegiance": "Zh",
                "stellar": "K9 V"
            })),
        ("This is not a system", pytest.raises(ValueError)),
    ])
def test_parse_system(line, expected):
    with expected as e:
        ret = sec.parse_system(line)
        for item in e:
            assert item in ret
            assert ret[item] == e[item]
            
goodsec = """
# Subsector A: Cronor

 1-14: Name
15-18: HexNbr
20-28: UWP
   31: Bases
33-47: Codes & Comments
   49: Zone
52-54: PBG
56-57: Allegiance
59-74: Stellar Data

....+....1....+....2....+....3....+....4....+....5....+....6....+....7....+....8

Zeycude       0101 C430698-9    De Na Ni Po        613 Zh K9 V
Reno          0102 C4207B9-A    De He Na Po Pi  A  603 Zh G8 V M1 V
Errere        0103 B563664-B  F Ni Ri O:0304       910 Zh M1 V M4 V
Cantrel       0104 C566243-9    Lo                 520 Zh F1 V
Gyomar        0108 C8B2889-8    Fl He Ph (Tethm    824 Na A8 V
Thengo        0202 C868586-5    Ag Ni Pr Lt        801 Zh G5 V M3 V
Rio           0301 C686648-8    Ag Ni Ga Ri        201 Na M0 V M1 V
Gesentown     0303 B31169B-C  F Ic Na Ni Da Ht  A  801 Zh M2 V M9 V
Chronor       0304 A6369A5-D  F Hi Cp Ht           810 Zh F8 V
Atsa          0307 B4337CA-A  F Na Po An Pz     A  810 Zh F7 V M3 V
Whenge        0503 D648500-8    Ag Ni              610 Na F8 V
Enlas-du      0601 E975776-6    Ag Pi              323 Na F1 V
Algebaster    0605 C665658-9    Ag Ni Ga Ri        410 Na M0 V M1 V
Rasatt        0607 E883401-7    Ni                 910 Na F0 V
Ninjar        0608 A311666-C  F Ic Na Ni Mr Ht     410 Zh A4 V
Sheyou        0610 B756779-A  F Ag Ga              111 Zh F4 V M0 V
Indo          0703 E434662-6    Ni O:0605          320 Na F6 V
Nerewhon      0704 E738475-7    Ni                 820 Na K5 V
Cipango       0705 A886865-C  F Ga Ri Pa Ph O:0    121 Zh G2 V
Stave         0710 E7667A8-2    Ag Ga Ri (Obeye    801 Na K9 V M2 V
Narval        0805 D525688-7  M Ni Da           A  603 Cz G4 V M6 V
Plaven        0807 E845300-5    Lo Lt              910 Na G8 V M7 V
Quar          0808 B532720-B  N Na Po Pz        A  401 Cs M2 V
Frond         0810 E9C3300-9    Fl Lo              103 Cs F8 V
"""
def test_parse_sec():
    lines = goodsec.splitlines()
    parsed = sec.parse_sec(lines)
    assert len(parsed) == 24
