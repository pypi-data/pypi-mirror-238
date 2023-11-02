from fastapi import Request
from fastapi.responses import HTMLResponse, Response, RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp, Receive, Scope, Send
import typing

from .client import AuthClient
from .etc import RevokedAuth


# TODO: ADD base middleware super, implement for redirect jank
class AuthMiddleware:
    def __init__(
            self,
            app: ASGIApp,
            client: AuthClient,
            available_scopes: typing.Optional[typing.Sequence[str]] = None,
            restricted_paths: typing.Optional[typing.Sequence[str]] = None,

    ) -> None:
        self.app = app
        self.client: AuthClient = client
        self.available_scopes = available_scopes
        self.restricted_paths = restricted_paths
        self.mingle = None  # Check for redis and other clients

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        # skip non-http requests like websockets
        if scope['type'] != 'http':
            await self.app(scope, receive, send)

        else:
            path: str = scope.get('path')
            request = Request(scope=scope)

            # catch authentication sdk endpoints
            if path.startswith('/bsAuth/callback'):
                response: Response
                ref = request.cookies.get('bt_rf')
                pack = self.client.full_fetch(ref)

                self.client.sessions[ref] = {'pending': False, 'revalidated': False, **pack['azp']}
                # language=html
                callback_html = """
                <!DOCTYPE html><html lang="en">
                <head><meta charset="UTF-8"><title>Authorized</title></head>
                <body>Good auth.<script>window.close()</script></body>
                </html>
                """

                response = HTMLResponse(callback_html, status_code=200)

                if self.client.sessions[ref]['user_id']:
                    response.set_cookie(key='user_id', value=self.client.sessions[ref]['user_id'], samesite='none',
                                        secure=True, expires=2147483647)
                else:
                    response.delete_cookie('bt_rf')

                await response(scope, receive, send)

            elif path.startswith('/bsAuth/login'):
                pending = self.client.build_auth()
                self.client.sessions[pending['ref']] = {'pending': True, 'user_id': None}
                resp = Response(content=pending['url'], status_code=200)
                resp.set_cookie('bt_rf', pending['ref'], httponly=True, secure=True, samesite='none',
                                expires=2147483647)
                await resp(scope, receive, send)

            elif path.startswith('/bsAuth/logout'):
                print(request)

                # language=html
                page_html = """
                    <!DOCTYPE html><html lang='en-us'>
                    <head><title>Logged Out</title></head>
                    <body>
                        <div><p>
                            Logout successful. 
                            Redirecting in <span id='countdown'>3</span> seconds. 
                            Click <a href='/'>here</a> to jump immediately.
                        </p></div>
                        
                        <script>
                            const elem = document.getElementById('countdown');
                            const updateOrJump = () => {
                                let curTime = Number(elem.innerText);
                                if (curTime > 0) {
                                    curTime--;
                                    elem.innerText = String(curTime);
                                    setTimeout(updateOrJump, 1000);
                                } else {
                                    window.location = '/';
                                }
                            }
                            window.onload = () => updateOrJump();
                        </script>
                    </body>
                    </html>
                    """

                # script-based redirection response for fallback logout,
                # typically this endpoint will be called via fetch, in which case the logout
                # flow will execute and the above redirect script can be ignored and the
                # response status can instead be used to trigger a callback function.
                response = HTMLResponse(content=page_html, status_code=200)

                # auth server token invalidation when active cookie present
                if ref := request.cookies.get('bt_rf'):
                    self.client.invalidate_ref(ref)
                    # cookie modification attached to the response
                    response.delete_cookie('bt_rf')

                # handle temp and complete failed logouts by clearing user
                if 'user_id' in request.cookies:
                    response.delete_cookie('user_id')

                await response(scope, receive, send)

            else:
                # Remove revoked tokens if present
                try:
                    self.client.user(request)
                    await self.app(scope, receive, send)
                except RevokedAuth:
                    response = RedirectResponse(path)
                    response.delete_cookie('bt_rf')
                    response.delete_cookie('user_id')
                    await response(scope, receive, send)
