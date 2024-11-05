from lists.models import Sticker as StickerModel
from lists.serializers import StickerSerializer


class Note:
    def get_all_stickers(self):
        raw_notes = StickerModel.mgr.all().values()
        serialize = StickerSerializer(raw_notes, many=True)

        notes = {s['movie']: s for s in serialize.data}
        return notes
