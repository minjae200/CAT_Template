import os, sys, json, git
import subprocess
from CCC.Helper.RestHelper import Rest
#from RestHelper import Rest

class Gerrit(Rest):

    ROOT_DIR = 'Repositories/'
    GIT_PATH_CMD = 'git rev-parse --git-dir'
    REPO_URL = 'ssh://{username}@wall.lge.com:29448/webos-pro/meta-lg-webos'
    GIT_HOOK_CURL = 'curl -o {git_path}/hooks/commit-msg https://wall.lge.com/static/commit-msg;'
    GIT_HOOK_CHMOD = 'chmod +x {git_path}/hooks/commit-msg'
    FIND_BB_FILE = 'find ./ -name {module}.bb'
    FIND_INC_FILE = 'find ./ -name {module}.inc'
    GIT_CONFIG_USER_NAME = 'git config user.name "{username}"'
    GIT_CONFIG_USER_EMAIL = 'git config user.email "{useremail}"'
    GIT_RESET_AUTHOR = 'git commit --amend --reset-author --no-edit'
    CHANGE_ENDPOINT = 'https://wall.lge.com/a/changes/'
    GERRIT_ENDPOINT = CHANGE_ENDPOINT + 'webos-pro%2Fmeta-lg-webos~'


    def __init__(self, user):
        super().__init__(user)
        self.user = user
        self.job = None
        self.working_directory = self.ROOT_DIR
        self.gerrit_id = None
        self.repo_url = self.REPO_URL.format(username=user['username'])

    def start_CCC(self, job):
        self.job = job
        self.working_directory = self.ROOT_DIR + '{id}_meta-lg-webos'.format(id=job.id)
        self._git_clone_meta_lg_webos()
        self._modify_bb_file()
        self._git_push()
        self._set_ccc_options()

    def _git_clone_meta_lg_webos(self):
        if os.path.exists(self.working_directory):
            os.system('rm -rf {}'.format(self.working_directory))
        try:
            print('try git clone (job.id = {})'.format(self.job.id))
            self.repo = git.Repo.clone_from(self.repo_url, self.working_directory, progress=None)
            git_path = subprocess.check_output('cd {} &&'.format(self.working_directory) + self.GIT_PATH_CMD, stderr=subprocess.STDOUT, shell=True).decode('utf-8').replace('\n', '')
            git_hook_curl = self.GIT_HOOK_CURL.format(git_path=git_path)
            git_hook_chmod = self.GIT_HOOK_CHMOD.format(git_path=git_path)
            os.system('cd {} && '.format(self.working_directory) + git_hook_curl)
            os.system('cd {} && '.format(self.working_directory) + git_hook_chmod)
            self.git = self.repo.git
            self.git.checkout(str(self.job.branch))
            self.git.pull("--rebase")
            print('git clone and checkout success')
        except Exception as Error:
            print('Error : {}'.format(Error))

    def _find_bb_file(self, module):
        move_dir = 'cd {} && '.format(self.working_directory)
        location = subprocess.check_output(move_dir + self.FIND_BB_FILE.format(module=module), shell=True, stderr=subprocess.STDOUT, encoding='utf-8')
        if not location:
            location = subprocess.check_output(move_dir + self.FIND_INC_FILE.format(module=module), shell=True, stderr=subprocess.STDOUT, encoding='utf-8')
        return self.working_directory + '/' + location.split('\n')[0] if location else None

    def _modify_bb_file(self):
        modules = self.job.module_set.all()
        for module in modules:
            location = self._find_bb_file(module.name)
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

    def _git_push(self, directory = None, branch = None):
        if self.git is None:
            return
        move_dir = 'cd {} && '.format(self.working_directory)
        try:
            print(self.git.status())
            os.system(move_dir + self.GIT_CONFIG_USER_NAME.format(username=self.user['username']))
            os.system(move_dir + self.GIT_CONFIG_USER_EMAIL.format(useremail='{}@lge.com'.format(self.user['username'])))
            self.git.add('*')
            self.git.commit(m='CCC Auto Create')
            self.git.push('origin', 'HEAD:refs/for/{}'.format(self.job.branch))
            self.change_id = self._get_change_id()
            self.gerrit_id = self._get_gerrit_id(change_id=self.change_id)

        except Exception as error:
            print(error)

    def _get_change_id(self):
        move_dir = 'cd {} && '.format(self.working_directory)
        git_log = subprocess.check_output(move_dir + 'git log -1', shell=True).decode('utf-8').split('\n')
        print(git_log)
        change_id = None
        for log in git_log:
            if 'Change-Id' in log:
                print(log)
                change_id = log.split(':')[-1].strip()
        print(change_id)
        return change_id

    def _get_gerrit_id(self, change_id):
        target = self.CHANGE_ENDPOINT + '?q=change:{}'.format(change_id)
        print(target)
        response = self.get(target=target)
        print(response.text)
        
        gerrit_id = json.loads(response.text.replace(')]}\'', ''))[0]['_number']
        print(gerrit_id)
        return gerrit_id 

    def _get_patchset(self, gerrit_id):
        target = self.GERRIT_ENDPOINT + '{gerrit_id}/comments'.format(gerrit_id=gerrit_id)
        response = self.get(target=target)
        response = json.loads(response.text.replace(']]}\'', ''))

        patch_set = None
        if '/COMMIT_MSG' in response:
            patch_set = response['/COMMIT_MSG'][-1]['patch_set']
        return patch_set

    def _set_ccc_options(self):
        patchset = self._get_patchset(self.gerrit_id)
        print(patchset)
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
        response = self.post(target=target, json=json.dumps(data))
        print(response)