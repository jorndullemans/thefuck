import pytest
from thedick.argument_parser import Parser
from thedick.const import ARGUMENT_PLACEHOLDER


def _args(**override):
    args = {'alias': None, 'command': [], 'yes': False,
            'help': False, 'version': False, 'debug': False,
            'force_command': None, 'repeat': False,
            'enable_experimental_instant_mode': False,
            'shell_logger': None}
    args.update(override)
    return args


@pytest.mark.parametrize('argv, result', [
    (['thedick'], _args()),
    (['thedick', '-a'], _args(alias='dick')),
    (['thedick', '--alias', '--enable-experimental-instant-mode'],
     _args(alias='dick', enable_experimental_instant_mode=True)),
    (['thedick', '-a', 'fix'], _args(alias='fix')),
    (['thedick', 'git', 'branch', ARGUMENT_PLACEHOLDER, '-y'],
     _args(command=['git', 'branch'], yes=True)),
    (['thedick', 'git', 'branch', '-a', ARGUMENT_PLACEHOLDER, '-y'],
     _args(command=['git', 'branch', '-a'], yes=True)),
    (['thedick', ARGUMENT_PLACEHOLDER, '-v'], _args(version=True)),
    (['thedick', ARGUMENT_PLACEHOLDER, '--help'], _args(help=True)),
    (['thedick', 'git', 'branch', '-a', ARGUMENT_PLACEHOLDER, '-y', '-d'],
     _args(command=['git', 'branch', '-a'], yes=True, debug=True)),
    (['thedick', 'git', 'branch', '-a', ARGUMENT_PLACEHOLDER, '-r', '-d'],
     _args(command=['git', 'branch', '-a'], repeat=True, debug=True)),
    (['thedick', '-l', '/tmp/log'], _args(shell_logger='/tmp/log')),
    (['thedick', '--shell-logger', '/tmp/log'],
     _args(shell_logger='/tmp/log'))])
def test_parse(argv, result):
    assert vars(Parser().parse(argv)) == result
