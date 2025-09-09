from typing import Any, Literal
from src.protocols.enums import GameWarning
from src.core.types import SystemMessage

def was_message_successful(
    message: SystemMessage
    ) -> bool:
    """
    Verifica se uma Mensagem do Sistema
    indica sucesso.

    Args:
        message (SystemMessage): Mensagem que será validada.

    Returns:
        bool: True para sucesso na mensagem, False para
            erro.
    """
    success = message.get("payload", {}).get("success", False)
    return was_successful(success, True, operator="is")

def was_successful(
    entry: Any,
    expected_entry: Any = GameWarning.OK,
    operator: Literal["==", "is"] = "=="
    ) -> bool:
    """
    Verifica se uma entrada é igual ou tem identidade igual
    a uma entrada esperada.

    Args:
        entry (Any): Entrada que será validada.
        expected_entry (Any): Entrada esperada.
            Por padrão é GameWarning.OK.
        operator (str): Indica qual operador usar na validação.
            Pode ser apenas "==" ou "is". Por padrão é "==".

    Returns:
        bool: True para entrada válida, False para
            inválida.
    """
    if operator == "is":
        return entry is expected_entry
    return entry == expected_entry
