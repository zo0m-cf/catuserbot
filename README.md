
# CAT USERBOT

### A maneira fácil de implantar o bot
Obtenha APP ID e API HASH de [AQUI] (https://my.telegram.org) e BOT TOKEN de [Bot Father] (https://t.me/botfather) e então gere stringsession clicando em run.on .repl.it abaixo e então clique em implantar no heroku. Antes de clicar em implantar no heroku, basta clicar no garfo e estrela logo abaixo

[![Get string session](https://repl.it/badge/github/sandy1709/sandeep1709)](https://generatestringsession.sandeep1709.repl.run/)

[![Deploy To Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/xmtscf/catuserbot)
<p align="center">
  <a href="https://github.com/xmtscf/catuserbot/fork">
    <img src="https://img.shields.io/github/forks/xmtscf/catuserbot?label=Fork&style=social">
    
  </a>
  <a href="https://github.com/xmtscf/catuserbot">
    <img src="https://img.shields.io/github/stars/xmtscf/catuserbot?style=social">
  </a>
</p>


[![catuserbot logo](https://telegra.ph/file/7e1e89621fabbf02596f8.jpg)](https://heroku.com/deploy?template=https://github.com/xmtscf/catuserbot)


### Junte-se [aqui] (https://t.me/catuserbot17) para atualizações e tuts e [aqui] (https://t.me/catuserbot_support) para discussões e bugs

### O Caminho Normal

Um exemplo de arquivo `local_config.py` poderia ser:

** Nem todas as variáveis **são obrigatórias**

__O Userbot deve funcionar definindo apenas as duas primeiras variáveis__

```python3
from heroku_config import Var

class Development(Var):
  APP_ID = 6
  API_HASH = "eb06d4abfb49dc3eeb1aeb98ae0f581e"
```

### Configuração UniBorg



** Configuração Heroku **
Simplesmente deixe o Config como está.

** Configuração Local **

Felizmente, não há vars obrigatórios para o UniBorg Support Config.

## Vars obrigatórias

- Apenas duas das variáveis de ambiente são obrigatórias.
- Isso ocorre por causa de  `telethon.errors.rpc_error_list.ApiIdPublishedFloodError`

    - ʻAPP_ID`: você pode obter este valor em https://my.telegram.org
    - ʻAPI_HASH`: Você pode obter este valor em https://my.telegram.org
- O userbot não funcionará sem definir os vars obrigatórios.
