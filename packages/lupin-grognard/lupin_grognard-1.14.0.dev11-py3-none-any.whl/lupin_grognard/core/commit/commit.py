import re
from datetime import datetime
from typing import Dict, List, Tuple, Union

from lupin_grognard.core.config import (
    INITIAL_COMMIT,
    MAJOR_COMMIT_TYPES,
    PATTERN,
)
from lupin_grognard.core.git import Git


class Commit:
    def __init__(self, commit: str):
        self.commit = commit
        self.associated_closed_issue = None
        self.associated_mr_approvers = None
        self.associated_mr_approvers_date = None
        self.parents = None
        self.associated_mr_commits_authors = []

    @classmethod
    def add_additional_commit_info(cls, commits: List["Commit"]) -> List["Commit"]:
        """
        Returns a list of Commit objects with additional information such as closed issues, approvers,
        and date it was approved for each commit from associated merge request

        :param commits: List of Commit objects
        :return: List of Commit objects with additional information

        additional information:
            self.associated_closed_issue = None if merge commit else "1"
            self.associated_mr_approvers = None if merge commit else "John Doe"
            self.associated_mr_approvers_date = None if merge commit else "10/03/23 06:48 PM"
            self.parrents = ["hash1", "hash2"] if merge commit else ["hash1"]
        """
        commits = get_parents_for_commits(commits=commits)
        merge_commits_hash, merge_commits_mapping = cls._get_data_from_merge_commit(
            commits=commits
        )
        commits = cls._add_associated_data_to_commit_from_merge(
            merge_commits_hash=merge_commits_hash,
            merge_commits_mapping=merge_commits_mapping,
            commits=commits,
        )
        return commits

    @classmethod
    def _get_data_from_merge_commit(
        cls, commits: List["Commit"]
    ) -> Tuple[List[str], Dict[str, Dict[str, Union[str, List[str], str]]]]:
        """
        Return a tuple containing a dictionary with information about merge commits and a list of merge commit hashes.

        The merge commit information dictionary has commit parent hash as keys, and the following information as values:
            - "closed_issue": L'id of the gitlab closed issue.
            - "approvers": A list of the usernames who approved the merge commit.
            - "date": The date the merge commit was approved.

        :param commits: A list of Commit objects.
        :type commits: List["Commit"]
        :return:
            - merge_commits_hash, merge_commits_mapping
            - A tuple containing the list of merge commit hashes and a merge commit information dictionary.
        :rtype: Tuple[List[str], Dict[str, Dict[str, Union[str, List[str], str]]]]
        """
        merge_commits_hash = []
        merge_commits_mapping = {}
        for commit in commits:
            if len(commit.parents) == 2:  # check if it is a merge commit
                merge_commits_hash.append(commit.hash)
                if commit.closes_issues:
                    merge_commits_mapping[commit.parents[1]] = {
                        "close_issue": commit.closes_issues[0],
                        "approvers": commit.approvers,
                        "date": commit.author_date,
                    }
        return merge_commits_hash, merge_commits_mapping

    @classmethod
    def _add_associated_data_to_commit_from_merge(
        cls,
        merge_commits_hash: List[str],
        merge_commits_mapping: Dict[str, Dict[str, Union[str, List[str], str]]],
        commits: List["Commit"],
    ) -> List["Commit"]:
        for commit in commits:
            if (
                len(commit.parents) == 1  # check if it is not a merge commit
                and commit.hash in merge_commits_mapping
                and commit.title not in INITIAL_COMMIT
            ):
                commit.associated_closed_issue = merge_commits_mapping[commit.hash][
                    "close_issue"
                ]
                commit.associated_mr_approvers = merge_commits_mapping[commit.hash][
                    "approvers"
                ]
                commit.associated_mr_approvers_date = merge_commits_mapping[
                    commit.hash
                ]["date"]
                if (
                    commit.parents[0] not in merge_commits_mapping
                    and commit.parents[0] not in merge_commits_hash
                ):  # the commit parent shares the same merge commit
                    merge_commits_mapping[commit.parents[0]] = merge_commits_mapping[
                        commit.hash
                    ]
        return commits

    def is_merge_commit(self) -> bool:
        return self.title.startswith("Merge branch")

    @property
    def hash(self) -> str:
        return self._extract(start="hash>>")

    @property
    def author(self) -> str:
        return self._extract(start="author>>")

    @property
    def author_mail(self) -> str:
        return self._extract(start="author_mail>>")

    @property
    def author_date(self) -> str:
        timestamp = self._extract(start="author_date>>")
        date_object = datetime.fromtimestamp(int(timestamp))
        return date_object.strftime("%d/%m/%y %I:%M %p")

    @property
    def title(self) -> str:
        return self._extract(start="title>>")

    @property
    def title_without_type_scope(self) -> str:
        """Returns commit title without type and scope"""
        start = self.title.find(":") + 1
        return self.title[start:].strip().capitalize()

    @property
    def type(self) -> str | None:
        """Returns the conventional commit type if present"""
        match = re.match(PATTERN, self.title)
        return match.groups()[0] if match else None

    @property
    def scope(self) -> str | None:
        """Returns the conventional commit scope if present"""
        match = re.match(PATTERN, self.title)
        return match.groups()[1] if match else None

    @property
    def body(self) -> List[str] | None:
        body = self._extract(start="body>>", end="<<body")
        if body == "":
            return None

        # remove last \n if present cause 'git commit -m "description"' or other git software adds it automatically
        body = body.rstrip("\n")

        return [
            self._remove_markdown_list_markers(message) for message in body.split("\n")
        ]

    @property
    def closes_issues(self) -> List | None:
        """Returns the list of issues closed by the commit"""
        if self.body:
            for line in self.body:
                if line.startswith("Closes #"):  # Closes #465, #190 and #400
                    return re.findall(r"#(\d+)", line)  # ['465', '190', '400']
        return None

    @property
    def approvers(self) -> List[str]:
        approvers = []
        if self.body:
            for line in self.body:
                if line.startswith("Approved-by: "):
                    approver = line.split("Approved-by: ")[1]
                    approver = approver.translate(str.maketrans("", "", "<>"))
                    approvers.append(approver)
            return approvers
        return list()

    @property
    def approvers_name(self) -> List[str]:
        if self.approvers:
            return [" ".join(approver.split(" ")[:-1]) for approver in self.approvers]
        return list()

    @property
    def approvers_mail(self) -> List[str]:
        if self.approvers:
            return [approver.split(" ")[-1] for approver in self.approvers]
        return list()

    def _extract(self, start: str, end: str = "\n") -> str:
        start_index = self.commit.find(start) + len(start)
        return self.commit[start_index : self.commit.find(end, start_index)]

    def is_major_commit(self) -> bool:
        """Returns if the commit is a major commit type"""
        return self.type in MAJOR_COMMIT_TYPES

    def is_not_initial_commit(self) -> bool:
        """Returns if the commit is not an initial commit"""
        return self.title not in INITIAL_COMMIT

    def _remove_markdown_list_markers(self, message: str) -> str:
        return message.lstrip("-* ")


def fill_authors_for_mr_commits(commits: List["Commit"]) -> List["Commit"]:
    """
    For each merge commit in the list, fill the authors of its children commits
    (that are associated to the merge request).

    Args:
        commits (List[Commit]): The list of commits to check.

    Returns:
        List[Commit]: The modified list of commits with the authors added to each merge commit.
    """

    commits = get_parents_for_commits(commits=commits)

    for commit in commits:
        if commit.is_merge_commit():
            add_author_to_merge_request(
                merge_request=commit, hash=commit.parents[1], commits=commits
            )
    return commits


def find_commit_by_hash(hash: str, commits: List["Commit"]) -> Commit:
    """Find a commit in a list of commits by its hash.

    Args:
        hash (str): The hash of the commit to retrieve.
        commits (List[Commit]): The list of commits to search in.

    Returns:
        Commit: The commit with the given hash.
    """
    for commit in commits:
        if commit.hash == hash:
            return commit


def add_author_to_merge_request(
    merge_request: Commit, hash: str, commits: List["Commit"]
) -> None:
    """
    Recursively adds the author of a child commit to the associated merge request.

    Args:
        merge_request (Commit): The merge request to add the author.
        hash (str): The hash of the child commit.
        commits (List[Commit]): The list of commits.

    Returns:
        None
    """
    child_commit = find_commit_by_hash(hash=hash, commits=commits)
    if not child_commit.is_merge_commit() and child_commit.is_not_initial_commit():
        merge_request.associated_mr_commits_authors.append(child_commit.author_mail)

        if len(child_commit.parents) == 1:
            add_author_to_merge_request(
                merge_request=merge_request,
                hash=child_commit.parents[0],
                commits=commits,
            )


def get_parents_for_commits(commits: List["Commit"]) -> List["Commit"]:
    """Get the parents for each commit in the list.

    Args:
        commits (List[Commit]): The list of commits.

    Returns:
        List[Commit]: The list of commits with the parents added.
    """
    for commit in commits:
        commit.parents = Git().get_parents(commit_hash=commit.hash)
    return commits
