# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Optional, List, Sequence
import re
import logging

from .external_parsers.base_parser import NullParser
from .external_parsers.website_parser import WebSiteParser
from .external_parsers.youtube_data_parser import ChannelInfoParser, VideoInfoParser
from .enums import PlacementTypeEnum, ExclusionTypeEnum

PARSEABLE = ("WEBSITE", "YOUTUBE_VIDEO", "YOUTUBE_CHANNEL")


class BaseExclusionSpecification:

    def __init__(self,
                 expression: str,
                 exclusion_type: Optional[ExclusionTypeEnum] = None,
                 parser=NullParser,
                 placement_type: Optional[PlacementTypeEnum] = None,
                 repository_name: Optional[str] = None):
        """Constructor for the class.

        Args:
            expression: exclusion expression in a form of `name > value`
            exclusion_type: type of the exclusion
            parser: parser for getting data from API and/or DB
        """
        elements = [element.strip() for element in expression.split(" ")]
        if len(elements) != 3:
            raise ValueError(
                "Incorrect expression, specify in 'name > value' format")
        if elements[1] not in (">", ">=", "<", "<=", "=", "!=", "regexp", "contains"):
            raise ValueError(
                "Incorrect operator for expression, "
                "only '>', '>=', '<', '<=', '=', '!=', 'regexp', 'contains' are supported")

        self.name = elements[0]
        self.operator = "==" if elements[1] == "=" else elements[1]
        self.value = elements[2].replace("'", "").replace('"', '')
        self.exclusion_type = exclusion_type
        self.parser = parser
        self.corresponding_placement_type = placement_type
        self.repository_name = repository_name

    def is_satisfied_by(self, placement_info, uow=None) -> bool:
        with uow:
            if (placement_info.placement_type in PARSEABLE and
                    self.exclusion_type != ExclusionTypeEnum.GOOGLE_ADS_INFO):
                placement = getattr(uow, self.repository_name).get_by_name(
                    placement_info.placement)
            else:
                placement = placement_info
            if not hasattr(placement, self.name):
                raise ValueError(f"{self.name} is not found!")
            if hasattr(placement,
                       "is_processed") and not placement.is_processed:
                logging.warning(
                    "Cannot get internal information on %s placement of type %s",
                    placement_info.placement, placement_info.placement_type)
                return False
            else:
                if self.operator in ("regexp", "contains"):
                    return self._check_regexp(placement)
                return self._eval_expression(placement)

    def _check_regexp(self, placement) -> bool:
        if placement_element := getattr(placement, self.name):
            return bool(re.search(fr"{self.value}", placement_element,
                                  re.IGNORECASE))
        else:
            return False

    def _eval_expression(self, placement):
        try:
            value = float(self.value)
        except ValueError:
            value = self.value
        if isinstance(value, float):
            return eval(
                f"{getattr(placement, self.name)}{self.operator} {value}")
        return eval(
            f"'{getattr(placement, self.name)}' {self.operator} '{value}'")

    def __str__(self):
        return f"{self.exclusion_type.name}:{self.name} {self.operator} {self.value}"

    def __repr__(self):
        return f"{self.__class__.__name__}(exclusion_type='{self.exclusion_type.name}', name='{self.name}', operator='{self.operator}', value='{self.value}')"

    def __eq__(self, other):
        return (self.exclusion_type, self.name, self.operator,
                self.value) == (other.exclusion_type, other.name,
                                other.operator, other.value)


class AdsExclusionSpecification(BaseExclusionSpecification):
    """Class for specifying exclusion rules."""

    def __init__(self, expression):
        super().__init__(expression,
                         exclusion_type=ExclusionTypeEnum.GOOGLE_ADS_INFO)


class ContentExclusionSpecification(BaseExclusionSpecification):

    def __init__(self, expression) -> None:
        super().__init__(expression=expression,
                         exclusion_type=ExclusionTypeEnum.WEBSITE_INFO,
                         parser=WebSiteParser,
                         placement_type=PlacementTypeEnum.WEBSITE,
                         repository_name="website_info")


class YouTubeChannelExclusionSpecification(BaseExclusionSpecification):

    def __init__(self, expression) -> None:
        super().__init__(expression=expression,
                         exclusion_type=ExclusionTypeEnum.YOUTUBE_CHANNEL_INFO,
                         parser=ChannelInfoParser,
                         placement_type=PlacementTypeEnum.YOUTUBE_CHANNEL,
                         repository_name="youtube_channel_info")


class YouTubeVideoExclusionSpecification(BaseExclusionSpecification):

    def __init__(self, expression) -> None:
        super().__init__(expression=expression,
                         exclusion_type=ExclusionTypeEnum.YOUTUBE_VIDEO_INFO,
                         parser=VideoInfoParser,
                         placement_type=PlacementTypeEnum.YOUTUBE_VIDEO,
                         repository_name="youtube_video_info")


class Specification:

    def __init__(self, uow=None):
        self.uow = uow
        self.allowed_placement_types = set([p.name for p in PlacementTypeEnum])

    def satisfies(self, specs: Sequence[Sequence[BaseExclusionSpecification]],
                  placement) -> List[str]:
        rules_satisfied: List[str] = []
        for spec_entry in specs:
            spec_satisfied: List[str] = []
            for spec in spec_entry:
                if spec.exclusion_type != ExclusionTypeEnum.GOOGLE_ADS_INFO:
                    formatted_exclusion_type = spec.exclusion_type.name.replace(
                        "_INFO", "")
                    if formatted_exclusion_type != placement.placement_type:
                        continue
                if spec.is_satisfied_by(placement, self.uow):
                    spec_satisfied.append(str(spec))
                    continue
                else:
                    break
            if spec_satisfied:
                rules_satisfied.append(spec_satisfied)
        return rules_satisfied 


class NullSpecification(BaseExclusionSpecification):

    def __init__(self, type, expression):
        super().__init__(type)
        raise ValueError(f"Incorrect type of rule: {type}")


class SpecificationFactory:

    def create_specification(self, type: str,
                             condition: str) -> BaseExclusionSpecification:
        if type == "GOOGLE_ADS_INFO":
            return AdsExclusionSpecification(condition)
        if type == "WEBSITE_INFO":
            return ContentExclusionSpecification(condition)
        if type == "YOUTUBE_CHANNEL_INFO":
            return YouTubeChannelExclusionSpecification(condition)
        if type == "YOUTUBE_VIDEO_INFO":
            return YouTubeVideoExclusionSpecification(condition)
        else:
            return NullSpecification(type, condition)
