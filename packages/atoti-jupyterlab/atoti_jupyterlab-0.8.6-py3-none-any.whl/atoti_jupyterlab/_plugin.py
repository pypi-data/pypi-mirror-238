from atoti_core import BaseSessionBound, Plugin
from typing_extensions import override

from ._notebook import Notebook
from ._widget import Widget


class JupyterLabPlugin(Plugin):
    _notebook = Notebook()

    @override
    def post_init_session(self, session: BaseSessionBound, /) -> None:
        def create_widget() -> object:
            return Widget(
                cell=self._notebook.current_cell,
                running_in_supported_kernel=self._notebook.running_in_supported_kernel,
                session=session,
            )

        session._create_widget = create_widget
