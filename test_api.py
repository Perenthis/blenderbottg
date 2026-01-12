from gigachat import GigaChat

giga = GigaChat(
   credentials="MDE5YmIzNWYtOGM2Ny03ZTlkLTk3YjAtMDc2ZWFhOGE3OTVjOmFiN2MyZmJlLWIwMzItNGU0Ny05YTM3LTc5OGFkNzQ2ZmNlYg==",
)

response = giga.chat("Привет! Как дела?")

print(response.choices[0].message.content)