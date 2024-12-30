from core.services import GSpreadModel
from datetime import datetime

class Emprestimos(GSpreadModel):
    id = int
    codigo = str
    valor_emprestado = float
    saldo_atual = float
    juros_mensal = float
    total_pago = float

    def __init__(self):
        self.worksheet_name = "emprestimos"
        super().__init__()

class Pagamentos(GSpreadModel):
    id = int
    emprestimo_id = int
    valor_pagamento = float
    data_pagamento = datetime

    def __init__(self):
        self.worksheet_name = "pagamentos"
        super().__init__()