import sys
import click
import threading
from io import StringIO
import tkinter
from typing import Callable, Optional

class RedirectText:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.queue = []
        self.lock = threading.Lock()

    def write(self, string):
        # Schedule the update on the main GUI thread
        if string:
            self.text_widget.after(0, self._append_text, string)

    def flush(self):
        pass

    def _append_text(self, string):
        self.text_widget.configure(state="normal")
        self.text_widget.insert("end", string)
        self.text_widget.see("end")
        self.text_widget.configure(state="disabled")

class ClickPatcher:
    """
    Context manager to patch click.echo and click.confirm
    """
    def __init__(self, text_output_widget, confirm_callback: Callable[[str], bool]):
        self.text_output_widget = text_output_widget
        self.redirector = RedirectText(text_output_widget)
        self.confirm_callback = confirm_callback
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        self.original_echo = click.echo
        self.original_confirm = click.confirm

    def __enter__(self):
        sys.stdout = self.redirector
        sys.stderr = self.redirector
        
        # Patch click.echo mostly relies on stdout/print so sys.stdout covers most
        # But explicit patching acts as a safeguard
        def patched_echo(message=None, file=None, nl=True, err=False, color=None):
            if message is not None:
                print(str(message), end='\n' if nl else '')
        
        click.echo = patched_echo

        # Patch click.confirm
        def patched_confirm(text, default=False, abort=False, show_default=True):
            print(f"Requesting confirmation: {text}") 
            result = self.confirm_callback(text)
            if abort and not result:
                print("Aborted!")
                # In CLI abort raises Abort exception, we must mimic or handle it
                # For now let's just raise it to stop execution flow if needed, 
                # or better, just return False and let the caller handle it.
                # However, original commands typically effectively stop if confirmation fails.
                # 'abort=True' in click raises click.Abort().
                raise click.Abort()
            return result

        click.confirm = patched_confirm
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr
        click.echo = self.original_echo
        click.confirm = self.original_confirm
