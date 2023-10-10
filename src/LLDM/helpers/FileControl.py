def read(path):
    file = open(path, "r")
    content = file.read()
    file.close()
    return content


def write(path, content):
    file = open(path, "w")
    file.write(content)
    file.close()


def append(path, content):
    file = open(path, "a")
    file.write("\n" + content)
    file.close()
