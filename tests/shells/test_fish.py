# -*- coding: utf-8 -*-

import pytest
from thedick.shells import Fish


@pytest.mark.usefixtures('isfile', 'no_memoize', 'no_cache')
class TestFish(object):
    @pytest.fixture
    def shell(self):
        return Fish()

    @pytest.fixture(autouse=True)
    def Popen(self, mocker):
        mock = mocker.patch('thedick.shells.fish.Popen')
        mock.return_value.stdout.read.side_effect = [(
            b'cd\nfish_config\ndick\nfunced\nfuncsave\ngrep\nhistory\nll\nls\n'
            b'man\nmath\npopd\npushd\nruby'),
            b'alias fish_key_reader /usr/bin/fish_key_reader\nalias g git']
        return mock

    @pytest.mark.parametrize('key, value', [
        ('TF_OVERRIDDEN_ALIASES', 'cut,git,sed'),  # legacy
        ('THEDICK_OVERRIDDEN_ALIASES', 'cut,git,sed'),
        ('THEDICK_OVERRIDDEN_ALIASES', 'cut, git, sed'),
        ('THEDICK_OVERRIDDEN_ALIASES', ' cut,\tgit,sed\n'),
        ('THEDICK_OVERRIDDEN_ALIASES', '\ncut,\n\ngit,\tsed\r')])
    def test_get_overridden_aliases(self, shell, os_environ, key, value):
        os_environ[key] = value
        assert shell._get_overridden_aliases() == {'cd', 'cut', 'git', 'grep',
                                                   'ls', 'man', 'open', 'sed'}

    @pytest.mark.parametrize('before, after', [
        ('cd', 'cd'),
        ('pwd', 'pwd'),
        ('dick', 'fish -ic "dick"'),
        ('find', 'find'),
        ('funced', 'fish -ic "funced"'),
        ('grep', 'grep'),
        ('awk', 'awk'),
        ('math "2 + 2"', r'fish -ic "math \"2 + 2\""'),
        ('man', 'man'),
        ('open', 'open'),
        ('vim', 'vim'),
        ('ll', 'fish -ic "ll"'),
        ('ls', 'ls'),
        ('g', 'git')])
    def test_from_shell(self, before, after, shell):
        assert shell.from_shell(before) == after

    def test_to_shell(self, shell):
        assert shell.to_shell('pwd') == 'pwd'

    def test_and_(self, shell):
        assert shell.and_('foo', 'bar') == 'foo; and bar'

    def test_or_(self, shell):
        assert shell.or_('foo', 'bar') == 'foo; or bar'

    def test_get_aliases(self, shell):
        assert shell.get_aliases() == {'fish_config': 'fish_config',
                                       'dick': 'dick',
                                       'funced': 'funced',
                                       'funcsave': 'funcsave',
                                       'history': 'history',
                                       'll': 'll',
                                       'math': 'math',
                                       'popd': 'popd',
                                       'pushd': 'pushd',
                                       'ruby': 'ruby',
                                       'g': 'git',
                                       'fish_key_reader': '/usr/bin/fish_key_reader'}

    def test_app_alias(self, shell):
        assert 'function dick' in shell.app_alias('dick')
        assert 'function DICK' in shell.app_alias('DICK')
        assert 'thedick' in shell.app_alias('dick')
        assert 'TF_SHELL=fish' in shell.app_alias('dick')
        assert 'TF_ALIAS=dick PYTHONIOENCODING' in shell.app_alias('dick')
        assert 'PYTHONIOENCODING=utf-8 thedick' in shell.app_alias('dick')

    def test_app_alias_alter_history(self, settings, shell):
        settings.alter_history = True
        assert 'builtin history delete' in shell.app_alias('DICK')
        assert 'builtin history merge' in shell.app_alias('DICK')
        settings.alter_history = False
        assert 'builtin history delete' not in shell.app_alias('DICK')
        assert 'builtin history merge' not in shell.app_alias('DICK')

    def test_get_history(self, history_lines, shell):
        history_lines(['- cmd: ls', '  when: 1432613911',
                       '- cmd: rm', '  when: 1432613916'])
        assert list(shell.get_history()) == ['ls', 'rm']

    @pytest.mark.parametrize('entry, entry_utf8', [
        ('ls', '- cmd: ls\n   when: 1430707243\n'),
        (u'echo café', '- cmd: echo café\n   when: 1430707243\n')])
    def test_put_to_history(self, entry, entry_utf8, builtins_open, mocker, shell):
        mocker.patch('thedick.shells.fish.time', return_value=1430707243.3517463)
        shell.put_to_history(entry)
        builtins_open.return_value.__enter__.return_value. \
            write.assert_called_once_with(entry_utf8)

    def test_how_to_configure(self, shell, config_exists):
        config_exists.return_value = True
        assert shell.how_to_configure().can_configure_automatically

    def test_how_to_configure_when_config_not_found(self, shell,
                                                    config_exists):
        config_exists.return_value = False
        assert not shell.how_to_configure().can_configure_automatically
