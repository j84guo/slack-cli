class SlackViewer(object):

    def view_channels(self, channels):
        out = []
        for c in channels:
            out.append("id:{}, name: {}, created: {}\n".format(c.id, c.name, c.created))
        return "".join(out)

    def view_instant_messages(self, instant_messages):
        out = []
        for im in instant_messages:
            out.append("id: {}, user: {}, created: {}\n".format(im.id, im.user, im.created))
        return "".join(out)

    def view_history(self, history):
        out = []
        for m in history:
            out.append("type: {}, text: {}, ts: {}\n".format(m.type, m.text, m.ts))
        return "".join(out)
