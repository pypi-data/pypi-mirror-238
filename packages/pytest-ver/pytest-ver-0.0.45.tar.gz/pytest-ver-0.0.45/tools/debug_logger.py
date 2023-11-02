import sys


# -------------------
## Holds all info for logging debug lines
class DebugLogger:
    # -------------------
    ## write a "line" line with the given message
    #
    # @param msg   the message to write
    # @return None
    @staticmethod
    def line(msg):
        DebugLogger._write_line(' ', msg)

    # -------------------
    ## write a "ok" line with the given message
    #
    # @param msg   the message to write
    # @return None
    @staticmethod
    def ok(msg):
        DebugLogger._write_line('OK', msg)

    # -------------------
    ## write a "err" line with the given message
    #
    # @param msg   the message to write
    # @return None
    @staticmethod
    def err(msg):
        DebugLogger._write_line('ERR', msg)

    # -------------------
    ## write a "err" line with the given message
    #
    # @param msg   the message to write
    # @return None
    @staticmethod
    def dbg(msg):
        DebugLogger._write_line('DBG', msg)

    # -------------------
    ## write the given line to stdout
    #
    # @param tag   the prefix tag
    # @param msg   the message to write
    # @return None
    @staticmethod
    def _write_line(tag, msg):
        print(f'{tag: <4} {msg}')  # print okay
        sys.stdout.flush()
