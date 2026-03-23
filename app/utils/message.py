def build_message(
    action: str,
    resource: str,
    count: int | None = None
) -> str:
    """
    Generate consistent API messages.

    action: create | get | list | update | delete
    resource: Book, Category, Publisher, etc.
    count: used only for list responses
    """

    actions = {
        "create": "created",
        "get": "retrieved",
        "list": "retrieved",
        "update": "updated",
        "delete": "deleted"
    }

    if action not in actions:
        raise ValueError(f"Invalid action: {action}")

    # Handle list separately
    if action == "list":
        if count is not None:
            return f"{count} {resource}s retrieved successfully"
        return f"{resource}s retrieved successfully"

    return f"{resource} {actions[action]} successfully"