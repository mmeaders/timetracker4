"""Time calculation and formatting utilities."""


def format_elapsed_time(seconds: int) -> str:
    """
    Format elapsed seconds into HH:MM:SS format.

    Args:
        seconds: Total elapsed seconds

    Returns:
        Formatted string (e.g., "02:35:42")
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def format_short_time(seconds: int) -> str:
    """
    Format elapsed seconds into a compact format.

    Args:
        seconds: Total elapsed seconds

    Returns:
        Formatted string (e.g., "2h 35m", "45m", "30s")
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    if hours > 0:
        return f"{hours}h {minutes}m"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"


def format_datetime_short(timestamp: int) -> str:
    """
    Format Unix timestamp into a short date/time string.

    Args:
        timestamp: Unix timestamp

    Returns:
        Formatted string (e.g., "12/03 09:15")
    """
    from datetime import datetime
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime("%m/%d %H:%M")


def format_datetime_full(timestamp: int) -> str:
    """
    Format Unix timestamp into a full date/time string.

    Args:
        timestamp: Unix timestamp

    Returns:
        Formatted string (e.g., "2024-12-03 09:15:42")
    """
    from datetime import datetime
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime("%Y-%m-%d %H:%M:%S")
