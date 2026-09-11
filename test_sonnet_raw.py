import sys
sys.path.insert(0, r"C:\Users\matheus\Desktop")
import EXTRAIR_MEGA_ATIVOS_SONNET5 as ext

res = ext.chamar_sonnet_5("Retorne apenas json.", "Gere um json simples com chave mensagem e valor amem.")
print("RAW RESPONSE:")
print(res)
