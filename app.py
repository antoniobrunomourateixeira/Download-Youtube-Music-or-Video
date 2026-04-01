import os
import sys
import shutil
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import yt_dlp

class YoutubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader by Bruno Moura")
        self.root.geometry("620x350")
        self.root.resizable(False, False)

        self.url_var = tk.StringVar()
        self.folder_var = tk.StringVar(value=os.path.join(os.getcwd(), "downloads"))
        self.mode_var = tk.StringVar(value="audio")  # default = audio
        self.progress_var = tk.DoubleVar(value=0)
        self.progress_text_var = tk.StringVar(value="0%")

        self._build_ui()

    def _build_ui(self):
        frame = tk.Frame(self.root, padx=15, pady=15)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="Link do YouTube:").grid(row=0, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.url_var, width=70).grid(
            row=1, column=0, columnspan=3, sticky="we", pady=(0, 10)
        )

        tk.Label(frame, text="Pasta de destino:").grid(row=2, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.folder_var, width=55).grid(
            row=3, column=0, columnspan=2, sticky="we", pady=(0, 10)
        )
        tk.Button(frame, text="Selecionar pasta", command=self.select_folder).grid(
            row=3, column=2, padx=(10, 0), sticky="we"
        )

        tk.Label(frame, text="Tipo de download:").grid(row=4, column=0, sticky="w")
        options_frame = tk.Frame(frame)
        options_frame.grid(row=5, column=0, columnspan=3, sticky="w", pady=(0, 10))

        tk.Radiobutton(
            options_frame, text="Áudio (padrão)", variable=self.mode_var, value="audio"
        ).pack(side="left", padx=(0, 20))

        tk.Radiobutton(
            options_frame, text="Vídeo", variable=self.mode_var, value="video"
        ).pack(side="left")

        tk.Label(frame, text="Progresso:").grid(row=6, column=0, sticky="w")

        self.progress_bar = ttk.Progressbar(
            frame,
            orient="horizontal",
            length=560,
            mode="determinate",
            maximum=100,
            variable=self.progress_var
        )
        self.progress_bar.grid(row=7, column=0, columnspan=3, sticky="we", pady=(5, 5))

        self.progress_label = tk.Label(frame, textvariable=self.progress_text_var, anchor="e")
        self.progress_label.grid(row=8, column=0, columnspan=3, sticky="we", pady=(0, 10))

        self.status_label = tk.Label(frame, text="Pronto.", anchor="w")
        self.status_label.grid(row=9, column=0, columnspan=3, sticky="we", pady=(5, 10))

        self.download_button = tk.Button(
            frame, text="Baixar", height=2, command=self.start_download
        )
        self.download_button.grid(
            row=10, column=0, columnspan=3, sticky="we", pady=(0, 10)
        )

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=0)

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_var.set(folder)

    def start_download(self):
        url = self.url_var.get().strip()
        folder = self.folder_var.get().strip()
        mode = self.mode_var.get()

        if not url:
            messagebox.showwarning("Atenção", "Informe o link do YouTube.")
            return

        if not folder:
            messagebox.showwarning("Atenção", "Selecione uma pasta de destino.")
            return

        os.makedirs(folder, exist_ok=True)

        ffmpeg_path = self.get_ffmpeg_location()
        self.download_button.config(state="disabled")
        self.status_label.config(text="Baixando...")
        self.progress_var.set(0)
        self.progress_text_var.set("0%")

        thread = threading.Thread(
            target=self.download_media,
            args=(url, folder, mode),
            daemon=True
        )
        thread.start()

    def progress_hook(self, d):
        try:
            status = d.get("status")

            if status == "downloading":
                percent_str = d.get("_percent_str", "0.0%").replace("%", "").strip()
                percent_str = percent_str.replace(",", ".")

                try:
                    percent = float(percent_str)
                except ValueError:
                    percent = 0

                speed = d.get("_speed_str", "")
                eta = d.get("_eta_str", "")

                self.root.after(0, lambda: self.update_progress(percent, speed, eta))

            elif status == "finished":
                self.root.after(0, lambda: self.update_progress(100, "", ""))
                self.root.after(0, lambda: self.status_label.config(text="Processando arquivo..."))

        except Exception:
            pass

    def update_progress(self, percent, speed="", eta=""):
        self.progress_var.set(percent)

        details = f"{percent:.1f}%"
        if speed:
            details += f" | Velocidade: {speed}"
        if eta:
            details += f" | ETA: {eta}"

        self.progress_text_var.set(details)

    def get_ffmpeg_location(self):
        bundled_base = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
        local_base = os.path.dirname(os.path.abspath(__file__))
        candidate_paths = [
            os.path.join(bundled_base, "ffmpeg", "ffmpeg.exe"),
            os.path.join(local_base, "ffmpeg", "ffmpeg.exe"),
        ]

        for path in candidate_paths:
            if os.path.exists(path):
                return path

        return shutil.which("ffmpeg") or "ffmpeg"

    def download_media(self, url, folder, mode):
        try:
            ffmpeg_path = self.get_ffmpeg_location()

            if mode == "audio":
                ydl_opts = {
                    "outtmpl": os.path.join(folder, "%(title)s.%(ext)s"),
                    "format": "bestaudio/best",
                    "noplaylist": True,
                    "progress_hooks": [self.progress_hook],
                }
                if ffmpeg_path:
                    ydl_opts["ffmpeg_location"] = ffmpeg_path
                    ydl_opts["postprocessors"] = [
                        {
                            "key": "FFmpegExtractAudio",
                            "preferredcodec": "mp3",
                            "preferredquality": "192",
                        }
                    ]
            else:
                ydl_opts = {
                    "outtmpl": os.path.join(folder, "%(title)s.%(ext)s"),
                    "noplaylist": True,
                    "progress_hooks": [self.progress_hook],
                }

                if ffmpeg_path:
                    ydl_opts["format"] = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best"
                    ydl_opts["merge_output_format"] = "mp4"
                    ydl_opts["ffmpeg_location"] = ffmpeg_path
                else:
                    # Sem ffmpeg, baixa apenas MP4 progressivo com áudio AAC/M4A.
                    # Isso evita vídeos mudos e reduz problemas com áudio Opus.
                    ydl_opts["format"] = (
                        "best[ext=mp4][acodec^=mp4a][vcodec!=none]/"
                        "best[ext=mp4][acodec^=aac][vcodec!=none]/"
                        "best[ext=mp4][acodec!=none][vcodec!=none]"
                    )

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                title = info.get("title", "arquivo")

            self.root.after(0, lambda: self.on_success(title, folder, mode))

        except Exception as e:
            error_message = str(e)
            self.root.after(0, lambda msg=error_message: self.on_error(msg))

    def on_success(self, title, folder, mode):
        self.download_button.config(state="normal")
        self.progress_var.set(100)
        self.progress_text_var.set("100%")
        self.status_label.config(text="Download concluído com sucesso.")
        tipo = "áudio" if mode == "audio" else "vídeo"

        messagebox.showinfo(
            "Sucesso",
            f"{tipo.capitalize()} baixado com sucesso.\n\nTítulo: {title}\nPasta: {folder}"
        )

    def on_error(self, error_message):
        self.download_button.config(state="normal")
        self.status_label.config(text="Erro no download.")
        messagebox.showerror(
            "Erro",
            f"Não foi possível concluir o download.\n\nDetalhes: {error_message}"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = YoutubeDownloaderApp(root)
    root.mainloop()
