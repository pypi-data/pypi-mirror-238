import enum


class APIStatus(enum.Enum):
    PROCESS = 1
    HOLD = 2
    SUCCESS = 3
    REFUNDED = 5
    FAILED = 13
    PARTIAL_REFUNDED = 19
    INCOMPLETE_BANK = 22
    INCOMPLETE = 23
    CREATED = 1000
    PROCESSING = 1001

    @property
    def description(self):
        match self.value:
            case self.PROCESS:
                return 'Payment is under process'
            case self.HOLD:
                return 'Payment was hold'
            case self.SUCCESS:
                return 'Payment is successful'
            case self.REFUNDED:
                return 'Payment was refunded'
            case self.FAILED:
                return 'Payment failed due to some errors'
            case self.PARTIAL_REFUNDED:
                return 'Was initiated a partial refund'
            case self.INCOMPLETE_BANK:
                return 'Payment timeout'
            case self.INCOMPLETE:
                return 'Payment is incomplete'
            case self.CREATED:
                return 'Payment was created'
            case self.PROCESSING:
                return 'Payment is processing and waiting to get update status'


class APIError(enum.Enum):
    OK = 0
    HTTP_AUTORIZATION_MERCHANT_ID_WRONG = 403
    HTTP_AUTORIZATION_MERCHANT_NOT_DEFINED = 402
    HTTP_AUTORIZATION_HASH_WRONG = 401
    ERROR_MERCHANT_IS_DISABLED = 101
    ERROR_MERCHANT_ID_NOT_DEFINED = 102
    ERROR_MERCHANT_ORDER_ID_NOT_DEFINED = 103
    ERROR_ORDER_PRICE_NOT_DEFINED = 104
    ERROR_ORDER_CURRENCY_NOT_DEFINED = 105
    ERROR_ORDER_CURRENCY_BAT_FORMAT = 106
    ERROR_LANGUAGE_BAD_FORMAT = 107
    ERROR_MIN_AMOUNT = 108
    ERROR_MAX_AMOUNT = 109
    ERROR_HASH = 110
    ERROR_BAD_FORMAT_OF_BACKLINKS = 111
    ERROR_BAD_FORMAT_OF_LOGO = 112
    ERROR_BAD_OF_ITEM_IN_LIST = 113
    ERROR_CARD_NOT_FOUND = 116
    ERROR_CHECKOUT_DEACTIVATED = 117
    ERROR_CHECKOUT_DOMAIN_NOT_RESOLVED = 118
    ERROR_PLATFORM_NOT_EXISTS = 119
    ERROR_CALLBACK_IS_EMPTY = 120
    ERROR_REQUEST_DATA_IS_EMPTY = 121
    ERROR_REASON_IS_EMPTY = 122
    ERROR_ORDER_NOT_FOUND = 123
    ERROR_CARD_TOKEN_IS_EMPTY = 124
    ERROR_MERCHANT_IS_REJECTED = 125
    ERROR_CURRENCY_IS_OUT_OF_DATE = 126
    ERROR_CURRENCY_IS_NOT_CONFIGURED = 127
    ERROR_PAYMENT_TYPE_IS_NOT_CORRECT = 128
    ERROR_PAYMENT_CHANNEL_NOT_FOUND = 129
    ERROR_RECURRING_OPTION_TURNED_OFF = 130
    INSUFFICIENT_FUNDS = 140
    AMOUNT_LIMIT_EXCEEDED = 141
    FREQUENCY_LIMIT_EXCEEDED = 142
    CARD_NOR_EFFECTIVE = 143
    CARD_EXPIRED = 144
    CARD_LOST = 145
    CARD_STOLEN = 146
    CARD_RESTRICTED = 147
    DECLINED_BY_ISSUER = 148
    BANK_SYSTEM_ERROR = 149
    UNKNOWN = 150
    AUTHENTICATION_FAILED = 151
    OFFER_TIMEOUT = 152

    def __repr__(self) -> str:
        return str(self.name)

    def __str__(self):
        return str(self.name)
