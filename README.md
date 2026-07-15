# YouDlp

YouTube videolarını ve ses dosyalarını indirmek için basit bir arayüz uygulamasıdır. Arka planda yt-dlp aracını kullanır.

## Özellikler

- YouTube videolarını MP4 olarak indirme
- YouTube ses dosyalarını MP3 olarak indirme
- Kalite seçimi (En İyi, 1080p, 720p, 480p, 360p)
- Belirli bir zaman aralığını indirme (örneğin 01:30 - 05:30)
- İndirme sırasında ilerleme göstergesi
- Koyu tema ile modern arayüz

## Gereksinimler

- Python 3.8 veya daha yüksek
- tkinter (Python ile birlikte gelir, bazen ayrıca yüklenmesi gerekir)
- ffmpeg (ses dönüşümleri için)
- İnternet bağlantısı

## Kurulum

Tek bir komutla kurulum yapabilirsiniz:
bash
curl -sL https://raw.githubusercontent.com/ByteChesterX/YouDlp/main/install.sh | bash


Bu komut şunları otomatik olarak yapar:

1. Python, tkinter ve ffmpeg yoksa yükler
2. Bir sanal ortam (virtual environment) oluşturur
3. Gerekli Python paketlerini yükler (yt-dlp, customtkinter)
4. ~/.local/bin/youdlp` dosyasını oluşturur (çalıştırma scripti)
5. Masaüstü uygulama kısayolu oluşturur

### Manuel Kurulum

Eğer install.sh'yi çalıştırmak istemezseniz:

bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py


## Kullanım

Kurulumdan sonra terminalden şu komutu çalıştırın:

bash
youdlp


Veya doğrudan:
bash
~/.local/bin/youdlp



Uygulama açıldıktan sonra:

1. YouTube video URL'sini yapıştırın
2. Video veya Ses formatını seçin
3. Kaliteyi seçin (sadece video için)
4. Kayıt konumunu değiştirmek isterseniz "Gözat" butonunu kullanın
5. Belirli bir zaman aralığı indirmek isterseniz "Belirli aralık indir" kutucuğunu işaretleyin ve başlangıç/bitiş zamanlarını girin (örnek: 01:30, 00:05:30)
6. "İndir" butonuna tıklayın

## Dosya Yapısı


YouDlp/
├── main.py            # Ana uygulama dosyası
├── requirements.txt   # Python bağımlılıkları
├── install.sh         # Otomatik kurulum scripti
└── README.md          # Bu dosya



Kurulumdan sonra dosyalar şunlara kopyalanır:

- ~/.local/share/youdlp/` - Uygulama dosyaları ve sanal ortam
- ~/.local/bin/youdlp` - Başlatma scripti
- ~/.local/share/applications/youdlp.desktop` - Masaüstü kısayolu

## Kaldırma

Uygulamayı kaldırmak için şu komutları çalıştırın:

bash
rm -rf ~/.local/share/youdlp
rm -rf ~/.local/bin/youdlp
rm -rf ~/.local/share/applications/youdlp.desktop


## Sorun Giderme

**"yt-dlp bulunamadı" hatası:**
Sanal ortam doğru yüklenmemiş olabilir. Kurulumu tekrar çalıştırın veya `pip install yt-dlp` komutunu çalıştırın.

**"tkinter bulunamadı" hatası:**
Linux'ta sudo pacman -S tk (Arch) veya sudo apt install python3-tk (Debian/Ubuntu) komutunu çalıştırın.

**İndirme başarısız oluyorsa:**
Bazı videoların erişim kısıtlaması olabilir. YouTube'un kendi sitesinde videoyu açıp açık olup olmadığını kontrol edin.

## Lisans
GPL-3.0
