from CCC.Helper.RestHelper import Rest

class Gerrit(Rest):

    def __init__(self, user):
        super().__init__(user)

    def start_CCC(self):
        self.git_clone_meta_lg_webos()
        self.checkout_branch()
        self.modify_bb_file()
        self.git_push()
        self.set_build_message()
        self.press_tas_button()
        self.press_make_ticket()

    def git_clone_meta_lg_webos(self):
        # git clone meta-lg-webos repository
        pass

    def checkout_branch(self):
        # git checkout @branch
        pass

    def find_bb_file(self):
        # find ./ -name module.bb -> find ./ -name module.inc
        pass

    def modify_bb_file(self):
        self.find_bb_file()
        # file open 
        # write append
        # close file
        pass

    def git_push(self):
        # git push origin HEAD:refs/for/@branch
        pass

    def set_build_message(self):
        # using REST api
        pass

    def press_tas_button(self):
        # using REST api
        pass

    def press_make_ticket(self):
        # using REST api
        pass
