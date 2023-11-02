import hashlib
from typing import List
import requests
from .pydantic import BasicUniPayResponse, BasicUniPayCallback
from .pydantic import OrderItem


class BaseAPI:
    def __init__(self):
        self.version = None
        self.urlBase = None
        self.create_order = f'{self.urlBase}/createorder'
        self.pre_auth_confirm = f'{self.urlBase}/confirm'
        self.get_saved_card = f'{self.urlBase}/get-card'


class APIMethodsV1(BaseAPI):
    def __init__(self):
        super().__init__()
        self.version = 1
        self.urlBase = 'https://api.unipay.com/checkout/'


class APIMethodsV2(BaseAPI):
    def __init__(self):
        super().__init__()
        self.version = 2
        self.urlBase = 'https://apiv2.unipay.com/custom/checkout/v1'


class APIMethodsTesting(BaseAPI):
    def __init__(self, url):
        super().__init__()
        self.version = 2
        self.urlBase = f'{url}/custom/checkout/v1'


class UniPayClient:
    def __init__(self,
                 secretkey: str,
                 merchant_id: int,
                 success_url: str,
                 cancel_url: str,
                 callback_url: str,
                 language: str = 'GE',
                 test: bool = False,
                 test_url: str = None
                 ):
        """
        UniPay.com API Client

        :param secretkey:
        :param merchant_id:
        :param success_url:
        :param cancel_url:
        :param callback_url:
        :param language:
        :param test:
        :param test_url:
        """
        self._secretKey = secretkey
        self.successUrl = success_url
        self.cancelUrl = cancel_url
        self.callbackUrl = callback_url
        self.merchant_id = merchant_id
        self.language = language
        self._api = APIMethodsTesting(test_url) if test else APIMethodsV2()

    def _calculate_hash(self,
                        customer_id,
                        order_id,
                        order_price,
                        order_currency,
                        order_name
                        ) -> str:
        sign_string = \
            f'{self.secretKey}|{self.merchant_id}|{customer_id}|{order_id}|{order_price}|{order_currency}|{order_name}'
        return hashlib.sha256(sign_string.encode('UTF-8')).hexdigest()  # noqa

    def _request_constructor(self,
                             hash_str: str,
                             merchant_user: str,
                             merchant_order_id: str,
                             order_price: float,
                             order_currency: str,
                             order_name: str,
                             order_description: str,
                             order_items: List[OrderItem],
                             is_pre: bool = False,
                             is_save_card: bool = False,
                             saved_card: str = None
                             ):
        items = []
        for item in order_items:
            items.append(item.model_dump())
        constructed = {
            'Hash': hash_str,
            'MerchantID': self.merchant_id,
            'MerchantUser': merchant_user,
            'MerchantOrderID': str(merchant_order_id),
            'OrderPrice': order_price,
            'OrderCurrency': order_currency,
            'SuccessRedirectUrl': self.successUrl,
            'CancelRedirectUrl': self.cancelUrl,
            'CallBackUrl': self.callbackUrl,
            'Language': self.language,
            'OrderName': order_name,
            'OrderDescription': order_description,
        }
        if items:
            constructed['Items'] = items
        if is_pre:
            constructed['OrderType'] = 'preauth'
        if is_save_card:
            constructed['InApp'] = "1"
        if saved_card:
            constructed['RegularPaymentID'] = saved_card
        return constructed

    def _send(self, payload: dict):
        data = requests.post(self._api.create_order, json=payload)
        return BasicUniPayResponse.model_validate(data.json())

    def create_order(self,
                     merchant_order_id: str,
                     merchant_order_user: str,
                     order_price: float,
                     order_name: str,
                     order_description: str = None,
                     items: List[OrderItem] = None,
                     order_currency: str = 'GEL',
                     ) -> BasicUniPayResponse:
        """
        Create basic order

        :return: unipay-sdk.pydantic.BasicUniPayResponse
        """
        if items is None:
            items = []
        order_hash = self._calculate_hash(merchant_order_user,
                                          merchant_order_id,
                                          order_price,
                                          order_currency,
                                          order_name)
        payload = self._request_constructor(hash_str=order_hash,
                                            merchant_user=merchant_order_user,
                                            merchant_order_id=merchant_order_id,
                                            order_price=order_price,
                                            order_currency=order_currency,
                                            order_name=order_name,
                                            order_description=order_description,
                                            order_items=items)
        return self._send(payload)

    def verify_callback(self, callback_data: dict) -> bool:
        """
        Provides callback hash verification, returns `True` if hash is valid

        :return: bool
        """
        data = BasicUniPayCallback.model_validate(callback_data)
        hash_str = f'{data.UnipayOrderID}|{data.MerchantOrderID}|{data.Status}|{self._secretKey}'
        return hashlib.sha256(hash_str) == data.Hash  # noqa

    def pre_authorize(self):
        raise NotImplemented

    def pre_authorize_confirm(self):
        raise NotImplemented

    def create_order_and_save_card(self):
        raise NotImplemented

    def pay_with_saved_card(self):
        raise NotImplemented

    def get_saved_card(self):
        raise NotImplemented
