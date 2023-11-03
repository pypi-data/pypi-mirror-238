import requests
import os
import ffmpeg
import numpy as np

class Audio:
    def __init__(self, name, url):
        self._name = name
        self._url = url

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url

    def __str__(self):
        return f'Audio: {self._name} {self._url}'

    @classmethod
    def load_audio(cls, file, sr):
        try:
            new_filename = file
            # Convertir a formato WAV si no lo está
            if not file.endswith(".wav"):
                new_filename = f"{file}.wav"
                if not os.path.isfile(new_filename):
                    (
                        ffmpeg.input(file)
                        .output(new_filename, format="wav")
                        .run(cmd=["ffmpeg", "-nostdin"], capture_stdout=True, capture_stderr=True)
                    )
            else:
                new_filename = file
                
            # Cargar el archivo formateado y devolverlo como NumPy array
            out, _ = (
                ffmpeg.input(new_filename)
                .output("-", format="f32le", acodec="pcm_f32le", ac=1, ar=sr)
                .run(cmd=["ffmpeg", "-nostdin"], capture_stdout=True, capture_stderr=True)
            )

            # Eliminar el archivo formateado
            if new_filename != file:
                os.remove(new_filename)    
        except Exception as e:
            raise RuntimeError(f"Failed to load audio: {e}")

        return np.frombuffer(out, np.float32).flatten()

    @classmethod
    def dowload_from_url(self, url = None, output = "./audios/file.wav"):
        """
        Descarga un aduio desde una url
        Args:
            path: Folder where the audio will be downloaded
        Returns:
            return: the path of the downloaded audio
        """
        request = requests.get(url, allow_redirects=True)
        open(output, 'wb').write(request.content)

        return output