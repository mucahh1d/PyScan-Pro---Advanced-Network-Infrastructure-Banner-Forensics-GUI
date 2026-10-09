# PyScan Pro - Advanced Network Infrastructure & Banner Forensics GUI

PyScan Pro; sızma testleri, yerel ağ denetimleri ve siber güvenlik analizleri için geliştirilmiş, **`customtkinter` altyapılı, modern ve yüksek performanslı bir ağ zafiyet tarama (Port Scanner) yazılımıdır.**

Arka planda çalışan 150 thread'li asenkron multithreading motoru sayesinde ağdaki zafiyetleri saniyeler içinde tespit ederken; kullanıcı dostu, donma yapmayan entegre grafik arayüzü (GUI) ile son derece konforlu bir analiz deneyimi sunar.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Stars](https://img.shields.io/github/stars/mucahidbalci/PyScanPro.svg)

## 🚀 Öne Çıkan Özellikler

* **🎨 Modern CustomTkinter GUI:** Sıkıcı CLI ekranları yerine, karanlık mod (dark mode) destekli, optimize edilmiş ve kullanıcı dostu pencereli arayüz.
* **⚡ 150 Thread Gücünde Multithreading:** Arka planda aynı anda 150 iş parçacığı yürüterek tüm alt ağları (Subnet) ve binlerce portu saniyeler içinde tarar.
* **🌐 Gelişmiş Hedef Çözümleme (Target Resolution):** Tekil IP adreslerini, alan adlarını (Domain) veya CIDR formatındaki ağ aralıklarını (`192.168.1.0/24` gibi 254 cihazı) otomatik olarak parse eder.
* **🎯 Hazır & Özel Port Profilleri:**
  * `Top 20 Common`: En kritik ve zafiyet barındıran 20 portu hedefler.
  * `Web Services`: Web sunucularına özel portları (`80`, `443`, `8080`, `8443` vb.) tarar.
  * `Full (1-1024)`: En popüler ilk 1024 portun tamamını kapsamlı şekilde inceler.
  * `Custom`: Virgülle veya tireyle ayrılmış (`22,80,1-500`) özel port aralıklarını esnekçe tarar.
* **👁️ Canlı Sistem Logları & Donmayan Mimari:** Entegre `queue` (kuyruk) yapısı sayesinde tarama esnasında arayüz asla kilitlenmez (freeze olmaz). Arka plan durumları canlı log alanından anlık izlenebilir.
* **📊 Banner Grabbing (Versiyon Tespiti):** Sadece portun açık olduğunu söylemekle kalmaz; HTTP GET istekleri ve raw socket analizleri ile sunucudaki yazılım versiyonlarını (`Server: nginx/1.18.0` gibi) çeker.
* **📥 Excel Uyumlu Raporlama (Export CSV):** Tarama sonuçlarını tek tıkla zaman damgalı (`scan_results_YYYYMMDD_HHMMSS.csv`) rapor dosyası olarak dışarı aktarır.

## 🎥 Canlı Demo

Aşağıdaki 20 saniyelik demo videoda PyScanPro'nun 150 thread multithreading motoru ile **tüm tarama modlarını** (Top 20 Common, Web Services ve Full 1-1024) gerçek zamanlı olarak çalışırken görebilirsiniz:

![PyScanPro Demo](assets/pscanspro-demo.gif)

> **Videoda neler oluyor?** 
> - **Top 20 Common**: Hedef IP'ye hızlı tarama (en kritik portlar)
> - **Web Services**: Web sunucularına özel port taraması (80, 443, 8080...)
> - **Full Scan (1-1024)**: İlk 1024 portun kapsamlı taraması
> - 150 thread aynı anda çalışıyor (arayüz donmuyor!)
> - Bulunan açık portlar ve servis versiyonları anlık listeleniyor
> - Tüm sonuçlar CSV olarak kaydedilmeye hazır

![PyScanPro GUI](https://github.com/user-attachments/assets/e1e33d43-c4ae-450a-9680-77beca091436)

## 🛠️ Sistem Gereksinimleri & Kurulum

Yazılımın çalışması için sisteminizde **Python 3.8** veya üzeri bir sürümün yüklü olması gerekmektedir.

1. Bağımlılıkları yükleyin:
```bash
git clone https://github.com/mucahidbalci/PyScanPro
pip install -r requirements.txt
```

2. Uygulamayı başlatın:
```bash
python advanced_scanner.py
```

## 📋 Örnek Tarama Senaryoları

* **Senaryo A (Tekil Cihaz Analizi):** Target alanına cihaz IP'sini girin, `Top 20 Common` profilini seçip `START SCAN` butonuna basın. Cihazın açık servisleri ve versiyonları saniyeler içinde listelenecektir.
* **Senaryo B (Tüm Subnet Taraması):** Target alanına `192.168.1.0/24` yazın, `Web Services` seçeneği ile ağdaki tüm aktif web sunucularını ve yönetim panellerini tek bir tabloda listeleyin.
* **Senaryo C (Kapsamlı Güvenlik Denetimi):** Target alanına hedef sunucuyu yazın, `Full (1-1024)` seçeneği ile tüm kritik portları tarayın ve detaylı rapor alın.
* **Senaryo D (Özel Port Kontrolü):** Target alanına hedef sunucuyu yazın, `Custom` seçeneğini işaretleyip yanındaki kutuya `22, 3306, 5432` yazarak doğrudan kritik servislerin (SSH, MySQL, PostgreSQL) durumunu kontrol edin.

## ⚠️ Yasal Uyarı / Disclaimer

**TR:** Bu yazılım tamamen eğitim, yerel ağ güvenliği denetimleri ve yasal sızma testleri süreçlerinde altyapı analizi yapmak amacıyla geliştirilmiştir. Yetkisiz veya izinsiz ağlar üzerinde kullanımı tamamen kullanıcının sorumluluğundadır. Geliştirici (Mücahid Balcı), oluşabilecek yasal sorunlardan veya kötüye kullanımlardan dolayı hiçbir sorumluluk kabul etmez.

**EN:** This software is developed strictly for educational purposes, local network auditing, and legal penetration testing. Any unauthorized use on external networks is entirely the responsibility of the user. The developer (Mücahid Balcı) assumes no liability for any misuse or damage caused by this program.

## 👤 Geliştirici / Developer

* **Mücahid Balcı** - *Genç Girişimci & Siber Güvenlik Araştırmacısı*
* **GitHub:** [@mucahidbalci](https://github.com/mucahidbalci)
* **Web Sitesi:** [mucahidbalci.github.io](https://mucahidbalci.github.io)

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakınız.
