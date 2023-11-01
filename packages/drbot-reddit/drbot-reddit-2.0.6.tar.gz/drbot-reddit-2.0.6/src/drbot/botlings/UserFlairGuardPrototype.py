from __future__ import annotations
from ..log import log
from ..reddit import reddit
from ..Botling import Botling

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Callable, Any


class UserFlairGuard(Botling):
    """Allows you to enforce custom criteria on user flair.
    flair_checker should accept a dictionary that looks like:
        `{'flair_css_class': 'userflair', 'user': Redditor(name='spez'), 'flair_text': 'My Illegal Flair'}`
    and should return a dictionary indicating what it wants to do with this user's flair.
    If the user's flair is OK, return `{}`. Otherwise, you can use the following keys to modify it (all are optional):
        - text: The flair's new text (e.g. "Level 12 Wizard"). Use `""` to reset it or `None` to leave it untouched.
        - flair_css_class: The flair's new CSS class (e.g. "userflair"). Use `""` to reset it or `None` to leave it untouched. You cannot set both this and flair_template_id.
        - flair_template_id: The flair's new template ID (e.g. "d81bd5ce-5c3e-11ee-8c99-0242ac120002"). Use `""` to reset it or `None` to leave it untouched. You cannot set both this and flair_css_class.
        - reason: A reason for why this flair was changed, which will be sent to the user (if you have that setting on). Use None to omit a reason. This will do nothing by itself - you must also set one of the other keys.
    Whatever change you make, make sure it leads to the flair no longer being illegal! Otherwise this will lead to spamming users with identical messages.
    Scans every single user who has ever assigned themselves flair in your sub, so this is not a good idea for bigger subs.
    When possible, it's recommended to use an automod rule instead, though that will only catch changed flair when the user makes a comment/post."""

    default_settings = {
        "modmail_user": True,
        "modmail_mods": False,  # Warning: this may clog your inbox.
    }

    def __init__(self, flair_checker: Callable[[dict[str, Any]], dict[str, str]], name: str | None = None) -> None:
        super().__init__(name)
        self.flair_checker = flair_checker

    def setup(self) -> None:
        # TBD schedule scan()
        pass

    def scan(self) -> None:
        log.info(f'Scanning user flair.')

        count = 0  # For logging
        for flair in reddit.sub.flair(limit=None):
            count += 1

            new_flair = self.flair_checker(flair)
            orig_return = str(new_flair)  # For logging

            # Check return value type
            if not isinstance(new_flair, dict):
                raise TypeError(f"Your flair checker must return a dict but for u/{flair['user'].name} with flair {flair} it returned a {type(new_flair)}: {new_flair}.")

            # Check for unknown keys
            legal_keys = set(["text", "flair_css_class", "flair_template_id", "reason"])
            unknown_keys = set(new_flair) - set(legal_keys)
            if len(unknown_keys) > 0:
                log.warning(f"Your flair_checker returned some unknown keys, which were ignored: {unknown_keys}")
            for k in unknown_keys:
                del new_flair[k]

            # Check for early exit
            if not new_flair:
                continue
            if "reason" in new_flair and len(new_flair) == 1:
                log.warning(f"Your flair_checker returned a reason for u/{flair['user'].name} with flair {flair}, but didn't ask to change the flair in any way, so it was ignored: {new_flair}")
                continue

            log.info(f'u/{flair["user"].name} has illegal flair {flair}.')

            # Make sure we don't try to set both flair_css_class and flair_template_id, since PRAW doesn't allow that
            if new_flair.get("flair_css_class", None) and new_flair.get("flair_template_id", None):
                raise ValueError(f"{self} tried to set both flair_css_class and flair_template_id for a user's flair at the same time, which is not allowed. Return dict: {new_flair}")

            # Figure out what we want to do to the flair
            operation = None

            if new_flair.get("text", None):
                operation = "delete" if new_flair["text"] == "" else "set"
            else:
                new_flair["text"] = flair.get("flair_text", "")

            if new_flair.get("flair_css_class", None):
                operation = "set"
            else:
                new_flair["flair_css_class"] = flair.get("flair_css_class", "")

            if new_flair.get("flair_template_id", None):
                operation = "set"
            else:
                new_flair["flair_template_id"] = flair.get("flair_template_id", None)

            # There should always be some operation by this point
            assert operation is not None, f"Logic failure in {self}. This shouldn't happen. Return value: {orig_return}"

            # TBD: Fake performing the operation and make sure flair_checker allows it now, to avoid loops.

            # Perform the operation on the flair
            if operation == "delete":
                if self.DR.global_settings.dry_run:
                    log.info(f"DRY RUN: would have reset the flair.")
                else:
                    raise NotImplementedError()
                    reddit.sub.flair.delete(flair['user'].name)
            elif operation == "set":
                if self.DR.global_settings.dry_run:
                    log.info(f"DRY RUN: would have set the flair to {new_flair}.")
                else:
                    raise NotImplementedError()
                    reddit.sub.flair.set(flair['user'].name, text=new_flair["text"], flair_css_class=new_flair["flair_css_class"], flair_template_id=new_flair["flair_template_id"])
            else:
                raise RuntimeError(f"Somehow decided on an unknown operation '{operation}' in {self}. This shouldn't happen. Return value: {orig_return}")

            # Send modmails
            core_message = "flair was illegal"
            if new_flair.get("reason", None):
                core_message += f" because {new_flair['reason']}"
            core_message += f". It has been "
            if operation == "delete":
                core_message += "reset"
            elif operation == "set" and new_flair["text"] != flair.get("flair_text", ""):
                pass
    #         else:
    #             {'reset' if operation == 'delete' else 'set to ' + }"
            
    #         If you are a star user and this was done in error, please respond to this message.
    #         if self.DR.settings.modmail_user:
    #             f"Hi u/{flair['user'].name}, your "
    #             reddit.DR.send_modmail(recipient=flair['user'].name,
    #                                 subject=f"Your flair was illegal and has been {'reset' if operation == 'delete' else 'changed'}",
    #                                 body=
                                
    # Your flair has been reset. If you are a star user and this was done in error, please respond to this message.""", add_common=False)

    #     log.info(f"Scanned flair for {count} users.")
