from CCC.Helper.RestHelper import Rest

class Gerrit(Rest):

    def __init__(self, username, password):
        super().__init__(username, password)

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
