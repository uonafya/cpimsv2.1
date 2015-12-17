from django import template
from django.conf import settings
import subprocess

register = template.Library()


@register.assignment_tag(takes_context=True)
def git_version(context):
    try:
        cmd = 'cd ' + settings.GIT_ROOT + ';'
        # --pretty=format:'%h %ai'
        cmd += "git log --abbrev-commit --date=local -1" + ';'
        # cmd += 'cd -'
        head = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        git_revision = str(head.stdout.readlines())
        git_vals = git_revision.replace('\\n', '')
        git_values = eval(git_vals)
        git_short = git_values[0], git_values[1], git_values[2]
    except Exception, e:
        print str(e)
        git_short = '3.0.0'
        return git_short
    else:
        return git_short
