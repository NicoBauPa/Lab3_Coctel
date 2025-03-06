import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile


ruta_carpeta = r"C:\Users\Nicole\OneDrive\Pictures\Screenshots\SEXTO SEMESTRE\LABS SEÑALES\Lab3.3"


archivos = ["Nicole.wav", "Gimena.wav", "Majo.wav", "ambiente.wav"]


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


potencias = {}


for archivo in archivos:
    try:
        
        sample_rate, audio_data = wavfile.read(f"{ruta_carpeta}\\{archivo}")
        
        
        if len(audio_data.shape) > 1:
            audio_data = audio_data[:, 0]
        
        
        audio_data = audio_data.astype(np.float32)

        
        potencias[archivo] = np.mean(audio_data ** 2)

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {archivo}.")
    except ValueError:
        print(f"Error: Archivo {archivo} no es un WAV válido.")
    except Exception as e:
        print(f"Error al procesar {archivo}: {e}")


potencia_ruido = potencias.get("ambiente.wav", None)

for archivo in archivos:
    try:
       
        sample_rate, audio_data = wavfile.read(f"{ruta_carpeta}\\{archivo}")
        
        
        if len(audio_data.shape) > 1:
            audio_data = audio_data[:, 0]
        
      
        audio_data = audio_data.astype(np.float32)

        potencia_senal = potencias.get(archivo, None)

       
        if potencia_ruido is not None and potencia_ruido > 0:
            if archivo == "ambiente.wav":
                snr_db = 0  # El ruido de referencia tiene SNR de 0 dB
            else:
                snr_db = 10 * np.log10(potencia_senal / potencia_ruido) if potencia_senal > potencia_ruido else float('-inf')
        else:
            snr_db = float('-inf')

        
        print(f"SNR de {archivo}: {snr_db:.2f} dB")

        
        audio_data_norm = audio_data / np.max(np.abs(audio_data))

      
        tiempo = np.arange(len(audio_data_norm)) / sample_rate

        
        plt.figure(figsize=(12, 5))

        
        plt.subplot(1, 2, 1)
        plt.plot(tiempo, audio_data_norm, color=colores_tiempo[archivo], alpha=0.7)
        plt.xlabel("Tiempo (s)")
        plt.ylabel("Amplitud")
        plt.title(f"Señal Temporal - {archivo}")
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.xlim(0, tiempo[-1])

       
        
        N = len(audio_data_norm)
        fft_data = np.fft.fft(audio_data_norm)
        freqs = np.fft.fftfreq(N, d=1/sample_rate)

        
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

        
        plt.tight_layout()
        plt.show()

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {archivo}.")
    except ValueError:
        print(f"Error: Archivo {archivo} no es un WAV válido.")
    except Exception as e:
        print(f"Error al procesar {archivo}: {e}")




