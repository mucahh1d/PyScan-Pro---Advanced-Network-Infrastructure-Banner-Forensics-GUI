# PyScan Pro - Advanced Network Infrastructure & Banner Forensics GUI

PyScan Pro; sızma testleri, yerel ağ denetimleri ve siber güvenlik analizleri için geliştirilmiş, **`customtkinter` altyapılı, modern ve yüksek performanslı bir ağ zafiyet tarama (Port Scanner) yazılımıdır.**

Arka planda çalışan 150 thread'li asenkron multithreading motoru sayesinde ağdaki zafiyetleri saniyeler içinde tespit ederken; kullanıcı dostu, donma yapmayan entegre grafik arayüzü (GUI) ile son derece konforlu bir analiz deneyimi sunar.

## 🚀 Öne Çıkan Özellikler

* **🎨 Modern CustomTkinter GUI:** Sıkıcı CLI ekranları yerine, karanlık mod (dark mode) destekli, optimize edilmiş ve kullanıcı dostu pencereli arayüz.
* **⚡ 150 Thread Gücünde Multithreading:** Arka planda aynı anda 150 iş parçacığı yürüterek tüm alt ağları (Subnet) ve binlerce portu saniyeler içinde tarar.
* **🌐 Gelişmiş Hedef Çözümleme (Target Resolution):** Tekil IP adreslerini, alan adlarını (Domain) veya CIDR formatındaki ağ aralıklarını (`192.168.1.0/24` gibi 254 cihazı) otomatik olarak parse eder.
* **🎯 Hazır & Özel Port Profilleri:**
  * `Top 20 Common`: En kritik ve zafiyet barındıran 20 portu hedefler.
  * `Web Services`: Web sunucularına özel portları (`80`, `443`, `8080` vb.) tarar.
  * `Full (1-1024)`: En popüler ilk 1024 portun tamamını inceler.
  * `Custom`: Virgülle veya tireyle ayrılmış (`22,80,1-500`) özel port aralıklarını esnekçe tarar.
* **👁️ Canlı Sistem Logları & Donmayan Mimari:** Entegre `queue` (kuyruk) yapısı sayesinde tarama esnasında arayüz asla kilitlenmez (freeze olmaz). Arka plan durumları canlı log alanından anlık izlenebilir.
* **📊 Banner Grabbing (Versiyon Tespiti):** Sadece portun açık olduğunu söylemekle kalmaz; HTTP GET istekleri ve raw socket analizleri ile sunucudaki yazılım versiyonlarını (`Server: nginx/1.18.0` gibi) çeker.
* **📥 Excel Uyumlı Raporlama (Export CSV):** Tarama sonuçlarını tek tıkla zaman damgalı (`scan_results_YYYYMMDD_HHMMSS.csv`) rapor dosyası olarak dışarı aktarır.

## 🛠️ Sistem Gereksinimleri & Kurulum

Yazılımın çalışması için sisteminizde **Python 3.8** veya üzeri bir sürümün yüklü olması gerekmektedir.

1. Bağımlılıkları yükleyin:
```bash
pip install customtkinter
```

2. Uygulamayı başlatın:
```bash
python advanced_scanner.py
```

## 📋 Örnek Tarama Senaryoları

* **Senaryo A (Tekil Cihaz Analizi):** Target alanına cihaz IP'sini girin, `Top 20 Common` profilini seçip `START SCAN` butonuna basın. Cihazın açık servisleri ve versiyonları saniyeler içinde listelenecektir.
* **Senaryo B (Tüm Subnet Taraması):** Target alanına `192.168.1.0/24` yazın, `Web Services` seçeneği ile ağdaki tüm aktif web sunucularını ve yönetim panellerini tek bir tabloda listeleyin.
* **Senaryo C (Özel Port Kontrolü):** Target alanına hedef sunucuyu yazın, `Custom` seçeneğini işaretleyip yanındaki kutuya `22, 3306, 5432` yazarak doğrudan kritik servislerin durumunu kontrol edin.

## ⚠️ Yasal Uyarı / Disclaimer

**TR:** Bu yazılım tamamen eğitim, yerel ağ güvenliği denetimleri ve yasal sızma testleri süreçlerinde altyapı analizi yapmak amacıyla geliştirilmiştir. Yetkisiz veya izinsiz ağlar üzerinde kullanımı tamamen kullanıcının sorumluluğundadır. Geliştirici (Mücahid Balcı), oluşabilecek yasal sorunlardan veya kötüye kullanımlardan dolayı hiçbir sorumluluk kabul etmez.

**EN:** This software is developed strictly for educational purposes, local network auditing, and legal penetration testing. Any unauthorized use on external networks is entirely the responsibility of the user. The developer (Mücahid Balcı) assumes no liability for any misuse or damage caused by this program.

## 👤 Geliştirici / Developer

* **Mücahid Balcı** - *Genç Girişimci & Siber Güvenlik Araştırmacısı*
* **GitHub:** [@mucahhid](https://github.com)
* **Web Sitesi:** [mucahidinc.freedev.app](https://freedev.app)
