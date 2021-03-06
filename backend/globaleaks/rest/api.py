# -*- coding: UTF-8
#   API
#   ***
#
#   This file contains the URI mapping for the GlobaLeaks API.

from globaleaks import LANGUAGES_SUPPORTED_CODES
from globaleaks.settings import GLSettings
from globaleaks.handlers import exception, \
                                node, submission, rtip, wbtip, receiver, \
                                files, authentication, admin, token, \
                                collection, langfiles, css, wizard
from globaleaks.handlers.base import BaseStaticFileHandler, BaseRedirectHandler
from globaleaks.handlers import exporter

uuid_regexp = r'([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})'
field_regexp = uuid_regexp
token_string = r'([a-zA-Z0-9]{42})'

# Here is created the mapping between urls and the associated handler.
#
# Most of th handlers conform to the following rules:
#
# * Create class: POST
#     manages the creation of a single resource
#
# * Instance: GET, PUT, DELETE, GET
#     manages the get, the update and the deletion of a single resource
#
# * Collection: GET
#    manages the get of a collection of resources

spec = [
    (r'/exception', exception.ExceptionHandler),

    ## Some Useful Redirects ##
    (r'/login', BaseRedirectHandler, {'url': '/#/login'}),
    (r'/admin', BaseRedirectHandler, {'url': '/#/admin'}),

    ## Authentication Handler ##
    (r'/authentication', authentication.AuthenticationHandler),

    ## Main Public Handlers ##
    (r'/node', node.NodeInstance),
    (r'/contexts', node.ContextsCollection),
    (r'/receivers' , node.ReceiversCollection),

    # Fake file hosting the Ahmia.fi descriptor
    (r'/description.json', node.AhmiaDescriptionHandler),

    ## Token Handlers ##
    (r'/token', token.TokenCreate),
    (r'/token/' + token_string, token.TokenInstance),

    ## Submission Handlers ##
    (r'/submission/' + token_string, submission.SubmissionInstance),
    (r'/submission/' + token_string + '/file', files.FileInstance),

    ## Receiver Tip Handlers ##
    (r'/rtip/' + uuid_regexp, rtip.RTipInstance),
    (r'/rtip/' + uuid_regexp + r'/comments', rtip.RTipCommentCollection),
    (r'/rtip/' + uuid_regexp + r'/receivers', rtip.RTipReceiversCollection),
    (r'/rtip/' + uuid_regexp + '/download/' + uuid_regexp, files.Download),
    (r'/rtip/' + uuid_regexp + '/collection(?:/(zipstored|zipdeflated))?',
            collection.CollectionDownload),
    (r'/rtip/' + uuid_regexp + '/messages', rtip.ReceiverMsgCollection),

    ## Whistleblower Tip Handlers
    (r'/wbtip', wbtip.WBTipInstance),
    (r'/wbtip/comments', wbtip.WBTipCommentCollection),
    (r'/wbtip/receivers', wbtip.WBTipReceiversCollection),
    (r'/wbtip/upload', files.FileAdd),
    (r'/wbtip/messages/' + uuid_regexp, wbtip.WBTipMessageCollection),

    ## Receiver Handlers ##
    (r'/receiver/preferences', receiver.ReceiverInstance),
    (r'/receiver/tips', receiver.TipsCollection),
    (r'/rtip/operations', receiver.TipsOperations),

    ## Admin Handlers ##
    (r'/admin/node', admin.NodeInstance),
    (r'/admin/contexts', admin.ContextsCollection),
    (r'/admin/context', admin.ContextCreate),
    (r'/admin/context/' + uuid_regexp, admin.ContextInstance),
    (r'/admin/receivers', admin.ReceiversCollection),
    (r'/admin/receiver', admin.ReceiverCreate),
    (r'/admin/receiver/' + uuid_regexp, admin.ReceiverInstance),
    (r'/admin/notification', admin.notification.NotificationInstance),
    (r'/admin/step', admin.field.StepCreate),
    (r'/admin/step/' + uuid_regexp, admin.field.StepInstance),
    (r'/admin/field', admin.field.FieldCreate),
    (r'/admin/field/' + uuid_regexp, admin.field.FieldInstance),
    (r'/admin/fieldtemplates', admin.field.FieldTemplatesCollection),
    (r'/admin/fieldtemplate', admin.field.FieldTemplateCreate),
    (r'/admin/fieldtemplate/' + field_regexp, admin.field.FieldTemplateInstance),
    (r'/admin/anomalies', admin.statistics.AnomaliesCollection),
    (r'/admin/stats/(\d+)', admin.statistics.StatsCollection),
    (r'/admin/activities/(summary|details)', admin.statistics.RecentEventsCollection),
    (r'/admin/history', admin.statistics.AnomalyHistoryCollection),
    (r'/admin/staticfiles', admin.staticfiles.StaticFileList),
    (r'/admin/l10n/(' + '|'.join(LANGUAGES_SUPPORTED_CODES) + ').json',
            admin.langfiles.AdminLanguageFileHandler),
    (r'/admin/staticfiles/([a-zA-Z0-9_\-\/\.]*)', admin.staticfiles.StaticFileInstance),
    (r'/admin/overview/tips', admin.overview.Tips),
    (r'/admin/overview/users', admin.overview.Users),
    (r'/admin/overview/files', admin.overview.Files),
    (r'/admin/wizard', wizard.FirstSetup),

    ## Special Files Handlers##
    (r'/(favicon.ico)', BaseStaticFileHandler),
    (r'/(robots.txt)', BaseStaticFileHandler),
    (r'/static/(.*)', BaseStaticFileHandler),
    (r'/styles.css', css.LTRCSSFileHandler),
    (r'/styles-rtl.css', css.RTLCSSFileHandler),
    (r'/l10n/(' + '|'.join(LANGUAGES_SUPPORTED_CODES) + ').json',
            langfiles.LanguageFileHandler, {'path': GLSettings.glclient_path}),

    (r'/s/current', exporter.CurrentStats),
    (r'/s/reportevent/(\w+)', exporter.ReportEvent),

    ## This Handler should remain the last one as it works like a last resort catch 'em all
    (r'/([a-zA-Z0-9_\-\/\.]*)', BaseStaticFileHandler, {'path': GLSettings.glclient_path})
]


