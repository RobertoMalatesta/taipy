# Copyright 2023 Avaiga Private Limited
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

from typing import Type

from taipy.config import Config

from .._manager._manager_factory import _ManagerFactory
from ..common._utils import _load_fct
from ._scenario_fs_repository import _ScenarioFSRepository
from ._scenario_manager import _ScenarioManager
from ._scenario_sql_repository import _ScenarioSQLRepository


class _ScenarioManagerFactory(_ManagerFactory):

    __REPOSITORY_MAP = {"default": _ScenarioFSRepository, "sql": _ScenarioSQLRepository}

    @classmethod
    def _build_repository(cls):
        return cls.__REPOSITORY_MAP.get(Config.global_config.repository_type, cls.__REPOSITORY_MAP.get("default"))()

    @classmethod
    def _build_manager(cls) -> Type[_ScenarioManager]:  # type: ignore
        if cls._using_enterprise():
            scenario_manager = _load_fct(
                cls._TAIPY_ENTERPRISE_CORE_MODULE + ".scenario._scenario_manager", "_ScenarioManager"
            )  # type: ignore
            build_repository = _load_fct(
                cls._TAIPY_ENTERPRISE_CORE_MODULE + ".scenario._scenario_manager", "_build_repository"
            )  # type: ignore
        else:
            scenario_manager = _ScenarioManager
            build_repository = cls._build_repository
        scenario_manager._repository = build_repository()  # type: ignore
        return _ScenarioManager
