class MissingConfigurationException(Exception):
    def __init__(self, configuration):
        super(MissingConfigurationException, self).__init__(
            f"Missing configuration at: {configuration}"
        )
