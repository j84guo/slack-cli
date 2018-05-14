"""
SlackConversation :
- common fields between channels and instant messages
"""
class SlackConversation(object):

    def __init__(self, id, created):
        self.id = id
        self.created = created

    def __str__(self):
        return "<SlackConversation object id:{}, created:{}>".format(id, created)

    def __repr__(self):
        return self.__str__()


"""
SlackChannel :
- can model public channels (channel)
- or private channel (group)
"""
class SlackChannel(SlackConversation):

    def __init__(self, id, created, name, topic, purpose, num_members):
        SlackConversation.__init__(self, id, created)

        self.name = name
        self.topic = topic
        self.purpose = purpose
        self.num_members = num_members

        self.is_archived = None
        self.creator = None
        self.name_normalized = None
        self.is_shared = None
        self.is_org_shared = None
        self.is_private = None
        self.members = None
        self.previous_names = None

    def set_is_archived(self, is_archived):
        self.is_archived = is_archived
        return self

    def set_creator(self, creator):
        self.creator = creator
        return self

    def set_name_normalized(self, name_normalized):
        self.name_normalized = name_normalized
        return self

    def set_is_shared(self, is_shared):
        self.is_shared = is_shared
        return self

    def set_is_org_shared(self, is_org_shared):
        self.is_org_shared = is_org_shared
        return self

    def set_is_private(self, is_private):
        self.is_private = is_private
        return self

    def set_members(self, members):
        self.members = members

    def set_previous_names(self, previous_names):
        self.previous_names = previous_names
        return self

    def __str__(self):
        return "<SlackChannel object id: {}, created: {}, name: {}, topic: {}, purpose: {}, num_members: {}>".format(self.id, self.created, self.name, self.topic, self.purpose, self.num_members)

    def __repr__(self):
        return self.__str__()


"""
SlackInstantMessage :
- models instant message (im)
"""
class SlackInstantMessage(SlackConversation):

    def __init__(self, id, created, user):
        SlackConversation.__init__(self, id, created)
        self.user = user

        self.is_org_shared = None
        self.is_user_deleted = None
        self.priority = None

    def set_is_org_shared(self, is_org_shared):
        self.is_org_shared = is_org_shared
        return self

    def set_is_user_deleted(self, is_user_deleted):
        self.is_user_deleted = is_user_deleted
        return self

    def set_priority(self, priority):
        self.priority = priority
        return self

    def __str__(self):
        return "<SlackInstantMessage object id: {}, created: {}, user: {}>".format(self.id, self.created, self.user)

    def __repr__(self):
        return self.__str__()


"""
SlackMessage :
- models a slack message
- either in a channel or instant message
"""
class SlackMessage(object):

    def __init__(self, type, text, ts):
        self.type = type
        self.text = text
        self.ts = ts

        self.user = None
        self.subtype = None
        self.file = None
        self.upload = None
        self.username = None

    def set_user(self, user):
        self.user = user
        return self

    def set_subtype(self, subtype):
        self.subtype = subtype
        return self

    def set_file(self, file):
        self.file = file
        return self

    def set_upload(self, upload):
        self.upload = upload
        return self

    def set_username(self, username):
        self.username = username
        return self

    def __str__(self):
        if self.subtype == "file_share":
            return "<SlackMessage object type: {}, text: {}, file: {}, ts: {}>".format(self.type, self.text, self.file, self.ts)
        else:
            return "<SlackMessage object type: {}, text: {}, ts: {}>".format(self.type, self.text, self.ts)

    def __repr__(self):
        return self.__str__()


"""
SlackFile :
- file upload in a message
"""
class SlackFile(object):

    def __init__(self, id, created, name, filetype, user):
        self.id = id
        self.created = created
        self.name = name
        self.filetype = filetype
        self.user = user

        self.timestamp = None
        self.title = None
        self.mimetype = None
        self.is_public = None
        self.public_url_shared = None
        self.url_private_download = None
        self.channels = None
        self.comments_count = None

    def set_timestamp(self, timestamp):
        self.timestamp = id
        return self

    def set_title(self, title):
        self.title = title
        return self

    def set_mimetype(self, mimetype):
        self.mimetype = mimetype
        return self

    def set_is_public(self, is_public):
        self.is_public = is_public
        return self

    def set_public_url_shared(self, public_url_shared):
        self.public_url_shared = public_url_shared
        return self

    def set_url_private_download(self, url_private_download):
        self.url_private_download = url_private_download
        return self

    def set_channels(self, channels):
        self.channels = channels
        return self

    def set_comments_count(self, comments_count):
        self.comments_count = comments_count
        return self

    def __str__(self):
        return "<SlackFile object id: {}, created: {}, name: {}, filetype:{}>".format(self.id, self.created, self.name, self.filetype)

    def __repr__(self):
        return self.__str__()


"""
SlackUser :
- models a slack user
"""
class SlackUser(object):

    def __init__(self, id, team_id, name, real_name):
        self.id = id
        self.team_id = team_id
        self.name = name
        self.real_name = real_name

        self.deleted = None
        self.is_admin = None

    def set_deleted(self, deleted):
        self.deleted = deleted
        return self

    def set_is_admin(self, is_admin):
        self.is_admin = is_admin
        return self

    def __str__(self):
        return "<SlackUser object id: {}, team_id: {}, name: {}, real_name:{}>".format(self.id, self.team_id, self.name, self.real_name)

    def __repr__(self):
        return self.__str__()
