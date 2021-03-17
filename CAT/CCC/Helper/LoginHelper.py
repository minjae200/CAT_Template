from django.contrib.auth.decorators import login_required as django_login_required
from ldap3 import Server, Connection, SAFE_SYNC
from functools import wraps

def authenticate(username, password, server_addr='ldap://165.186.39.123'):
    try:
        # ldap://lge.net port 3268 -> ldap://165.186.39.123
        server = Server(host=server_addr)
        dn = 'ou=LGE Users,dc=lge,dc=net'
        connection = Connection(server, username + '@lge.net', password, client_strategy=SAFE_SYNC, auto_bind=True)
        ldap_result = connection.search(search_base=dn, search_filter='(cn={})'.format(username), attributes=['name', 'department', 'mail'])
        data = ldap_result[2][0]['attributes']
        user_info = {
            'mail': data['mail'],
            'name': data['name'],
            'department': data['department']
        }
        return user_info
    except Exception as error:
        print('Error: {}'.format(error))
        return dict()

def login_required(view_func):
    @wraps(view_func)
    def decorator(*args, **kwargs):
        if args:
            request = args[0]
            sessionId = request.session.session_key
            userId = request.session.get('username')
            if sessionId != None and userId != None:
                return view_func(*args, **kwargs)
            else:
                return django_login_required(view_func)(*args, **kwargs)
    return decorator

if __name__ == '__main__':
    import time
    start_time = time.time()
    print(authenticate('minjae.choi', 'sgu1064018@'))

    print(time.time() - start_time)