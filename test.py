class Y(object):
    y_val = 2


class X(Y):
    val = 1

    x = "some string"

    @property
    def test(self):
        return "test"


def get_attributes(obj):
    return {k: getattr(obj, k) for k in dir(obj) if not k.startswith("__")}


# print(dir(X))
print(get_attributes(X))
