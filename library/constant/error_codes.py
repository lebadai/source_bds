from django.utils.translation import ugettext_lazy as _

# API error code & messages
JSON_BODY_EMPTY = 'JSON_BODY_EMPTY'
BODY_PARSE_ERROR = 'JSON_BODY_EMPTY'
BEARER_TOKEN_NOT_FOUND = 'BEARER_TOKEN_NOT_FOUND'
BEARER_TOKEN_NOT_VALID = 'BEARER_TOKEN_NOT_VALID'

ERROR_CODE_MESSAGE = {
    JSON_BODY_EMPTY: _('Json body empty'),
    BODY_PARSE_ERROR: _('Parsing body occurred error'),
    BEARER_TOKEN_NOT_FOUND: _('Can not found bearer token in header'),
    BEARER_TOKEN_NOT_VALID: _('Bearer token is not valid')
}