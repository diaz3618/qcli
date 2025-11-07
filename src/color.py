COLOR_MAP = {
    'error': '\033[31m',              # Red
    'missingFiles': '\033[91m',       # Bright Red
    'uploading': '\033[34m',          # Blue
    'stoppedUP': '\033[90m',          # Bright Black (Gray)
    'queuedUP': '\033[94m',           # Bright Blue
    'stalledUP': '\033[36m',          # Cyan
    'checkingUP': '\033[96m',         # Bright Cyan
    'forcedUP': '\033[1;34m',         # Bold Blue
    'downloading': '\033[32m',        # Green
    'metaDL': '\033[36m',             # Cyan
    'forcedMetaDL': '\033[1;36m',     # Bold Cyan
    'stoppedDL': '\033[90m',          # Bright Black (Gray)
    'queuedDL': '\033[92m',           # Bright Green
    'stalledDL': '\033[36m',          # Cyan
    'checkingDL': '\033[96m',         # Bright Cyan
    'forcedDL': '\033[1;32m',         # Bold Green
    'checkingResumeData': '\033[95m', # Magenta
    'moving': '\033[93m',             # Yellow
    'completed': '\033[35m',          # Magenta
    'pausedDL': '\033[33m',           # Yellow
    'pausedUP': '\033[33m',           # Yellow
    'unknown': '\033[37m',            # White
}
RESET = '\033[0m'

def color_state(state: str) -> str:
    color = COLOR_MAP.get(state, '')
    if color:
        return f"{color}{state:<16}{RESET}"
    return f"{state:<16}"
