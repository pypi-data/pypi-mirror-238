class Version:
    def __init__(self, major, minor, revision):
        self.major = major
        self.minor = minor
        self.revision = revision

    @staticmethod
    def from_str(version: str):
        if isinstance(version, Version):
            return version

        ss = version.split(".")
        if len(ss) == 0:
            return Version(0, 0, 0)
        elif len(ss) == 1:
            return Version(int(ss[0]), 0, 0)
        elif len(ss) == 2:
            return Version(int(ss[0]), int(ss[1]), 0)
        else:
            return Version(int(ss[0]), int(ss[1]), int(ss[2]))

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.revision}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        other = Version.from_str(other)
        return self.major == other.major and self.minor == other.minor and self.revision == other.revision

    def __lt__(self, other):
        other = Version.from_str(other)

        if self.major < other.major:
            return True
        elif self.major > other.major:
            return False

        if self.minor < other.minor:
            return True
        elif self.minor > other.minor:
            return False

        return self.revision < other.revision

    def __gt__(self, other):
        other = Version.from_str(other)

        if self.major > other.major:
            return True
        elif self.major < other.major:
            return False

        if self.minor > other.minor:
            return True
        elif self.minor < other.minor:
            return False

        return self.revision > other.revision

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)
