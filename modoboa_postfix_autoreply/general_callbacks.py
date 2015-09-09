"""Event callbacks."""

from django.utils.translation import ugettext_lazy, ugettext as _

from modoboa.lib import events, parameters

from .forms import ARmessageForm


@events.observe("ExtraUprefsJS")
def extra_js(user):
    return ["""function autoreply_cb() {
    $('.datefield').datetimepicker({
        format: 'YYYY-MM-DD HH:mm:ss',
        language: '%(lang)s'
    });
}
""" % {'lang': parameters.get_user(user, "LANG", app="core")}
    ]


@events.observe("UserMenuDisplay")
def menu(target, user):
    if target != "uprefs_menu":
        return []
    if not user.mailbox_set.count():
        return []
    return [
        {"name": "autoreply",
         "class": "ajaxnav",
         "url": "autoreply/",
         "label": ugettext_lazy("Auto-reply message")}
    ]


@events.observe("ExtraAccountForm")
def extra_account_form(user, account=None):
    """Add autoreply form to the account edition form."""
    result = []
    if user.group in ("SuperAdmins", "DomainAdmins"):
        mailbox = account.mailbox_set.first()
        if mailbox:
            extraform = {
                "id": "auto_reply_message",
                "title": _("Auto reply"),
                "cls": ARmessageForm,
                "new_args": [mailbox]
            }
            result.append(extraform)
    return result


@events.observe("FillAccountInstances")
def fill_account_tab(user, account, instances):
    if user.group in ("SuperAdmins", "DomainAdmins"):
        mailbox = account.mailbox_set.first()
        if mailbox:
            instances["auto_reply_message"] = mailbox.armessage_set.first()
