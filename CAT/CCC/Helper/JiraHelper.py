from CCC.Helper.RestHelper import Rest

class Jira(Rest):

    def __init__(self, user):
        super().__init__(user)

    def observer(self):
        pass