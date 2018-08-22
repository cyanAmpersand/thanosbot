def loadToken(filename):
    f = open(filename,"r")
    token = f.read()
    f.close()
    return token

def getMember(members,id):
    for m in members:
        if m.id == id:
            return m
    return None