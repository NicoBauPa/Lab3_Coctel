import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

# Ruta de la carpeta donde están los audios
ruta_carpeta = r"C:\Users\Santiago\OneDrive\Pictures\Screenshots\SEXTO SEMESTRE\LABS SEÑALES\Lab3.3"

# Lista de audios a procesar
archivos = ["Nicole.wav", "Gimena.wav", "Majo.wav", "ambiente.wav"]

# Colores personalizados para cada señal
colores_tiempo = {
    "Nicole.wav": "#17becf",  # Cian
    "Gimena.wav": "#2ca02c",   # Verde
    "Majo.wav": "#9467bd",     # Púrpura
    "ambiente.wav": "#7f7f7f"  # Gris
}

colores_frecuencia = {
   "Nicole.wav": "#17becf",  # Cian
   "Gimena.wav": "#2ca02c",   # Verde
   "Majo.wav": "#9467bd",     # Púrpura
   "ambiente.wav": "#7f7f7f"  # Gris
}

# Diccionario para almacenar potencias de las señales
potencias = {}

# Procesar cada archivo para calcular la potencia
for archivo in archivos:
    try:
        # Leer el archivo de audio
        sample_rate, audio_data = wavfile.read(f"{ruta_carpeta}\\{archivo}")
        
        # Convertir a mono si el audio es estéreo (se toma el primer canal)
        if len(audio_data.shape) > 1:
            audio_data = audio_data[:, 0]
        
        # Convertir la señal a tipo float para cálculos precisos
        audio_data = audio_data.astype(np.float32)

        # Calcular la potencia de la señal
        potencias[archivo] = np.mean(audio_data ** 2)

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {archivo}.")
    except ValueError:
        print(f"Error: Archivo {archivo} no es un WAV válido.")
    except Exception as e:
        print(f"Error al procesar {archivo}: {e}")

# Definir la potencia de ruido (ambiente.wav)
potencia_ruido = potencias.get("ambiente.wav", None)

# Iterar sobre cada archivo para calcular el SNR y graficar
for archivo in archivos:
    try:
        # Leer el archivo de audio
        sample_rate, audio_data = wavfile.read(f"{ruta_carpeta}\\{archivo}")
        
        # Convertir a mono si el audio es estéreo (se toma el primer canal)
        if len(audio_data.shape) > 1:
            audio_data = audio_data[:, 0]
        
        # Convertir la señal a tipo float
        audio_data = audio_data.astype(np.float32)

        # Obtener la potencia de la señal
        potencia_senal = potencias.get(archivo, None)

        # Calcular el SNR si hay potencia de ruido disponible
        if potencia_ruido is not None and potencia_ruido > 0:
            if archivo == "ambiente.wav":
                snr_db = 0  # El ruido de referencia tiene SNR de 0 dB
            else:
                snr_db = 10 * np.log10(potencia_senal / potencia_ruido) if potencia_senal > potencia_ruido else float('-inf')
        else:
            snr_db = float('-inf')

        # Mostrar el SNR en la consola
        print(f"SNR de {archivo}: {snr_db:.2f} dB")

        # Normalizar la señal
        audio_data_norm = audio_data / np.max(np.abs(audio_data))

        # Crear eje de tiempo
        tiempo = np.arange(len(audio_data_norm)) / sample_rate

        # Crear nueva figura para cada señal
        plt.figure(figsize=(12, 5))

        # ========================================
        # Gráfica en el dominio del tiempo
        # ========================================
        plt.subplot(1, 2, 1)
        plt.plot(tiempo, audio_data_norm, color=colores_tiempo[archivo], alpha=0.7)
        plt.xlabel("Tiempo (s)")
        plt.ylabel("Amplitud")
        plt.title(f"Señal Temporal - {archivo}")
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.xlim(0, tiempo[-1])

        # ========================================
        # Gráfica en el dominio de la frecuencia
        # ========================================
        # Calcular la FFT
        N = len(audio_data_norm)
        fft_data = np.fft.fft(audio_data_norm)
        freqs = np.fft.fftfreq(N, d=1/sample_rate)

        # Tomar mitad positiva del espectro
        fft_magnitude = np.abs(fft_data[:N//2])
        freqs = freqs[:N//2]

        plt.subplot(1, 2, 2)
        plt.plot(freqs, fft_magnitude, label=f"SNR: {snr_db:.2f} dB", 
                 color=colores_frecuencia[archivo], alpha=0.7)
        plt.xlabel("Frecuencia (Hz)")
        plt.ylabel("Magnitud")
        plt.title(f"Espectro de Frecuencias - {archivo}")
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.xscale("log")
        plt.xlim(20, 10000)

        # Mostrar la figura de cada señal por separado
        plt.tight_layout()
        plt.show()

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {archivo}.")
    except ValueError:
        print(f"Error: Archivo {archivo} no es un WAV válido.")
    except Exception as e:
        print(f"Error al procesar {archivo}: {e}")




