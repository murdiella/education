class MegaDirection:
    def __init__(
        self,
        *,
        ref: str,
        name: str,
        number: str,
        contacts: str,
        active: bool,
    ):
        self.ref = ref
        self.name = name
        self.number = number
        self.contacts = contacts
        self.active = active

    def __repr__(self):
        return f"MegaDirection(ref={self.ref!r}, name={self.name!r}, number={self.number!r}, contacts={self.contacts!r}, active={self.active!r})"
