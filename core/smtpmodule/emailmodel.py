
class myEmail(object):
    def __init__(self, email):
        self.email = email

    def send(self):
        # Send email
        pass

    def __str__(self):
        return self.email

    def __repr__(self):
        return self.email

    def __eq__(self, other):
        return self.email == other.email

    def __ne__(self, other):
        return self.email != other.email

    def __hash__(self):
        return hash(self.email)

    def __len__(self):
        return len(self.email)

    def __getitem__(self, key):
        return self.email[key]

    def __setitem__(self, key, value):
        self.email[key] = value

    def __delitem__(self, key):
        del self.email[key]

    def __contains__(self, item):
        return item in self.email

    def __iter__(self):
        return iter(self.email)

    def __reversed__(self):
        return reversed(self.email)

    def __add__(self, other):
        return self.email + other.email

    def __radd__(self, other):
        return other.email + self.email

    def __mul__(self, other):
        return self.email * other

    def __rmul__(self, other):
        return other * self.email

    def __iadd__(self, other):
        self.email += other.email
        return self

    def __imul__(self, other):
        self.email *= other
        return self

    def __lt__(self, other):
        return self.email < other.email

    def __le__(self, other):
        return self.email <= other.email

    def __gt__(self, other):
        return self.email > other.email

    def __ge__(self, other):
        return self.email >= other.email

    def __getattr__(self, name):
        return getattr(self.email, name)

    def __setattr__(self, name, value):
        setattr(self.email, name, value)

    def __delattr__(self, name):
        delattr(self.email, name)

    def __call__(self, *args, **kwargs):
        return self.email(*args, **kwargs)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __next__(self):
        return