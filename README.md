## Adquisición de la señal

[![Figure-2024-10-30-225518.png](https://i.postimg.cc/sXgy03J2/Figure-2024-10-30-225518.png)](https://postimg.cc/wtZS18ZK)

Se toma la captura de la señal ECG por medio de amplificador AD8232 Y un Arduino Mega 2560, se utiliza una frecuencia de muestreo de 9600Hz.
Teniendo en cuenta la frecuencia de muestreo se obtienen los siguientes datos estadísticos 

Media: 0.009821821821821841

Desviación estándar: 19.613604891115983

Coeficiente de variación: 1996.941631290749

Frecuencia media: 26.89720453709372 Hz

Niveles de cuantificación: 1024 

La señal fue capturada y exportada como archivo .mat a Python para su posterior procesamiento 

          data = loadmat('ecg.mat')
          val = data['val'].squeeze()
          # Tiempo de la señal
          Fs = 9600
          Ts = 1 / Fs
          N = len(val)
          t = np.arange(N) * Ts  # Vector de tiempo
          
          # Características principales
          media_ecg = np.mean(val)
          print('Media:', media_ecg)
          Std_ecg = np.std(val)
          print('Desviación estándar:', Std_ecg)
          coeficiente_variacion = Std_ecg / media_ecg
          print('Coeficiente de variación:', coeficiente_variacion)
          
          # Transformada de Fourier para obtener el espectro de frecuencias
          frequencies = np.fft.fftfreq(N, Ts)
          spectrum = np.fft.fft(val)
          
          # Magnitud del espectro (sólo parte positiva)
          magnitudes = np.abs(spectrum[:N // 2])
          frequencies = frequencies[:N // 2]
          
          # Calcular la frecuencia media (promedio ponderado)
          frequency_mean = np.sum(frequencies * magnitudes) / np.sum(magnitudes)
          print("Frecuencia media:", frequency_mean, "Hz")

## Preprocesamiento
Para procesar la señal se utilizaron dos filtros de tipo de respuesta Butterworth, un pasa banda de 0.01Hz a 100Hz y un rechaza banda de 59Hz a 61Hz 
Filtro pasa banda 
Se utiliza un filtro de tercer orden para ello se utiliza una normalización de las frecuencias de corte, dividiendo por las frecuencias de Nyquist 
Se utilizo la función Butter de pyhton para obtener el tipo de respuesta mas conveniente para esta señal.

Filtro rechaza banda 

Al igual que con el filtro pasa banda se realizó la respectiva normalización para aplicar la función Butter con los parámetros de las frecuencias de corte y el tipo de filtro que queríamos. 

[![Figure-2024-10-30-232231.png](https://i.postimg.cc/4d2GDj8Q/Figure-2024-10-30-232231.png)](https://postimg.cc/wyNnJ4Y1)

Captura de los primeros instantes de la señal para poder observar después de aplicar los filtros 

          # Filtro rechazabanda: para eliminar el ruido en el rango 59-61 Hz
          lowcut_rej = 59  # Frecuencia de corte baja
          highcut_rej = 61  # Frecuencia de corte alta
          order_rej = 5   # Orden del filtro rechazabanda
          
          # Crear el filtro Butterworth rechazabanda
          nyquist = 0.5 * Fs  # Frecuencia de Nyquist
          low_rej = lowcut_rej / nyquist
          high_rej = highcut_rej / nyquist
          
          # Diseñar y aplicar el filtro rechazabanda
          b_rej, a_rej = butter(order_rej, [low_rej, high_rej], btype='bandstop')
          val_rej_filtered = filtfilt(b_rej, a_rej, val)
          
          # Filtro pasabanda: para pasar solo frecuencias entre 0.01 Hz y 100 Hz
          lowcut_pass = 0.01  # Frecuencia de corte baja del pasabanda
          highcut_pass = 100  # Frecuencia de corte alta del pasabanda
          order_pass = 3      # Orden del filtro pasabanda
          
          # Normalizar las frecuencias de corte para el filtro pasabanda
          low_pass = lowcut_pass / nyquist
          high_pass = highcut_pass / nyquist
          
          # Diseñar y aplicar el filtro pasabanda
          b_pass, a_pass = butter(order_pass, [low_pass, high_pass], btype='bandpass')
          val_bandpass_filtered = filtfilt(b_pass, a_pass, val_rej_filtered)




1. Espectrograma usando la Transformada Wavelet Continua (CWT)
En este análisis, hemos utilizado la Transformada Wavelet Continua (CWT) para visualizar cómo cambian las frecuencias en la señal de HRV a lo largo del tiempo. La wavelet Morlet ha sido seleccionada para realizar la CWT. Esta wavelet es comúnmente usada para el análisis de señales biológicas, como el ECG, porque ofrece una buena resolución en tiempo y frecuencia, permitiendo observar variaciones de frecuencia de corta duración con precisión.

La wavelet Morlet es adecuada para este tipo de análisis porque:

Combina una función seno y una envolvente Gaussiana, lo que le da una buena capacidad para detectar cambios transitorios en las señales.
Es ideal para capturar las frecuencias de interés en la HRV, especialmente en el rango de frecuencias bajas y altas que son relevantes para el análisis de la variabilidad de la frecuencia cardíaca (HRV).
Proporciona una representación suave y continua en el tiempo, lo que facilita la visualización de las transiciones en la potencia espectral.

2. Análisis en la Banda de Baja Frecuencia (LF) y Alta Frecuencia (HF)
Para el análisis, hemos separado la señal de HRV en las bandas de baja frecuencia (LF) y alta frecuencia (HF):

Banda de Baja Frecuencia (LF): Rango de 0.04 a 0.15 Hz. Esta banda refleja tanto la actividad del sistema nervioso simpático como la parasimpática. Un aumento en la potencia en esta banda suele estar relacionado con la regulación del sistema autónomo en respuesta a factores como el estrés o el esfuerzo físico.

Banda de Alta Frecuencia (HF): Rango de 0.15 a 0.4 Hz. Esta banda está asociada principalmente con la actividad del sistema nervioso parasimpático y con la frecuencia respiratoria. Variaciones en esta banda suelen reflejar la modulación de la HRV por la respiración y el tono vagal.

Para cada banda, hemos calculado la potencia espectral a lo largo del tiempo para observar cómo varía en ambas.

3. Descripción Crítica de las Variaciones en las Frecuencias y Cambios en la Potencia Espectral
Espectrograma de HRV
El espectrograma de HRV obtenido con la CWT muestra cómo cambian las frecuencias a lo largo del tiempo. Las zonas de colores más intensos (rojo/amarillo) indican puntos de mayor amplitud y, por lo tanto, mayor potencia en ciertas frecuencias.

Observaciones generales del espectrograma:

Las frecuencias en el rango de HF (0.15-0.4 Hz) muestran variaciones a lo largo del tiempo, que pueden estar asociadas con cambios en la respiración.
Las frecuencias en el rango LF (0.04-0.15 Hz) tienen zonas de mayor amplitud en ciertos periodos, lo cual puede reflejar un aumento en la actividad del sistema nervioso autónomo en respuesta a factores externos.
Potencia Espectral en LF y HF
Al observar la potencia espectral en las bandas LF y HF:

Potencia en la banda LF:

Un aumento en la potencia LF podría indicar una respuesta del sistema nervioso simpático, especialmente si ocurre en períodos de estrés o actividad física.
La potencia LF suele ser más estable y de baja variabilidad a lo largo del tiempo en individuos en reposo.
Potencia en la banda HF:

Cambios en la potencia HF están comúnmente relacionados con el ciclo respiratorio y la actividad parasimpática.
Si la potencia en HF es alta, se interpreta como un mayor dominio del sistema parasimpático, lo cual es indicativo de relajación o descanso.
Comparación de la Potencia entre LF y HF:

Un predominio de la potencia en LF sobre HF sugiere un dominio simpático, mientras que un predominio de HF sugiere un dominio parasimpático.
La variabilidad entre LF y HF puede reflejar cómo el cuerpo responde a factores de estrés o condiciones de relajación en diferentes momentos.
Conclusión del Análisis
Este análisis proporciona una visión detallada del balance entre las bandas de baja y alta frecuencia en la HRV:

Cambios en LF y HF pueden reflejar adaptaciones del sistema autónomo en respuesta a cambios fisiológicos y ambientales.
La Transformada Wavelet Continua (CWT) con la wavelet Morlet es una herramienta poderosa para el análisis de HRV, ya que permite visualizar cómo varían las frecuencias en tiempo real y facilita la observación de patrones complejos en la potencia espectral.
Este enfoque ayuda a entender la dinámica del sistema nervioso autónomo a lo largo del tiempo, permitiendo identificar momentos de alta o baja variabilidad de la frecuencia cardíaca y su relación con la actividad simpática y parasimpática.

