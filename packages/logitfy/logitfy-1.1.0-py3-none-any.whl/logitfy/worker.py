"""Worker for processing logging requests"""

import traceback
from threading import Thread

from typing import List, Callable
from datetime import datetime

from gitaudit.github.instance import Github


from gitaudit.analysis.changelog.changelog import GithubChangeLog
from gitaudit.branch.serialization import log_to_json
from gitaudit.render.change_log import render_change_log_to_text

from .model import State, LoggingRequest


COMMIT_QUERY_DATA = "oid committedDate"


class LoggingRequestError(Exception):
    """Exception for logging requests"""""


class Worker:
    """Worker for processing logging requests"""

    def __init__(
        self,
        tmp_git_checkout_location: str,
        tmp_github_cache_location: str,
        json_upload_callback: Callable[[str], str],
        html_upload_callback: Callable[[str], str],
        commit_url_provider: Callable[[str, str, str], str],
        issues_provider: Callable,
        github: Github,
    ) -> None:
        self.tmp_git_checkout_location = tmp_git_checkout_location
        self.tmp_github_cache_location = tmp_github_cache_location
        self.json_upload_callback = json_upload_callback
        self.html_upload_callback = html_upload_callback
        self.commit_url_provider = commit_url_provider
        self.issues_provider = issues_provider
        self.github = github

        self.queue_requests: List[LoggingRequest] = []
        self.done_requests: List[LoggingRequest] = []
        self.current_request: LoggingRequest = None

        self.queue_worker = None


    @property
    def requests(self) -> List[LoggingRequest]:
        """Returns all requests"""
        arr = []
        arr.extend(self.done_requests)
        if self.current_request:
            arr.append(self.current_request)

        arr.extend(self.queue_requests)

        return arr
    
    def _get_commit(self, owner, repo, ref):
        if '@' in ref:
            branch_name, datetime_text = ref.split('@')
            date_time = datetime.fromisoformat(datetime_text)
            return self.github.get_first_commit_before_date(
                owner=owner,
                repo=repo,
                ref=branch_name,
                commit_date_time=date_time,
                querydata=COMMIT_QUERY_DATA,
            )

        return self.github.get_commit_for_expression(
            owner=owner,
            repo=repo,
            expression=ref,
            querydata=COMMIT_QUERY_DATA,
        )


    def _validate_current_request(self):
        owner, repo = self.current_request.root_repository.split('/')

        try:
            start_commit = self._get_commit(owner, repo, self.current_request.start_ref)
        except Exception as esc:
            raise LoggingRequestError((
                f'Start expression "{self.current_request.start_ref}" does not exist in '
                f'repository "{self.current_request.root_repository}"'
            )) from esc

        try:
            end_commit = self._get_commit(owner, repo, self.current_request.end_ref)
        except Exception as esc:
            raise LoggingRequestError((
                f'End expression "{self.current_request.end_ref}" does not exist in '
                f'repository "{self.current_request.root_repository}"'
            )) from esc

        if start_commit.committed_date > end_commit.committed_date:
            raise LoggingRequestError((
                f'Start expression "{self.current_request.start_ref}" is newer than '
                f'end expression "{self.current_request.end_ref}" in '
                f'repository "{self.current_request.root_repository}"'
            ))

        return start_commit.oid, end_commit.oid

    def _execute_current_request(self, start_oid, end_oid):
        gitub_changelog = GithubChangeLog(
            self.github,
            self.tmp_git_checkout_location,
            self.tmp_github_cache_location,
        )

        owner, repo = self.current_request.root_repository.split('/')

        changelog = gitub_changelog.get_change_log(
            owner=owner,
            repo=repo,
            start_ref=start_oid,
            end_ref=end_oid,
            pr_querydata=(
                "title id number url mergeCommit { oid } "
                "repository { nameWithOwner owner { login } name }"
            ),
            no_patch_if_no_submodules=True,
            follow_submodules=True,
            specify_submodules=self.current_request.submodule_names,
            commit_url_provider=self.commit_url_provider,
            issues_provider=self.issues_provider,
            no_submodule_entries_on_first_commit=True,
            assert_start_ref_in_first_parent_log=True,
        )

        # Use Callback to upload changelog
        if self.json_upload_callback:
            changelog_json = log_to_json(changelog)
            self.current_request.json_uri = self.json_upload_callback(
                self.current_request,
                changelog_json,
            )

        if self.html_upload_callback:
            changelog_html = render_change_log_to_text(
                changelog,
                root_repo_name=self.current_request.root_repository,
            )
            self.current_request.html_uri = self.html_upload_callback(
                self.current_request,
                changelog_html,
            )

    def _run_queue(self):
        while self.queue_requests:
            self.current_request = self.queue_requests.pop(0)

            try:
                self.current_request.state = State.Running

                start_oid, end_oid = self._validate_current_request()
                self._execute_current_request(start_oid, end_oid)

                self.current_request.state = State.Finished
            except Exception as e:
                self.current_request.state = State.Error
                self.current_request.error_message = str(e)
                self.current_request.stack_trace = traceback.format_exc()
            finally:
                self.done_requests.append(self.current_request)
                self.current_request = None

        self.queue_worker = None


    def append_request(self, request: LoggingRequest):
        """Appends a new request to the queue

        Args:
            request (LoggingRequest): The request to append
        """
        self.queue_requests.append(request)

        if not self.queue_worker:
            self.queue_worker = Thread(target=self._run_queue)
            self.queue_worker.start()
