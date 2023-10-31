from .autoauth import AutoAuth
from .github import GithubAuth
from .google import GoogleAuth
from .user import AutoUser

current_user = None
auth_required = AutoAuth.auth_required
