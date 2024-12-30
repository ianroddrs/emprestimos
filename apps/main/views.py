from django.shortcuts import render
from .models import Emprestimos

def photo_wall(request):
  # emprestimos = Emprestimos.objects.all()
  emprestimos = Emprestimos.objects.filter(juros_mensal=0.02, saldo_atual = 1200)
  print(emprestimos)
  emprestimo = Emprestimos.objects.get(id=2)
  print(emprestimo)
  return render(request, 'photowall.html', {'photos': []})


















def emp():
  # Dados iniciais
  principal = 20000  # valor do empréstimo inicial
  juros_mensal = 0.02  # taxa de juros (2% ao mês)
  pagamento = 700  # pagamento nos meses subsequentes

  # Simulação dos pagamentos
  saldo = principal  # saldo inicial é igual ao valor emprestado
  total_pago = 0
  meses = 0

  # Agora, simular os pagamentos de 700 reais até quitar o saldo
  while saldo > 0:
      saldo = saldo * (1 + juros_mensal) - pagamento
      total_pago += pagamento
      meses += 1

  # Se o saldo ficou negativo (pagamento maior que a dívida), ajustar o valor pago
  if saldo < 0:
      total_pago += saldo  # subtrair o excesso pago do total

  print(meses, total_pago)