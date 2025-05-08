"""
Test configuration for pytest.
"""
import pytest
import tkinter as tk

@pytest.fixture(autouse=True)
def setup_teardown():
    """Setup and teardown for each test."""
    yield
    # Clean up any remaining Tk windows
    for widget in tk.Tk.winfo_children(tk._default_root) if tk._default_root else []:
        widget.destroy() 