from copy import deepcopy
from logging import getLogger

from langkit.pattern_loader import PatternLoader
from whylogs.experimental.core.udf_schema import register_dataset_udf, _multicolumn_udfs
from . import LangKitConfig, lang_config, prompt_column, response_column
from whylogs.core.stubs import pd
from typing import Dict, List, Optional, Set, Union

diagnostic_logger = getLogger(__name__)


pattern_loader = PatternLoader()
response_pattern_loader = PatternLoader()


def count_patterns(group, text: str) -> int:
    count = 0
    for expression in group["expressions"]:
        if expression.search(text):
            count += 1

    return count


def wrapper(pattern_group, column):
    def wrappee(text: Union[pd.DataFrame, Dict[str, List]]) -> Union[pd.Series, List]:
        return [count_patterns(pattern_group, input) for input in text[column]]

    return wrappee


_registered: Set[str] = set()


def _unregister(language: str):
    # WARNING: Uses private whylogs internals. Do not copy this code.
    # TODO: Add proper whylogs API to support this.

    global _registered
    _multicolumn_udfs[language] = [
        u
        for u in _multicolumn_udfs[language]
        if list(u.udfs.keys())[0] not in _registered
    ]
    _registered = set()


def _register_udfs(language: str):
    global _registered
    _unregister(language)
    regex_groups = pattern_loader.get_regex_groups()
    if regex_groups is not None:
        column = prompt_column
        for group in regex_groups:
            udf_name = f"{column}.{group['name']}_count"
            register_dataset_udf(
                [column],
                udf_name=udf_name,
                schema_name=language,
            )(wrapper(group, column))
            _registered.add(udf_name)

    regex_groups = response_pattern_loader.get_regex_groups()
    if regex_groups is not None:
        column = response_column
        for group in regex_groups:
            udf_name = f"{column}.{group['name']}_count"
            register_dataset_udf(
                [column],
                udf_name=udf_name,
                schema_name=language,
            )(wrapper(group, column))
            _registered.add(udf_name)


def init(
    language: str = "",
    pattern_file_path: Optional[str] = None,
    config: Optional[LangKitConfig] = None,
    response_pattern_file_path: Optional[str] = None,
):
    config = deepcopy(config or lang_config)
    if pattern_file_path:
        config.pattern_file_path = pattern_file_path
    if response_pattern_file_path:
        config.response_pattern_file_path = response_pattern_file_path
    global pattern_loader, response_pattern_loader
    pattern_loader = PatternLoader(config.pattern_file_path)
    response_pattern_loader = PatternLoader(config.response_pattern_file_path)
    _register_udfs(language)
