#!/Users/pete/Projects/tool-library/gmail-tool/venv/bin/python
"""
Compatibility shim to make gmail_advanced work with the new requests-based implementation
"""

class ServiceWrapper:
    """Wraps AuthorizedSession to provide googleapiclient-like interface"""
    
    def __init__(self, session, base_url):
        self.session = session
        self.base_url = base_url
        
    def users(self):
        return UsersResource(self.session, self.base_url)


class UsersResource:
    def __init__(self, session, base_url):
        self.session = session
        self.base_url = base_url
        
    def messages(self):
        return MessagesResource(self.session, self.base_url)
        
    def labels(self):
        return LabelsResource(self.session, self.base_url)
        
    def settings(self):
        return SettingsResource(self.session, self.base_url)


class MessagesResource:
    def __init__(self, session, base_url):
        self.session = session
        self.base_url = base_url
        
    def list(self, userId='me', **params):
        return Request(self.session.get, f'{self.base_url}/users/{userId}/messages', params=params)
        
    def get(self, userId='me', id=None, **params):
        return Request(self.session.get, f'{self.base_url}/users/{userId}/messages/{id}', params=params)
        
    def modify(self, userId='me', id=None, body=None):
        return Request(self.session.post, f'{self.base_url}/users/{userId}/messages/{id}/modify', json=body)
        
    def trash(self, userId='me', id=None):
        return Request(self.session.post, f'{self.base_url}/users/{userId}/messages/{id}/trash')
        
    def delete(self, userId='me', id=None):
        return Request(self.session.delete, f'{self.base_url}/users/{userId}/messages/{id}')
        
    def batchDelete(self, userId='me', body=None):
        return Request(self.session.post, f'{self.base_url}/users/{userId}/messages/batchDelete', json=body)


class LabelsResource:
    def __init__(self, session, base_url):
        self.session = session
        self.base_url = base_url
        
    def list(self, userId='me'):
        return Request(self.session.get, f'{self.base_url}/users/{userId}/labels')
        
    def create(self, userId='me', body=None):
        return Request(self.session.post, f'{self.base_url}/users/{userId}/labels', json=body)


class SettingsResource:
    def __init__(self, session, base_url):
        self.session = session
        self.base_url = base_url
        
    def filters(self):
        return FiltersResource(self.session, self.base_url)


class FiltersResource:
    def __init__(self, session, base_url):
        self.session = session
        self.base_url = base_url
        
    def list(self, userId='me'):
        return Request(self.session.get, f'{self.base_url}/users/{userId}/settings/filters')
        
    def create(self, userId='me', body=None):
        return Request(self.session.post, f'{self.base_url}/users/{userId}/settings/filters', json=body)


class Request:
    """Mimics googleapiclient request interface"""
    def __init__(self, method, url, **kwargs):
        self.method = method
        self.url = url
        self.kwargs = kwargs
        
    def execute(self):
        response = self.method(self.url, timeout=30, **self.kwargs)
        if response.status_code == 204:
            return None
        elif response.status_code == 200:
            return response.json()
        else:
            # Mimic HttpError
            error = HttpError(response, response.content)
            raise error


class HttpError(Exception):
    """Compatibility for googleapiclient.errors.HttpError"""
    def __init__(self, resp, content):
        self.resp = resp
        self.content = content
        super().__init__(f"HttpError {resp.status_code}: {content}")