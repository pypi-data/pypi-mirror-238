import keyring
# This is the  key ring of the file it which stores the session and the path 
# where to want to want to store the file and data 
class Store:
    def __init__(self):
        self.servicename = "SNALABS"
        self.username = "SNALABS"

    def setkey(self, password):
        keyring.set_password(self.servicename, self.username, password)

    def getkey(self):
        if keyring.get_password(self.servicename, self.username):
            return True

    def getsess(self):
        sess = keyring.get_password(self.servicename, self.username)
        return sess

    def deletekey(self):
        if keyring.get_password(self.servicename, self.username):
            if keyring.delete_password(self.servicename, self.username):
                return True
        return False
