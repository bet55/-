from lists.models import Sticker as StickerModel, AppUser, Film, Sticker
from lists.serializers import StickerSerializer
from collections import defaultdict

from pydantic_models import RateMovieRequestModel


class Note:
    @classmethod
    def get_all_notes(cls) -> dict[int, list]:
        notes = defaultdict(list)

        raw_notes = StickerModel.mgr.all()
        serialize = StickerSerializer(raw_notes, many=True)

        for note in serialize.data:
            notes[note['film']].append(note)

        return dict(notes)

    @classmethod
    def create_note(cls, note_body: dict):
        modeling = RateMovieRequestModel(**note_body)
        formated_request = modeling.model_dump(exclude_none=True, exclude_defaults=True, exclude_unset=True)

        # formated_request['user'] = AppUser.objects.get(id=formated_request['user'])
        # formated_request['film'] = Film.mgr.get(kp_id=formated_request['film'])

        user = AppUser.objects.get(id=formated_request['user'])
        film = Film.mgr.get(kp_id=formated_request['film'])
        rating = formated_request['rating']

        # Todo Хак, нужно переписать на create_or_update
        sticky_model = [Sticker(user=user, film=film, rating=rating)]

        res = Sticker.mgr.bulk_create(sticky_model,
                                                        update_conflicts=True,
                                                        update_fields=['rating', 'text'],
                                                        unique_fields=['film', 'user'])
        return True
