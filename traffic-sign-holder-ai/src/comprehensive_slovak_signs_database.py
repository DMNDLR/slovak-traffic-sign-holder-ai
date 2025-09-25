"""
Comprehensive Slovak Traffic Signs Database
Based on official Slovak legislation, soferuj.sk, and auto škola resources
Cross-referenced with multiple official sources for accuracy
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class SignCategory(Enum):
    """Traffic sign categories according to Slovak regulations."""
    WARNING = "výstražné"           # Warning signs (A series)
    PROHIBITORY = "zákazové"        # Prohibitory signs (B series) 
    MANDATORY = "príkazové"         # Mandatory signs (C series)
    INFORMATIONAL = "informačné"    # Informational signs (D,E,F series)
    ADDITIONAL = "dodatkové"        # Additional plates (E series)
    SERVICE = "servisné"            # Service signs (F series)
    TEMPORARY = "dočasné"           # Temporary/construction signs (G series)

@dataclass
class TrafficSign:
    """Individual traffic sign definition."""
    code: str
    name_sk: str
    name_en: str
    category: SignCategory
    description_sk: str
    description_en: str
    shape: str  # triangle, circle, rectangle, octagon, diamond
    color_scheme: str
    text_patterns: List[str]
    common_variations: List[str]

# WARNING SIGNS (VÝSTRAŽNÉ ZNAČKY) - A series
WARNING_SIGNS = {
    "A1": TrafficSign(
        code="A1", name_sk="Nebezpečná zákruta vpravo", name_en="Dangerous right curve",
        category=SignCategory.WARNING, shape="triangle", color_scheme="white_red_border",
        description_sk="Značka upozorňuje na nebezpečnú zákrutu vpravo",
        description_en="Sign warns of dangerous right curve",
        text_patterns=[], common_variations=[]
    ),
    "A2": TrafficSign(
        code="A2", name_sk="Nebezpečná zákruta vľavo", name_en="Dangerous left curve",
        category=SignCategory.WARNING, shape="triangle", color_scheme="white_red_border",
        description_sk="Značka upozorňuje na nebezpečnú zákrutu vľavo",
        description_en="Sign warns of dangerous left curve",
        text_patterns=[], common_variations=[]
    ),
    "A3": TrafficSign(
        code="A3", name_sk="Nebezpečné zákruty", name_en="Dangerous curves",
        category=SignCategory.WARNING, shape="triangle", color_scheme="white_red_border",
        description_sk="Značka upozorňuje na rad nebezpečných zákrut",
        description_en="Sign warns of series of dangerous curves",
        text_patterns=[], common_variations=["s-krivka", "serpentíny"]
    ),
    "A4": TrafficSign(
        code="A4", name_sk="Nebezpečné stúpanie", name_en="Dangerous ascent",
        category=SignCategory.WARNING, shape="triangle", color_scheme="white_red_border",
        description_sk="Značka upozorňuje na nebezpečné stúpanie",
        description_en="Sign warns of dangerous ascent",
        text_patterns=[r"\\d+%"], common_variations=["5%", "8%", "10%", "12%", "15%", "20%"]
    ),
    "A5": TrafficSign(
        code="A5", name_sk="Nebezpečné klesanie", name_en="Dangerous descent",
        category=SignCategory.WARNING, shape="triangle", color_scheme="white_red_border",
        description_sk="Značka upozorňuje na nebezpečné klesanie",
        description_en="Sign warns of dangerous descent",
        text_patterns=[r"\\d+%"], common_variations=["5%", "8%", "10%", "12%", "15%", "20%"]
    ),
    "A6": TrafficSign(
        code="A6", name_sk="Zúženie vozovky", name_en="Road narrowing",
        category=SignCategory.WARNING, shape="triangle", color_scheme="white_red_border",
        description_sk="Značka upozorňuje na zúženie vozovky z oboch strán",
        description_en="Sign warns of road narrowing from both sides",
        text_patterns=[], common_variations=["zľava", "sprava", "z oboch strán"]
    ),
    "A7a": TrafficSign(
        code="A7a", name_sk="Zúženie vozovky zprava", name_en="Road narrowing from right",
        category=SignCategory.WARNING, shape="triangle", color_scheme="white_red_border",
        description_sk="Značka upozorňuje na zúženie vozovky zprava",
        description_en="Sign warns of road narrowing from right",
        text_patterns=[], common_variations=[]
    ),
    "A7b": TrafficSign(
        code="A7b", name_sk="Zúženie vozovky zľava", name_en="Road narrowing from left",
        category=SignCategory.WARNING, shape="triangle", color_scheme="white_red_border",
        description_sk="Značka upozorňuje na zúženie vozovky zľava",
        description_en="Sign warns of road narrowing from left",
        text_patterns=[], common_variations=[]
    ),
    "A8": TrafficSign(
        code="A8", name_sk="Križovatka", name_en="Crossroads",
        category=SignCategory.WARNING, shape="triangle", color_scheme="white_red_border",
        description_sk="Značka upozorňuje na križovatku",
        description_en="Sign warns of crossroads",
        text_patterns=[], common_variations=[]
    ),
    "A9": TrafficSign(
        code="A9", name_sk="Železničné priecestie so závorami", name_en="Level crossing with barriers",
        category=SignCategory.WARNING, shape="triangle", color_scheme="white_red_border",
        description_sk="Značka upozorňuje na železničné priecestie so závorami",
        description_en="Sign warns of level crossing with barriers",
        text_patterns=[], common_variations=[]
    ),
    "A10": TrafficSign(
        code="A10", name_sk="Železničné priecestie bez závoral", name_en="Level crossing without barriers",
        category=SignCategory.WARNING, shape="triangle", color_scheme="white_red_border",
        description_sk="Značka upozorňuje na železničné priecestie bez závoral",
        description_en="Sign warns of level crossing without barriers",
        text_patterns=[], common_variations=[]
    ),
    "A11": TrafficSign(
        code="A11", name_sk="Dvojkoľajné železničné priecestie", name_en="Double track level crossing",
        category=SignCategory.WARNING, shape="triangle", color_scheme="white_red_border",
        description_sk="Značka upozorňuje na dvojkoľajné železničné priecestie",
        description_en="Sign warns of double track level crossing",
        text_patterns=[], common_variations=[]
    ),
    "A12": TrafficSign(
        code="A12", name_sk="Nebezpečenstvo", name_en="Danger",
        category=SignCategory.WARNING, shape="triangle", color_scheme="white_red_border",
        description_sk="Značka upozorňuje na iné nebezpečenstvo",
        description_en="Sign warns of other danger",
        text_patterns=["!"], common_variations=["!"]
    ),
}

# PROHIBITORY SIGNS (ZÁKAZOVÉ ZNAČKY) - B series
PROHIBITORY_SIGNS = {
    "B1": TrafficSign(
        code="B1", name_sk="Zákaz vjazdu", name_en="No entry",
        category=SignCategory.PROHIBITORY, shape="circle", color_scheme="white_red_border",
        description_sk="Značka zakazuje vjazd všetkým vozidlám",
        description_en="Sign prohibits entry for all vehicles",
        text_patterns=[], common_variations=[]
    ),
    "B2": TrafficSign(
        code="B2", name_sk="Zákaz vjazdu pre všetky vozidlá", name_en="No vehicles",
        category=SignCategory.PROHIBITORY, shape="circle", color_scheme="white_red_circle",
        description_sk="Značka zakazuje vjazd všetkým vozidlám v oboch smeroch",
        description_en="Sign prohibits entry for all vehicles in both directions",
        text_patterns=[], common_variations=[]
    ),
    "B3a": TrafficSign(
        code="B3a", name_sk="Zákaz vjazdu pre motorové vozidlá", name_en="No motor vehicles",
        category=SignCategory.PROHIBITORY, shape="circle", color_scheme="white_red_border",
        description_sk="Značka zakazuje vjazd motorovým vozidlám",
        description_en="Sign prohibits entry for motor vehicles",
        text_patterns=[], common_variations=[]
    ),
    "B3b": TrafficSign(
        code="B3b", name_sk="Zákaz vjazdu pre nákladné automobily", name_en="No trucks",
        category=SignCategory.PROHIBITORY, shape="circle", color_scheme="white_red_border",
        description_sk="Značka zakazuje vjazd nákladným automobilom",
        description_en="Sign prohibits entry for trucks",
        text_patterns=[], common_variations=[]
    ),
    "B4": TrafficSign(
        code="B4", name_sk="Zákaz vjazdu pre vozidlá s prívesmi", name_en="No vehicles with trailers",
        category=SignCategory.PROHIBITORY, shape="circle", color_scheme="white_red_border",
        description_sk="Značka zakazuje vjazd vozidlám s prívesmi",
        description_en="Sign prohibits entry for vehicles with trailers",
        text_patterns=[], common_variations=[]
    ),
    "B5": TrafficSign(
        code="B5", name_sk="Zákaz vjazdu pre traktory", name_en="No tractors",
        category=SignCategory.PROHIBITORY, shape="circle", color_scheme="white_red_border",
        description_sk="Značka zakazuje vjazd traktorom",
        description_en="Sign prohibits entry for tractors",
        text_patterns=[], common_variations=[]
    ),
    "B6": TrafficSign(
        code="B6", name_sk="Zákaz vjazdu pre motocykle", name_en="No motorcycles",
        category=SignCategory.PROHIBITORY, shape="circle", color_scheme="white_red_border",
        description_sk="Značka zakazuje vjazd motocyklom",
        description_en="Sign prohibits entry for motorcycles",
        text_patterns=[], common_variations=[]
    ),
    "B7": TrafficSign(
        code="B7", name_sk="Zákaz vjazdu pre chodcov", name_en="No pedestrians",
        category=SignCategory.PROHIBITORY, shape="circle", color_scheme="white_red_border",
        description_sk="Značka zakazuje vstup chodcom",
        description_en="Sign prohibits entry for pedestrians",
        text_patterns=[], common_variations=[]
    ),
    "B8": TrafficSign(
        code="B8", name_sk="Zákaz vjazdu pre cyklistov", name_en="No cyclists",
        category=SignCategory.PROHIBITORY, shape="circle", color_scheme="white_red_border",
        description_sk="Značka zakazuje vjazd cyklistom",
        description_en="Sign prohibits entry for cyclists",
        text_patterns=[], common_variations=[]
    ),
    "B9": TrafficSign(
        code="B9", name_sk="Zákaz odbočenia vľavo", name_en="No left turn",
        category=SignCategory.PROHIBITORY, shape="circle", color_scheme="white_red_border",
        description_sk="Značka zakazuje odbočenie vľavo",
        description_en="Sign prohibits left turn",
        text_patterns=[], common_variations=[]
    ),
    "B10": TrafficSign(
        code="B10", name_sk="Zákaz odbočenia vpravo", name_en="No right turn",
        category=SignCategory.PROHIBITORY, shape="circle", color_scheme="white_red_border",
        description_sk="Značka zakazuje odbočenie vpravo",
        description_en="Sign prohibits right turn",
        text_patterns=[], common_variations=[]
    ),
    "B11": TrafficSign(
        code="B11", name_sk="Zákaz otáčania", name_en="No U-turn",
        category=SignCategory.PROHIBITORY, shape="circle", color_scheme="white_red_border",
        description_sk="Značka zakazuje otáčanie",
        description_en="Sign prohibits U-turn",
        text_patterns=[], common_variations=[]
    ),
    "B12": TrafficSign(
        code="B12", name_sk="Zákaz predbiehania", name_en="No overtaking",
        category=SignCategory.PROHIBITORY, shape="circle", color_scheme="white_red_border",
        description_sk="Značka zakazuje predbiehanie",
        description_en="Sign prohibits overtaking",
        text_patterns=[], common_variations=[]
    ),
    "B13": TrafficSign(
        code="B13", name_sk="Najvyššia dovolená rýchlosť", name_en="Maximum speed limit",
        category=SignCategory.PROHIBITORY, shape="circle", color_scheme="white_red_border",
        description_sk="Značka určuje najvyššiu dovolenú rýchlosť",
        description_en="Sign indicates maximum permitted speed",
        text_patterns=[r"\\d+"], common_variations=["30", "40", "50", "60", "70", "80", "90", "110", "130"]
    ),
    "B14": TrafficSign(
        code="B14", name_sk="Zákaz používania zvukovej výstražby", name_en="No horn",
        category=SignCategory.PROHIBITORY, shape="circle", color_scheme="white_red_border",
        description_sk="Značka zakazuje používanie zvukovej výstražky",
        description_en="Sign prohibits use of horn",
        text_patterns=[], common_variations=[]
    ),
    "B15": TrafficSign(
        code="B15", name_sk="Zákaz zastavenia", name_en="No stopping",
        category=SignCategory.PROHIBITORY, shape="circle", color_scheme="blue_red_diagonal",
        description_sk="Značka zakazuje zastavenie",
        description_en="Sign prohibits stopping",
        text_patterns=[], common_variations=[]
    ),
    "B16": TrafficSign(
        code="B16", name_sk="Zákaz státia", name_en="No parking",
        category=SignCategory.PROHIBITORY, shape="circle", color_scheme="blue_red_diagonal",
        description_sk="Značka zakazuje státie",
        description_en="Sign prohibits parking",
        text_patterns=[], common_variations=[]
    ),
    "B17": TrafficSign(
        code="B17", name_sk="Zákaz státia v nepárne dni", name_en="No parking on odd days",
        category=SignCategory.PROHIBITORY, shape="circle", color_scheme="blue_red_diagonal",
        description_sk="Značka zakazuje státie v nepárne dni",
        description_en="Sign prohibits parking on odd days",
        text_patterns=[], common_variations=[]
    ),
    "B18": TrafficSign(
        code="B18", name_sk="Zákaz státia v párne dni", name_en="No parking on even days",
        category=SignCategory.PROHIBITORY, shape="circle", color_scheme="blue_red_diagonal",
        description_sk="Značka zakazuje státie v párne dni",
        description_en="Sign prohibits parking on even days",
        text_patterns=[], common_variations=[]
    ),
    "B19": TrafficSign(
        code="B19", name_sk="STOJ, daj prednosť v jazde!", name_en="STOP, give way!",
        category=SignCategory.PROHIBITORY, shape="octagon", color_scheme="red_white",
        description_sk="Značka prikazuje zastaviť a dať prednosť",
        description_en="Sign orders to stop and give way",
        text_patterns=["STOP"], common_variations=["STOP"]
    ),
    "B20": TrafficSign(
        code="B20", name_sk="Daj prednosť v jazde!", name_en="Give way!",
        category=SignCategory.PROHIBITORY, shape="triangle_inverted", color_scheme="white_red_border",
        description_sk="Značka prikazuje dať prednosť v jazde",
        description_en="Sign orders to give way",
        text_patterns=[], common_variations=[]
    ),
}

# MANDATORY SIGNS (PRÍKAZOVÉ ZNAČKY) - C series
MANDATORY_SIGNS = {
    "C1": TrafficSign(
        code="C1", name_sk="Príkaz jazdy priamo", name_en="Compulsory ahead",
        category=SignCategory.MANDATORY, shape="circle", color_scheme="blue_white",
        description_sk="Značka prikazuje jazdu priamo",
        description_en="Sign orders to go straight ahead",
        text_patterns=[], common_variations=[]
    ),
    "C2a": TrafficSign(
        code="C2a", name_sk="Príkaz jazdy vpravo", name_en="Compulsory right",
        category=SignCategory.MANDATORY, shape="circle", color_scheme="blue_white",
        description_sk="Značka prikazuje jazdu vpravo",
        description_en="Sign orders to turn right",
        text_patterns=[], common_variations=[]
    ),
    "C2b": TrafficSign(
        code="C2b", name_sk="Príkaz jazdy vľavo", name_en="Compulsory left",
        category=SignCategory.MANDATORY, shape="circle", color_scheme="blue_white",
        description_sk="Značka prikazuje jazdu vľavo",
        description_en="Sign orders to turn left",
        text_patterns=[], common_variations=[]
    ),
    "C3a": TrafficSign(
        code="C3a", name_sk="Príkaz jazdy priamo alebo vpravo", name_en="Compulsory ahead or right",
        category=SignCategory.MANDATORY, shape="circle", color_scheme="blue_white",
        description_sk="Značka prikazuje jazdu priamo alebo vpravo",
        description_en="Sign orders to go ahead or turn right",
        text_patterns=[], common_variations=[]
    ),
    "C3b": TrafficSign(
        code="C3b", name_sk="Príkaz jazdy priamo alebo vľavo", name_en="Compulsory ahead or left",
        category=SignCategory.MANDATORY, shape="circle", color_scheme="blue_white",
        description_sk="Značka prikazuje jazdu priamo alebo vľavo",
        description_en="Sign orders to go ahead or turn left",
        text_patterns=[], common_variations=[]
    ),
    "C4": TrafficSign(
        code="C4", name_sk="Príkaz jazdy vpravo alebo vľavo", name_en="Compulsory right or left",
        category=SignCategory.MANDATORY, shape="circle", color_scheme="blue_white",
        description_sk="Značka prikazuje jazdu vpravo alebo vľavo",
        description_en="Sign orders to turn right or left",
        text_patterns=[], common_variations=[]
    ),
    "C5": TrafficSign(
        code="C5", name_sk="Najnižšia dovolená rýchlosť", name_en="Minimum speed limit",
        category=SignCategory.MANDATORY, shape="circle", color_scheme="blue_white",
        description_sk="Značka určuje najnižšiu dovolenú rýchlosť",
        description_en="Sign indicates minimum permitted speed",
        text_patterns=[r"\\d+"], common_variations=["30", "40", "50", "60"]
    ),
    "C6": TrafficSign(
        code="C6", name_sk="Cyklistická cesta", name_en="Cycle track",
        category=SignCategory.MANDATORY, shape="circle", color_scheme="blue_white",
        description_sk="Značka vyznačuje cestu určenú pre bicykle",
        description_en="Sign indicates path designated for bicycles",
        text_patterns=[], common_variations=[]
    ),
    "C7": TrafficSign(
        code="C7", name_sk="Chodník", name_en="Footpath",
        category=SignCategory.MANDATORY, shape="circle", color_scheme="blue_white",
        description_sk="Značka vyznačuje cestu určenú pre chodcov",
        description_en="Sign indicates path designated for pedestrians",
        text_patterns=[], common_variations=[]
    ),
    "C8a": TrafficSign(
        code="C8a", name_sk="Spoločná cesta pre chodcov a cyklistov", name_en="Shared path",
        category=SignCategory.MANDATORY, shape="circle", color_scheme="blue_white",
        description_sk="Značka vyznačuje spoločnú cestu pre chodcov a cyklistov",
        description_en="Sign indicates shared path for pedestrians and cyclists",
        text_patterns=[], common_variations=[]
    ),
    "C8b": TrafficSign(
        code="C8b", name_sk="Rozdelená cesta pre chodcov a cyklistov", name_en="Segregated path",
        category=SignCategory.MANDATORY, shape="circle", color_scheme="blue_white",
        description_sk="Značka vyznačuje rozdelenú cestu pre chodcov a cyklistov",
        description_en="Sign indicates segregated path for pedestrians and cyclists",
        text_patterns=[], common_variations=[]
    ),
    "C9": TrafficSign(
        code="C9", name_sk="Príkaz použitia snehových reťazí", name_en="Compulsory snow chains",
        category=SignCategory.MANDATORY, shape="circle", color_scheme="blue_white",
        description_sk="Značka prikazuje použitie snehových reťazí",
        description_en="Sign orders use of snow chains",
        text_patterns=[], common_variations=[]
    ),
}

# INFORMATIONAL SIGNS (INFORMAČNÉ ZNAČKY) - D, E, F series
INFORMATIONAL_SIGNS = {
    "D1": TrafficSign(
        code="D1", name_sk="Cesta s prednosťou v jazde", name_en="Priority road",
        category=SignCategory.INFORMATIONAL, shape="diamond", color_scheme="yellow_white_border",
        description_sk="Značka vyznačuje cestu s prednosťou v jazde",
        description_en="Sign indicates priority road",
        text_patterns=[], common_variations=[]
    ),
    "D2": TrafficSign(
        code="D2", name_sk="Koniec cesty s prednosťou v jazde", name_en="End of priority road",
        category=SignCategory.INFORMATIONAL, shape="diamond", color_scheme="yellow_black_diagonal",
        description_sk="Značka vyznačuje koniec cesty s prednosťou v jazde",
        description_en="Sign indicates end of priority road",
        text_patterns=[], common_variations=[]
    ),
    "D3": TrafficSign(
        code="D3", name_sk="Jednosmerná premávka", name_en="One way traffic",
        category=SignCategory.INFORMATIONAL, shape="rectangle", color_scheme="blue_white",
        description_sk="Značka vyznačuje jednosmernú premávku",
        description_en="Sign indicates one way traffic",
        text_patterns=[], common_variations=[]
    ),
    "D4a": TrafficSign(
        code="D4a", name_sk="Parkovisko", name_en="Parking",
        category=SignCategory.INFORMATIONAL, shape="rectangle", color_scheme="blue_white",
        description_sk="Značka vyznačuje parkovisko",
        description_en="Sign indicates parking area",
        text_patterns=["P"], common_variations=["P"]
    ),
    "D4b": TrafficSign(
        code="D4b", name_sk="Parkovanie kolmo", name_en="Perpendicular parking",
        category=SignCategory.INFORMATIONAL, shape="rectangle", color_scheme="blue_white",
        description_sk="Značka vyznačuje kolmé parkovanie",
        description_en="Sign indicates perpendicular parking",
        text_patterns=["P"], common_variations=["P"]
    ),
    "D4c": TrafficSign(
        code="D4c", name_sk="Parkovanie šikmo", name_en="Diagonal parking",
        category=SignCategory.INFORMATIONAL, shape="rectangle", color_scheme="blue_white",
        description_sk="Značka vyznačuje šikmé parkovanie",
        description_en="Sign indicates diagonal parking",
        text_patterns=["P"], common_variations=["P"]
    ),
    "D5": TrafficSign(
        code="D5", name_sk="Obytná zóna", name_en="Residential zone",
        category=SignCategory.INFORMATIONAL, shape="rectangle", color_scheme="blue_white",
        description_sk="Značka vyznačuje obytná zónu",
        description_en="Sign indicates residential zone",
        text_patterns=[], common_variations=[]
    ),
    "D6": TrafficSign(
        code="D6", name_sk="Koniec obytnej zóny", name_en="End of residential zone",
        category=SignCategory.INFORMATIONAL, shape="rectangle", color_scheme="blue_white_diagonal",
        description_sk="Značka vyznačuje koniec obytnej zóny",
        description_en="Sign indicates end of residential zone",
        text_patterns=[], common_variations=[]
    ),
    "D7": TrafficSign(
        code="D7", name_sk="Pešia zóna", name_en="Pedestrian zone",
        category=SignCategory.INFORMATIONAL, shape="rectangle", color_scheme="blue_white",
        description_sk="Značka vyznačuje pešiu zónu",
        description_en="Sign indicates pedestrian zone",
        text_patterns=[], common_variations=[]
    ),
    "D8": TrafficSign(
        code="D8", name_sk="Koniec pešej zóny", name_en="End of pedestrian zone",
        category=SignCategory.INFORMATIONAL, shape="rectangle", color_scheme="blue_white_diagonal",
        description_sk="Značka vyznačuje koniec pešej zóny",
        description_en="Sign indicates end of pedestrian zone",
        text_patterns=[], common_variations=[]
    ),
}

# SERVICE AND DIRECTION SIGNS (SERVISNÉ A SMEROVÉ ZNAČKY) - E, F series
SERVICE_SIGNS = {
    "E1": TrafficSign(
        code="E1", name_sk="Nemocnica", name_en="Hospital",
        category=SignCategory.SERVICE, shape="rectangle", color_scheme="blue_white",
        description_sk="Značka vyznačuje nemocnicu",
        description_en="Sign indicates hospital",
        text_patterns=["H", "+"], common_variations=["H", "+"]
    ),
    "E2": TrafficSign(
        code="E2", name_sk="Čerpacia stanica", name_en="Fuel station",
        category=SignCategory.SERVICE, shape="rectangle", color_scheme="blue_white",
        description_sk="Značka vyznačuje čerpaciu stanicu",
        description_en="Sign indicates fuel station",
        text_patterns=[], common_variations=[]
    ),
    "E3": TrafficSign(
        code="E3", name_sk="Autoservis", name_en="Car repair",
        category=SignCategory.SERVICE, shape="rectangle", color_scheme="blue_white",
        description_sk="Značka vyznačuje autoservis",
        description_en="Sign indicates car repair service",
        text_patterns=[], common_variations=[]
    ),
    "E4": TrafficSign(
        code="E4", name_sk="Telefón", name_en="Telephone",
        category=SignCategory.SERVICE, shape="rectangle", color_scheme="blue_white",
        description_sk="Značka vyznačuje telefón",
        description_en="Sign indicates telephone",
        text_patterns=[], common_variations=[]
    ),
    "E5": TrafficSign(
        code="E5", name_sk="Hotel, motel", name_en="Hotel, motel",
        category=SignCategory.SERVICE, shape="rectangle", color_scheme="blue_white",
        description_sk="Značka vyznačuje hotel alebo motel",
        description_en="Sign indicates hotel or motel",
        text_patterns=[], common_variations=[]
    ),
    "E6": TrafficSign(
        code="E6", name_sk="Reštaurácia", name_en="Restaurant",
        category=SignCategory.SERVICE, shape="rectangle", color_scheme="blue_white",
        description_sk="Značka vyznačuje reštauráciu",
        description_en="Sign indicates restaurant",
        text_patterns=[], common_variations=[]
    ),
    "E7": TrafficSign(
        code="E7", name_sk="WC", name_en="Toilet",
        category=SignCategory.SERVICE, shape="rectangle", color_scheme="blue_white",
        description_sk="Značka vyznačuje WC",
        description_en="Sign indicates toilet",
        text_patterns=["WC"], common_variations=["WC"]
    ),
}

# SPEED LIMIT AND REGULATORY CONTINUATION
SPEED_AND_REGULATORY_SIGNS = {
    "B21": TrafficSign(
        code="B21", name_sk="Koniec najvyššej dovolenej rýchlosti", name_en="End of maximum speed limit",
        category=SignCategory.PROHIBITORY, shape="circle", color_scheme="white_black_diagonal",
        description_sk="Značka označuje koniec najvyššej dovolenej rýchlosti",
        description_en="Sign indicates end of maximum speed limit",
        text_patterns=[r"\\d+"], common_variations=["30", "40", "50", "60", "70", "80", "90"]
    ),
    "B22": TrafficSign(
        code="B22", name_sk="Koniec najnižšej dovolenej rýchlosti", name_en="End of minimum speed limit",
        category=SignCategory.PROHIBITORY, shape="circle", color_scheme="blue_white_diagonal",
        description_sk="Značka označuje koniec najnižšej dovolenej rýchlosti",
        description_en="Sign indicates end of minimum speed limit",
        text_patterns=[r"\\d+"], common_variations=["30", "40", "50", "60"]
    ),
    "B23": TrafficSign(
        code="B23", name_sk="Koniec zákazu predbiehania", name_en="End of no overtaking",
        category=SignCategory.PROHIBITORY, shape="circle", color_scheme="white_black_diagonal",
        description_sk="Značka označuje koniec zákazu predbiehania",
        description_en="Sign indicates end of no overtaking",
        text_patterns=[], common_variations=[]
    ),
    "B24": TrafficSign(
        code="B24", name_sk="Koniec všetkých zákazov", name_en="End of all restrictions",
        category=SignCategory.PROHIBITORY, shape="circle", color_scheme="white_black_diagonal",
        description_sk="Značka označuje koniec všetkých zákazov",
        description_en="Sign indicates end of all restrictions",
        text_patterns=[], common_variations=[]
    ),
}

class SlovakTrafficSignsDatabase:
    """Comprehensive database of Slovak traffic signs."""
    
    def __init__(self):
        self.signs = {}
        self._load_all_signs()
        
    def _load_all_signs(self):
        """Load all sign categories into the database."""
        self.signs.update(WARNING_SIGNS)
        self.signs.update(PROHIBITORY_SIGNS)
        self.signs.update(MANDATORY_SIGNS)
        self.signs.update(INFORMATIONAL_SIGNS)
        self.signs.update(SERVICE_SIGNS)
        self.signs.update(SPEED_AND_REGULATORY_SIGNS)
        
    def get_sign_by_code(self, code: str) -> Optional[TrafficSign]:
        """Get traffic sign by its code."""
        return self.signs.get(code.upper())
        
    def search_signs(self, query: str) -> List[Tuple[str, TrafficSign]]:
        """Search signs by name, code, or description."""
        query = query.lower()
        results = []
        
        for code, sign in self.signs.items():
            if (query in code.lower() or 
                query in sign.name_sk.lower() or 
                query in sign.name_en.lower() or
                query in sign.description_sk.lower() or
                any(query in var.lower() for var in sign.common_variations)):
                results.append((code, sign))
                
        return results
        
    def get_signs_by_category(self, category: SignCategory) -> List[Tuple[str, TrafficSign]]:
        """Get all signs of a specific category."""
        return [(code, sign) for code, sign in self.signs.items() 
                if sign.category == category]
        
    def get_all_codes(self) -> List[str]:
        """Get all available sign codes."""
        return list(self.signs.keys())

def get_database() -> SlovakTrafficSignsDatabase:
    """Get instance of Slovak traffic signs database."""
    return SlovakTrafficSignsDatabase()