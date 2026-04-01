# Criar ambiente virtual 
python -m venv .venv

# Ativar o ambiente virtual
Ativar o ambiente virtual

# Instalar as dependências
pip install -r requirements.txt

# Rodar em modo desenvolvimento
python app.py ou py app.py

# Gera EXE
python -m PyInstaller --noconsole --onefile --name YouTubeDownloader --add-data "ffmpeg;ffmpeg" app.py

## Depois disso, o executável ficará em:
Depois disso, o executável ficará em: _dist\YoutubeDownloader.exe_
