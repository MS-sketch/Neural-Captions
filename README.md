# Neural-Captions
Neural Captions is a project intended for generating accurate AI Subtitles, with Proper Sync System, such that the subs match with the dialogue in the Audio Track. 
> **Note:** This project is currently in its Beta Version.

## Functioning
### Tools
- The Project uses [OpenAI Whisper](https://github.com/openai/whisper), [PyTorch](https://github.com/pytorch/pytorch) and [Faster Whisper](https://github.com/SYSTRAN/faster-whisper), as the basic Audio Transcribing Library.
- [librosa](https://github.com/librosa/librosa), [webrtcvad](https://github.com/wiseman/py-webrtcvad) and [Demucs](https://github.com/adefossez/demucs) for Audio Speech Detection & Analysis, used for Syncing Audio.
- [Numpy](https://github.com/numpy/numpy) and [Pandas](https://pandas.pydata.org/) for other required Processing.

  
### Logic
1. When the Video is selected by the user, the Audio Track Gets Extracted by [FFmpeg](https://www.ffmpeg.org/).
2. Then the audio of a voice is detected and the extracted.
3. The extraced Voice Audio is then Processed and Cut into timestamps based of whether there is a voice or not.
4. Then Based on the timestamps the Audio is transcribed and saved into a SRT file.

## System Requirements
Although this can run nearly on any system as it can be ran on CPU too, but due to the complexity involved. 
So it is highly recommended for it to run faster, please use a GPU 

> For Context on an Intel i3-7100U (Mobile Chip for Light Tasks), with 4GB RAM (DDR3) and No GPU, for it to process a 25 Minute Video, it took about 2.5 Hours.
<br><br>
> Optimized it to use all the Threads of the CPU and the Utilization was at 100% for the duration of the Test.

### Minimum Requirements:
- CPU: **Intel i3** 6th Generation or **AMD** Equivalent
- GPU: **Not Required**
- RAM: **4GB**

### Recommended Requirements:
- CPU: **Intel i5** 7th Generation or **AMD** Equivalent
- GPU: **RTX 2080Ti** or **AMD** Equivalent
- RAM: **8GB**

## To Be Added
- Better Optimisation and Faster Running On Older Hardware.
- Charecter Speech Detection
  > Enabling the User to type in the Name of Charecters & an Audio Sample, which can be used to detect who is saying what & implement in Captions
- Better Speech Detection
  > Specially In Music Video, using APIs to find the Lyrics & Syncing them with the Audio.


## Contact
Email: sarkar.mainakh@yandex.com
