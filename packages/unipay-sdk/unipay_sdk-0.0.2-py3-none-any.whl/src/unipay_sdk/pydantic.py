from pydantic import BaseModel


class _BasicData(BaseModel):
    Checkout: str
    UnipayOrderHashID: str


class BasicUniPayResponse(BaseModel):
    errorcode: int
    message: str
    data: _BasicData


class BasicUniPayCallback(BaseModel):
    MerchantOrderID: int
    Status: int
    Hash: str
    Amount: float
    UnipayOrderID: str
    ErrorCode: int
    ErrorMessage: str
    Reason: str


class OrderItem(BaseModel):
    price: float
    quantity: int
    title: str
    description: str
