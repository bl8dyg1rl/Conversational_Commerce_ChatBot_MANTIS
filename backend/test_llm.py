from app.services.llm_service import extract_intent


messages = [
    "Quiero cosas para hacer hamburguesas.",
    "¿Tienen pan de hamburguesa?",
    "¿Tienen 20 panes de hamburguesa?",
    "Necesito 100 hamburguesas.",
    "¿Qué productos venden?"
]


for message in messages:

    print("\n================================")
    print("MENSAJE:")
    print(message)

    result = extract_intent(
        message
    )

    print("\nRESULTADO:")
    print(result)