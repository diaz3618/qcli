COLOR_MAP = {
    'error': '\033[31m',
    'missingFiles': '\033[91m',
    'uploading': '\033[34m',
    'stoppedUP': '\033[90m',
    'queuedUP': '\033[94m',
    'stalledUP': '\033[36m',
    'checkingUP': '\033[96m',
    'forcedUP': '\033[1;34m',
    'downloading': '\033[32m',
    'metaDL': '\033[36m',
    'forcedMetaDL': '\033[1;36m',
    'stoppedDL': '\033[90m',
    'queuedDL': '\033[92m',
    'stalledDL': '\033[36m',
    'checkingDL': '\033[96m',
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
