import itertools
import folium

# Lista de ciudades en el mismo orden que las filas/columnas de la matriz
ciudades = [
    "Bogotá", 
    "Chía", 
    "Tabio", 
    "La Vega", 
    "Fusa", 
    "Ibagué", 
    "Girardot", 
    "Tunja", 
    "Barbosa"
]

# Matriz de distancias (km u otra unidad) entre las ciudades en el orden anterior
matriz = [
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

# Diccionario para mapear cada ciudad a su índice en la matriz
city_to_index = {ciudad: i for i, ciudad in enumerate(ciudades)}

def calcula_costos(ruta):
    """
    Calcula el costo total de una ruta, cerrando el ciclo (vuelve a la ciudad de inicio).
    """
    total_costo = 0
    n = len(ruta)
    for i in range(n):
        ciudad_actual = ruta[i]
        ciudad_siguiente = ruta[(i + 1) % n]  # Cierra el ciclo: la última conecta con la primera
        idx_actual = city_to_index[ciudad_actual]
        idx_siguiente = city_to_index[ciudad_siguiente]
        total_costo += matriz[idx_actual][idx_siguiente]
    return total_costo

def plot_route(route, coords_dict):
    """
    Dibuja en un mapa Folium la ruta dada (lista/tupla de ciudades) en el orden recibido.
    Se agrega el punto de partida al final para cerrar la ruta.
    """
    # Obtenemos la lista de coordenadas en el orden de la ruta
    route_coords = [coords_dict[city] for city in route]
    # Agregamos la primera coordenada al final para cerrar el ciclo en el mapa
    route_coords.append(coords_dict[route[0]])
    
    # Creamos el mapa centrado en la primera ciudad de la ruta
    m = folium.Map(location=route_coords[0], zoom_start=8)
    
    # Agregamos marcadores para cada ciudad (sin duplicar el marcador de la ciudad de inicio)
    for city in route:
        folium.Marker(
            location=coords_dict[city],
            popup=city
        ).add_to(m)
    
    # Dibuja la línea que conecta las ciudades (ruta cerrada)
    folium.PolyLine(route_coords, color="red", weight=2.5, opacity=1).add_to(m)
    
    return m

# Diccionario con coordenadas aproximadas (lat, lon) para cada ciudad
city_coords = {
    "Bogotá":   (4.6607300999999994, -74.0597178),
    "Chía":     (4.8612861, -74.0602202),
    "Tabio":    (4.9160762999999994, -74.0989799),
    "La Vega":  (4.9997310000000006, -74.3394526),
    "Fusa":     (4.3438892, -74.3619791),
    "Ibagué":   (4.4446183, -75.242961999999991),
    "Girardot": (4.2970372999999995, -74.807146),
    "Tunja":    (5.5324627, -73.3615504),
    "Barbosa":  (5.93081, -73.6162499)
}

def main():
    # Fijamos Bogotá como ciudad de inicio para evitar rutas equivalentes por rotación
    ciudad_inicio = "Bogotá"
    
    # Otras ciudades sin incluir la de inicio
    otras_ciudades = [c for c in ciudades if c != ciudad_inicio]

    min_costo = float('inf')
    ruta_optima = None

    # Recorremos todas las permutaciones de las demás ciudades
    for perm in itertools.permutations(otras_ciudades):
        # Construimos la ruta comenzando en 'Bogotá'
        ruta = (ciudad_inicio,) + perm
        costo = calcula_costos(ruta)
        if costo < min_costo:
            min_costo = costo
            ruta_optima = ruta

    # Para mostrar la ruta cerrada, añadimos el punto de partida al final
    ruta_completa = ruta_optima + (ruta_optima[0],)

    # Mostramos la ruta óptima y su costo
    print("Ruta óptima:", " -> ".join(ruta_completa))
    print(f"Distancia total: {min_costo:.2f}km")

    # Generamos el mapa con Folium y lo guardamos en un archivo HTML
    mapa = plot_route(ruta_optima, city_coords)
    mapa.save("ruta_optima.html")
    print("Mapa guardado como 'ruta_optima.html'")

if __name__ == "__main__":
    main()
