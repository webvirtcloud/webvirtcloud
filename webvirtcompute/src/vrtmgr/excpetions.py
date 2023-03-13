class FirewallRuleError(Exception):
    def __init__(self, msg):
        self.msg = msg
        Exception.__init__(self, msg)


class IPRedirectError(Exception):
    def __init__(self, msg):
        self.message = msg
        Exception.__init__(self, msg)
