# 🐍 Yılan Oyunu (Computer Vision & Hand Tracking)

Kamera (Webcam) aracılığıyla el hareketlerinizi kullanarak oynayabileceğiniz, baştan sona dokunmatik hissi veren modern ve eğlenceli bir **Yılan Oyunu (Snake Game)**!

Uygulama, MediaPipe üzerinden el işaret noktalarını tespit etmek için `cvzone` kullanır. İşaret parmağınızı kontrol ederek yılanın yönünü çizer, çörekleri (donut) yiyerek uzar ve kendi kuyruğunuzdan ve haritadaki rastgele çıkan patlayıcılardan sıyrılarak **En Yüksek Skoru** yapmaya çalışırsınız!

---

## 🌟 Özellikleri (Features)
- 🎯 **%100 Dokunmatik Kontrol:** Eliniz kameradayken işaret parmağınızın ucu ile oyundaki yılanın başını yönlendirirsiniz. 
- 🤏 **Çimdikleyerek Yeniden Başlatma (Pinch-to-Restart):** Oyunu kaybettiğinizde klavyeden tuşlara basmaya son! İşaret parmağınızla başparmağınızı birbirine yaklaştırarak temassız şekilde anında oyuna tekrar başlayın.
- 💣 **Rastgele Bombalar (Engeller):** Ekranın çeşitli yerlerinde aniden beliren bombalara (B) çaprmamaya çalışın! Eğer değerseniz oyun biter.
- 🏆 **Otomatik Kaydedilen "En Yüksek Skor (High Score)" Sistemi:** Skor bilgisayarınıza otomatik (highscore.txt) olarak yazılır. Oyunu kapatıp açsanız dahi başarılarınız her zaman güvende.
- 🎵 **Ses Efektleri (Arkaplan Bip Sesleri):** Donut yerken, yanarken veya baştan başlarken, oyunun anlık etkileşimli hissini artıran uyarı sesleri alırsınız.

---

## 🛠 Kullanılan Kütüphaneler & Bağımlılıklar (Requirements)
Bu projenin kendi bilgisayarınızda sorunsuzca çalışabilmesi için sistemde `Python` yüklü olmalı ve aşağıdaki modüller pip aracılığıyla güncel tutulmalıdır:
- `opencv-python` (cv2) : Kamerayı açıp görüntü işleme sağlar.
- `cvzone` : opencv üzerine kurulmuş, MediaPipe modülleri vs içeren HandTracker kütüphanesi.
- `mediapipe` : Arka planda cvzone'u besleyen gelişmiş el takibi ve makine öğrenmesi algoritmaları.
- `numpy` : Boyut matrislerini oluşturma ve çokgen çarpışma hesaplamaları için gereklidir.

> Kısaca kurulum için şu kodu terminale/komut satırına yazabilirsiniz:
> ```bash
> pip install opencv-python cvzone mediapipe numpy
> ```

---

## ⚙ Nasıl Çalıştırılır? / Oynanış

1. Proje dosyaları arasındaki `Donut.png` (Yiyecek resmi) hazır bulunmalıdır. (Yoksa otomatik düz kare oluşturur).
2. Masaüstündeki veya bulunduğunuz klasördeki terminal üzerinden **`python YılanOyunu.py`** komutunu çalıştırın.
3. Kamera açıldığında elinizi kaldırın ve dik olarak kameranın görmesini sağlayın.
4. Yılan, sadece **İşaret Parmağınızın** ucunu takip ederek onun peşinden ilerleyecektir.
5. Ortaya çıkan Yiyeceği (Donut) işaret parmağınızla yakalamalısınız.
6. Yılan uzadıkça, yılanın gövdesine (kırmızı noktalara) veya nadiren çıkan siyah/kırmızı **B** şeklindeki bombalara **çapmamaya/dokunmamaya** dikkat edin!
7. Oyun Bittiğinde: İşaret parmağınız ve başparmağınızla "Çimdik" hareketi verin (iki ucunu birbirine sürtecek kadar çok yakınlaştırın) oyun anında baştan başlayacaktır.
8. Ayrıca manuel olarak çıkmak isterseniz `ESC` tuşuna, klavyeyle yeniden başlamak isterseniz `R` tuşuna da basabilirsiniz.

---

 
