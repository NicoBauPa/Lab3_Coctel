import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import butter, lfilter
from sklearn.decomposition import FastICA

def butter_bandpass_filter(data, lowcut, highcut, fs, order=1): 
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return lfilter(b, a, data)

ruta_carpeta = r"C:\Users\Nicole\OneDrive\Pictures\Screenshots\SEXTO SEMESTRE\LABS SEÑALES\Lab3.3"
archivos_colores = {"Nicole.wav": "blue", "Gimena.wav": "red", "Majo.wav": "green", "ambiente.wav": "gray"}
archivos_ica = ["Nicole.wav", "Majo.wav", "Gimena.wav"]


archivo_ruido = os.path.join(ruta_carpeta, "ambiente.wav")
potencia_ruido = None

if os.path.exists(archivo_ruido):
    sample_rate_ruido, audio_ruido = wavfile.read(archivo_ruido)
    if len(audio_ruido.shape) > 1:
        audio_ruido = audio_ruido[:, 0]
    audio_ruido = audio_ruido.astype(np.float32)
    potencia_ruido = np.mean(audio_ruido ** 2)


snr_originales = {}
for archivo, color in archivos_colores.items():
    archivo_path = os.path.join(ruta_carpeta, archivo)
    if os.path.exists(archivo_path):
        sample_rate, audio_data = wavfile.read(archivo_path)
        if len(audio_data.shape) > 1:
            audio_data = audio_data[:, 0]
        audio_data = audio_data.astype(np.float32)
        potencia_senal = np.mean(audio_data ** 2)

        if potencia_ruido is not None and potencia_ruido > 0:
            snr_db = 10 * np.log10(potencia_senal / potencia_ruido)
        else:
            snr_db = float('-inf')

        snr_originales[archivo] = snr_db

print("\n Valores de SNR de las señales originales:")
for archivo, snr in snr_originales.items():
    print(f"🔹 {archivo}: {snr:.2f} dB")


audio_signals, sample_rates = [], []
for archivo in archivos_ica:
    archivo_path = os.path.join(ruta_carpeta, archivo)
    if os.path.exists(archivo_path):
        sample_rate, audio_data = wavfile.read(archivo_path)
        if len(audio_data.shape) > 1:
            audio_data = audio_data[:, 0]
        audio_data = audio_data.astype(np.float32)
        audio_data /= np.max(np.abs(audio_data))  # Normalización
        audio_signals.append(audio_data)
        sample_rates.append(sample_rate)


if len(audio_signals) > 0:
    min_length = min(map(len, audio_signals))
    audio_signals = [signal[:min_length] for signal in audio_signals]

    X = np.vstack(audio_signals).T
    ica = FastICA(n_components=len(archivos_ica), max_iter=2000)
    S_ica = ica.fit_transform(X)

     (150 Hz - 4000 Hz)
    S_ica_filtered = np.array([butter_bandpass_filter(S_ica[:, i], 150, 4000, sample_rates[0]) for i in range(len(archivos_ica))]).T

 
    energia = [np.sum(np.square(S_ica_filtered[:, i])) for i in range(len(archivos_ica))]
    idx_voz = np.argmax(energia)
    voz_filtrada = S_ica_filtered[:, idx_voz]

    
    potencia_senal_filtrada = np.mean(voz_filtrada ** 2)

    
    if np.max(np.abs(voz_filtrada)) > 0:
        voz_filtrada /= np.max(np.abs(voz_filtrada))

 
    voz_wav = (voz_filtrada * 32767).astype(np.int16)
    wavfile.write(os.path.join(ruta_carpeta, "voz_sin_ruido.wav"), sample_rates[0], voz_wav)

   
    potencia_senal = potencia_senal_filtrada  # Ahora tomamos la potencia antes de normalizar
    potencia_ruido = np.mean((np.sum(audio_signals, axis=0) - voz_filtrada) ** 2)

    if potencia_ruido > 0:
        SNR_final = 10 * np.log10(potencia_senal / potencia_ruido)
    else:
        SNR_final = float('inf')

    print(f"\n🔹 SNR de la señal predominante: {SNR_final:.2f} dB")

    plt.figure(figsize=(10, 6))
    for i in range(len(archivos_ica)):
        plt.tight_layout()
        plt.show()
        plt.subplot(len(archivos_ica), 1, i+1)
        plt.plot(S_ica_filtered[:, i], label=f"Voz Separada {i+1}", color="green" if i != idx_voz else "r", linewidth=2)
        plt.xlabel("Tiempo (s)")
        plt.ylabel("Amplitud (V)")
        plt.legend()
        plt.grid()
        if i == idx_voz:
            plt.title("Voz separada sin Ruido")
    plt.tight_layout()
    plt.show()
