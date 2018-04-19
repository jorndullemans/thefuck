from .generic import Generic, ShellConfiguration


class Powershell(Generic):
    def app_alias(self, alias_name):
        return 'function ' + alias_name + ' {\n' \
               '    $history = (Get-History -Count 1).CommandLine;\n' \
               '    if (-not [string]::IsNullOrWhiteSpace($history)) {\n' \
               '        $dick = $(thedick $args $history);\n' \
               '        if (-not [string]::IsNullOrWhiteSpace($dick)) {\n' \
               '            if ($dick.StartsWith("echo")) { $dick = $dick.Substring(5); }\n' \
               '            else { iex "$dick"; }\n' \
               '        }\n' \
               '    }\n' \
               '}\n'

    def and_(self, *commands):
        return u' -and '.join('({0})'.format(c) for c in commands)

    def how_to_configure(self):
        return ShellConfiguration(
            content=u'iex "thedick --alias"',
            path='$profile',
            reload='& $profile',
            can_configure_automatically=False)
