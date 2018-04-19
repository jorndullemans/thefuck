# -*- coding: utf-8 -*-

import os
import pytest
from thedick.shells.zsh import Zsh


@pytest.mark.usefixtures('isfile', 'no_memoize', 'no_cache')
class TestZsh(object):
    @pytest.fixture
    def shell(self):
        return Zsh()

    @pytest.fixture(autouse=True)
    def shell_aliases(self):
        os.environ['TF_SHELL_ALIASES'] = (
            'dick=\'eval $(thedick $(fc -ln -1 | tail -n 1))\'\n'
            'l=\'ls -CF\'\n'
            'la=\'ls -A\'\n'
            'll=\'ls -alF\'')

    @pytest.mark.parametrize('before, after', [
        ('dick', 'eval $(thedick $(fc -ln -1 | tail -n 1))'),
        ('pwd', 'pwd'),
        ('ll', 'ls -alF')])
    def test_from_shell(self, before, after, shell):
        assert shell.from_shell(before) == after

    def test_to_shell(self, shell):
        assert shell.to_shell('pwd') == 'pwd'

    def test_and_(self, shell):
        assert shell.and_('ls', 'cd') == 'ls && cd'

    def test_or_(self, shell):
        assert shell.or_('ls', 'cd') == 'ls || cd'

    def test_get_aliases(self, shell):
        assert shell.get_aliases() == {
            'dick': 'eval $(thedick $(fc -ln -1 | tail -n 1))',
            'l': 'ls -CF',
            'la': 'ls -A',
            'll': 'ls -alF'}

    def test_app_alias(self, shell):
        assert 'dick () {' in shell.app_alias('dick')
        assert 'DICK () {' in shell.app_alias('DICK')
        assert 'thedick' in shell.app_alias('dick')
        assert 'PYTHONIOENCODING' in shell.app_alias('dick')

    def test_app_alias_variables_correctly_set(self, shell):
        alias = shell.app_alias('dick')
        assert "dick () {" in alias
        assert 'TF_SHELL=zsh' in alias
        assert "TF_ALIAS=dick" in alias
        assert 'PYTHONIOENCODING=utf-8' in alias
        assert 'TF_SHELL_ALIASES=$(alias)' in alias

    def test_get_history(self, history_lines, shell):
        history_lines([': 1432613911:0;ls', ': 1432613916:0;rm'])
        assert list(shell.get_history()) == ['ls', 'rm']

    def test_how_to_configure(self, shell, config_exists):
        config_exists.return_value = True
        assert shell.how_to_configure().can_configure_automatically

    def test_how_to_configure_when_config_not_found(self, shell,
                                                    config_exists):
        config_exists.return_value = False
        assert not shell.how_to_configure().can_configure_automatically
