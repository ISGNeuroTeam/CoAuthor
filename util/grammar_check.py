import language_tool_python


def download_tool():
    return language_tool_python.LanguageTool('ru')


def find_mistakes(s, tool):
    return tool.check(s)


def correct(s, matches):
    return language_tool_python.utils.correct(s, matches)


def print_match(match):
    context = match.context + "\n\r"
    error_flag = " " * match.offsetInContext + "^" * match.errorLength + "\n\r"
    message = match.message
    return context, error_flag, message
