

def clear_layout(layout):
    """
    Clears all widgets from the given QLayout.

    Args:
        layout (QLayout): The QLayout to be cleared.

    Returns:
        None
    """
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget:
            widget.deleteLater()
