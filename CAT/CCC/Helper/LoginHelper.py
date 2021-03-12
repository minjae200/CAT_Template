from django.contrib.auth.decorators import login_required as django_login_required
from ldap3 import Server, Connection, SAFE_SYNC
from functools import wraps

def authenticate(username, password, server_addr='ldap://lge.net'):
    try:
        server = Server(host=server_addr, port=3268)
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
    authenticate('minjae.choi', 'sgu1064018@')