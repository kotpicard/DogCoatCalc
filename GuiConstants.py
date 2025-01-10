import wx

# Goal Type Colors
Hex_GOALCOLOR = "649D48"
Hex_GOALCOLORLIGHT = "75C34E"
Hex_GOALPATTERN = "489A9D"
Hex_GOALPATTERNLIGHT = "52D6DA"
Hex_GOALWHITE = "48499D"
Hex_GOALWHITELIGHT = "5052E5"
Hex_GOALMERLE = "81489D"
Hex_GOALMERLELIGHT = "9B49C4"
Hex_GOALTICKING = "9D486B"
Hex_GOALTICKINGLIGHT = "D45388"
Hex_GOALGREYING = "9D4848"
Hex_GOALGREYINGLIGHT = "BF5151"

# other
Hex_BACKGROUND = "D9D9D9"
Hex_BACKGROUNDBOX = "C4C4C4"
Hex_BUTTONCOLOR = "2C2C2C"
Hex_BUTTONCOLORHOVER = "080707"
Hex_FONTCOLORBG = "150F0F"
Hex_FONTLINKCOLORHOVER = "4548EF"
Hex_FONTLINKCOLOR = "48499D"

# allele hex codes
Hex_ALLELE = "13557E"
Hex_NOTALLELE = "7E1313"
Hex_ANYALLELE = "968C1F"


class Color:
    def __init__(self, hex):
        self.hex = hex
        self.red = int(self.hex[:2], 16)
        self.green = int(self.hex[2:4], 16)
        self.blue = int(self.hex[4:6], 16)
        self.rgb = (self.red, self.green, self.blue, 255)


# GOAL FORMAT: (Name, Type) -> ("Black", "COLOR")
GOALCOLORS = {
    "COLOR_BLACK": (Color(Hex_GOALCOLOR).rgb, Color(Hex_GOALCOLORLIGHT).rgb),
    "COLOR_RED": (Color(Hex_GOALCOLOR).rgb, Color(Hex_GOALCOLORLIGHT).rgb),
    "K_LOCUS": (Color(Hex_GOALPATTERN).rgb, Color(Hex_GOALPATTERNLIGHT).rgb),
    "E_LOCUS": (Color(Hex_GOALPATTERN).rgb, Color(Hex_GOALPATTERNLIGHT).rgb),
    "AGOUTI": (Color(Hex_GOALPATTERN).rgb, Color(Hex_GOALPATTERNLIGHT).rgb),
    "WHITE": (Color(Hex_GOALWHITE).rgb, Color(Hex_GOALWHITELIGHT).rgb),
    "MERLE": (Color(Hex_GOALMERLE).rgb, Color(Hex_GOALMERLELIGHT).rgb),
    "TICKING": (Color(Hex_GOALTICKING).rgb, Color(Hex_GOALTICKINGLIGHT).rgb),
    "GREYING": (Color(Hex_GOALGREYING).rgb, Color(Hex_GOALGREYINGLIGHT).rgb)
}

BUTTONCOLORS = (Color(Hex_BUTTONCOLOR).rgb, Color(Hex_BUTTONCOLORHOVER).rgb)

BREEDINGTYPES = ("CONVENTIONAL", "PICKMATE", "PICKPAIR", "CREATE")

FONT_DEFAULT = wx.Font()
FONT_BIG = wx.Font()
FONT_BIG.SetPointSize(20)
