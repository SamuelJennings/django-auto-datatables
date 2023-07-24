class X(object):
    val = 1

    x = "some string"


def get_attributes(obj):
    return {k: v for k, v in vars(obj).items() if not k.startswith("__")}


print(get_attributes(X))
