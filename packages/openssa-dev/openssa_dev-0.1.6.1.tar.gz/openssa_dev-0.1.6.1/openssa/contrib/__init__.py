"""OpenSSM Contrib."""


from collections.abc import Sequence

from .streamlit_chatssa import ChatSSAComponent as ChatSSAStreamlitComponent


__all__: Sequence[str] = (
    'ChatSSAStreamlitComponent',
)
