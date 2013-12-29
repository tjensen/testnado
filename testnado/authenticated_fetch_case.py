from testnado.credentials.helpers import build_fetch_arguments
from testnado.fetch_case import FetchCase


class AuthenticatedFetchCase(FetchCase):

    def get_credentials(self):
        raise NotImplementedError(
            "Method 'get_credentials' must be implemented in order to "
            "use 'authenticated_fetch'.")

    def authenticated_fetch(
            self, url, method=None, headers=None, body=None,
            auth_username=None, auth_password=None, auth_mode=None, **kwargs):

        headers = headers or {}

        # fetch arguments is the explicit list of overwritable arguments
        # for fetch() calls. For instance, 'method' isn't overwritable,
        # because that would be very bizarre if you could change the method
        # of a test fetch() call just based on the credentials...

        # TODO: change URL to query for query arguments instead...

        fetch_arguments = build_fetch_arguments(
            url=url, headers=headers, body=body, auth_mode=auth_mode,
            auth_username=auth_username, auth_password=auth_password)

        update_credentials = self.get_credentials()
        update_credentials(fetch_arguments)

        arguments = {
            "url": fetch_arguments.url,
        }

        if method:
            arguments["method"] = method

        if fetch_arguments.body:
            arguments["body"] = fetch_arguments.body
        if fetch_arguments.headers:
            arguments["headers"] = fetch_arguments.headers
        if fetch_arguments.auth_mode:
            arguments["auth_mode"] = fetch_arguments.auth_mode
        if fetch_arguments.auth_password:
            arguments["auth_password"] = fetch_arguments.auth_password
        if fetch_arguments.auth_username:
            arguments["auth_username"] = fetch_arguments.auth_username

        arguments.update(kwargs)
        self.fetch(**arguments)