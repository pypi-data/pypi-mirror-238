from volstreet import config


def set_large_order_threshold(threshold: int) -> None:
    config.LARGE_ORDER_THRESHOLD = threshold


def set_error_notification_settings(key, value) -> None:
    config.ERROR_NOTIFICATION_SETTINGS[key] = value


def set_notifier_level(level: str) -> None:
    config.NOTIFIER_LEVEL = level


def set_price_limit_buffer(buffer: float) -> None:
    config.LIMIT_PRICE_BUFFER = buffer
