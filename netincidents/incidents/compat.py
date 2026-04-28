import sys
from copy import copy

import django


def patch_django_template_context_copy():
    if sys.version_info < (3, 14) or django.VERSION >= (5, 0):
        return

    from django.template.context import BaseContext, Context

    if getattr(BaseContext.__copy__, "_netincidents_py314_patch", False):
        return

    def _basecontext_copy(self):
        duplicate = self.__class__.__new__(self.__class__)
        duplicate.__dict__ = self.__dict__.copy()
        duplicate.dicts = self.dicts[:]
        return duplicate

    def _context_copy(self):
        duplicate = BaseContext.__copy__(self)
        duplicate.render_context = copy(self.render_context)
        return duplicate

    _basecontext_copy._netincidents_py314_patch = True
    _context_copy._netincidents_py314_patch = True

    BaseContext.__copy__ = _basecontext_copy
    Context.__copy__ = _context_copy
