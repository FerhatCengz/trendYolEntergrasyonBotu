from pytrends.request import TrendReq
import matplotlib.pyplot as plt
import pandas as pd
import logging

# Logging yapılandırması
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Popüler e-ticaret kategorileri
categories = [
    "Spor Ayakkabı", "Topuklu Ayakkabı", "Günlük Ayakkabı",
    "Telefon", "Akıllı Saat", "Laptop",
    "Spor Giyim", "Fitness Ekipmanları",
    "Makyaj", "Cilt Bakımı", "Parfüm"
]

# Google Trends verilerini çek
def fetch_trend_data(categories):
    pytrends = TrendReq(hl='tr-TR', tz=360)
    trend_data_list = []
    
    for category in categories:
        try:
            logging.info(f"{category} kategorisi için veri çekiliyor...")
            pytrends.build_payload([category], cat=0, timeframe='today 12-m', geo='TR', gprop='')
            trend_data = pytrends.interest_over_time()
            
            if not trend_data.empty:
                trend_data_list.append(trend_data[[category]])
        except Exception as e:
            logging.error(f"{category} kategorisi için veri çekme hatası: {e}")
    
    if trend_data_list:
        return pd.concat(trend_data_list, axis=1)
    else:
        logging.warning("Hiçbir kategori için trend verisi bulunamadı.")
        return pd.DataFrame()

# Trend verilerini görselleştir
def plot_trends(trend_data):
    plt.figure(figsize=(16, 10))  # Grafiğin boyutunu genişlettik
    ax = plt.gca()

    # Her bir kategori için çizim yap
    for column in trend_data.columns:
        trend_data[column].plot(ax=ax, label=column, linewidth=2)

    plt.title("Google Trends: E-Ticaret Ürün Aramaları", fontsize=14)
    plt.xlabel('Tarih', fontsize=12)
    plt.ylabel('İlgi Düzeyi', fontsize=12)
    plt.legend(loc='upper right', fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.6)

    # En yüksek ilgi düzeyini işaretle
    for column in trend_data.columns:
        max_interest = trend_data[column].max()
        max_date = trend_data[trend_data[column] == max_interest].index[0]

        # Etiketlerin daha iyi yerleştirilmesi
        ax.annotate(
            f'{column}: {int(max_interest)}', 
            xy=(max_date, max_interest), 
            xytext=(max_date, max_interest + 20),  # Daha iyi görünürlük için metin konumunu yukarı taşıdık
            arrowprops=dict(facecolor='black', arrowstyle="->", lw=1),
            fontsize=9, 
            color='black',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='black')
        )
    
    plt.tight_layout(pad=3)  # Boşlukları artırarak yerleşimi optimize ettik
    plt.show()

# Trend verilerini analiz et ve en popüler kategoriyi belirle
def analyze_trends(trend_data):
    if trend_data.empty:
        logging.warning("Trend verileri boş. Analiz yapılamadı.")
        return

    # Ortalama ilgi düzeylerini hesapla
    mean_interest = trend_data.mean()
    std_interest = trend_data.std()
    max_interest = trend_data.max()
    
    # En popüler kategoriyi bul
    most_popular_category = mean_interest.idxmax()
    most_popular_mean = mean_interest.max()

    print(f"\nGoogle Trends'e göre ortalama en popüler ürün kategorisi: '{most_popular_category}'")
    print(f"Bu kategori ortalama ilgi düzeyine {most_popular_mean:.2f} ulaştı.")
    
    # Ek analiz: Ortalama ilgi düzeyine göre en popüler ilk N kategoriler
    top_n = 3
    top_categories = mean_interest.nlargest(top_n)
    print("\nOrtalama ilgi düzeyine göre en popüler ilk {} kategoriler:".format(top_n))
    for category, interest in top_categories.items():
        max_val = max_interest[category]
        max_date = trend_data[category].idxmax().strftime('%Y-%m-%d')
        print(f"Kategori: {category}, Ortalama İlgi Düzeyi: {interest:.2f}, En Yüksek İlgi Düzeyi: {max_val} (Tarih: {max_date})")
    
    # Varyansı göster
    print("\nKategorilerin ilgi düzeyi varyansı:")
    for category, variance in std_interest.items():
        print(f"Kategori: {category}, Varyans: {variance:.2f}")

# Ana çalışma mantığı
def main():
    # Popüler kategoriler için trend verilerini al
    trend_data = fetch_trend_data(categories)
    
    if not trend_data.empty:
        # Trend verilerini görselleştir ve analiz et
        plot_trends(trend_data)
        analyze_trends(trend_data)
    else:
        logging.warning("Trend verileri alınamadı. Analiz yapılamadı.")

if __name__ == "__main__":
    main()
