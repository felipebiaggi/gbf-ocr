from typing import List, Tuple
from gbf_automata.schema.image import ImageModel
from gbf_automata.schema.display import DisplayModel
from gbf_automata.enums.template_match import TemplateMatch


class GameArea:
    def __init__(
        self,
        aspect_ratio: dict,
        top: ImageModel,
        bottom: ImageModel,
    ) -> None:
        self.top = top
        self.bottom = bottom
        self.aspect_ratio = DisplayModel(**aspect_ratio)

    # Display
    ##########################################################################
    #               (top)
    #                 |
    #                 |
    #                 v  (Game Area)
    #       (left) -> +--------------+
    #                 |              |
    #                 |              |
    #                 |              |
    #                 |              |
    #                 |              |
    #                 |              |
    #                 |              |
    #                 |              |
    #                 +--------------+
    #
    #
    #

    def area(self) -> dict:
        top_loc = self.top.max_loc
        bottom_loc = self.bottom.max_loc

        if self.top.method in [
            TemplateMatch.TM_SQDIFF,
            TemplateMatch.TM_SQDIFF_NORMED,
        ]:
            top_loc = self.top.min_loc
            bottom_loc = self.bottom.min_loc

        return {
            "top": self.aspect_ratio.top + top_loc[1],
            "left": self.aspect_ratio.left + top_loc[0],
            "width": self.aspect_ratio.width
            - (self.aspect_ratio.width - (bottom_loc[0] + self.bottom.image_width))
            - top_loc[0],
            "height": self.aspect_ratio.height
            - (self.aspect_ratio.height - (bottom_loc[1] + self.bottom.image_height))
            - top_loc[1],
        }

    def accuracy(self) -> List[Tuple[str, float]]:
        return [("top", self.top.accuracy()), ("bottom", self.bottom.accuracy())]

    def display_area(self) -> dict:
        return {
            "top": self.aspect_ratio.top,
            "left": self.aspect_ratio.left,
            "width": self.aspect_ratio.width,
            "height": self.aspect_ratio.height,
        }

    def correction(self) -> Tuple[float, float]:
        top_loc = self.top.max_loc

        if self.top.method in [
            TemplateMatch.TM_SQDIFF,
            TemplateMatch.TM_SQDIFF_NORMED,
        ]:
            top_loc = self.top.min_loc

        return (self.aspect_ratio.left + top_loc[0], self.aspect_ratio.top + top_loc[1])
