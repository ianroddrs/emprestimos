from django.shortcuts import render
from .models import Emprestimos, Pagamentos

def home(request):
   return render(request, 'index.html')

def tables(request):
    emprestimos = Emprestimos.objects.all()
    pagamentos = Pagamentos.objects.all()

    total_emprestado = 0
    saldo_total = 0 
    total_pago = 0

    for emprestimo in emprestimos:
        total_emprestado += float(emprestimo['valor_emprestado'])
        saldo_total += float(emprestimo['saldo_atual'])
        total_pago += float(emprestimo['total_pago'])

        emprestimo['valor_emprestado'] = f'R$ {emprestimo["valor_emprestado"]:.2f}'
        emprestimo['saldo_atual'] = f'R$ {emprestimo["saldo_atual"]:.2f}'
        emprestimo['juros_mensal'] = f'{float(emprestimo["juros_mensal"])*100:.2f}%'
        emprestimo['total_pago'] = f'R$ {emprestimo["total_pago"]:.2f}'

    context = {
        'emprestimos': emprestimos,
        'pagamentos': pagamentos,
        'total_emprestado': f'{total_emprestado:.2f}',
        'saldo_total': f'{saldo_total:.2f}',
        'total_pago': f'{total_pago:.2f}'
    }

    return render(request, 'tabelas.html', context)


















def emp():
  # Dados iniciais
  principal = 20000  # valor do empréstimo inicial
  juros_mensal = 0.0165 # taxa de juros (2% ao mês)
  pagamentos = [700]  # pagamento nos meses subsequentes

  # Simulação dos pagamentos
  saldo = principal  # saldo inicial é igual ao valor emprestado
  total_pago = 0
  meses = 0

  # Agora, simular os pagamentos de 700 reais até quitar o saldo
  for pagamento in pagamentos:
      valor_juros = saldo * juros_mensal
      if pagamento > saldo + valor_juros:
          pagamento = saldo + valor_juros
      saldo = saldo * (1 + juros_mensal) - pagamento
      total_pago += pagamento
      meses += 1

      texto = f"""
          mes: {meses}
          valor_emprestado: ${principal:.2f}
          pagamento: ${pagamento:.2f}
          juros (1,65%): ${valor_juros:.2f}
          saldo restante: ${saldo:.2f}
          total pago: ${total_pago}
      """
      print(texto)
