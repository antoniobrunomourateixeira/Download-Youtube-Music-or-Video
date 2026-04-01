# YouTube Downloader

Aplicativo em Python com interface `tkinter` para baixar áudio em `mp3` e vídeo do YouTube.

## Requisitos

- Python 3 instalado
- `ffmpeg` instalado para:
  - converter áudio para `mp3`
  - juntar vídeo e áudio com melhor compatibilidade

## Instalar ffmpeg

Baixe o `ffmpeg` no site oficial:

https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-n8.1-latest-win64-gpl-8.1.zip

No Windows, você pode:

1. Baixar o pacote compatível com Windows
2. Extrair os arquivos
3. Deixar o executável em `ffmpeg/ffmpeg.exe` dentro do projeto

Estrutura esperada:

```text
py download_youtube/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── ffmpeg/
│   └── ffmpeg.exe
└── downloads/
```

## Criar ambiente virtual

```powershell
python -m venv .venv
```

## Ativar o ambiente virtual

```powershell
.venv\Scripts\Activate.ps1
```

## Instalar dependências

```powershell
pip install -r requirements.txt
```

## Rodar em desenvolvimento

```powershell
python app.py
```

ou

```powershell
py app.py
```

## Gerar o executável

```powershell
python -m PyInstaller --noconsole --onefile --name YouTubeDownloader --add-data "ffmpeg;ffmpeg" app.py
```

## Saída do build

Depois do build, o executável ficará em:

```text
dist\YouTubeDownloader.exe
```
