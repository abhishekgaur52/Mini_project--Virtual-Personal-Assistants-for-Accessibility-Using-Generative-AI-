class AccessibilityProfile:
    def __init__(self, disability_type="visual"):
        self.disability_type = disability_type

        if disability_type == "visual":
            self.speech_rate = 160
            self.response_style = "normal"
            self.output_mode = "audio"

        elif disability_type == "cognitive":
            self.speech_rate = 120
            self.response_style = "simple"
            self.output_mode = "audio"

        elif disability_type == "hearing":
            self.speech_rate = 150
            self.response_style = "detailed"
            self.output_mode = "text"

        else:
            self.speech_rate = 150
            self.response_style = "normal"
            self.output_mode = "audio"

    def get_profile(self):
        return {
            "disability_type": self.disability_type,
            "speech_rate": self.speech_rate,
            "response_style": self.response_style,
            "output_mode": self.output_mode
        }