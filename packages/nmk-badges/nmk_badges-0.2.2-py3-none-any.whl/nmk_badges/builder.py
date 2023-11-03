"""
Python module for **nmk-badges** builders.
"""

from typing import Dict, List

from nmk.model.builder import NmkTaskBuilder
from nmk.utils import is_condition_set


class NmkBadgesBuilder(NmkTaskBuilder):
    """
    Builder for **badges** task.
    """

    def build(self, badges: List[Dict[str, str]], begin_pattern: str, end_pattern: str):
        """
        Build logic for **badges** task:

        * looks for the begin/end patterns in the input file
        * replace lines between them by generated ones for configured badges
        * skip badges when "if" or "unless" condition is not met
        * touch the output stamp file

        :param badges: List of configured badges to be inserted
        :param begin_pattern: Begin pattern to look for in input file
        :param end_pattern: End pattern to look for in input file
        """

        # Read lines from target file
        with self.main_input.open() as f:
            all_lines = f.readlines()

        # Check for patterns
        begin_index, end_index = None, None
        for index, some_line in enumerate(all_lines):
            if begin_pattern in some_line and begin_index is None:
                begin_index = index
            elif end_pattern in some_line and begin_index is not None:
                end_index = index
                break

        # Index found?
        if begin_index is not None and end_index is not None and end_index > begin_index:
            # Browse required badges
            new_lines = all_lines[: begin_index + 1]
            for badge in badges:
                # Check for conditions
                ok_to_insert = True
                for condition, expected in [("if", True), ("unless", False)]:
                    if condition in badge and (is_condition_set(badge[condition]) != expected):
                        # Condition not met: skip this badge insertion
                        self.logger.debug(f"Skipped bad generation for '{badge['alt']}': {condition} condition not met")  # NOQA:B028
                        ok_to_insert = False
                        break

                # Insert badge
                if ok_to_insert:
                    new_lines.append(f"[![{badge['alt']}]({badge['img']})]({badge['url']})\n")
            new_lines.extend(all_lines[end_index:])

            # Write updated lines
            with self.main_input.open("w") as f:
                f.writelines(new_lines)

            # Touch the stamp file
            self.main_output.touch()
        else:
            self.logger.warning(f"Invalid or missing pattern in {self.main_input.name} file")
