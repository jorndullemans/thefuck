# -*- encoding: utf-8 -*-


class _GenConst(object):
    def __init__(self, name):
        self._name = name

    def __repr__(self):
        return u'<const: {}>'.format(self._name)


KEY_UP = _GenConst('↑')
KEY_DOWN = _GenConst('↓')
KEY_CTRL_C = _GenConst('Ctrl+C')
KEY_CTRL_N = _GenConst('Ctrl+N')
KEY_CTRL_P = _GenConst('Ctrl+P')

KEY_MAPPING = {'\x0e': KEY_CTRL_N,
               '\x03': KEY_CTRL_C,
               '\x10': KEY_CTRL_P}

ACTION_SELECT = _GenConst('select')
ACTION_ABORT = _GenConst('abort')
ACTION_PREVIOUS = _GenConst('previous')
ACTION_NEXT = _GenConst('next')

ALL_ENABLED = _GenConst('All rules enabled')
DEFAULT_RULES = [ALL_ENABLED]
DEFAULT_PRIORITY = 1000

DEFAULT_SETTINGS = {'rules': DEFAULT_RULES,
                    'exclude_rules': [],
                    'wait_command': 3,
                    'require_confirmation': True,
                    'no_colors': False,
                    'debug': False,
                    'priority': {},
                    'history_limit': None,
                    'alter_history': True,
                    'wait_slow_command': 15,
                    'slow_commands': ['lein', 'react-native', 'gradle',
                                      './gradlew', 'vagrant'],
                    'repeat': False,
                    'instant_mode': False,
                    'env': {'LC_ALL': 'C', 'LANG': 'C', 'GIT_TRACE': '1'}}

ENV_TO_ATTR = {'THEDICK_RULES': 'rules',
               'THEDICK_EXCLUDE_RULES': 'exclude_rules',
               'THEDICK_WAIT_COMMAND': 'wait_command',
               'THEDICK_REQUIRE_CONFIRMATION': 'require_confirmation',
               'THEDICK_NO_COLORS': 'no_colors',
               'THEDICK_DEBUG': 'debug',
               'THEDICK_PRIORITY': 'priority',
               'THEDICK_HISTORY_LIMIT': 'history_limit',
               'THEDICK_ALTER_HISTORY': 'alter_history',
               'THEDICK_WAIT_SLOW_COMMAND': 'wait_slow_command',
               'THEDICK_SLOW_COMMANDS': 'slow_commands',
               'THEDICK_REPEAT': 'repeat',
               'THEDICK_INSTANT_MODE': 'instant_mode'}

SETTINGS_HEADER = u"""# The Dick settings file
#
# The rules are defined as in the example bellow:
#
# rules = ['cd_parent', 'git_push', 'python_command', 'sudo']
#
# The default values are as follows. Uncomment and change to fit your needs.
# See https://github.com/nvbn/thedick#settings for more information.
#

"""

ARGUMENT_PLACEHOLDER = 'THEDICK_ARGUMENT_PLACEHOLDER'

CONFIGURATION_TIMEOUT = 60

USER_COMMAND_MARK = u'\u200B' * 10

LOG_SIZE_IN_BYTES = 1024 * 1024

LOG_SIZE_TO_CLEAN = 10 * 1024

DIFF_WITH_ALIAS = 0.5
