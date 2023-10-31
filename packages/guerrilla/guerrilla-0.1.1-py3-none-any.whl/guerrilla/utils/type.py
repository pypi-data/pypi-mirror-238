from box import Box


class DefaultBox(Box):
    def __getattr__(self, item):
        if item not in self and "default" in self:
            return self["default"]

        return super().__getattr__(item)
