1. Sistema Nervioso Autónomo (SNA)
El Sistema Nervioso Autónomo (SNA) es la parte del sistema nervioso que controla involuntariamente funciones corporales vitales, como el ritmo cardíaco, la respiración, la digestión y la presión arterial. Se divide en dos ramas principales:

Sistema Nervioso Simpático (SNS): Se activa en situaciones de estrés o actividad física, aumentando el ritmo cardíaco y preparando al cuerpo para una respuesta de “lucha o huida”.
Sistema Nervioso Parasimpático (SNP): Actúa para relajar el cuerpo y conservar energía, disminuyendo el ritmo cardíaco y promoviendo funciones de “descanso y digestión”.
El SNA regula el ritmo cardíaco mediante un equilibrio dinámico entre estas dos ramas. La actividad de estos sistemas puede evaluarse indirectamente a través de la Variabilidad de la Frecuencia Cardíaca (HRV).

2. Variabilidad de la Frecuencia Cardíaca (HRV)
La Variabilidad de la Frecuencia Cardíaca (HRV) es una medida que refleja las fluctuaciones en los intervalos de tiempo entre latidos cardíacos consecutivos (los intervalos R-R). Es un indicador importante de la salud del SNA y se utiliza para evaluar el equilibrio entre la actividad simpática y parasimpática.

HRV Alta: Se asocia con un SNA flexible y saludable, lo que indica una buena capacidad de adaptación a los cambios fisiológicos y ambientales. Una HRV alta es deseable y sugiere un tono parasimpático predominante.
HRV Baja: Puede ser un signo de estrés, fatiga o disfunción del SNA, y se ha asociado con un mayor riesgo de enfermedades cardiovasculares. Una HRV baja indica una menor capacidad de adaptación.
Parámetros Clave de la HRV en el Dominio del Tiempo:
Media de los Intervalos R-R: Indica el ritmo cardíaco promedio.
Desviación Estándar de los Intervalos R-R (SDNN): Mide la dispersión o variabilidad de los intervalos R-R. Una SDNN más alta refleja una mayor HRV.
Coeficiente de Variación (CV): Proporciona una medida de la variabilidad relativa en relación con la media.

3. Transformada Wavelet Continua (CWT)
La Transformada Wavelet Continua (CWT) es una herramienta matemática que descompone una señal en componentes de frecuencia y las representa a lo largo del tiempo. Es útil para analizar señales no estacionarias, como las de HRV, donde las frecuencias pueden cambiar dinámicamente.

Wavelet Morlet: Es una función seno modulada por una envolvente Gaussiana, utilizada frecuentemente para el análisis de señales biológicas debido a su buena resolución tanto en tiempo como en frecuencia. La wavelet Morlet permite detectar transiciones rápidas en las frecuencias de la señal, lo que es crucial para analizar cómo varía la HRV en diferentes momentos.
Aplicación de la CWT en el Análisis de HRV
La CWT se usa para obtener un espectrograma de la HRV, que muestra cómo la potencia de las frecuencias cambia con el tiempo. Esto es particularmente útil para analizar las bandas de frecuencia relevantes:

Banda de Baja Frecuencia (LF, 0.04-0.15 Hz): Relacionada con la actividad simpática y parasimpática.
Banda de Alta Frecuencia (HF, 0.15-0.4 Hz): Asociada principalmente con la actividad parasimpática y la respiración.
El análisis espectral de estas bandas permite evaluar el equilibrio autonómico y cómo el cuerpo responde a diferentes estímulos fisiológicos o ambientales.

Resumen Crítico
El SNA juega un papel crucial en la regulación del ritmo cardíaco y otras funciones vitales.
La HRV es un indicador de la salud y la capacidad de adaptación del SNA, con aplicaciones en la evaluación de estrés, bienestar y riesgo cardiovascular.
La Transformada Wavelet Continua (CWT) es una herramienta avanzada para analizar señales no estacionarias como la HRV, proporcionando información detallada sobre cómo varían las frecuencias en el tiempo y permitiendo el estudio de la dinámica del SNA.

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


![image](https://github.com/user-attachments/assets/21316124-b216-4e91-83cd-603724c3b821)


![image](https://github.com/user-attachments/assets/423beb3f-63bb-43e2-b3f6-912fbfc3395a)


Gráfica 1: Señal ECG Filtrada con Picos R Detectados
En esta gráfica, se muestra la señal de ECG filtrada con los picos R marcados. Los picos R son puntos de interés en la señal de ECG que representan las contracciones ventriculares, y los intervalos entre ellos (R-R) son fundamentales para el análisis de HRV.
Se observa que los picos R están correctamente identificados y distribuidos de manera variable a lo largo del tiempo, lo que ya sugiere la presencia de cierta variabilidad en los intervalos R-R.
Gráfica 2: Distribución de los Intervalos R-R
La segunda gráfica muestra un histograma de los intervalos R-R. El eje horizontal representa la duración de los intervalos R-R en segundos, y el eje vertical representa la frecuencia de cada intervalo.
La distribución parece tener una forma aproximadamente asimétrica hacia la derecha, con la mayoría de los intervalos R-R centrados alrededor de 0.7 segundos y una menor cantidad de intervalos extendiéndose hacia valores más altos.
Parámetros Estadísticos de la HRV
Media de los Intervalos R-R:

La media de los intervalos R-R es una medida del ritmo cardíaco promedio. En general, una media más alta indica un ritmo cardíaco más lento y una más baja indica un ritmo cardíaco más rápido.
La media observada de los intervalos R-R en el histograma parece estar alrededor de 0.7 segundos, lo que correspondería a un ritmo cardíaco promedio de aproximadamente 
60
0.7
≈
86
0.7
60
​
 ≈86 latidos por minuto.
Desviación Estándar de los Intervalos R-R (SDNN):

La desviación estándar de los intervalos R-R es un indicador común de la HRV. Una desviación estándar alta sugiere una mayor variabilidad en los intervalos R-R, lo cual es generalmente un signo de un sistema nervioso autónomo saludable y adaptable.
En la gráfica, se observa que hay una dispersión significativa en los intervalos, especialmente con algunos valores que se extienden por encima de 0.9 segundos. Esto indica cierta variabilidad, pero también podría haber presencia de valores atípicos.
Coeficiente de Variación de los Intervalos R-R:

El coeficiente de variación (CV) se calcula como la desviación estándar dividida por la media de los intervalos R-R, y proporciona una medida de la variabilidad relativa.
Un CV más alto indica una mayor variabilidad relativa, mientras que un CV bajo indica que los intervalos son más uniformes.
Análisis Crítico de la HRV
Variabilidad Observada:

La presencia de variabilidad en los intervalos R-R es una señal de una adecuada regulación autónoma del ritmo cardíaco. Sin embargo, si la variabilidad es excesivamente alta o baja, podría indicar problemas en el control autonómico del corazón.
En esta muestra, parece haber una variabilidad moderada con algunos intervalos R-R más largos (hacia 1.0-1.2 segundos), lo que podría estar relacionado con fluctuaciones en la actividad del sistema nervioso parasimpático.
Potenciales Valores Atípicos:

Algunos de los intervalos R-R en la distribución se extienden hacia 1.0-1.2 segundos. Estos intervalos más largos podrían ser valores atípicos, o podrían indicar eventos fisiológicos específicos, como cambios en el tono vagal o en la respiración.
Es importante analizar si estos intervalos extremos afectan significativamente las medidas de HRV y si representan algún evento anómalo.
Salud Cardiovascular y HRV:

Una HRV alta es generalmente indicativa de un sistema nervioso autónomo flexible y saludable, asociado con un buen equilibrio entre las actividades simpática y parasimpática.
Una HRV baja podría estar asociada con estrés, fatiga, o disfunción del sistema nervioso autónomo. La distribución observada aquí parece mostrar una HRV razonable, aunque sería importante compararla con valores de referencia para determinar si está dentro de un rango saludable.
Conclusión
Los parámetros básicos de la HRV, como la media y la desviación estándar de los intervalos R-R, son esenciales para evaluar la regulación autónoma del corazón. En este análisis:

La media de los intervalos R-R sugiere un ritmo cardíaco moderadamente rápido.
La desviación estándar indica una variabilidad notable, lo que es positivo desde el punto de vista de la salud cardiovascular.
Sin embargo, es crucial realizar un análisis más detallado y considerar la posible presencia de valores atípicos que puedan influir en las estadísticas generales.
Este análisis ayuda a comprender cómo el sistema nervioso autónomo está regulando el ritmo cardíaco y puede ser un indicador útil en la evaluación de la salud cardíaca general.


![image](https://github.com/user-attachments/assets/c25253e3-7ae5-4ca3-9f40-d3b6de4803af)



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

