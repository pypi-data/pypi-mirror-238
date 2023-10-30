# -*- coding: utf-8 -*-


class Scope(object):
    def apply(self, builder, model):
        """
        Apply the scope to a given query builder.

        :param builder: The query builder
        :type builder: active_wrapper.orm.Builder

        :param model: The model
        :type model: active_wrapper.orm.Model
        """
        raise NotImplementedError
