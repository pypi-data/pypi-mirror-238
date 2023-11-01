from __future__ import annotations
from praw.models import Submission
from pytimeparse import parse
from ..Botling import Botling
from ..log import log
from ..reddit import reddit


# TBD:
# - Figure out the delay
# - Test flair - do I need text? Does flair clearing work with ""?


class AutoLocker(Botling):
    """Auto-locks all posts after a given amount of time.
    Most useful if you want to "archive" posts after a delay different than reddit's default 6 months.
    Inspired by AutoLockBot - https://www.reddit.com/r/AutoLockBot"""

    default_settings = {
        "lock_delay": "1 month",  # The duration before a post is locked, e.g. "2 weeks" or "1 hour 10 mins".
        "ignore_mods": True,  # Don't lock posts made by mods.
        "ignore_css_classes": [],  # Don't lock posts made by users with certain CSS classes.
        "set_flair": False  # After locking a post, set its flair to this. Use "False" to disable this option, "" for no flair, and an invalid value like "X" to get a list of valid options.
    }

    def validate_settings(self) -> None:
        delay = parse(self.DR.settings.lock_delay)
        assert delay is not None, f'Could not parse delay "{self.DR.settings.lock_delay}".'
        assert delay > 0, f'Delay must be greater than zero.'
        assert isinstance(self.DR.settings.ignore_mods, bool)
        assert isinstance(self.DR.settings.ignore_css_classes, list) and all(isinstance(x, str) for x in self.DR.settings.ignore_css_classes), "ignore_css_classes must be a list of strings"

        assert isinstance(self.DR.settings.set_flair, bool) or isinstance(self.DR.settings.set_flair, str)
        if isinstance(self.DR.settings.set_flair, str):
            flair_ids = list(x['id'] for x in reddit.sub.flair.link_templates)
            assert self.DR.settings.set_flair in flair_ids, f"flair template ID \"{self.DR.settings.set_flair}\" doesn't exist on your sub. Options:       " + "       ".join(f"{flair['id']}: `{flair['text']}`" for flair in reddit.sub.flair.link_templates)

    def setup(self) -> None:
        self.delay = parse(self.DR.settings.lock_delay)
        self.DR.streams.post.subscribe(self, self.handle)  # How to delay?

    def handle(self, item: Submission) -> None:
        # Ignore posts from mods (if setting is on)
        if self.DR.settings.ignore_mods and reddit.DR.is_mod(item.author):
            return

        # Ignore posts from users with allowed useflair CSS classes (if setting is on)
        if len(self.DR.settings.ignore_css_classes) > 0:
            flairdict = reddit.DR.get_userflair(item.author)
            css_class = "" if flairdict is None else (flairdict["flair_css_class"] or "")  # "" means no class or no flair
            if css_class in self.DR.settings.ignore_css_classes:
                return

        # Lock the post
        if self.DR.global_settings.dry_run:
            log.info(f"""DRY RUN: would have locked post {item.fullname}.""")
        else:
            item.mod.lock()

        # Set flair (if setting is on)
        if isinstance(self.DR.settings.set_flair, str):
            if self.DR.global_settings.dry_run:
                log.info(f"""DRY RUN: would have changed post {item.fullname}'s flair to {self.DR.settings.set_flair}.""")
            else:
                item.mod.flair(flair_template_id=self.DR.settings.set_flair)
