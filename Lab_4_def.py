# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 21:49:32 2024

@author: Santiago
"""

from scipy.io import loadmat
from scipy.signal import butter, filtfilt, find_peaks, morlet
import numpy as np
import matplotlib.pyplot as plt

# Cargar el archivo .mat
data = loadmat('ecg.mat')

# Acceder al vector 'val' dentro del archivo
val = data['val'].squeeze()

# Amplitud de la señal
G = 9.99
val = val / G

# Tiempo de la señal
Fs = 1000
Ts = 1 / Fs
N = len(val)
t = np.arange(N) * Ts  # Vector de tiempo

# Características principales de la señal ECG
media_ecg = np.mean(val)
print('Media:', media_ecg)
Std_ecg = np.std(val)
print('Desviación estándar:', Std_ecg)
coeficiente_variacion = Std_ecg / media_ecg
print('Coeficiente de variación:', coeficiente_variacion)

# Transformada de Fourier para obtener el espectro de frecuencias
frequencies = np.fft.fftfreq(N, Ts)
spectrum = np.fft.fft(val)

# Magnitud del espectro (solo parte positiva)
magnitudes = np.abs(spectrum[:N // 2])
frequencies = frequencies[:N // 2]

# Calcular la frecuencia media
frequency_mean = np.sum(frequencies * magnitudes) / np.sum(magnitudes)
print("Frecuencia media:", frequency_mean, "Hz")

# Filtro rechazabanda: para eliminar el ruido en el rango 59-61 Hz
lowcut_rej = 59
highcut_rej = 61
order_rej = 5

nyquist = 0.5 * Fs
low_rej = lowcut_rej / nyquist
high_rej = highcut_rej / nyquist

b_rej, a_rej = butter(order_rej, [low_rej, high_rej], btype='bandstop')
val_rej_filtered = filtfilt(b_rej, a_rej, val)

# Filtro pasabanda: para pasar solo frecuencias entre 0.01 Hz y 100 Hz
lowcut_pass = 0.01
highcut_pass = 100
order_pass = 3

low_pass = lowcut_pass / nyquist
high_pass = highcut_pass / nyquist

b_pass, a_pass = butter(order_pass, [low_pass, high_pass], btype='bandpass')
val_bandpass_filtered = filtfilt(b_pass, a_pass, val_rej_filtered)

# Graficar ECG original y filtrado (primeros 1000 puntos)
plt.figure(figsize=(10, 5))
plt.plot(t[:1000], val[:1000], label='ECG Original')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud (μV)')
plt.title('Señal ECG Original')
plt.legend()
plt.show()

plt.figure(figsize=(10, 5))
plt.plot(t[:1000], val_bandpass_filtered[:1000], label='ECG Filtrado (Pasabanda + Rechazabanda)', color='green')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud (μV)')
plt.title('Señal ECG Filtrada')
plt.legend()
plt.show()

# Detección de picos R y cálculo de intervalos R-R
peaks, _ = find_peaks(val_bandpass_filtered, distance=0.6 * Fs)
RR_intervals = np.diff(peaks) / Fs
RR_times = t[peaks[1:]]

# Cálculo de HRV en el dominio del tiempo
mean_RR = np.mean(RR_intervals)
std_RR = np.std(RR_intervals)

print("Media de los intervalos R-R:", mean_RR, "s")
print("Desviación estándar de los intervalos R-R:", std_RR, "s")

# Graficar la señal ECG con picos R
plt.figure(figsize=(10, 5))
plt.plot(t[:1000], val_bandpass_filtered[:1000], label='ECG Filtrado')
plt.plot(t[peaks[:100]], val_bandpass_filtered[peaks[:100]], 'rx', label='Picos R')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud (μV)')
plt.title('Señal ECG Filtrada con Picos R Detectados')
plt.legend()
plt.show()

# Histograma de los intervalos R-R
plt.figure(figsize=(10, 5))
plt.hist(RR_intervals, bins=30, edgecolor='black')
plt.xlabel('Intervalo R-R (s)')
plt.ylabel('Frecuencia')
plt.title('Distribución de los Intervalos R-R')
plt.show()

# Espectrograma de HRV usando Transformada Wavelet Continua (CWT) con wavelet Morlet
hrv_signal = RR_intervals - np.mean(RR_intervals)
hrv_interpolated_time = np.linspace(RR_times[0], RR_times[-1], len(hrv_signal))
hrv_interpolated = np.interp(hrv_interpolated_time, RR_times, hrv_signal)

# Crear un conjunto de escalas para la transformada wavelet
scales = np.arange(20, 128)  # Ajuste para enfocarse en el rango 0.04 a 0.4 Hz

# Realizar la Transformada Wavelet Continua usando Morlet
cwt_matrix = np.zeros((len(scales), len(hrv_interpolated)))
for i, scale in enumerate(scales):
    wavelet = morlet(len(hrv_interpolated), w=5, s=scale)
    cwt_matrix[i, :] = np.abs(np.convolve(hrv_interpolated, wavelet, mode='same'))

# Graficar el espectrograma de la HRV usando CWT
plt.figure(figsize=(10, 6))
plt.imshow(cwt_matrix, extent=[hrv_interpolated_time[0], hrv_interpolated_time[-1], scales[-1], scales[0]],
           aspect='auto', cmap='jet')
plt.colorbar(label='Amplitud')
plt.ylabel('Escalas (relacionadas con frecuencia)')
plt.xlabel('Tiempo (s)')
plt.title('Espectrograma de la HRV usando Transformada Wavelet Continua (Morlet)')
plt.show()
