import math
import folium

# ======== Datos y Algoritmo TSP (Held-Karp) ========

# Lista de ciudades y matriz de distancias (km)
ciudades = ["Bogotá", "Chía", "Tabio", "La Vega", "Fusa", "Ibagué", "Girardot", "Tunja", "Barbosa"]
dist = [
    [0.00,  27.17,  39.70,  66.13,  69.25, 201.05, 142.82, 142.12, 187.52],
    [27.17,  0.00,   9.50,  67.74,  93.27, 214.36, 146.88, 124.18, 166.54],
    [39.70,  9.50,   0.00,  60.52,  97.94, 219.02, 151.55, 128.18, 165.14],
    [66.13, 67.74,  60.52,   0.00, 121.89, 223.86, 175.50, 193.34, 234.09],
    [69.25, 93.27,  97.94, 121.89,   0.00, 131.55,  70.47, 208.48, 253.88],
    [201.05,214.36, 219.02, 223.86, 131.55,  0.00,  68.12, 339.93, 380.71],
    [142.82,146.88, 151.55, 175.50,  70.47, 68.12,   0.00, 272.49, 313.24],
    [142.12,124.18, 128.18, 193.34, 208.48, 339.93, 272.49,  0.00,  70.99],
    [187.52,166.54, 165.14, 234.09, 253.88, 380.71, 313.24, 70.99,   0.00]
]
n = len(ciudades)
INF = math.inf

# Inicialización de las tablas DP y de predecesores para reconstrucción del tour
dp = [[INF] * n for _ in range(1 << n)]
padre = [[None] * n for _ in range(1 << n)]
dp[1][0] = 0  # Partimos de Bogotá (índice 0)

# Algoritmo Held-Karp
for mask in range(1 << n):
    for ultimo in range(n):
        if not (mask & (1 << ultimo)) or dp[mask][ultimo] == INF:
            continue
        for siguiente in range(n):
            if mask & (1 << siguiente):
                continue
            nueva_mask = mask | (1 << siguiente)
            costo = dp[mask][ultimo] + dist[ultimo][siguiente]
            if costo < dp[nueva_mask][siguiente]:
                dp[nueva_mask][siguiente] = costo
                padre[nueva_mask][siguiente] = ultimo

# Determinar el tour óptimo y costo mínimo
mask_completa = (1 << n) - 1
min_cost = INF
ultimo_final = None
for i in range(1, n):
    costo_total = dp[mask_completa][i] + dist[i][0]
    if costo_total < min_cost:
        min_cost = costo_total
        ultimo_final = i

# Reconstrucción del recorrido óptimo
tour = []
mask = mask_completa
ultimo = ultimo_final
while ultimo is not None:
    tour.append(ultimo)
    nuevo = padre[mask][ultimo]
    mask &= ~(1 << ultimo)
    ultimo = nuevo

tour.reverse()  # Obtener el orden correcto (de Bogotá hasta la última ciudad)
tour.append(0)  # Cerrar el ciclo regresando a Bogotá

# Mostrar resultados en consola
print("Ruta óptimo:", " -> ".join(ciudades[i] for i in tour))
print(f"Distancia total: {min_cost:.2f}km")


# ======== Representación Gráfica con Folium ========

# Diccionario con coordenadas aproximadas de cada ciudad
coords = {
    "Bogotá":   (4.6607301, -74.0597178),
    "Chía":     (4.8612861, -74.0602202),
    "Tabio":    (4.9160763, -74.0989799),
    "La Vega":  (4.999731,  -74.3394526),
    "Fusa":     (4.3438892, -74.3619791),
    "Ibagué":   (4.4446183, -75.2429620),
    "Girardot": (4.2970373, -74.807146),
    "Tunja":    (5.5324627, -73.3615504),
    "Barbosa":  (5.93081,   -73.6162499)
}

# Crear el mapa centrado en Bogotá
mapa = folium.Map(location=coords["Bogotá"], zoom_start=7)

# Agregar marcadores para cada ciudad
for ciudad in ciudades:
    folium.Marker(location=coords[ciudad], popup=ciudad).add_to(mapa)

# Dibujar la ruta óptima siguiendo el tour
ruta_coords = [coords[ciudades[i]] for i in tour]
folium.PolyLine(ruta_coords, color="red", weight=5, opacity=0.8).add_to(mapa)

# Guardar el mapa en un archivo HTML
mapa.save("tour_optimo_map.html")
print("El mapa ha sido guardado en 'tour_optimo_map.html'")
