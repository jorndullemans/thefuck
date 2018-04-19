# -*- coding: utf-8 -*-

import pytest
from thedick.shells import Generic


class TestGeneric(object):
    @pytest.fixture
    def shell(self):
        return Generic()

    def test_from_shell(self, shell):
        assert shell.from_shell('pwd') == 'pwd'

    def test_to_shell(self, shell):
        assert shell.to_shell('pwd') == 'pwd'

    def test_and_(self, shell):
        assert shell.and_('ls', 'cd') == 'ls && cd'

    def test_or_(self, shell):
        assert shell.or_('ls', 'cd') == 'ls || cd'

    def test_get_aliases(self, shell):
        assert shell.get_aliases() == {}

    def test_app_alias(self, shell):
        assert 'alias dick' in shell.app_alias('dick')
        assert 'alias DICK' in shell.app_alias('DICK')
        assert 'thedick' in shell.app_alias('dick')
        assert 'TF_ALIAS=dick PYTHONIOENCODING' in shell.app_alias('dick')
        assert 'PYTHONIOENCODING=utf-8 thedick' in shell.app_alias('dick')

    def test_get_history(self, history_lines, shell):
        history_lines(['ls', 'rm'])
        # We don't know what to do in generic shell with history lines,
        # so just ignore them:
        assert list(shell.get_history()) == []

    def test_split_command(self, shell):
        assert shell.split_command('ls') == ['ls']
        assert shell.split_command(u'echo café') == [u'echo', u'café']

    def test_how_to_configure(self, shell):
        assert shell.how_to_configure() is None
