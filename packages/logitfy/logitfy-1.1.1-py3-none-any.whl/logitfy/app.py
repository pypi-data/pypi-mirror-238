
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from typing import List, Callable

import os

from gitaudit.github.instance import Github
from gitaudit.git.change_log_entry import Issue

from .model import LoggingRequest
from .worker import Worker


JsonUploadCallback = Callable[[LoggingRequest, str], str]
HtmlUploadCallback = Callable[[LoggingRequest, str], str]
CommitUrlProvider = Callable[[str, str, str], str]
IssuesProvider = Callable[[str, str], List[Issue]]


ROOT_PATH = os.path.dirname(__file__)
print(ROOT_PATH)

class App:
    def __init__(
            self,
            tmp_git_checkout_location: str,
            tmp_github_cache_location: str,
            json_upload_callback: JsonUploadCallback,
            html_upload_callback: HtmlUploadCallback,
            commit_url_provider: CommitUrlProvider,
            issues_provider: IssuesProvider,
            github: Github,
        ) -> None:
        self.app = FastAPI()

        # self.app.root_path = os.path.join(ROOT_PATH, "logitfy-app", "dist")
        # self.templates = Jinja2Templates(directory=self.app.root_path)

        origins = [
            "*",
        ]

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        self.worker = Worker(
            tmp_git_checkout_location=tmp_git_checkout_location,
            tmp_github_cache_location=tmp_github_cache_location,
            json_upload_callback=json_upload_callback,
            html_upload_callback=html_upload_callback,
            commit_url_provider=commit_url_provider,
            issues_provider=issues_provider,
            github=github,
        )

        # self.app.get("/")(self.serve_react_app)

        self.app.get('/loggingRequests')(self.get_logging_requests)
        self.app.get('/repoSubmodules/{owner}/{repo}')(self.get_repo_submodules)
        self.app.post('/addNewRequest')(self.add_new_request)

        # self.app.mount("/", StaticFiles(directory=self.app.root_path), name="ui")

    def get_logging_requests(self) -> List[LoggingRequest]:
        """Returns all requests"""
        return self.worker.requests   

    def get_repo_submodules(self, owner: str, repo: str) -> List[str]:
        """Returns all submodules for a repository"""
        default_branch_ref = self.worker.github.get_repository(owner, repo, 'defaultBranchRef {name }').default_branch_ref.name
        submodules = self.worker.github.get_submodules(owner, repo, default_branch_ref, 'gitUrl name')
        submodule_names = list(map(lambda x: x.name, submodules))
        return submodule_names

    def add_new_request(self, request: LoggingRequest):
        """Adds a new request to the queue"""
        self.worker.append_request(request)

    # def serve_react_app(self, request: Request):
    #     return self.templates.TemplateResponse("index.html", {"request": request})
