"""Contains global helper functions for general application tasks"""
import os

def try_except(key_to_check, failure, *exceptions):
    """Checks for env_vars or returns the default"""
    try:
        return os.environ[key_to_check]
    except KeyError:
        return failure
