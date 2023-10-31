from pip_services4_components.context import IContext


class ContextResolver:
    """
    Context resolver that processes context and extracts values from there.
    See :class:`IContext <pip_services4_components.context.IContext.IContext>`
    """

    @staticmethod
    def get_trace_id(context: IContext) -> str:
        """
        Extracts trace id from execution context.

        :param context: execution context to trace execution through call chain.
        :return: a trace id or <code>null</code> if it is not defined.

        See :class:`IContext <pip_services4_components.context.IContext.IContext>`
        """
        if not context:
            return ""
        trace_id = context.get('trace_id') or context.get('traceId')
        return trace_id or ""

    @staticmethod
    def get_client(context: IContext) -> str:
        """
        Extracts client name from execution context.

        :param context: execution context to trace execution through call chain.
        :return: a client name or <code>null</code> if it is not defined.

        See :class:`IContext <pip_services4_components.context.IContext.IContext>`

        """
        if not context:
            return ""
        trace_id = context.get('client')
        return trace_id or ""

    @staticmethod
    def get_user(context: IContext) -> str:
        """
        Extracts user name (identifier) from execution context.

        :param context: execution context to trace execution through call chain.
        :return: a user reference or <code>null</code> if it is not defined.
        """
        if not context:
            return ""
        trace_id = context.get('user')
        return trace_id or ""
