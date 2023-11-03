# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import datetime
from typing import Literal
from typing import Union

import pydantic
from canonical import ResourceName

from .commentuser import CommentUser
from .picqerresource import PicqerResource


class CommentFulfillmentCustomer(pydantic.BaseModel):
    idfulfilment_customer: int
    username: str
    name: str


class Mention(pydantic.BaseModel):
    text: str
    mentioned_type: str
    mentioned: CommentUser | CommentFulfillmentCustomer


class CustomerCommentSource(pydantic.BaseModel):
    idcustomer: int

    @property
    def document_number(self) -> str:
        return str(self.idcustomer)

    @property
    def id(self) -> int:
        return self.idcustomer


class OrderCommentSource(pydantic.BaseModel):
    idorder: int
    orderid: str

    @property
    def document_number(self) -> str:
        return str(self.orderid)

    @property
    def id(self) -> int:
        return self.idorder


class PicklistCommentSource(pydantic.BaseModel):
    idpicklist: int
    picklistid: str

    @property
    def document_number(self) -> str:
        return str(self.picklistid)

    @property
    def id(self) -> int:
        return self.idpicklist


class ProductCommentSource(pydantic.BaseModel):
    idproduct: int
    productcode: str

    @property
    def document_number(self) -> str:
        return str(self.productcode)

    @property
    def id(self) -> int:
        return self.idproduct


class PurchaseOrderCommentSource(pydantic.BaseModel):
    idpurchaseorder: int
    purchaseorderid: str

    @property
    def document_number(self) -> str:
        return str(self.purchaseorderid)

    @property
    def id(self) -> int:
        return self.idpurchaseorder


class ReceiptCommentSource(pydantic.BaseModel):
    idreceipt: int
    receiptid: str

    @property
    def document_number(self) -> str:
        return str(self.receiptid)

    @property
    def id(self) -> int:
        return self.idreceipt


class ReturnCommentSource(pydantic.BaseModel):
    idreturn: int
    returnid: str

    @property
    def document_number(self) -> str:
        return str(self.returnid)

    @property
    def id(self) -> int:
        return self.idreturn


class CommentSource(pydantic.BaseModel):
    __root__: Union[
        CustomerCommentSource,
        OrderCommentSource,
        PicklistCommentSource,
        ProductCommentSource,
        PurchaseOrderCommentSource,
        ReceiptCommentSource,
        ReturnCommentSource,
    ]

    @property
    def id(self) -> int:
        return self.__root__.id

    @property
    def document_number(self) -> str:
        return self.__root__.document_number


class Comment(PicqerResource):
    created_at: datetime.datetime
    author_type: str
    author: CommentUser
    idcomment: int
    body: str
    mentions: list[Mention] = []
    show_at_related: bool
    source_type: Literal[
        'customer',
        'order',
        'picklist',
        'product',
        'purchaseorder',
        'receipt',
        'return',
        'supplier',
    ]
    source: CommentSource
    updated_at: datetime.datetime

    @property
    def source_id(self) -> int:
        return self.source.id

    @property
    def document_number(self) -> str:
        return self.source.document_number

    @property
    def resource_name(self) -> ResourceName:
        return ResourceName(f'//{self._client.domain}/comments/{self.idcomment}')

    class Meta:
        base_endpoint: str = '/v1/comments'