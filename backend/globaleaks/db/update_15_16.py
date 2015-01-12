# -*- encoding: utf-8 -*-

"""
  Changes

    Receiver table:
      - introduced ping_mail_address, ping_

    Notification table:
      - introduced two boolean TODO - write what they are 
      - introduced ping templates

    Node table:
      - introduced default_language and default_timezone

    User table:
      - introduced language and timezone

    Context table:
      - fields refactored entirely adding Field and Step table;
      - all data is migrated.

    InternalTip table:
      - changed from wb_fields to wb_steps; all data is migrated.
"""

from storm.locals import Int, Bool, Unicode, DateTime, JSON, ReferenceSet
from globaleaks.db.base_updater import TableReplacer
from globaleaks.models import Model, Field, Step
from globaleaks.utils.utility import every_language

class Context_version_15(Model):
    __storm_table__ = 'context'
    selectable_receiver = Bool()
    show_small_cards = Bool()
    show_receivers = Bool()
    maximum_selectable_receivers = Int()
    select_all_receivers = Bool()
    tip_max_access = Int()
    file_max_download = Int()
    tip_timetolive = Int()
    submission_timetolive = Int()
    last_update = DateTime()
    name = JSON()
    description = JSON()
    receiver_introduction = JSON()
    postpone_superpower = Bool()
    can_delete_submission = Bool()
    enable_private_messages = Bool()
    presentation_order = Int()

# this has never been performed during old migration script and will need
# to be done in situations like the one generated in this particular migration
Context_version_15.steps = ReferenceSet(Context_version_15.id,
                                        Step.context_id)


class Receiver_version_15(Model):
    __storm_table__ = 'receiver'
    user_id = Unicode()
    name = Unicode()
    description = JSON()
    configuration = Unicode()
    gpg_key_info = Unicode()
    gpg_key_fingerprint = Unicode()
    gpg_key_status = Unicode()
    gpg_key_armor = Unicode()
    gpg_enable_notification = Bool()
    mail_address = Unicode()
    can_delete_submission = Bool()
    postpone_superpower = Bool()
    last_update = DateTime()
    tip_notification = Bool()
    comment_notification = Bool()
    file_notification = Bool()
    message_notification = Bool()
    presentation_order = Int()


class Notification_version_15(Model):
    __storm_table__ = 'notification'
    server = Unicode()
    port = Int()
    username = Unicode()
    password = Unicode()
    source_name = Unicode()
    source_email = Unicode()
    security = Unicode()
    admin_anomaly_template = JSON()
    encrypted_tip_template = JSON()
    encrypted_tip_mail_title = JSON()
    plaintext_tip_template = JSON()
    plaintext_tip_mail_title = JSON()
    encrypted_file_template = JSON()
    encrypted_file_mail_title = JSON()
    plaintext_file_template = JSON()
    plaintext_file_mail_title = JSON()
    encrypted_comment_template = JSON()
    encrypted_comment_mail_title = JSON()
    plaintext_comment_template = JSON()
    plaintext_comment_mail_title = JSON()
    encrypted_message_template = JSON()
    encrypted_message_mail_title = JSON()
    plaintext_message_template = JSON()
    plaintext_message_mail_title = JSON()
    pgp_expiration_alert = JSON()
    pgp_expiration_notice = JSON()
    zip_description = JSON()


class Replacer1516(TableReplacer):

    def migrate_Context(self):
        print "%s Context migration assistant" % self.std_fancy

        old_contexts = self.store_old.find(self.get_right_model("Context", 15))

        for old_context in old_contexts:

            new_context = self.get_right_model("Context", 16)()

            for _, v in new_context._storm_columns.iteritems():
                setattr(new_context, v.name, getattr(old_context, v.name))

            self.store_new.add(new_context)

        self.store_new.commit()

    def migrate_Receiver(self):
        print "%s Receiver migration assistant" % self.std_fancy

        old_receivers = self.store_old.find(self.get_right_model("Receiver", 15))

        for old_receiver in old_receivers:

            new_receiver = self.get_right_model("Receiver", 16)()

            for _, v in new_receiver._storm_columns.iteritems():

                if v.name == 'configuration':
                    if old_receiver.configuration == 'hidden':
                        new_receiver.configuration = 'forcefully_selected'
                    else:
                        new_receiver.configuration = old_receiver.configuration
                    continue

                if v.name == 'presentation_order':
                    if old_receiver.presentation_order == 0:
                        new_receiver.presentation_order = 1
                    continue

                if v.name == 'ping_mail_address':
                    new_receiver.ping_mail_address = old_receiver.mail_address
                    continue

                if v.name == 'ping_notification':
                    new_receiver.ping_notification = False
                    continue

                setattr(new_receiver, v.name, getattr(old_receiver, v.name))

            self.store_new.add(new_receiver)

        self.store_new.commit()

    def migrate_Field(self):
        print "%s Field migration assistant" % self.std_fancy

        old_fields = self.store_old.find(self.get_right_model("Field", 15))

        for old_field in old_fields:

            new_field = self.get_right_model("Field", 16)()

            for _, v in new_field._storm_columns.iteritems():
                if v.name == 'is_template':
                    if old_field.is_template is None:
                        new_field.is_template = False
                    else:
                        new_field.is_template = old_field.is_template
                    continue

                setattr(new_field, v.name, getattr(old_field, v.name))

            self.store_new.add(new_field)

        self.store_new.commit()

    def migrate_Notification(self):
        print "%s Notification migration assistant: (disable_notification flags, ping_templates)" % self.std_fancy

        old_notification = self.store_old.find(self.get_right_model("Notification", 15)).one()
        new_notification = self.get_right_model("Notification", 16)()

        for _, v in new_notification._storm_columns.iteritems():

            if v.name == 'disable_admin_notification_emails':
                new_notification.disable_admin_notification_emails = False
                continue

            if v.name == 'disable_receivers_notification_emails':
                new_notification.disable_receivers_notification_emails = False
                continue

            if v.name == 'ping_mail_template':
                new_notification.ping_mail_template = every_language("")
                continue

            if v.name == 'ping_mail_title':
                new_notification.ping_mail_title = every_language("")
                continue

            setattr(new_notification, v.name, getattr(old_notification, v.name) )

        self.store_new.add(new_notification)
        self.store_new.commit()
