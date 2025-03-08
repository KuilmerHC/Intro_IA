import math
import folium

# ======== Datos y Algoritmo TSP (Held-Karp) ========

# Lista de ciudades y matriz de distancias (km)
ciudades = ["Bogotá", "Chía", "Tabio", "La Vega", "Fusa", "Ibagué", "Girardot", "Tunja", "Barbosa"]
dist = [
    [0.00, 44.79, 66.72, 88.06, 133.70, 259.86, 200.89, 139.17, 230.70],
    [44.79, 0.00, 29.53, 84.24, 150.70, 263.44, 196.82, 118.59, 206.94],
    [66.72, 29.53, 0.00, 91.09, 160.44, 273.16, 206.54, 135.04, 209.61],
    [88.06, 84.24, 91.09, 0.00, 176.47, 286.34, 222.58, 200.19, 288.49],
    [133.70, 150.70, 160.44, 176.47, 0.00, 137.25, 84.57, 260.98, 352.51],
    [259.86, 263.44, 273.16, 286.34, 137.25, 0.00, 73.51, 380.34, 467.68],
    [200.89, 196.82, 206.54, 222.58, 84.57, 73.51, 0.00, 312.75, 401.07],
    [139.17, 118.59, 135.04, 200.19, 260.98, 380.34, 312.75, 0.00, 96.69],
    [230.70, 206.94, 209.61, 288.49, 352.51, 467.68, 401.07, 96.69, 0.00]
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
horas = int(min_cost // 60)
minutos = int(min_cost % 60)
print(f"Tiempo total: {horas} horas y {minutos} minutos")


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