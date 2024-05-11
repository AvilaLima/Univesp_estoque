def verificar_forca_senha(senha):


  comprimento_minimo = 8
  tem_letra_maiuscula = False
  tem_letra_minuscula = False
  tem_numero = False
  tem_caractere_especial = False

  # Verificando o comprimento da senha
  if len(senha) < comprimento_minimo:
    return f"Sua senha e muito curta. Recomenda-se no minimo {comprimento_minimo} caracteres."

  # Verificando se a senha contém letras maiúsculas, minúsculas, números e carateres especiais
  for caracter in senha:
    if caracter.isupper():
        tem_letra_maiuscula = True
    elif caracter.islower():
        tem_letra_minuscula = True
    elif caracter.isdigit():
        tem_numero = True
    else:
        tem_caractere_especial = True

  # Verificando se a senha contém sequências comuns
  sequencias_comuns = ["123456", "abcdef"]
  for sequencia in sequencias_comuns:
    if sequencia in senha:
      return "Sua senha contem uma sequencia comum. Tente uma senha mais complexa."

  # Verificando se a senha contém palavras comuns
  palavras_comuns = ["password", "123456", "qwerty"]
  if senha in palavras_comuns:
    return "Sua senha e muito comum. Tente uma senha mais complexa."

  # Verificando o comprimento mínimo e critérios de validação
  if tem_numero == False:
    return "Sua senha deve conter pelo menos um número"
  if tem_caractere_especial == False:
    return "Sua senha deve conter pelo menos um caracter especial como !, @, #, $, %, etc."
  if tem_letra_maiuscula == False:
    return "Sua senha deve conter pelo menos uma letra maiúscula."
  if tem_letra_minuscula == False:
    return "Sua senha deve conter pelo menos uma letra minúscula."
  
  if tem_letra_maiuscula and tem_letra_minuscula and tem_numero and tem_caractere_especial:
    return "Sua senha atende aos requisitos de seguranca. Parabens!"
  else:
    return "Sua senha nao atende aos requisitos de seguranca." 
  
# Obtendo a senha do usuário
senha = input().strip()

# Verificando a força da senha
resultado = verificar_forca_senha(senha)

# Imprimindo o resultado
print(resultado)