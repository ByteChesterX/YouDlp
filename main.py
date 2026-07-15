import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import subprocess
import os
import re


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class YoutubedlpGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YouDlp")
        self.root.geometry("650x600")
        self.root.minsize(650, 600)

        self.process = None
        self.downloading = False

        self.create_widgets()

    def create_widgets(self):
        self.root.grid_columnconfigure(0, weight=1)

        header = ctk.CTkLabel(
            self.root,
            text="YouDlp",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        header.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")

        subtitle = ctk.CTkLabel(
            self.root,
            text="YouTube Video & Ses İndirici",
            font=ctk.CTkFont(size=13),
            text_color="gray"
        )
        subtitle.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="w")

        url_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        url_frame.grid(row=2, column=0, padx=20, sticky="ew")
        url_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(url_frame, text="URL", font=ctk.CTkFont(size=12, weight="bold")).grid(row=0, column=0, sticky="w", pady=(0, 5))

        self.url_entry = ctk.CTkEntry(
            url_frame,
            placeholder_text="https://www.youtube.com/watch?v=...",
            height=40,
            font=ctk.CTkFont(size=13)
        )
        self.url_entry.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        settings_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        settings_frame.grid(row=3, column=0, padx=20, sticky="ew")
        settings_frame.grid_columnconfigure((0, 1), weight=1)

        type_frame = ctk.CTkFrame(settings_frame)
        type_frame.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        type_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(type_frame, text="Tür", font=ctk.CTkFont(size=12, weight="bold")).grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5))

        self.format_var = ctk.StringVar(value="video")
        format_segment = ctk.CTkSegmentedButton(
            type_frame,
            values=["Video", "Ses"],
            command=self.on_format_change,
            font=ctk.CTkFont(size=12),
            height=32
        )
        format_segment.set("Video")
        format_segment.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))

        quality_frame = ctk.CTkFrame(settings_frame)
        quality_frame.grid(row=0, column=1, sticky="ew", padx=(5, 0))
        quality_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(quality_frame, text="Kalite", font=ctk.CTkFont(size=12, weight="bold")).grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5))

        self.quality_var = ctk.StringVar(value="En İyi")
        self.quality_menu = ctk.CTkOptionMenu(
            quality_frame,
            values=["En İyi", "1080p", "720p", "480p", "360p"],
            variable=self.quality_var,
            height=32,
            font=ctk.CTkFont(size=12)
        )
        self.quality_menu.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))

        save_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        save_frame.grid(row=4, column=0, padx=20, sticky="ew", pady=(5, 0))
        save_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(save_frame, text="Kayıt Konumu", font=ctk.CTkFont(size=12, weight="bold")).grid(row=0, column=0, sticky="w", pady=(0, 5))

        path_frame = ctk.CTkFrame(save_frame, fg_color="transparent")
        path_frame.grid(row=1, column=0, sticky="ew")
        path_frame.grid_columnconfigure(0, weight=1)

        self.save_path = ctk.StringVar(value=os.path.expanduser("~/Downloads"))
        self.path_entry = ctk.CTkEntry(
            path_frame,
            textvariable=self.save_path,
            height=36,
            font=ctk.CTkFont(size=12)
        )
        self.path_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        ctk.CTkButton(
            path_frame,
            text="Gözat",
            width=80,
            height=36,
            font=ctk.CTkFont(size=12),
            command=self.browse_folder
        ).grid(row=0, column=1)

        section_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        section_frame.grid(row=5, column=0, padx=20, sticky="ew", pady=(10, 0))
        section_frame.grid_columnconfigure(0, weight=1)

        self.section_enabled = ctk.BooleanVar(value=False)
        section_check = ctk.CTkCheckBox(
            section_frame,
            text="Belirli aralık indir",
            variable=self.section_enabled,
            onvalue=True,
            offvalue=False,
            font=ctk.CTkFont(size=12),
            command=self.toggle_section
        )
        section_check.grid(row=0, column=0, sticky="w", pady=(0, 5))

        self.section_inputs_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        self.section_inputs_frame.grid(row=1, column=0, sticky="ew")
        self.section_inputs_frame.grid_columnconfigure((0, 2), weight=1)

        ctk.CTkLabel(self.section_inputs_frame, text="Başlangıç (dk:sn)", font=ctk.CTkFont(size=11)).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(self.section_inputs_frame, text="Bitiş (dk:sn)", font=ctk.CTkFont(size=11)).grid(row=0, column=2, sticky="w", padx=(10, 0))

        self.start_time = ctk.StringVar(value="00:00")
        self.end_time = ctk.StringVar(value="00:00")

        self.start_entry = ctk.CTkEntry(
            self.section_inputs_frame,
            textvariable=self.start_time,
            placeholder_text="00:00",
            height=32,
            font=ctk.CTkFont(size=12),
            width=120
        )
        self.start_entry.grid(row=1, column=0, sticky="w")

        ctk.CTkLabel(self.section_inputs_frame, text="-", font=ctk.CTkFont(size=16, weight="bold")).grid(row=1, column=1, padx=8)

        self.end_entry = ctk.CTkEntry(
            self.section_inputs_frame,
            textvariable=self.end_time,
            placeholder_text="05:30",
            height=32,
            font=ctk.CTkFont(size=12),
            width=120
        )
        self.end_entry.grid(row=1, column=2, sticky="w")

        self.toggle_section()

        self.progress = ctk.CTkProgressBar(self.root, height=6)
        self.progress.grid(row=6, column=0, padx=20, pady=(15, 5), sticky="ew")
        self.progress.set(0)

        self.status_var = ctk.StringVar(value="Hazır")
        self.status_label = ctk.CTkLabel(
            self.root,
            textvariable=self.status_var,
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.status_label.grid(row=7, column=0, padx=20, sticky="w")

        btn_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        btn_frame.grid(row=8, column=0, padx=20, pady=(15, 20), sticky="ew")
        btn_frame.grid_columnconfigure((0, 1), weight=1)

        self.download_btn = ctk.CTkButton(
            btn_frame,
            text="İndir",
            height=42,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.start_download
        )
        self.download_btn.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        self.cancel_btn = ctk.CTkButton(
            btn_frame,
            text="İptal",
            height=42,
            font=ctk.CTkFont(size=14),
            fg_color="#555555",
            hover_color="#666666",
            command=self.cancel_download,
            state="disabled"
        )
        self.cancel_btn.grid(row=0, column=1, sticky="ew", padx=(5, 0))

    def on_format_change(self, value):
        if value == "Ses":
            self.quality_menu.configure(state="disabled")
            self.quality_var.set("En İyi")
        else:
            self.quality_menu.configure(state="normal")

    def toggle_section(self):
        state = "normal" if self.section_enabled.get() else "disabled"
        self.start_entry.configure(state=state)
        self.end_entry.configure(state=state)

    def browse_folder(self):
        folder = filedialog.askdirectory(initialdir=self.save_path.get())
        if folder:
            self.save_path.set(folder)

    def start_download(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Uyarı", "Lütfen bir URL girin!")
            return

        if not self.is_valid_url(url):
            messagebox.showwarning("Uyarı", "Geçersiz YouTube URL'si!")
            return

        if self.section_enabled.get():
            start = self.start_time.get().strip()
            end = self.end_time.get().strip()
            if not self.is_valid_time(start) or not self.is_valid_time(end):
                messagebox.showwarning("Uyarı", "Geçersiz zaman formatı!\nÖrnek: 01:30 veya 00:05:30")
                return

        self.downloading = True
        self.download_btn.configure(state="disabled")
        self.cancel_btn.configure(state="normal")
        self.progress.configure(mode="indeterminate")
        self.progress.start()
        self.status_var.set("İndiriliyor...")

        thread = threading.Thread(target=self.download, args=(url,), daemon=True)
        thread.start()

    def is_valid_url(self, url):
        pattern = r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+'
        return re.match(pattern, url) is not None

    def is_valid_time(self, time_str):
        pattern = r'^(\d{1,2}:)?\d{1,2}:\d{2}$'
        return re.match(pattern, time_str) is not None

    def download(self, url):
        save_dir = self.save_path.get()
        fmt = self.format_var.get()
        quality = self.quality_var.get()

        cmd = ["yt-dlp", "-o", os.path.join(save_dir, "%(title)s.%(ext)s")]

        if self.section_enabled.get():
            start = self.start_time.get().strip()
            end = self.end_time.get().strip()
            if start and end:
                cmd += ["--download-sections", f"*{start}-{end}"]

        if fmt == "Ses":
            cmd += ["-x", "--audio-format", "mp3"]
        else:
            quality_map = {
                "En İyi": "best",
                "1080p": "1080",
                "720p": "720",
                "480p": "480",
                "360p": "360"
            }
            q = quality_map.get(quality, "best")
            if q != "best":
                cmd += ["-f", f"bestvideo[height<={q}]+bestaudio/best[height<={q}]"]
            else:
                cmd += ["-f", "bestvideo+bestaudio/best"]

        cmd.append(url)

        try:
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )

            for line in self.process.stdout:
                line = line.strip()
                if line:
                    short = line[:80] + "..." if len(line) > 80 else line
                    self.root.after(0, lambda l=short: self.status_var.set(l))

            self.process.wait()

            if self.process.returncode == 0:
                self.root.after(0, lambda: self.status_var.set("İndirme tamamlandı!"))
                self.root.after(0, lambda: messagebox.showinfo("Başarılı", "İndirme tamamlandı!"))
            else:
                self.root.after(0, lambda: self.status_var.set("Hata oluştu"))
                self.root.after(0, lambda: messagebox.showerror("Hata", "İndirme başarısız oldu!"))

        except FileNotFoundError:
            self.root.after(0, lambda: self.status_var.set("yt-dlp bulunamadı"))
            self.root.after(0, lambda: messagebox.showerror("Hata", "yt-dlp bulunamadı!\npip install yt-dlp"))
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set("Hata oluştu"))
            self.root.after(0, lambda: messagebox.showerror("Hata", str(e)))
        finally:
            self.root.after(0, self.reset_ui)

    def cancel_download(self):
        if self.process:
            self.process.terminate()
            self.process = None
        self.downloading = False
        self.reset_ui()
        self.status_var.set("İptal edildi")

    def reset_ui(self):
        self.downloading = False
        self.download_btn.configure(state="normal")
        self.cancel_btn.configure(state="disabled")
        self.progress.stop()
        self.progress.set(0)


def main():
    root = ctk.CTk()
    app = YoutubedlpGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
