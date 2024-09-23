from apps.campaigns.domain.entites import MegaDirection as Entity


class MegaDirection:
    @staticmethod
    def load_entities(service):
        mega_directions = service.pull("МАИ_МегаНаправления")
        for mega_direction in mega_directions:
            yield Entity(
                ref=mega_direction["Ref_Key"],
                name=mega_direction["Description"],
                number=mega_direction["Code"],
                active=not mega_direction["DeletionMark"],
            )
