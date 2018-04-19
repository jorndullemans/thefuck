import re
from thedick.shells import shell
from thedick.specific.git import git_support
from thedick.system import Path
from thedick.utils import memoize


@memoize
def _get_missing_file(command):
    pathspec = re.findall(
        r"error: pathspec '([^']*)' "
        r'did not match any file\(s\) known to git.', command.output)[0]
    if Path(pathspec).exists():
        return pathspec


@git_support
def match(command):
    return ('did not match any file(s) known to git.' in command.output
            and _get_missing_file(command))


@git_support
def get_new_command(command):
    missing_file = _get_missing_file(command)
    formatme = shell.and_('git add -- {}', '{}')
    return formatme.format(missing_file, command.script)
