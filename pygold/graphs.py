import matplotlib.pyplot as plt
from matplotlib import cycler


def configurar_grafica():
    # Define un ciclo de colores personalizados para los gráficos
    colors = cycler(
        "color", ["#669FEE", "#66EE91", "#9988DD", "#EECC55", "#88BB44", "#FFBBBB"]
    )

    # Configura el color de fondo de la figura a un tono oscuro
    plt.rc("figure", facecolor="#313233")

    # Configura los ejes del gráfico
    plt.rc(
        "axes",
        facecolor="#313233",  # Color de fondo de los ejes
        edgecolor="none",  # Sin borde en los ejes
        axisbelow=True,  # Coloca la cuadrícula por debajo de los elementos gráficos
        grid=True,  # Activa la cuadrícula
        prop_cycle=colors,  # Aplica el ciclo de colores definido anteriormente
        labelcolor="gray",  # Color de las etiquetas de los ejes
    )

    # Configura el color y el estilo de las líneas de la cuadrícula
    plt.rc("grid", color="474A4A", linestyle="solid")

    # Configura el color de las marcas del eje x
    plt.rc("xtick", color="gray")

    # Configura el color y la dirección de las marcas del eje y
    plt.rc("ytick", direction="out", color="gray")

    # Configura el color de fondo y el borde de la leyenda
    plt.rc("legend", facecolor="#313233", edgecolor="#313233")

    # Configura el color del texto en los gráficos
    plt.rc("text", color="#C9C9C9")


# Llama a la función para aplicar la configuración
configurar_grafica()
