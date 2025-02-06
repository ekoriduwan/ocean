import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

def optimize_charging_stations(zones, budget, evs_per_zone, distances, congestion_levels, charge_station_proportion, peak_hour_proportion, serving_rate, lambda_coef):
    # Menghitung permintaan pengisian di setiap zona
    charging_demand_per_zone = evs_per_zone * charge_station_proportion

    # Mendefinisikan fungsi biaya sosial
    def social_cost(x):
        total_cost = 0
        for i in range(zones):
            for j in range(zones):
                if i != j:
                    travel_time = lambda_coef * distances[i, j] * congestion_levels[i, j]
                    queuing_time = charging_demand_per_zone[j] / (serving_rate * x[j])
                    total_cost += travel_time + queuing_time
        return total_cost

    # Mendefinisikan batasan
    constraints = [{'type': 'eq', 'fun': lambda x: np.sum(x) - budget}]
    bounds = [(1, budget) for _ in range(zones)]

    # Tebakan awal untuk jumlah pengisi daya di setiap zona
    x0 = np.ones(zones) * (budget / zones)

    # Mengoptimalkan alokasi stasiun pengisian
    result = minimize(social_cost, x0, bounds=bounds, constraints=constraints)

    # Membulatkan alokasi optimal ke bilangan bulat terdekat
    optimal_allocation = np.round(result.x).astype(int)
    print("Alokasi optimal stasiun pengisian:", optimal_allocation)

    # Menampilkan hasil dalam bentuk grafik PIE dengan jumlah stasiun pengisian
    plt.figure(figsize=(10, 7))
    plt.pie(optimal_allocation, labels=[f'Zona {i+1}: {optimal_allocation[i]}' for i in range(zones)], startangle=140)
    plt.axis('equal')
    plt.title('Alokasi Optimal Stasiun Pengisian')
    plt.show()

# Input pengguna untuk parameter dengan panduan dalam bahasa Indonesia
print("Silakan masukkan parameter berikut:")
zones = int(input("Masukkan jumlah zona (misalnya, 23): "))
budget = float(input("Masukkan rencana pembangunan SPKLU (misalnya, 300): "))

# Input jumlah EV di setiap zona
evs_per_zone = []
print(f"Masukkan perkiraan jumlah kendaraan listrik (EV) di setiap zona (misalnya, untuk {zones} zona):")
for i in range(zones):
    evs_per_zone.append(int(input(f"Zona {i+1}: ")))
evs_per_zone = np.array(evs_per_zone)

# Input jarak antar zona
distances = []
print(f"Masukkan jarak antar zona (km) dalam bentuk matriks {zones}x{zones} (misalnya, jarak antara zona 1 dan zona 2):")
for i in range(zones):
    row = []
    for j in range(zones):
        if i == j:
            row.append(0.0)  # Jarak dari satu zona ke dirinya sendiri adalah 0
        else:
            row.append(float(input(f"Jarak dari Zona {i+1} ke Zona {j+1}: ")))
    distances.append(row)
distances = np.array(distances)

# Input tingkat kemacetan antar zona
congestion_levels = []
print(f"Masukkan tingkat kemacetan antar zona dalam bentuk matriks {zones}x{zones} (misalnya, tingkat kemacetan antara zona 1 dan zona 2):")
print("Nilai rujukan untuk tingkat kemacetan: 0.1 (rendah), 0.5 (sedang), 1.0 (tinggi)")
for i in range(zones):
    row = []
    for j in range(zones):
        if i == j:
            row.append(0.0)  # Tingkat kemacetan dari satu zona ke dirinya sendiri adalah 0
        else:
            row.append(float(input(f"Tingkat kemacetan dari Zona {i+1} ke Zona {j+1}: ")))
    congestion_levels.append(row)
congestion_levels = np.array(congestion_levels)

charge_station_proportion = float(input("Masukkan proporsi EV yang mengisi daya di stasiun pengisian (misalnya, 0.10 untuk 10%): "))
peak_hour_proportion = float(input("Masukkan proporsi EV yang mengisi daya selama jam sibuk (misalnya, 0.10 untuk 10%): "))
serving_rate = float(input("Masukkan tingkat layanan pengisi daya (jumlah EV yang dapat dilayani oleh satu pengisi daya dalam satu jam, misalnya, 6): "))
lambda_coef = float(input("Masukkan koefisien linier untuk waktu perjalanan. Semakin tinggi nilai koefisien, semakin besar pengaruh jarak & tingkat kemacetan terhadap waktu perjalanan (misalnya, 0.2): "))

# Penjelasan tambahan untuk setiap parameter:
print("\nPenjelasan tambahan:")
print("1. Jumlah zona: Jumlah zona yang ingin Anda analisis. Misalnya, jika Anda ingin menganalisis 23 zona, masukkan '23'.")
print("2. Anggaran: Anggaran total yang tersedia untuk membangun stasiun pengisian. Misalnya, jika anggaran Anda adalah 300 unit, masukkan '300'.")
print("3. Jumlah EV di setiap zona: Masukkan jumlah kendaraan listrik (EV) di setiap zona.")
print("4. Jarak antar zona: Masukkan jarak antar zona dalam bentuk matriks. Misalnya, jarak antara zona 1 dan zona 2.")
print("5. Tingkat kemacetan antar zona: Masukkan tingkat kemacetan antar zona dalam bentuk matriks. Misalnya, tingkat kemacetan antara zona 1 dan zona 2.")
print("   Nilai rujukan untuk tingkat kemacetan: 0.1 (rendah), 0.5 (sedang), 1.0 (tinggi)")
print("6. Proporsi pengisian di stasiun: Proporsi EV yang mengisi daya di stasiun pengisian daripada di rumah. Misalnya, jika 10% dari EV mengisi daya di stasiun pengisian, masukkan '0.10'.")
print("7. Proporsi pengisian selama jam sibuk: Proporsi EV yang mengisi daya selama jam sibuk. Misalnya, jika 10% dari EV mengisi daya selama jam sibuk, masukkan '0.10'.")
print("8. Tingkat layanan pengisi daya: Jumlah EV yang dapat dilayani oleh satu pengisi daya dalam satu jam. Misalnya, jika satu pengisi daya dapat melayani 6 EV per jam, masukkan '6'.")
print("9. Koefisien linier untuk waktu perjalanan: Koefisien ini digunakan untuk menghitung waktu perjalanan berdasarkan jarak dan tingkat kemacetan.")
print("   Nilai rujukan untuk koefisien linier: 0.2")
print("   Koefisien linier ini mengukur seberapa besar pengaruh jarak dan tingkat kemacetan terhadap waktu perjalanan. Semakin tinggi nilai koefisien, semakin besar pengaruhnya.")

# Menjalankan optimasi dengan parameter yang ditentukan oleh pengguna
optimize_charging_stations(zones, budget, evs_per_zone, distances, congestion_levels, charge_station_proportion, peak_hour_proportion, serving_rate, lambda_coef)
