# -*- coding: utf-8 -*-

import wget
import os
import scipy.io.wavfile as wavfile
from .utils import downloader
from .vc_infer_pipeline import VC
from .myutils import Audio
from .infer_pack.models import (
    SynthesizerTrnMs256NSFsid,
    SynthesizerTrnMs256NSFsid_nono,
    SynthesizerTrnMs768NSFsid,
    SynthesizerTrnMs768NSFsid_nono,
)
from fairseq import checkpoint_utils
from .config import Config
import torch
import numpy as np
import traceback
import os
import warnings
import logging
import shutil
import sys

config = Config()
warnings.filterwarnings("ignore")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s: %(levelname)s [%(filename)s:%(lineno)s] %(message)s",
    datefmt="%m-%d-%Y %H:%M%p",
    handlers=[
        logging.StreamHandler()
    ]
)


class Inference:
    
    inference_cont = 0
    hubert_model = None
    weight_path = "weights"
    output_audios = "audio-outputs"
    zips_path = "zips"
    unzips_path = "unzips"
        
    def __init__(
        self,
        source_audio_path=None,
        output_file_name=None,
        feature_index_path="",
        speaker_id=0,
        transposition=-2,
        f0_method="harvest",
        crepe_hop_length=160,
        harvest_median_filter=3,
        resample=0,
        mix=1,
        feature_ratio=0.78,
        protection_amnt=0.33,
        protect1=False,
        model_dir=None,
        auto_remove=False
    ):
        Inference.inference_cont += 1
        self._source_audio_path = source_audio_path
        self._output_file_name = output_file_name
        self._feature_index_path = feature_index_path
        self._speaker_id = speaker_id
        self._transposition = transposition
        self._f0_method = f0_method
        self._crepe_hop_length = crepe_hop_length
        self._harvest_median_filter = harvest_median_filter
        self._resample = resample
        self._mix = mix
        self._feature_ratio = feature_ratio
        self._protection_amnt = protection_amnt
        self._protect1 = protect1
        self._id = Inference.inference_cont
        self.now_dir = os.getcwd()
        self.sid = 0
        self._model_dir = model_dir
        self._auto_remove = auto_remove
        
        if not self._output_file_name:
            self._output_file_name = os.path.join(Inference.output_audios, os.path.basename(source_audio_path))
        
        os.makedirs(os.path.join(self.now_dir, Inference.output_audios), exist_ok=True)
        os.makedirs(os.path.join(self.now_dir, Inference.weight_path), exist_ok=True)
        
        torch.manual_seed(114514)
        
        if not os.path.exists("./hubert_base.pt"):
            logging.debug("Downloading hubert base...")
            wget.download(
                "https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/hubert_base.pt", out="./hubert_base.pt")
        if not os.path.exists("./rmvpe.pt"):
            logging.debug("Downloading rmvpe model...")
            wget.download(
                "https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/rmvpe.pt", out="./rmvpe.pt"
            )
    
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id
    
    @property
    def audio(self):
        return self._audio

    @audio.setter
    def audio_file(self, audio):
        self._audio_file = audio

    @property
    def source_audio_path(self):
        return self._source_audio_path

    @source_audio_path.setter
    def source_audio_path(self, source_audio_path):
        if not self._output_file_name:
            self._output_file_name = os.path.join(Inference.output_audios, os.path.basename(source_audio_path))
        self._source_audio_path = source_audio_path

    @property
    def output_file_name(self):
        return self._output_file_name

    @output_file_name.setter
    def output_file_name(self, output_file_name):
        self._output_file_name = output_file_name

    @property
    def feature_index_path(self):
        return self._feature_index_path

    @feature_index_path.setter
    def feature_index_path(self, feature_index_path):
        self._feature_index_path = feature_index_path

    @property
    def speaker_id(self):
        return self._speaker_id

    @speaker_id.setter
    def speaker_id(self, speaker_id):
        self._speaker_id = speaker_id

    @property
    def transposition(self):
        return self._transposition

    @transposition.setter
    def transposition(self, transposition):
        self._transposition = transposition

    @property
    def f0_method(self):
        return self._f0_method

    @f0_method.setter
    def f0_method(self, f0_method):
        self._f0_method = f0_method

    @property
    def crepe_hop_length(self):
        return self._crepe_hop_length

    @crepe_hop_length.setter
    def crepe_hop_length(self, crepe_hop_length):
        self._crepe_hop_length = crepe_hop_length

    @property
    def harvest_median_filter(self):
        return self._harvest_median_filter

    @crepe_hop_length.setter
    def harvest_median_filter(self, harvest_median_filter):
        self._harvest_median_filter = harvest_median_filter

    @property
    def resample(self):
        return self._resample

    @resample.setter
    def resample(self, resample):
        self._resample = resample

    @property
    def mix(self):
        return self._mix

    @mix.setter
    def mix(self, mix):
        self._mix = mix

    @property
    def feature_ratio(self):
        return self._feature_ratio

    @feature_ratio.setter
    def feature_ratio(self, feature_ratio):
        self._feature_ratio = feature_ratio

    @property
    def protection_amnt(self):
        return self._protection_amnt

    @protection_amnt.setter
    def protection_amnt(self, protection_amnt):
        self._protection_amnt = protection_amnt

    @property
    def protect1(self):
        return self._protect1

    @protect1.setter
    def protect1(self, protect1):
        self._protect1 = protect1
        
    @property
    def model_dir(self):
        return self._model_dir

    @model_dir.setter
    def model_dir(self, model_dir):
        self._model_dir = model_dir
    
    def infer_by_model_url(self, url):
        modelname = downloader.ModelDownloader(url, Inference.zips_path, Inference.weight_path)
        self.model_dir = os.path.join(self.now_dir, Inference.weight_path, modelname)
        
        return self._run()
            
    def infer_by_model_path(self):
        if not self.model_dir:
            raise Exception("Model path not specified")
        
        return self._run()
            
    def _delete_files(self):
        if os.path.exists(self.model_dir):
            shutil.rmtree(self.model_dir)
    
    def _get_model(self):
        resources = {}
        for root, dirs, files in os.walk(self._model_dir):
            for file in files:
                if file.endswith('.index'):
                    resources['index'] =  os.path.join(root, file)
                if file.endswith('.pth'):
                    resources['pth'] =  os.path.join(root, file)
        return resources

    def _run(self):
        try:
            model_info = self._get_model()
            self.feature_index_path = model_info.get('index', '')
            self._model_path = model_info.get('pth', None)
            
            if not os.path.exists(self.source_audio_path):
                raise Exception(f"The input file '%s' does not exist" % self.source_audio_path)
            
            if self._model_path is None or not os.path.exists(self._model_path):
                raise Exception(f"The specified model directory does not exists or has not a .pth file...")
            
            self.vc = self._get_vc()
            if self.vc is None:
                raise Exception("Model not found or not initialized...")
            audio = self._vc_single()
            wavfile.write(
                os.path.join(Inference.output_audios, os.path.basename(self.output_file_name)),
                self.tgt_sr,
                audio
            )
            logging.debug("Conversion complete.")
            
            if self._auto_remove:
                self._delete_files()
            
            return os.path.join(Inference.output_audios, os.path.basename(self.output_file_name))
        
        except Exception as err:
            logging.exception(err)
            return None
    
    def _load_hubert(self):
        # Determinar si existe una tarjeta N que pueda usarse para entrenar y acelerar la inferencia.
        models, _, _ = checkpoint_utils.load_model_ensemble_and_task(
            ["hubert_base.pt"],
            suffix="",
        )
        self.hubert_model = models[0]
        self.hubert_model = self.hubert_model.to(config.device)
        if config.is_half:
            self.hubert_model = self.hubert_model.half()
        else:
            self.hubert_model = self.hubert_model.float()
        self.hubert_model.eval()

    def _vc_single(self):
        if self.source_audio_path is None:
            raise Exception("You need to upload an audio")
        f0_up_key = int(self.transposition)
        try:
            audio = Audio.load_audio(self.source_audio_path, 16000)

            audio_max = np.abs(audio).max() / 0.95
            if audio_max > 1:
                audio /= audio_max
            times = [0, 0, 0]
            if not self.hubert_model:
                self._load_hubert()
            if_f0 = self.cpt.get("f0", 1)
            file_index = (
                    self.feature_index_path.strip(" ")
                    .strip('"')
                    .strip("\n")
                    .strip('"')
                    .strip(" ")
                    .replace("trained", "added")
            )

            audio_opt = self.vc.pipeline(
                self.hubert_model,
                self.net_g,
                self.sid,
                audio,
                self.source_audio_path,
                times,
                f0_up_key,
                self.f0_method,
                file_index,
                self.feature_ratio,
                if_f0,
                self.harvest_median_filter,
                self.tgt_sr,
                self.resample,
                self.mix,
                self.version,
                self.protection_amnt,
                self.crepe_hop_length
            )
            if self.tgt_sr != self.resample >= 16000:
                self.tgt_sr = self.resample
            index_info = (
                "Using index:%s." % file_index
                if os.path.exists(file_index)
                else "Index not used."
            )
            print(index_info)
            return audio_opt
        except:
            info = traceback.format_exc()
            raise Exception("Conversion failed: %s" % info)

    def _get_vc(self):
        # Comprobar si se pasó uno o varios modelos
        if self._model_path == "" or self._model_path == []:
            if self.hubert_model is not None:  # 考虑到轮询, 需要加个判断看是否 sid 是由有模型切换到无模型的
                logging.debug("Cleaning caché...")
                del self.net_g, self.vc, self.hubert_model, self.tgt_sr  # ,cpt

                # Si hay una GPU disponible, libera la memoria de la GPU
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()

                # Bloque de abajo no limpia completamente
                if_f0 = self.cpt.get("f0", 1)
                self.version = self.cpt.get("version", "v1")
                if self.version == "v1":
                    if if_f0 == 1:
                        self.net_g = SynthesizerTrnMs256NSFsid(
                            *self.cpt["config"], is_half=config.is_half
                        )
                    else:
                        self.net_g = SynthesizerTrnMs256NSFsid_nono(*self.cpt["config"])
                elif self.version == "v2":
                    if if_f0 == 1:
                        self.net_g = SynthesizerTrnMs768NSFsid(
                            *self.cpt["config"], is_half=config.is_half
                        )
                else:
                    self.net_g = SynthesizerTrnMs768NSFsid_nono(*self.cpt["config"])

                del self.net_g, self.cpt
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                self.cpt = None
            return None
        
        logging.debug("Loading %s" % self._model_path)
        self.cpt = torch.load(self._model_path, map_location="cpu")
        self.tgt_sr = self.cpt["config"][-1]
        self.cpt["config"][-3] = self.cpt["weight"]["emb_g.weight"].shape[0]
        if_f0 = self.cpt.get("f0", 1)
        self.version = self.cpt.get("version", "v1")

        if self.version == "v1":
            if if_f0 == 1:
                self.net_g = SynthesizerTrnMs256NSFsid(
                    *self.cpt["config"], is_half=config.is_half)
            else:
                self.net_g = SynthesizerTrnMs256NSFsid_nono(*self.cpt["config"])
        elif self.version == "v2":
            if if_f0 == 1:
                self.net_g = SynthesizerTrnMs768NSFsid(
                    *self.cpt["config"], is_half=config.is_half)
        else:
            self.net_g = SynthesizerTrnMs768NSFsid_nono(*self.cpt["config"])
        del self.net_g.enc_q

        print(self.net_g.load_state_dict(self.cpt["weight"], strict=False))
        self.net_g.eval().to(config.device)
        if config.is_half:
            self.net_g = self.net_g.half()
        else:
            self.net_g = self.net_g.float()
        return VC(self.tgt_sr, config)
    
if __name__ == "__main__":
    #infer = Inference(source_audio_path="C:/Users/admin/Downloads/Michael Jackson - Billie Jean Vocals Only 30 seg.wav")
    # infer.infer_by_model_url("https://huggingface.co/juuxn/RVCModels/resolve/main/Spreen_(RVC_-_1000_Epochs).zip")
    
    infer = Inference(
        source_audio_path="C:/Users/admin/Downloads/Michael Jackson - Billie Jean Vocals Only 30 seg.wav",
        model_dir='weights/5928e255-af72-42d8-bfc3-4a63f5251dc6',
        auto_remove=False
    )
    infer.infer_by_model_path()
    