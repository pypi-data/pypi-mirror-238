import multiprocessing
from dataclasses import dataclass
from multiprocessing.context import SpawnProcess
from pathlib import Path
from time import sleep
from typing import TYPE_CHECKING
from typing import Any
from typing import TypeAlias

from amsdal_data.table_schemas.manager import TableSchemasManager
from amsdal_framework.configs.main import settings
from amsdal_framework.errors import AmsdalRuntimeError
from amsdal_framework.manager import AmsdalManager
from amsdal_framework.schemas.manager import SchemaManager
from amsdal_models.classes.manager import ClassManager
from amsdal_server.server import start
from amsdal_utils.classes.version_manager import ClassVersionManager
from amsdal_utils.config.manager import AmsdalConfigManager
from rich import print
from watchfiles import run_process
from watchfiles.filters import PythonFilter

from amsdal_cli.commands.serve.filters.models_watch_filter import ModelsWatchFilter
from amsdal_cli.commands.serve.filters.static_files_watch_filter import StaticFilesWatchFilter

spawn_context = multiprocessing.get_context('spawn')

START_SERVER_EVENT = 'start_server'
STOP_SERVER_EVENT = 'stop_server'

if TYPE_CHECKING:
    QueueType: TypeAlias = multiprocessing.Queue[str]
else:
    QueueType: TypeAlias = multiprocessing.Queue


@dataclass
class ProcessState:
    server: SpawnProcess | None = None
    watch_models: SpawnProcess | None = None
    watch_static_files: SpawnProcess | None = None
    watch_fixtures: SpawnProcess | None = None
    watch_transactions: SpawnProcess | None = None


class Supervisor:
    def __init__(
        self,
        app_source_path: Path,
        output_path: Path,
        config_path: Path,
    ) -> None:
        self._app_source_path: Path = app_source_path
        self._output_path: Path = output_path
        self._config_path: Path = config_path
        self._process_state: ProcessState = ProcessState()
        self._queue: QueueType = spawn_context.Queue()

    def run(self) -> None:
        try:
            self.start()

            while True:
                sleep(0.1)
        except (KeyboardInterrupt, Exception):
            self.stop()

    def start(self) -> None:
        self._process_state.server = self._run_server(
            self._queue,
            self._output_path,
            self._config_path,
        )
        self._process_state.watch_models = self._run_watch_models(
            self._queue,
            self._app_source_path,
            self._output_path,
            self._config_path,
        )
        self._process_state.watch_static_files = self._run_watch_static_files(
            self._app_source_path,
            self._output_path,
            self._config_path,
        )
        self._process_state.watch_transactions = self._run_watch_transactions(
            self._app_source_path,
            self._output_path,
            self._config_path,
        )

    def stop(self) -> None:
        if self._process_state.server is not None and self._process_state.server.is_alive():
            self._process_state.server.terminate()

        if self._process_state.watch_models is not None and self._process_state.watch_models.is_alive():
            self._process_state.watch_models.terminate()

        if self._process_state.watch_static_files is not None and self._process_state.watch_static_files.is_alive():
            self._process_state.watch_static_files.terminate()

        if self._process_state.watch_transactions is not None and self._process_state.watch_transactions.is_alive():
            self._process_state.watch_transactions.terminate()

    def wait(self) -> None:
        if self._process_state.server is not None and self._process_state.server.is_alive():
            self._process_state.server.join()

        if self._process_state.watch_models is not None and self._process_state.watch_models.is_alive():
            self._process_state.watch_models.join()

        if self._process_state.watch_static_files is not None and self._process_state.watch_static_files.is_alive():
            self._process_state.watch_static_files.join()

        if self._process_state.watch_transactions is not None and self._process_state.watch_transactions.is_alive():
            self._process_state.watch_transactions.join()

    @classmethod
    def _run_server(
        cls,
        queue: QueueType,
        output_path: Path,
        config_path: Path,
    ) -> SpawnProcess:
        process = spawn_context.Process(
            target=cls._check_and_serve,
            kwargs={
                'queue': queue,
                'is_development_mode': False,
                'output_path': output_path,
                'config_path': config_path,
            },
        )
        process.start()

        return process

    @classmethod
    def _check_and_serve(
        cls,
        queue: QueueType,
        *,
        is_development_mode: bool,
        output_path: Path,
        config_path: Path,
    ) -> None:
        _server_process: SpawnProcess | None = None

        try:
            while True:
                event = queue.get()
                if event == STOP_SERVER_EVENT:
                    if _server_process is not None and _server_process.is_alive():
                        _server_process.terminate()
                elif event == START_SERVER_EVENT:
                    _server_process = spawn_context.Process(
                        target=cls._serve,
                        kwargs={
                            'is_development_mode': is_development_mode,
                            'output_path': output_path,
                            'config_path': config_path,
                        },
                    )
                    _server_process.start()
        except KeyboardInterrupt:
            if _server_process is not None and _server_process.is_alive():
                _server_process.terminate()

    @classmethod
    def _run_watch_models(
        cls,
        queue: QueueType,
        app_source_path: Path,
        output_path: Path,
        config_path: Path,
    ) -> SpawnProcess:
        process = spawn_context.Process(
            target=cls._watch,
            args=(
                'ModelsWatch',
                app_source_path / 'models',
            ),
            kwargs={
                'target': cls._build_models_and_migrate,
                'kwargs': {
                    'queue': queue,
                    'app_source_path': app_source_path,
                    'output_path': output_path,
                    'config_path': config_path,
                },
                'watch_filter': ModelsWatchFilter(),
            },
        )
        process.start()

        return process

    @classmethod
    def _run_watch_static_files(
        cls,
        app_source_path: Path,
        output_path: Path,
        config_path: Path,
    ) -> SpawnProcess:
        process = spawn_context.Process(
            target=cls._watch,
            args=(
                'StaticFilesWatch',
                app_source_path,
            ),
            kwargs={
                'target': cls._build_static_files,
                'kwargs': {
                    'app_source_path': app_source_path,
                    'output_path': output_path,
                    'config_path': config_path,
                },
                'watch_filter': StaticFilesWatchFilter(),
            },
        )
        process.start()

        return process

    @classmethod
    def _run_watch_transactions(
        cls,
        app_source_path: Path,
        output_path: Path,
        config_path: Path,
    ) -> SpawnProcess:
        process = spawn_context.Process(
            target=cls._watch,
            args=(
                'TransactionsWatch',
                app_source_path / 'transactions',
            ),
            kwargs={
                'target': cls._build_transactions_and_apply,
                'kwargs': {
                    'app_source_path': app_source_path,
                    'output_path': output_path,
                    'config_path': config_path,
                },
                'watch_filter': PythonFilter(),
            },
        )
        process.start()

        return process

    @classmethod
    def _serve(
        cls,
        output_path: Path,
        config_path: Path,
        **kwargs: Any,
    ) -> None:
        from amsdal_utils.lifecycle.consumer import LifecycleConsumer
        from amsdal_utils.lifecycle.enum import LifecycleEvent
        from amsdal_utils.lifecycle.producer import LifecycleProducer

        cls._invalidate_amsdal_state()

        class AmsdalInitConsumer(LifecycleConsumer):
            def on_event(self, *args: Any, **kwargs: Any) -> None:  # noqa: ARG002
                settings.override(APP_PATH=output_path)

                config_manager = AmsdalConfigManager()
                config_manager.load_config(config_path)

                amsdal_manager = AmsdalManager()
                amsdal_manager.setup()
                amsdal_manager.authenticate()
                amsdal_manager.init_class_versions()

        LifecycleProducer.add_listener(LifecycleEvent.ON_SERVER_STARTUP, AmsdalInitConsumer)
        start(**kwargs)

    @classmethod
    def _build_models_and_migrate(
        cls,
        queue: QueueType,
        app_source_path: Path,
        output_path: Path,
        config_path: Path,
    ) -> None:
        queue.put(STOP_SERVER_EVENT)
        cls._invalidate_amsdal_state()
        settings.override(APP_PATH=output_path)

        config_manager = AmsdalConfigManager()
        config_manager.load_config(config_path)

        amsdal_manager = AmsdalManager()
        amsdal_manager.pre_setup()

        print('[blue]Building models...[/blue]', end=' ')
        amsdal_manager.build_models(app_source_path / 'models')
        print('[green]OK![/green]')

        print('[blue]Apply migrations...[/blue]')
        amsdal_manager = AmsdalManager()
        amsdal_manager.setup()
        amsdal_manager.authenticate()
        amsdal_manager.migrate()
        print('[green]OK![/green]')

        print('[blue]Building fixtures...[/blue]', end=' ')
        amsdal_manager.build_fixtures(app_source_path / 'models')
        print('[green]OK![/green]')

        print('[blue]Applying fixtures...[/blue]', end=' ')
        amsdal_manager.apply_fixtures()
        print('[green]OK![/green]')

        queue.put(START_SERVER_EVENT)

    @staticmethod
    def _invalidate_amsdal_state() -> None:
        try:
            amsdal_manager = AmsdalManager()
            amsdal_manager.teardown()
        except AmsdalRuntimeError:
            ...

        AmsdalManager.invalidate()
        ClassManager.invalidate()
        ClassVersionManager.invalidate()
        SchemaManager.invalidate()
        TableSchemasManager.invalidate()

    @staticmethod
    def _build_static_files(
        app_source_path: Path,
        output_path: Path,
        config_path: Path,
    ) -> None:
        settings.override(APP_PATH=output_path)

        config_manager = AmsdalConfigManager()
        config_manager.load_config(config_path)

        amsdal_manager = AmsdalManager()
        amsdal_manager.pre_setup()

        print('[blue]Building static files...[/blue]', end=' ')
        amsdal_manager.build_static_files(app_source_path)
        print('[green]OK![/green]')

    @staticmethod
    def _build_transactions_and_apply(
        app_source_path: Path,
        output_path: Path,
        config_path: Path,
    ) -> None:
        settings.override(APP_PATH=output_path)

        config_manager = AmsdalConfigManager()
        config_manager.load_config(config_path)

        amsdal_manager = AmsdalManager()
        amsdal_manager.pre_setup()

        print('[blue]Building transactions...[/blue]', end=' ')
        amsdal_manager.build_transactions(app_source_path)
        print('[green]OK![/green]')

    @staticmethod
    def _watch(name: str, *args: Any, **kwargs: Any) -> None:
        try:
            run_process(*args, **kwargs)
        except KeyboardInterrupt:
            print(f'[yellow]Task {name} was gracefully stopped[/yellow]')
