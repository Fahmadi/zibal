from mongoengine import StringField, Document, ReferenceField, IntField, BooleanField


class GatewayMerchant(Document):
    title = StringField(max_length=120, required=True)
    website = StringField(max_length=50)
    merchant_key = StringField(max_length=50)
    user_id = IntField(max_length=50)
    user_activate = BooleanField(default=True)
    meta = {'allow_inheritance': True}


class Transaction(Document):
    amount = IntField(max_length=50)
    callback_url=StringField(max_length=70)
    gateway_id = ReferenceField(GatewayMerchant)
    merchant_key = StringField(max_length=70)
    payir_transaction_id = StringField(max_length=50)
    status = BooleanField(default=False)
    card_number = IntField(max_length=16, null=True)
    transId = IntField(max_length=16 , null=True)
