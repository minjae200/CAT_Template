from CCC.Helper.RestHelper import Rest

class Gerrit(Rest):

    def __init__(self, user):
        super().__init__(user)
        self.gerrit_id = None

    def start_CCC(self):
        self.git_clone_meta_lg_webos()
        self.modify_bb_file()
        self.git_push()
        self.set_build_message()
        self.press_tas_make_ticket()

    def git_clone_meta_lg_webos(self):
        if not os.path.exists('Repo'):
            os.makedirs('Repo')
        # if os.path.exists('Repo/{}_meta-lg-webos'.format(self.job['id'])):
        #     os.system('cd Repo && rm -rf {}_meta-lg-webos'.format(self.job['id']))
        try:
            # git_url = "ssh://{}@wall.lge.com:29448/webos-pro/meta-lg-webos".format(self.user['name'])
            git_hook = "gitdir=$(git rev-parse --git-dir); curl -o ${gitdir}/hooks/commit-msg https://wall.lge.com/static/commit-msg ; chmod +x ${gitdir}/hooks/commit-msg"
            # repo = git.Repo.clone_from(git_url, 'Repo/{}_meta-lg-webos'.format(self.job['id']), progress=None)
            # git_ = repo.git
            # hook_result = subprocess.check_output('cd Repo/{}_meta-lg-webos && {}'.format(self.job['id'], git_hook), shell=True, stderr=subprocess.STDOUT)
            os.system('cd Repo/{}_meta-lg-webos && {}'.format(self.job['id'], git_hook))
            # os.chdir('Repo/{}_meta-lg-webos'.format(self.job['id']))
            # print(os.getcwd())
            # os.system('cd Repo && cd {}_meta-lg-webos && {}'.format(self.job['id'], git_hook))
            # git_.checkout("{}".format(self.job['branch']))
            # git_.pull("--rebase")
            print('git clone and checkout success')
        except Exception as Error:
            print('Error : {}'.format(Error))

    def find_bb_file(self, module):
        location = subprocess.check_output('find ./ -name {}.bb'.format(module), shell=True, stderr=subprocess.STDOUT, encoding='utf-8')
        if not location:
            location = subprocess.check_output('find ./ -name {}.inc'.format(module), shell=True, stderr=subprocess.STDOUT, encoding='utf-8')
        return location.split('\n')[0]

    def modify_bb_file(self):
        modules = self.job['modules']
        for module, value in modules.items():
            location = self.find_bb_file(module)
            with open(location, 'r') as file:
                lines = file.readlines() 
            tag = value['tag'].split('submissions/')[-1]
            hash_value = value['hash']
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

    def git_push(self):
        os.chdir('Repo/{}_meta-lg-webos'.format(self.job['id']))
        os.system('git add *')
        os.system('git commit -m "CCC Automation"')
        os.system('git push origin HEAD:refs/for/{}'.format(job['branch']))
        # self.gerrit_id = ....

    def get_patchset(self):
        target= "https://wall.lge.com/a/changes/webos-pro%2Fmeta-lg-webos~{}/comments".format(self.gerrit_id)
        data = self.get(target=target, headers=self.headers, auth=self.auth)
        print(data)

    def press_tas_make_ticket(self):
        patchset = self.get_patchset()
        target = 'https://wall.lge.com/a/changes/webos-pro%2Fmeta-lg-webos~{gerrit_id}/revisions/{patchset}/review'.format(gerrit_id=self.gerrit_id, patchset=patchset)
        # using REST api
        # + set_message_and_button
        # gerrit_endpoint = "https://wall.lge.com/changes/webos"
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