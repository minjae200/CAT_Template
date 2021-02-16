
def is_valid_module(data):
    if data['name'] == '' or data['tag'] == '' or data['hash_value'] == '':
        return False
    return True

def is_exist_module(job, data):
    queryset = job.module_set.all()
    exist = False
    for query in queryset:
        if data['name'] == query.name:
            exist = True
    return exist
