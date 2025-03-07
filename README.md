# Laboratorio 3. Problema del coctel
## Introducción:
En el presente laboratorio se explora el "problema de la fiesta de cóctel", que consiste en simular una conversación en un entorno ruidoso con múltiples fuentes de sonido. Utilizando un tres micrófonos (uno por integrante del grupo) con el fin de captar por medio de celulares a diversas distancias el sonido y percibido calcular el SNR de cada
una de las señales, adicionalmente se realiza un análisis espectral con la tranformada rápida de fourier para cada señal, separando el ruido de la señal por medio de filtrado.

## Paso a paso:
1. Configuración del sistema:
   
- Conectar los tres micrófonos al sistema de adquisición de datos.
- Ubicarlos en la sala de manera que cada uno capture una combinación diferente de sonidos.
- Colocar a tres personas en posiciones fijas y orientadas en distintas direcciones para simular un ambiente con varias fuentes de sonido (como en una fiesta).
  
2. Captura de la señal:
  
- Pedir a cada persona que diga una frase diferente al mismo tiempo mientras los micrófonos graban.
- Guardar las grabaciones para analizarlas después.
- Medir la cantidad de ruido en el ambiente (SNR). Si alguna señal tiene mucho ruido, repetir la medición y explicar por qué ocurrió.
  
3. Procesamiento de señales:
   
- Analizar cómo varía el sonido con el tiempo y en frecuencia.
- Investigar y aplicar técnicas para separar las voces, como el Análisis de Componentes Independientes (ICA).
  
5. Evaluación de resultados
- Comparar la señal aislada con la original.
. Usar métricas como la relación señal/ruido (SNR) para medir qué tan bien se logró separar cada voz

### Ubicación Microfonos:

![image](https://github.com/user-attachments/assets/25055362-f824-4df7-84e1-2f07ddf13da8)

Se observa la disposición de tres dispositivos (celulares) formando un triángulo dentro de una sala de laboratorio, con sus distancias medidas (2.23 m, 2.11 m y 2.27 m). Estos micrófonos captarán el sonido de las personas ubicadas estratégicamente, quienes emitirán frases distintas para simular un ambiente con múltiples fuentes sonoras.
Durante la captura de la señal, se registrarán las voces y se medirá la relación señal/ruido (SNR) para evaluar la calidad del audio.

### Explicacion código Python:

-Importación de librerías:

```
import os  
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import butter, lfilter
from sklearn.decomposition import FastICA

```
- **os** Para manejar rutas y verificar la existencia de archivos.
numpy→ Para cálculos numéricos y procesamiento de señales.
- **NumPy** para cálculos numéricos.
- **Matplotlib** tpara graficar las señales.
- **scipy.io.wavfile** para leer archivos de audio en formato WAV
- **scipy.signal.lfilter**  Para aplicar un filtro pasa banda y eliminar el ruido fuera del rango de voz.
- **sklearn.decomposition.FastICA** Para aplicar Análisis de Componentes Independientes (ICA) y separar la voz del ruido.

- Definición de la ruta de la carpeta y archivos:

```  
ruta_carpeta = r"C:\Users\Nicole\OneDrive\Pictures\Screenshots\SEXTO SEMESTRE\LABS SEÑALES\Lab3.3"
archivos = ["Nicole.wav", "Gimena.wav", "Majo.wav", "ambiente.wav"]

```
Se define la ruta donde están los archivos de audio y se almacenan en ruta_carpeta.
Luego, archivos es una lista con los nombres de los archivos de audio a procesar.

- Cálculo de la potencia de las señales.
```  
potencias = {}

for archivo in archivos:
    try:
        sample_rate, audio_data = wavfile.read(f"{ruta_carpeta}\\{archivo}")

        if len(audio_data.shape) > 1:
            audio_data = audio_data[:, 0]  # Convertir a mono si es estéreo

        audio_data = audio_data.astype(np.float32)  # Convertir a flotante
        potencias[archivo] = np.mean(audio_data ** 2)  # Cálculo de potencia

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {archivo}.")
    except ValueError:
        print(f"Error: Archivo {archivo} no es un WAV válido.")
    except Exception as e:
        print(f"Error al procesar {archivo}: {e}")

```
Inicializa potencias = {} para almacenar la potencia de cada señal.
Itera sobre cada archivo en archivosy:
Se carga el archivo WAV con wavfile.read(), obteniendo:
sample_rate: la frecuencia de muestreo en Hz.
audio_data:los datos de la señal.
(se toma solo el primer canal audio_data[:, 0]).
Convierte la señal a flotante ( np.float32) para cálculos precisos.

<img width="302" alt="image" src="https://github.com/user-attachments/assets/a2eb43b4-3fdc-42ed-9535-07d5298779c7" />


Manejo de errores :

Si el archivo no existe, muestra Error: No se encontró el archivo.
Si el archivo no es válido, muestra Error: Archivo no es un WAV válido.

- Definir la potencia del ruido ambiente:
```  
potencia_ruido = potencias.get("ambiente.wav", None)

```
Se extrae la potencia del archivo ambiente.wav(considerado como ruido) para usarlo en el cálculo del SNR .

- Cálculo del SNR y generación de gráficos:
  
```
for archivo in archivos:
    try:
        sample_rate, audio_data = wavfile.read(f"{ruta_carpeta}\\{archivo}")

        if len(audio_data.shape) > 1:
            audio_data = audio_data[:, 0]

        audio_data = audio_data.astype(np.float32)

        potencia_senal = potencias.get(archivo, None)

        if potencia_ruido is not None and potencia_ruido > 0:
            if archivo == "ambiente.wav":
                snr_db = 0  
            else:
                snr_db = 10 * np.log10(potencia_senal / potencia_ruido) if potencia_senal > potencia_ruido else float('-inf')
        else:
            snr_db = float('-inf')

        print(f"SNR de {archivo}: {snr_db:.2f} dB")

```
Explicación del cálculo de SNR (Relación señal-ruido)
El SNR se calcula con la fórmula:

<img width="212" alt="image" src="https://github.com/user-attachments/assets/c2078987-e550-40b7-a2d7-2dc8785f6bce" />


Si archivo == "ambiente.wav", el SNR es 0 dB porque es la referencia de ruido.
Si la potencia de la señal es menor que la del ruido, se devuelve -inf(SNR indefinido).

- Normalización de la señal y graficado:
  
```
audio_data_norm = audio_data / np.max(np.abs(audio_data))  # Normalizar
        tiempo = np.arange(len(audio_data_norm)) / sample_rate  # Eje de tiempo

        plt.figure(figsize=(12, 5))

        # === Gráfica en el dominio del tiempo ===
        plt.subplot(1, 2, 1)
        plt.plot(tiempo, audio_data_norm, color=colores_tiempo[archivo], alpha=0.7)
        plt.xlabel("Tiempo (s)")
        plt.ylabel("Amplitud")
        plt.title(f"Señal Temporal - {archivo}")
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.xlim(0, tiempo[-1])
```
Normalización : Se divide la señal por su valor máximo para escalar entre -1y 1.
Eje de tiempo : Se genera con np.arange(len(audio_data_norm)) / sample_rate.
Se grafica la señal en el dominio del tiempo .

- Transformada de Fourier y gráfica en el dominio de la frecuencia:
- 
```
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
```
Se aplica la Transformada Rápida de Fourier (FFT) con np.fft.fft().
Se extrae la mitad del espectro ( [:N//2]porque la FFT es simétrica).
Se grafica el espectro en el dominio de la frecuencia en escala logarítmica.

- Mostrar gráficos:
  
```
plt.tight_layout()
        plt.show()
plt.tight_layout()

```
Se cargarán los archivos de audio WAV.
Se calcula la potencia de cada señal.
Se calcula el SNR con referencia al ruido.
Se normalizan las señales.
Se grafican en el dominio del tiempo y frecuencia.
El código permite comparar señales de audio en términos de energía y ruido con una visualización efectiva.

- *SNR Nicole = 29.51 dB*
Este es un *SNR alto*, lo que indica que la señal está limpia y tiene poco ruido de fondo.
- *SNR Gimena = 29.84 dB*  
Muy similar a "Nicole.wav", lo que indica una señal limpia y bien separada del ruido de fondo.
- *SNR Majo = 24.36 dB*  
Este es un SNR más bajo que las señales anteriores, lo que indica que tiene *más ruido de fondo*

![image](https://github.com/user-attachments/assets/83f88512-a863-4f19-bb4d-8674d1682d1f)

**Nicole.wav** es una señal de voz con una buena relación señal-ruido y clara diferenciación en el espectro de frecuencias. Es adecuada para análisis de voz o procesamiento de señales de audio.

Presenta picos pronunciados en el rango *100 Hz - 1000 Hz*, característico de la voz humana.
La mayor parte de la energía se concentra en el rango de *bajas frecuencias (<1000 Hz)*, lo que es normal en señales de voz.

![image](https://github.com/user-attachments/assets/0b98f840-40dd-438f-9af5-9c207450bcdd)

**Gimena.wav** es otra señal de voz con *buena calidad* y *alta relación señal-ruido*. Su espectro de frecuencia muestra una mayor riqueza de armónicos, lo que podría interpretarse como una voz con más variaciones tonales.

![image](https://github.com/user-attachments/assets/93717c60-2ae3-4abe-a75e-2e6e29cfd551)

**Majo.wav** también es una señal de voz, pero con *más ruido ambiental* que las anteriores. Si se desea mejorar la calidad, se podría aplicar un filtro de reducción de ruido.

![image](https://github.com/user-attachments/assets/3afabb3e-4ced-49c7-b67c-77cdc3b1c904)

"Ambiente.wav" es una señal de ruido de fondo utilizada para calcular el SNR de las otras señales. Su espectro amplio indica que contiene ruido de diversas frecuencias sin un patrón definido.
**SNR = 0.00 dB**  
Como se esperaba, este es el *ruido de referencia* y por eso su SNR es 0 dB.

- Definición de una función de filtrado pasa banda:
  
```
def butter_bandpass_filter(data, lowcut, highcut, fs, order=1):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return lfilter(b, a, data)
```
Esta función implementa un filtro pasa banda usando el filtro de Butterworth :

Se define un orden bajo (1) para evitar distorsiones en la señal.
Se establecieron los límites de frecuencia (lowcut, highcut) en proporción a la frecuencia de Nyquist ( fs/2).
Se usa la función butter()para calcular los coeficientes del filtro.
Se aplica el filtro con lfilter()
Elimina frecuencias fuera del rango especificado, permitiendo solo las frecuencias entre lowcuty highcut.

- Carga del ruido ambiente:
  
```
archivo_ruido = os.path.join(ruta_carpeta, "ambiente.wav")
potencia_ruido = None

if os.path.exists(archivo_ruido):
    sample_rate_ruido, audio_ruido = wavfile.read(archivo_ruido)
    if len(audio_ruido.shape) > 1:
        audio_ruido = audio_ruido[:, 0]
    audio_ruido = audio_ruido.astype(np.float32)
    potencia_ruido = np.mean(audio_ruido ** 2)

```
Se verifica si existe el archivo ambiente.wav(ruido de fondo).
Se carga el archivo de ruido y se convierte a mono (si tiene más de un canal).
Se convierte a float32 para evitar errores de precisión en los cálculos.
Se calcula la potencia del ruido usando la ecuacion

- Aplicación del Análisis de Componentes Independientes (ICA):

```
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

```
Se cargan las señales de archivos_ica.
Se convierte en mono y se normaliza.
Se almacenan en audio_signalspara aplicar ICA.

- Separación de señales con ICA:

```
if len(audio_signals) > 0:
    min_length = min(map(len, audio_signals))
    audio_signals = [signal[:min_length] for signal in audio_signals]

    X = np.vstack(audio_signals).T
    ica = FastICA(n_components=len(archivos_ica), max_iter=2000)
    S_ica = ica.fit_transform(X)

```
Se recortan todas las señales al mismo tamaño ( min_length).
Se utiliza FastICA para separar las señales mezcladas en sus componentes independientes.

- Filtrado de las señales separadas:
  
```
S_ica_filtered = np.array([butter_bandpass_filter(S_ica[:, i], 150, 4000, sample_rates[0]) for i in range(len(archivos_ica))]).T

```
Se aplica el filtro pasa banda (150-4000 Hz) para eliminar frecuencias fuera del rango de voz.

- Selección de la señal predominante:

```
energia = [np.sum(np.square(S_ica_filtered[:, i])) for i in range(len(archivos_ica))]
idx_voz = np.argmax(energia)
voz_filtrada = S_ica_filtered[:, idx_voz]

```
Se selecciona la señal con mayor energía.

- Guardado y graficado de la voz filtrada:

```
voz_wav = (voz_filtrada * 32767).astype(np.int16)
wavfile.write(os.path.join(ruta_carpeta, "voz_sin_ruido.wav"), sample_rates[0], voz_wav)

```
Se guarda la señal de voz sin ruido como un nuevo archivo WAV.

- **Señal 1 - "Voz Separada 1**

![image](https://github.com/user-attachments/assets/6997b2d9-a522-466e-86b5-bee6a1429ade)

Se observan pausas y momentos de menor actividad, lo que es característico de una conversación con silencios naturales.
La señal es relativamente fuerte y mantiene una estructura con picos de amplitud bien definidos.
La amplitud parece más grande que en la *voz filtrada, lo que sugiere que aún tiene componentes adicionales (posiblemente ruido de fondo)

- **Señal 2 - "Voz Separada 2**

![image](https://github.com/user-attachments/assets/02923b6c-bd38-4769-8486-cc67db12f1ce)

La forma de la onda es muy similar a la primera señal, pero se observa *una reducción de ruido* y mayor claridad en la estructura de la señal.
La amplitud ha sido normalizada, manteniendo valores en un rango más estable.
Se observa un patrón de voz más claro, lo que indica que **esta es la señal predominante tras la separación con ICA** y el filtrado.
Esta es la *señal final filtrada*, en la que se ha eliminado la mayor cantidad de ruido.
El filtrado pasa banda (150-4000 Hz) ha permitido *conservar las frecuencias de la voz humana* mientras elimina otros componentes no deseados.
Esta señal es la que se ha guardado en *"voz_sin_ruido.wav"* como el resultado óptimo

- **Señal 3 - "Voz Separada 3**

![image](https://github.com/user-attachments/assets/264252f7-b309-4ac9-b740-66c4da8d914e)

Es otra de las señales separadas por ICA.
Puede contener *una mezcla de voz y ruido residual* que no fue clasificado como la señal predominante.
Se parece mucho a "Voz Separada 1", lo que indica que ambas contienen información de voz con distintos niveles de interferencia.

- **SNR de la señal predominante: 14.26 dB**
La señal final tiene un SNR menor que las señales originales , lo que sugiere que ICA ha separado la voz principal, pero también ha reducido su energía .
ICA es menor, puede haber captado algo de ruido residual.

- Separación de señales con Beamforming



## Conclusión.

El procesamiento de señales aplicado en el experimento permitió mejorar significativamente la relación señal-ruido (SNR). Inicialmente, el ambiente presentó un SNR de 0 dB, lo que indica que el ruido predominaba completamente sobre la señal. Luego del procesamiento, se observaron mejoras, pues se alcanzaron valores de 29.51 dB para Nicole, 29.84 dB para Gimena y 24.36 dB para Majo. Sin embargo, en la etapa final del procesamiento, la SNR se redujo a 14.26 dB en los tres casos, esto demuestra que, si bien se logró una mejora en la extracción de la señal, aún persisten niveles considerables de ruido. Estos resultados destacan la efectividad de las técnicas empleadas, pero también indican la necesidad de optimizar los algoritmos para mejorar aún más la separación de señales y minimizar la pérdida de calidad en la señal recuperada, reconociendo una posible mayor efectividad para una proxima ejecución de este laboratorio en aumentar la distancia de la ubicación de los micrófonos ya que si los micrófonos están demasiado cerca de una fuente, captarán principalmente su sonido y tendrán dificultades para registrar las demás señales con claridad, lo que puede sesgar el procesamiento. Por el contrario, si los micrófonos están muy alejados o mal distribuidos, pueden captar un exceso de ruido ambiental y reflejos, dificultando la identificación precisa de cada fuente sonora.


## Referencias.
- F. Sáenz, C. Romero, y P. Bernal, «Análisis de señales acústicas para dispositivos de personas con discapacidad, aplicando teoría de procesamiento de radar», 3 de junio de 2016. https://sedici.unlp.edu.ar/handle/10915/53175
- O. C. L. Germán, «Análisis de la disminución del ruido en el estándar de audio DAB», 1 de febrero de 2021. https://dspace.ups.edu.ec/handle/123456789/19746
- A. Estrella-T, D. Nicolalde-R, y C. Escobar-T, «Estimación de distancia de detección de cantos de rana en grabaciones automáticas de ecoacústica», Revistapuce, abr. 2018, doi: 10.26807/revpuce.v0i106.134.
- C. L. Camila, «Comparación de métodos para reducir el ruido en señales emitidas por delfines Tursiops truncatus.», Repositorio de la Universidad Tecnológica de Pereira, 2015. https://repositorio.utp.edu.co/entities/publication/753d0a17-ccf2-435c-9b18-48573bb82435
- G. Shankar, «Blind Source Separation using ICA - A Practical Guide to Separate Audio Signals», Gowri Shankar, 24 de julio de 2021. https://gowrishankar-info.translate.goog/blog/blind-source-separation-using-ica-a-practical-guide-to-separate-audio-signals/?_x_tr_sl=en&_x_tr_tl=es&_x_tr_hl=es&_x_tr_pto=tc
