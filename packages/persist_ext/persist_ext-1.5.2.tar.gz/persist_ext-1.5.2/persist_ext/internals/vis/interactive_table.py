from persist_ext.internals.data.prepare import prepare
from persist_ext.internals.data.validate import DEFAULT_PREPROCESS_FN
from persist_ext.internals.widgets.interactive_table.interactive_table_widget import (
    InteractiveTableWidget,
)
from persist_ext.internals.widgets.trrackable_output.output_with_trrack_widget import (
    OutputWithTrrackWidget,
)


def interactive_table(data, preprocess_fn=DEFAULT_PREPROCESS_FN):
    data = prepare(data, preprocess_fn)

    return OutputWithTrrackWidget(
        body_widget=InteractiveTableWidget(data=data), data=data
    )
