from mongoengine import StringField, Document, ReferenceField, IntField, BooleanField


class GatewayMerchant(Document):
    title = StringField(max_length=120, required=True)
    website = StringField(max_length=50)
    merchant_key = StringField(max_length=50)
    user_id = IntField(max_length=50)
    user_activate = BooleanField(default=True)
    meta = {'allow_inheritance': True}