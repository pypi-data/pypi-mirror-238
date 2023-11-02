# Copyright 2023 Google LLC
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

from dataclasses import dataclass
from typing import Any, List, Optional, Sequence, Union
import re

from .exclusion_specification import BaseExclusionSpecification, SpecificationFactory


@dataclass(frozen=True)
class Rule:
    exclusion_type: str
    exclusion_rule: str


class RulesParser:

    def __init__(self):
        self.spec_factory = SpecificationFactory()

    def generate_specifications(
        self, raw_rules: Union[str, Sequence[str]]
    ) -> Optional[List[List[BaseExclusionSpecification]]]:
        if not raw_rules:
            return None
        parsed_rules = self.generate_rules(raw_rules)
        specifications = []
        for rules in parsed_rules:
            specification_entry = []
            for rule in rules:
                specification_entry.append(
                    self.spec_factory.create_specification(
                        rule.exclusion_type, rule.exclusion_rule))
            specifications.append(specification_entry)
        return specifications

    def generate_rules(
            self, raw_rules: Union[str, Sequence[str]]) -> List[List[Rule]]:
        rules = []
        default_exclusion_type = "GOOGLE_ADS_INFO"
        if isinstance(raw_rules, str):
            raw_rules = self._format_raw_rules(raw_rules)
        for rule in raw_rules:
            current_exclusion_type = None
            if "," in rule:
                types = rule.split(",")
            else:
                types = rule.split(" AND ")
            rule_entry = []
            for type_ in types:
                spec_ = type_.split(":")
                if len(spec_) == 1:
                    if not current_exclusion_type:
                        exclusion_type = default_exclusion_type
                    else:
                        exclusion_type = str(current_exclusion_type)
                    expression_position = 0
                else:
                    exclusion_type = spec_[0]
                    expression_position = 1
                current_exclusion_type = str(exclusion_type)
                exclusion_rule = spec_[expression_position].rstrip()
                rule_entry.append(Rule(exclusion_type, exclusion_rule))
            rules.append(rule_entry)
        return rules

    def _format_raw_rules(self, raw_rules: str) -> List[str]:
        # remove brackets
        raw_rules = re.sub("[(|)]", "", raw_rules)
        # add whitespace in front of operators
        raw_rules = re.sub("([>|<|>=|<=|!=|=])", r" \1 ", raw_rules)
        # split rules by OR operator
        raw_rules = re.sub(" +", " ", raw_rules)
        return raw_rules.split(" OR ")
