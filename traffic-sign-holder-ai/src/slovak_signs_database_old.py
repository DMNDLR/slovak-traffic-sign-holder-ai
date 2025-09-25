"""
Slovak Traffic Signs Database
Comprehensive database of Slovak traffic signs with codes, names, and descriptions.
Based on official Slovak traffic regulations and soferuj.sk reference.
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class SignCategory(Enum):
    """Traffic sign categories according to Slovak regulations."""
    WARNING = "výstražné"           # Warning signs (100-199)
    REGULATORY = "regulačné"        # Regulatory signs (200-299) 
    INFORMATIONAL = "informačné"    # Informational signs (300-399)
    ADDITIONAL = "dodatkové"        # Additional plates (500-599)
    ROAD_MARKINGS = "vodorovné"     # Road markings (600-699)
    TRAFFIC_DEVICES = "zariadenia"  # Traffic devices (700-799)

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
    color_scheme: str  # primary colors
    text_patterns: List[str]  # Common text patterns found on this sign
    common_variations: List[str]  # Common text/number variations

# Complete Slovak Traffic Signs Database
# Based on official Slovak legislation and soferuj.sk resources

# Warning Signs (Výstražné značky) - 100 series
WARNING_SIGNS = {
    "101": TrafficSign(
        code="101",
        name_sk="Nebezpečenstvo",
        name_en="Danger",
        category=SignCategory.WARNING,
        description_sk="Značka upozorňuje na iné nebezpečenstvo ako na to, na ktoré možno upozorniť vhodnou výstražnou značkou",
        description_en="Sign warns of other danger that cannot be indicated by appropriate warning sign",
        shape="triangle",
        color_scheme="white_red_border",
        text_patterns=["!"],
        common_variations=["!"]
    ),
    
    "110": TrafficSign(
        code="110",
        name_sk="Zákruta",
        name_en="Dangerous curve",
        category=SignCategory.WARNING,
        description_sk="Značka upozorňuje na nebezpečnú zákrutu vo vyznačenom smere",
        description_en="Sign warns of dangerous curve in indicated direction",
        shape="triangle",
        color_scheme="white_red_border",
        text_patterns=[],
        common_variations=["pravá", "ľavá"]
    ),
    
    "111": TrafficSign(
        code="111",
        name_sk="Dvojitá zákruta",
        name_en="Double curve",
        category=SignCategory.WARNING,
        description_sk="Značka upozorňuje na dve alebo viac zákrut nasledujúcich bezprostredne za sebou",
        description_en="Sign warns of two or more curves following immediately one after another",
        shape="triangle",
        color_scheme="white_red_border",
        text_patterns=[],
        common_variations=["S-krivka"]
    ),
    
    "112": TrafficSign(
        code="112",
        name_sk="Klesanie",
        name_en="Steep descent",
        category=SignCategory.WARNING,
        description_sk="Značka upozorňuje na nebezpečné klesanie",
        description_en="Sign warns of dangerous descent",
        shape="triangle",
        color_scheme="white_red_border",
        text_patterns=[r"\d+%"],
        common_variations=["5%", "8%", "10%", "12%", "15%", "20%"]
    ),
    
    "113": TrafficSign(
        code="113",
        name_sk="Stúpanie",
        name_en="Steep ascent",
        category=SignCategory.WARNING,
        description_sk="Značka upozorňuje na nebezpečné stúpanie",
        description_en="Sign warns of dangerous ascent",
        shape="triangle",
        color_scheme="white_red_border",
        text_patterns=[r"\d+%"],
        common_variations=["5%", "8%", "10%", "12%", "15%", "20%"]
    ),
    
    "114": TrafficSign(
        code="114",
        name_sk="Zúžená vozovka",
        name_en="Road narrows",
        category=SignCategory.WARNING,
        description_sk="Značka upozorňuje na zúženú vozovku z vyznačenej strany alebo strán",
        description_en="Sign warns of road narrowing from indicated side or sides",
        shape="triangle",
        color_scheme="white_red_border",
        text_patterns=[],
        common_variations=["zľava", "zprava", "z oboch strán"]
    ),
    
    "115": TrafficSign(
        code="115",
        name_sk="Nerovnosť vozovky",
        name_en="Uneven road",
        category=SignCategory.WARNING,
        description_sk="Značka upozorňuje na nerovnosti povrchu vozovky ako sú výtlky, výmole alebo vyjazdené koľaje",
        description_en="Sign warns of road surface irregularities such as potholes, ruts or worn tracks",
        shape="triangle",
        color_scheme="white_red_border",
        text_patterns=[],
        common_variations=[]
    ),
    
    "116": TrafficSign(
        code="116",
        name_sk="Nebezpečná krajnica",
        name_en="Dangerous verge",
        category=SignCategory.WARNING,
        description_sk="Značka upozorňuje na zníženú, nespevnenú alebo inak nebezpečnú krajnicu",
        description_en="Sign warns of lowered, unpaved or otherwise dangerous verge",
        shape="triangle",
        color_scheme="white_red_border",
        text_patterns=[],
        common_variations=[]
    )
}

# Regulatory Signs (Regulačné značky) - 200 series
REGULATORY_SIGNS = {
    "201": TrafficSign(
        code="201",
        name_sk="Stoj, daj prednosť v jazde!",
        name_en="Stop, give way!",
        category=SignCategory.REGULATORY,
        description_sk="Značka prikazuje zastaviť vozidlo a dať prednosť v jazde",
        description_en="Sign orders to stop vehicle and give way",
        shape="octagon",
        color_scheme="red_white",
        text_patterns=["STOP"],
        common_variations=["STOP"]
    ),
    
    "202": TrafficSign(
        code="202",
        name_sk="Daj prednosť v jazde!",
        name_en="Give way!",
        category=SignCategory.REGULATORY,
        description_sk="Značka prikazuje dať prednosť v jazde vozidlám na križujúcej sa ceste",
        description_en="Sign orders to give way to vehicles on intersecting road",
        shape="triangle_inverted",
        color_scheme="white_red_border",
        text_patterns=[],
        common_variations=[]
    ),
    
    "211": TrafficSign(
        code="211",
        name_sk="Zákaz vjazdu",
        name_en="No entry",
        category=SignCategory.REGULATORY,
        description_sk="Značka zakazuje vjazd všetkým vozidlám v oboch smeroch",
        description_en="Sign prohibits entry for all vehicles in both directions",
        shape="circle",
        color_scheme="white_red_border",
        text_patterns=[],
        common_variations=[]
    ),
    
    "212": TrafficSign(
        code="212",
        name_sk="Zákaz vjazdu pre vozidlá v oboch smeroch",
        name_en="No entry for vehicles in both directions",
        category=SignCategory.REGULATORY,
        description_sk="Značka zakazuje vjazd všetkým vozidlám v oboch smeroch",
        description_en="Sign prohibits entry for all vehicles in both directions",
        shape="circle",
        color_scheme="white_red",
        text_patterns=[],
        common_variations=[]
    ),
    
    "221": TrafficSign(
        code="221",
        name_sk="Zákaz odbočovania vľavo",
        name_en="No left turn",
        category=SignCategory.REGULATORY,
        description_sk="Značka zakazuje odbočovanie vľavo",
        description_en="Sign prohibits left turn",
        shape="circle",
        color_scheme="white_red_border",
        text_patterns=[],
        common_variations=[]
    ),
    
    "222": TrafficSign(
        code="222",
        name_sk="Zákaz odbočovania vpravo",
        name_en="No right turn",
        category=SignCategory.REGULATORY,
        description_sk="Značka zakazuje odbočovanie vpravo",
        description_en="Sign prohibits right turn",
        shape="circle",
        color_scheme="white_red_border",
        text_patterns=[],
        common_variations=[]
    ),
    
    "223": TrafficSign(
        code="223",
        name_sk="Zákaz otáčania",
        name_en="No U-turn",
        category=SignCategory.REGULATORY,
        description_sk="Značka zakazuje otáčanie vozidla",
        description_en="Sign prohibits U-turn of vehicle",
        shape="circle",
        color_scheme="white_red_border",
        text_patterns=[],
        common_variations=[]
    ),
    
    "250": TrafficSign(
        code="250",
        name_sk="Najvyššia dovolená rýchlosť",
        name_en="Maximum permitted speed",
        category=SignCategory.REGULATORY,
        description_sk="Značka zakazuje jazdiť rýchlosťou vyššou ako vyznačenou rýchlosťou v kilometroch za hodinu",
        description_en="Sign prohibits driving at speed higher than indicated speed in kilometers per hour",
        shape="circle",
        color_scheme="white_red_border",
        text_patterns=[r"\d+"],
        common_variations=["20", "30", "40", "50", "60", "70", "80", "90", "100", "110", "130"]
    ),
    
    "260": TrafficSign(
        code="260",
        name_sk="Koniec najnižšej dovolenej rýchlosti",
        name_en="End of minimum permitted speed",
        category=SignCategory.REGULATORY,
        description_sk="Značka ukončuje príkaz vyplývajúci z predchádzajúcej značky Najnižšia dovolená rýchlosť",
        description_en="Sign ends order resulting from previous Minimum permitted speed sign",
        shape="circle",
        color_scheme="white_black_diagonal",
        text_patterns=[r"\d+"],
        common_variations=["50", "60", "70", "80", "90"]
    ),
    
    "270": TrafficSign(
        code="270",
        name_sk="Zákaz zastavenia",
        name_en="No stopping",
        category=SignCategory.REGULATORY,
        description_sk="Značka zakazuje zastavenie a státie",
        description_en="Sign prohibits stopping and parking",
        shape="circle",
        color_scheme="blue_red_diagonal",
        text_patterns=[],
        common_variations=[]
    ),
    
    "271": TrafficSign(
        code="271",
        name_sk="Zákaz státia",
        name_en="No parking",
        category=SignCategory.REGULATORY,
        description_sk="Značka zakazuje státie",
        description_en="Sign prohibits parking",
        shape="circle",
        color_scheme="blue_red_diagonal",
        text_patterns=[],
        common_variations=[]
    ),
    
    "272": TrafficSign(
        code="272",
        name_sk="Parkovanie",
        name_en="Parking",
        category=SignCategory.REGULATORY,
        description_sk="Značka označuje miesto alebo priestor, kde je dovolené zastavenie a státie vozidiel",
        description_en="Sign indicates place or space where stopping and parking of vehicles is permitted",
        shape="rectangle",
        color_scheme="blue_white",
        text_patterns=["P"],
        common_variations=["P"]
    )
}

# Informational Signs (Informačné značky) - 300 series  
INFORMATIONAL_SIGNS = {
    "301": TrafficSign(
        code="301",
        name_sk="Cesta s prednostou",
        name_en="Priority road",
        category=SignCategory.INFORMATIONAL,
        description_sk="Značka označuje cestu s prednostou",
        description_en="Sign indicates priority road",
        shape="diamond",
        color_scheme="yellow_white_border",
        text_patterns=[],
        common_variations=[]
    ),
    
    "302": TrafficSign(
        code="302",
        name_sk="Koniec cesty s prednostou",
        name_en="End of priority road",
        category=SignCategory.INFORMATIONAL,
        description_sk="Značka označuje koniec cesty s prednostou",
        description_en="Sign indicates end of priority road",
        shape="diamond",
        color_scheme="yellow_white_border_diagonal",
        text_patterns=[],
        common_variations=[]
    ),
    
    "350": TrafficSign(
        code="350",
        name_sk="Názov obce",
        name_en="Town name",
        category=SignCategory.INFORMATIONAL,
        description_sk="Značka označuje názov obce na začiatku zastavaného územia obce",
        description_en="Sign indicates town name at beginning of built-up area",
        shape="rectangle",
        color_scheme="white_black_border",
        text_patterns=[r"[A-ZÁČĎÉÍĽĹŇÓÔŔŠŤÚÝŽ][a-záčďéíľĺňóôŕšťúýž\s-]+"],
        common_variations=["Bratislava", "Košice", "Prešov", "Žilina", "Banská Bystrica", "Nitra", "Trnava", "Trenčín"]
    ),
    
    "351": TrafficSign(
        code="351",
        name_sk="Koniec obce",
        name_en="End of town",
        category=SignCategory.INFORMATIONAL,
        description_sk="Značka označuje koniec zastavaného územia obce",
        description_en="Sign indicates end of built-up area of town",
        shape="rectangle",
        color_scheme="white_black_border_diagonal",
        text_patterns=[r"[A-ZÁČĎÉÍĽĹŇÓÔŔŠŤÚÝŽ][a-záčďéíľĺňóôŕšťúýž\s-]+"],
        common_variations=["Bratislava", "Košice", "Prešov", "Žilina", "Banská Bystrica", "Nitra", "Trnava", "Trenčín"]
    ),
    
    "360": TrafficSign(
        code="360",
        name_sk="Tabuľový smerník",
        name_en="Direction sign",
        category=SignCategory.INFORMATIONAL,
        description_sk="Značka informuje o smere jazdy k vyznačeným cieľom a vzdialenosti k nim",
        description_en="Sign informs about direction of travel to indicated destinations and distances to them",
        shape="rectangle",
        color_scheme="white_black_border",
        text_patterns=[r"[A-ZÁČĎÉÍĽĹŇÓÔŔŠŤÚÝŽ][a-záčďéíľĺňóôŕšťúýž\s-]+", r"\d+\s*km"],
        common_variations=["→", "←", "↑", "↓", "km"]
    ),
    
    "370": TrafficSign(
        code="370",
        name_sk="Ohlasovacia tabuľa",
        name_en="Advance direction sign",
        category=SignCategory.INFORMATIONAL,
        description_sk="Značka informuje o blízkosti výjazdu, diaľničného uzla alebo odpočívadla",
        description_en="Sign informs about proximity of exit, highway junction or rest area",
        shape="rectangle",
        color_scheme="blue_white",
        text_patterns=[r"[A-ZÁČĎÉÍĽĹŇÓÔŔŠŤÚÝŽ][a-záčďéíľĺňóôŕšťúýž\s-]+", r"\d+\s*m"],
        common_variations=["500 m", "1000 m", "1500 m", "2000 m"]
    )
}

class SlovakSignsDatabase:
    """Main database class for Slovak traffic signs."""
    
    def __init__(self):
        self.signs = {}
        self.signs.update(WARNING_SIGNS)
        self.signs.update(REGULATORY_SIGNS)
        self.signs.update(INFORMATIONAL_SIGNS)
        
    def get_sign_by_code(self, code: str) -> Optional[TrafficSign]:
        """Get sign information by code."""
        return self.signs.get(code)
    
    def search_signs_by_name(self, name: str, lang: str = "sk") -> List[TrafficSign]:
        """Search signs by name (Slovak or English)."""
        results = []
        name_lower = name.lower()
        
        for sign in self.signs.values():
            if lang == "sk" and name_lower in sign.name_sk.lower():
                results.append(sign)
            elif lang == "en" and name_lower in sign.name_en.lower():
                results.append(sign)
        
        return results
    
    def get_signs_by_category(self, category: SignCategory) -> List[TrafficSign]:
        """Get all signs from specific category."""
        return [sign for sign in self.signs.values() if sign.category == category]
    
    def match_text_pattern(self, text: str) -> List[Tuple[TrafficSign, str]]:
        """Match extracted OCR text against known sign patterns."""
        import re
        matches = []
        
        for sign in self.signs.values():
            for pattern in sign.text_patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    matches.append((sign, pattern))
            
            # Check common variations
            for variation in sign.common_variations:
                if variation.lower() in text.lower():
                    matches.append((sign, variation))
        
        return matches
    
    def get_sign_categories(self) -> Dict[str, List[str]]:
        """Get all sign codes organized by category."""
        categories = {}
        for code, sign in self.signs.items():
            cat_name = sign.category.value
            if cat_name not in categories:
                categories[cat_name] = []
            categories[cat_name].append(code)
        
        return categories
    
    def validate_sign_code(self, code: str) -> bool:
        """Validate if sign code exists in database."""
        return code in self.signs
    
    def get_expected_text_for_code(self, code: str) -> List[str]:
        """Get expected text patterns for a sign code."""
        sign = self.get_sign_by_code(code)
        if sign:
            return sign.text_patterns + sign.common_variations
        return []
    
    def export_to_json(self) -> Dict:
        """Export database to JSON format."""
        export_data = {
            "metadata": {
                "source": "Slovak Traffic Regulations",
                "reference": "soferuj.sk, slov-lex.sk",
                "total_signs": len(self.signs),
                "categories": list(SignCategory)
            },
            "signs": {}
        }
        
        for code, sign in self.signs.items():
            export_data["signs"][code] = {
                "code": sign.code,
                "name_sk": sign.name_sk,
                "name_en": sign.name_en,
                "category": sign.category.value,
                "description_sk": sign.description_sk,
                "description_en": sign.description_en,
                "shape": sign.shape,
                "color_scheme": sign.color_scheme,
                "text_patterns": sign.text_patterns,
                "common_variations": sign.common_variations
            }
        
        return export_data

# Global database instance
slovak_signs_db = SlovakSignsDatabase()

def get_database() -> SlovakSignsDatabase:
    """Get the global Slovak signs database instance."""
    return slovak_signs_db

# Utility functions for sign recognition
def classify_sign_by_appearance(shape: str, colors: List[str]) -> List[str]:
    """Classify potential sign codes based on visual appearance."""
    candidates = []
    
    for code, sign in slovak_signs_db.signs.items():
        # Match shape
        if shape.lower() == sign.shape.lower():
            # Match color scheme
            sign_colors = sign.color_scheme.lower().split('_')
            if any(color.lower() in sign_colors for color in colors):
                candidates.append(code)
    
    return candidates

def enhance_ocr_with_sign_context(ocr_text: str, detected_codes: List[str]) -> str:
    """Enhance OCR results using sign context and expected patterns."""
    enhanced_text = ocr_text
    
    # Apply sign-specific text corrections
    for code in detected_codes:
        sign = slovak_signs_db.get_sign_by_code(code)
        if sign:
            # Apply common corrections based on sign type
            if code == "250":  # Speed limit signs
                # Extract numbers and validate
                import re
                numbers = re.findall(r'\d+', enhanced_text)
                if numbers:
                    speed = numbers[0]
                    if speed in sign.common_variations:
                        enhanced_text = speed
            elif code == "201":  # Stop sign
                enhanced_text = "STOP"
            elif code == "272":  # Parking sign
                enhanced_text = "P"
    
    return enhanced_text