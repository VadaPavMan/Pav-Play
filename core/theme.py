def getThemeColors(self, isDarkMode):

    if self.isDarkMode:

        return {
            "window": "#121212",
            "nav": "#1E1E1E",
            "media": "#181818",
            "player": "#282828",
            "playlist": "#1E1E1E",
            "controls": "#1E1E1E",

            "surface": "#262626",
            "surface_hover": "#2E2222",

            "text": "#F2F2F2",
            "secondary_text": "#BDBDBD",

            "border": "#3A3A3A",
            "divider": "#2A2A2A",

            "slider_bg": "#141414",

            "accent": "#FF3344",
        }

    else:

        return {
            "window": "#F2F2F2",
            "nav": "#FFFFFF",
            "media": "#E8E8E8",
            "player": "#E6E6E6",
            "playlist": "#FFFFFF",
            "controls": "#FFFFFF",

            "surface": "#E8E8E8",
            "surface_hover": "#FFE5E8",

            "text": "#181818",
            "secondary_text": "#555555",

            "border": "#CFCFCF",
            "divider": "#DADADA",

            "slider_bg": "#D0D0D0",

            "accent": "#FF3344",
        }