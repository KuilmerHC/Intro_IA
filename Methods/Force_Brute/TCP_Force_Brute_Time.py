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
    horas = int(min_costo // 60)
    minutos = int(min_costo % 60)
    print(f"Tiempo total: {horas} horas y {minutos} minutos")

    # Generamos el mapa con Folium y lo guardamos en un archivo HTML
    mapa = plot_route(ruta_optima, city_coords)
    mapa.save("ruta_optima.html")
    print("Mapa guardado como 'ruta_optima.html'")

if __name__ == "__main__":
    main()
