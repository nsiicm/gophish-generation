class User:
    def __init__(self, nom, prenom, email, id, status):
        self.nom=nom
        self.prenom=prenom
        self.email=email
        self.id=id
        self.status=status
    
    def __repr__(self):
        return "User id : " + self.id + " , User Email : " + self.email