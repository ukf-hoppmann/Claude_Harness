"""cloud_sync.sync_branch against a local bare repository as origin (no network)."""

import os
import subprocess
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

import helpers  # noqa: F401  (adds plugin/scripts to sys.path)
from cloud_sync import sync_branch

GIT_ENV = {
    "GIT_AUTHOR_NAME": "Test",
    "GIT_AUTHOR_EMAIL": "test@example.invalid",
    "GIT_COMMITTER_NAME": "Test",
    "GIT_COMMITTER_EMAIL": "test@example.invalid",
    "GIT_CONFIG_GLOBAL": os.devnull,
    "GIT_CONFIG_NOSYSTEM": "1",
}


def git(cwd, *args):
    result = subprocess.run(
        ["git", "-c", "init.defaultBranch=main", *args],
        cwd=cwd, check=True, capture_output=True, text=True, env={**os.environ, **GIT_ENV},
    )
    return result.stdout.strip()


def commit(repo, name, text=None):
    (repo / name).write_text(text if text is not None else name)
    git(repo, "add", name)
    git(repo, "commit", "-q", "-m", name)
    return git(repo, "rev-parse", "HEAD")


class SyncBranchTest(unittest.TestCase):
    def setUp(self):
        self._env = mock.patch.dict(os.environ, GIT_ENV)
        self._env.start()
        self._tmp = tempfile.TemporaryDirectory()
        base = Path(self._tmp.name)
        self.origin = base / "origin.git"
        self.upstream = base / "upstream"
        self.clone = base / "clone"
        git(base, "init", "-q", "--bare", str(self.origin))
        git(base, "init", "-q", str(self.upstream))
        commit(self.upstream, "a")
        git(self.upstream, "remote", "add", "origin", str(self.origin))
        git(self.upstream, "push", "-q", "origin", "main")
        git(base, "clone", "-q", str(self.origin), str(self.clone))

    def tearDown(self):
        self._tmp.cleanup()
        self._env.stop()

    def push_upstream(self, *names):
        for name in names:
            commit(self.upstream, name)
        git(self.upstream, "push", "-q", "origin", "main")
        return git(self.upstream, "rev-parse", "HEAD")

    def head(self):
        return git(self.clone, "rev-parse", "HEAD")

    def test_same_state_is_silent(self):
        self.assertIsNone(sync_branch(self.clone))

    def test_fast_forward_when_clean(self):
        old = self.head()
        new = self.push_upstream("b", "c")
        message = sync_branch(self.clone)
        self.assertEqual(self.head(), new)
        self.assertIn("fast-forwarded main", message)
        self.assertIn(old[:7], message)
        self.assertIn(new[:7], message)
        self.assertIn("2 new commit(s)", message)

    def test_untracked_files_do_not_block(self):
        (self.clone / "scratch.txt").write_text("x")
        new = self.push_upstream("b")
        self.assertIn("fast-forwarded", sync_branch(self.clone))
        self.assertEqual(self.head(), new)

    def test_dirty_tree_is_reported_not_changed(self):
        old = self.head()
        self.push_upstream("b")
        (self.clone / "a").write_text("changed")
        message = sync_branch(self.clone)
        self.assertEqual(self.head(), old)
        self.assertEqual((self.clone / "a").read_text(), "changed")
        self.assertIn("1 commit(s) behind origin/main", message)
        self.assertIn("git merge --ff-only origin/main", message)

    def test_local_commits_only_is_silent(self):
        local = commit(self.clone, "local")
        self.assertIsNone(sync_branch(self.clone))
        self.assertEqual(self.head(), local)

    def test_diverged_is_reported_not_changed(self):
        local = commit(self.clone, "local")
        self.push_upstream("b", "c")
        message = sync_branch(self.clone)
        self.assertEqual(self.head(), local)
        self.assertIn("diverged", message)
        self.assertIn("1 local", message)
        self.assertIn("2 remote", message)
        self.assertIn("git rebase origin/main", message)
        self.assertIn("only if the user asks", message)

    def test_shallow_clone_without_common_history(self):
        for name in ("b", "c", "d"):
            commit(self.upstream, name)
        git(self.upstream, "push", "-q", "origin", "main")
        shallow = Path(self._tmp.name) / "shallow"
        git(Path(self._tmp.name), "clone", "-q", "--depth", "1", self.origin.as_uri(), str(shallow))
        old = git(shallow, "rev-parse", "HEAD")
        # Rewrite history on origin below the shallow boundary (force-push of a rebased branch).
        git(self.upstream, "reset", "-q", "--hard", "HEAD~2")
        new = commit(self.upstream, "rewritten")
        git(self.upstream, "push", "-q", "--force", "origin", "main")
        message = sync_branch(shallow)
        self.assertEqual(git(shallow, "rev-parse", "HEAD"), old)
        self.assertEqual(git(shallow, "rev-parse", "--is-shallow-repository"), "true")
        self.assertIn("shares no history with origin/main", message)
        self.assertIn(old[:7], message)
        self.assertIn(new[:7], message)
        self.assertIn("git reset --hard origin/main", message)

    def test_shallow_clone_fast_forward_keeps_it_shallow(self):
        shallow = Path(self._tmp.name) / "shallow"
        git(Path(self._tmp.name), "clone", "-q", "--depth", "1", self.origin.as_uri(), str(shallow))
        new = self.push_upstream("b")
        self.assertIn("fast-forwarded", sync_branch(shallow))
        self.assertEqual(git(shallow, "rev-parse", "HEAD"), new)
        self.assertEqual(git(shallow, "rev-parse", "--is-shallow-repository"), "true")

    def test_fetch_failure_is_reported(self):
        git(self.clone, "remote", "set-url", "origin", str(Path(self._tmp.name) / "missing.git"))
        message = sync_branch(self.clone)
        self.assertIn("could not fetch origin/main", message)
        self.assertIn("may be stale", message)

    def test_fetch_timeout_is_reported(self):
        git(self.clone, "remote", "set-url", "origin", "ssh://example.invalid/repo.git")
        with mock.patch.dict(os.environ, {"GIT_SSH_COMMAND": "sleep 10; :"}):
            started = time.monotonic()
            message = sync_branch(self.clone, fetch_timeout=0.5)
        self.assertLess(time.monotonic() - started, 5)
        self.assertIn("could not fetch origin/main", message)
        self.assertIn("timed out", message)

    def test_branch_missing_on_origin_is_silent(self):
        git(self.clone, "checkout", "-q", "-b", "feature")
        commit(self.clone, "feature")
        self.assertIsNone(sync_branch(self.clone))

    def test_detached_head_is_silent(self):
        self.push_upstream("b")
        git(self.clone, "checkout", "-q", "--detach")
        old = self.head()
        self.assertIsNone(sync_branch(self.clone))
        self.assertEqual(self.head(), old)

    def test_no_origin_is_silent(self):
        git(self.clone, "remote", "remove", "origin")
        self.assertIsNone(sync_branch(self.clone))

    def test_not_a_repository_is_silent(self):
        folder = Path(self._tmp.name) / "plain"
        folder.mkdir()
        self.assertIsNone(sync_branch(folder))

    def test_fetch_updates_only_the_current_branch(self):
        git(self.upstream, "checkout", "-q", "-b", "other")
        commit(self.upstream, "other")
        git(self.upstream, "push", "-q", "origin", "other")
        git(self.upstream, "checkout", "-q", "main")
        self.push_upstream("b")
        sync_branch(self.clone)
        refs = git(self.clone, "for-each-ref", "--format=%(refname)", "refs/remotes/origin/")
        self.assertNotIn("refs/remotes/origin/other", refs.splitlines())


if __name__ == "__main__":
    unittest.main()
