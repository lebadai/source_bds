from django.utils.translation import gettext_lazy as _

PAGINATOR_PER_PAGE = 5


# --- Sort method ---
ORDER_BY_ASC = 1
ORDER_BY_DESC = 2

SORT_TYPE = {
    ORDER_BY_ASC: _('asc'),
    ORDER_BY_DESC: _('desc'),
}

SORT_TYPE_CHOICE = ((k, v) for k, v in SORT_TYPE.items())
SORT_TYPE_LIST = [(k, v) for k, v in SORT_TYPE.items()]

SORT_TYPE_TO_ID = {
    'asc': ORDER_BY_ASC,
    'desc': ORDER_BY_DESC
}

SERVICE_CODE_DEVICE_INVALID = 100       # thiết bị không hợp lệ
SERVICE_CODE_NOT_EXISTS_USER = 101      # không tồn tại User
SERVICE_CODE_WRONG_PASSWORD = 102       # Sai mật khẩu
SERVICE_CODE_WRONG_TOKEN = 103          # Sai token
SERVICE_CODE_USER_IS_LOCKED = 104       # Tài khoản bị Aber khóa
SERVICE_CODE_USER_NOT_ACTIVE = 105      # Tài khoản chưa kích hoạt
SERVICE_CODE_DEVICE_OTP_INVALID = 106   # sai OTP

SERVICE_CODE_NOT_FOUND = 200            # data tìm không thấy
SERVICE_CODE_ERROR = 201                # Dùng chung
SERVICE_CODE_ERROR_SEND_SMS = 202       # số di động không hợp lệ
SERVICE_CODE_BODY_PARSE_ERROR = 203     # parse body từ client
SERVICE_CODE_NOT_EXISTS_BODY = 204      # body client gửi lên không tồn tại
SERVICE_CODE_TOKEN_INVALID = 205        # dùng trong service gọi sms otp của khách hàng
SERVICE_CODE_HEADER_INVALID = 206       # header không chứa thông tin nhận diện

SERVICE_CODE_SPAM = 400
SERVICE_CODE_NOT_ACCEPTABLE = 406   # Mật khẩu không đúng

# -- Dictionary --
SERVICE_MESSAGE = {
    SERVICE_CODE_DEVICE_INVALID: 'Thiết bị không hợp lệ',
    SERVICE_CODE_DEVICE_OTP_INVALID: 'OTP không hợp lệ',
    SERVICE_CODE_NOT_EXISTS_USER: 'Không tồn tại tài khoản',
    SERVICE_CODE_WRONG_PASSWORD: 'Sai thông tin đăng nhập',
    SERVICE_CODE_WRONG_TOKEN: 'Token không hợp lệ',
    SERVICE_CODE_USER_NOT_ACTIVE: 'Tài khoản chưa kích hoạt. Vui lòng liên hệ Admin.',
    SERVICE_CODE_USER_IS_LOCKED: 'Tài khoản của bạn bị khóa. Vui lòng liên hệ Admin.',
    SERVICE_CODE_NOT_FOUND: 'Không tồn tại dữ liệu',
    SERVICE_CODE_SPAM: 'Spam',
    SERVICE_CODE_HEADER_INVALID: 'Header không hợp lệ',
    SERVICE_CODE_BODY_PARSE_ERROR: 'Body parse lỗi',
}

SORT_TYPE_TO_ID = {
    'asc': ORDER_BY_ASC,
    'desc': ORDER_BY_DESC
}