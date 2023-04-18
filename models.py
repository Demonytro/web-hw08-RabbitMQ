from mongoengine import *

connect(host="mongodb://localhost:27017/hw8rabbitmq")


class Contact(Document):
    fullname = StringField(max_length=50)
    email = StringField(required=True)
    check_send = BooleanField(required=True, default=False)
    phone = StringField(max_length=20)
    tags_contact = ListField(StringField(max_length=30))


# class TextContact(Contact):
#     content = StringField()
#
#
# class ImageContact(Contact):
#     image_path = StringField()
#
#
# class LinkContact(Contact):
#     link_url = StringField()

# class Post(Document):
#     title = StringField(max_length=120, required=True)
#     author = ReferenceField(User, reverse_delete_rule=CASCADE)
#     tags = ListField(StringField(max_length=30))
#     meta = {'allow_inheritance': True}
#
#
