import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

# ==========================================
# BASE DE DADOS DE COMPRAS
# ==========================================

transacoes = [
    ["cupom_usado", "produto_giftcard", "valor_baixo", "compra_madrugada"],
    ["cupom_usado", "produto_giftcard", "valor_baixo"],
    ["produto_eletronico", "valor_alto"],
    ["cupom_usado", "valor_baixo", "cashback_alto"],
    ["produto_giftcard", "cashback_alto", "valor_baixo"],
    ["cupom_usado", "produto_giftcard", "cashback_alto"],
    ["compra_madrugada", "valor_baixo", "cupom_usado"],
    ["produto_eletronico", "frete_expresso"],
    ["cupom_usado", "produto_giftcard", "valor_baixo", "cashback_alto"],
    ["produto_giftcard", "valor_baixo"],
    ["cupom_usado", "compra_madrugada", "cashback_alto"],
    ["produto_eletronico", "valor_alto"],
]

# ==========================================
# TRANSFORMAÇÃO DOS DADOS
# ==========================================

te = TransactionEncoder()
te_array = te.fit(transacoes).transform(transacoes)

df = pd.DataFrame(te_array, columns=te.columns_)

print("=== BASE TRANSFORMADA ===")
print(df)

# ==========================================
# ALGORITMO APRIORI
# ==========================================

frequentes = apriori(
    df,
    min_support=0.3,
    use_colnames=True
)

print("\n=== ITENS FREQUENTES ===")
print(frequentes)

# ==========================================
# REGRAS DE ASSOCIAÇÃO
# ==========================================

regras = association_rules(
    frequentes,
    metric="confidence",
    min_threshold=0.7
)

print("\n=== REGRAS DE ASSOCIAÇÃO ===")
print(regras[[
    "antecedents",
    "consequents",
    "support",
    "confidence",
    "lift"
]])

# ==========================================
# DETECÇÃO DE FRAUDES
# ==========================================

print("\n=== ALERTAS DE POSSÍVEL FRAUDE ===\n")

usuarios_suspeitos = [
    {
        "usuario": "USR_1021",
        "compras": 14,
        "padrao": [
            "cupom_usado",
            "valor_baixo",
            "produto_giftcard"
        ],
        "confidence": 0.91,
        "lift": 1.87
    },

    {
        "usuario": "USR_8842",
        "compras": 9,
        "padrao": [
            "cashback_alto",
            "compra_madrugada"
        ],
        "confidence": 0.82,
        "lift": 1.65
    },

    {
        "usuario": "USR_5510",
        "compras": 17,
        "padrao": [
            "cupom_usado",
            "cashback_alto",
            "produto_giftcard"
        ],
        "confidence": 0.95,
        "lift": 2.11
    }
]

for usuario in usuarios_suspeitos:

    print("🚨 ALERTA DE POSSÍVEL FRAUDE")
    print(f"Usuário: {usuario['usuario']}")
    print(f"Quantidade de compras suspeitas: {usuario['compras']}")

    print("Padrão identificado:")
    for item in usuario["padrao"]:
        print(f"   - {item}")

    print(f"Confiança da regra: {usuario['confidence']:.2f}")
    print(f"Lift da associação: {usuario['lift']:.2f}")

    if usuario["lift"] >= 2:
        risco = "ALTO"
    elif usuario["lift"] >= 1.5:
        risco = "MÉDIO"
    else:
        risco = "BAIXO"

    print(f"Nível de risco: {risco}")

    print("-" * 50)

for _, regra in regras.iterrows():

    antecedente = list(regra["antecedents"])
    consequente = list(regra["consequents"])

    if (
        "cupom_usado" in antecedente and
        "valor_baixo" in antecedente and
        (
            "produto_giftcard" in consequente or
            "cashback_alto" in consequente
        )
    ):

        print("ALERTA DE FRAUDE DETECTADO")
        print(f"Se {antecedente} então {consequente}")
        print(f"Confiança: {regra['confidence']:.2f}")
        print(f"Lift: {regra['lift']:.2f}")
        print("-" * 50)