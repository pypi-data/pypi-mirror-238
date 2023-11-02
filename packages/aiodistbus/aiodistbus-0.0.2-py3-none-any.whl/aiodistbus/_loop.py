import asyncio
import sys


def setup():
    """Setup event loop policy according to platform"""
    if sys.platform in ["win32", "cygwin", "cli"]:
        import winloop

        asyncio.set_event_loop_policy(winloop.WinLoopPolicy())
    else:  # linux or macos
        import uvloop

        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
