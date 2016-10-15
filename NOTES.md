# Audio Notes

Nyquist Frequency

  - Half the Sample Rate.
  
  - The maximum frequency that can be encoded for a given Sample Rate.


Pulse-code Modulation (PCM)

  - Standard form for representing digital audio.

  - Linear Pulse-code Modulation (LPCM) 

  

Analog Vs. Digital signals

  - Analog signals are physical measurements of some continous, time varying feature.

  - Voltage, current, and frequency are common physical attributes.


Sample (explanation)

  - Sound can represented digitally as a list of numbers (values).

  - Each value being one point of amplitude in a waveform.

  - One sample is one value.

  - However, 'Sample' is used to refer to either an individual value, or a list of values.


Sample Rate

  - Samples per second (Hz), how 'quickly' a sound is interpretted.

  - Sample Rate relates to the maximum frequency possible.

  - Common Sample Rates: 44100 Hz, 48 kHz, 88.2 kHz, 96 kHz, 192 kHz

  - Some devices only support certain sample rates.

  - The range of human hearing is 20kHz which explains 44.1kHz which as a maximum frequency of 22.05kHz (see Nyquest Frequency).


Bit Depth

  - Bits per value (sample).

  - Bit Depth is ultimately the resolution of the sound, the more bits the more possible values of a sample.

  - Greater Bit Depth means greater range of amplitude.

  - synonyms: word size, resolution, sample size, format, sample format.


Bit Rate

  - Number of bits transmitted per seconds.

  - Often used to describe bandwidth / throughput.

  - Can be calculated as (bitdepth * samplerate * channels).


Quantization

  - Transforming continous signals to discrete values.

  - Digital signals have discrete values while analog signals are continous.

  - There are theoretically infinite possible values for an analog signal.

  - Quantization error is the distortion resulting from analog to digital conversion.


Dithering
  
  - Random noise added to mask quantization error.


Channel

  - Seperate audio streams.


