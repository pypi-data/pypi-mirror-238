from rich import traceback as tb, inspect
tb.install(show_locals=False, suppress=['click', 'rich', 'requests', 'urllib3'])

