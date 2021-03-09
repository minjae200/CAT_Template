import os, sys, json, git
import subprocess
# from CCC.Helper.RestHelper import Rest
from RestHelper import Rest

class Gerrit(Rest):

    ROOT_DIR = 'Repositories/'
    GIT_PATH_CMD = 'git rev-parse --git-dir'
    REPO_URL = 'ssh://{username}@wall.lge.com:29448/webos-pro/meta-lg-webos'
    GIT_HOOK_CURL = 'curl -o {git_path}/hooks/commit-msg https://wall.lge.com/static/commit-msg'
    GIT_HOOK_CHMOD = 'chmod +x {git_path}/hooks/commit-msg'
    FIND_BB_FILE = 'find ./ -name {module}.bb'
    FIND_INC_FILE = 'find ./ -name {module}.inc'
    GIT_ADD_ALL = 'git add *'
    GIT_COMMIT = 'git commit -m "CCC Automation"'
    GIT_PUSH = 'git push origin HEAD:refs/for/{branch}'
    GIT_CONFIG_USER_NAME = 'git config --global user.name {username}'
    GIT_CONFIG_USER_EMAIL = 'git config --global user.email {useremail}'
    GIT_RESET_AUTHOR = 'git commit --amend --reset-author --no-edit'
    GERRIT_ENDPOINT = 'https://wall.lge.com/a/changes/webos-pro%2Fmeta-lg-webos~'


    def __init__(self, user):
        super().__init__(user)
        self.job = None
        self.working_directory = self.ROOT_DIR
        self.gerrit_id = None
        self.repo_url = self.REPO_URL.format(username=user['username'])

    def start_CCC(self, job):
        self.job = job
        self.working_directory = ROOT_DIR + '{id}_meta-lg-webos'.format(job.id)
        self._git_clone_meta_lg_webos()
        # self._modify_bb_file()
        # self._git_push()
        # self._set_ccc_options()

    def _git_clone_meta_lg_webos(self):
        if os.path.exists(self.working_directory):
            os.system('rm -rf {}'.format(self.working_directory))
        try:
            print('try git clone (job.id = {})'.format(self.job.id))
            repo = git.Repo.clone_from(self.repo_url, self.working_directory, progress=None)
            git_path = subprocess.check_output(self.GIT_PATH_CMD, stderr=subprocess.STDOUT).decode('utf-8').replace('\n', '')
            git_hook_curl = self.GIT_HOOK_CURL.format(git_path=git_path)
            git_hook_chmod = self.GIT_HOOK_CHMOD.format(git_path=git_path)
            os.system('cd {} && '.format(self.working_directory) + git_hook_curl)
            os.system('cd {} && '.format(self.working_directory) + git_hook_chmod)
            self.git = repo.git
            self.git.checkout("{}".format(self.job.branch))
            self.git.pull("--rebase")
            print('git clone and checkout success')
        except Exception as Error:
            print('Error : {}'.format(Error))

    def _find_bb_file(self, module, job):
        move_dir = 'cd {} && '.format(self.working_directory)
        location = subprocess.check_output(move_dir + self.FIND_BB_FILE.format(module=module), shell=True, stderr=subprocess.STDOUT, encoding='utf-8')
        if not location:
            location = subprocess.check_output(move_dir + self.FIND_INC_FILE.format(module=module), shell=True, stderr=subprocess.STDOUT, encoding='utf-8')
        return location.split('\n')[0] if location else None

    def _modify_bb_file(self):
        modules = self.job.modules_set.all()
        for module in modules:
            location = self.find_bb_file(module.name)
            if location is None: continue
            with open(location, 'r') as file:
                lines = file.readlines() 
            tag = module.tag.split('submissions/')[-1]
            hash_value = module.hash_value
            for idx, line in enumerate(lines):
                if "WEBOS_VERSION" in line:
                    revision_tag_hash = line.split('"')
                    revision = revision_tag_hash[1].split('-')[0]
                    revision_tag_hash[1] = '"{}-{}_{}"'.format(revision, tag, hash_value)
                    change = ''.join(revision_tag_hash)
                    lines[idx] = change
                    break
            with open(location, 'w', encoding='utf-8') as file:
                file.writelines(lines)

    def git_push(self, directory = None, branch = None):
        if directory is not None:
            self.working_directory = directory
        move_dir = 'cd {} && '.format(self.working_directory)
        print(self.git.status())
        self.git.add()
        self.git.commit("CCC automation")
        self.git.push('origin', 'HEAD:refs/for/{}'.format(self.job.branch))
        # os.system(move_dir + self.GIT_ADD_ALL)
        # os.system(move_dir + self.GIT_COMMIT)
        # result = subprocess.check_output(self.GIT_PUSH.format(branch=self.job.branch), stderr=subprocess.STDOUT).decode('utf-8')
        # os.system(move_dir + self.GIT_CONFIG_USER_NAME.format(username='minjae.choi'))
        # os.system(move_dir + self.GIT_CONFIG_USER_EMAIL.format(useremail='minjae.choi@lge.com'))
        # os.system(move_dir + self.GIT_RESET_AUTHOR)
        try:
            result = subprocess.check_output(move_dir + self.GIT_PUSH.format(branch=branch), stderr=subprocess.STDOUT, executable='/bin/bash').decode('utf-8')
        except Exception as error:
            print(error)
        print(type(result))
        print(result)
        # self.gerrit_id = ....

    def _get_patchset(self):
        target = self.GERRIT_ENDPOINT + '{gerrit_id}/comments'.format(gerrit_id=self.gerrit_id)
        data = self.get(target=target, headers=self.headers, auth=self.auth)
        print(data)

    def _set_ccc_options(self):
        patchset = self.get_patchset()
        target = self.GERRIT_ENDPOINT + '{gerrit_id}/revisions/{patchset}/review'.format(gerrit_id=self.gerrit_id, patchset=patchset)
        data = {
            'drafts': 'PUBLISH_ALL_REVISIONS',
            'labels': {
                'Build': 0,
                'Code-Review': 0,
                'MakeCCCTicket': 0,
                'Run-Unit-Test': 0,
                'RunStaticAnalysis': 0,
                'Send-Notify': 0,
                'TAS': 0,
                'Verified': 0,
            },
            'message': 'minjae',
            'reviewers': []
        }
        response = self.post(target=target, json=json.dumps(data), auth=self.auth, headers=self.headers)
        print(response)

if __name__ == '__main__':

    gerrit = Gerrit({'username': 'minjae.choi', 'password': 'sgu1064018@'})
    gerrit.git_push(directory='../../Repo/92_meta-lg-webos', branch='@jardine')
