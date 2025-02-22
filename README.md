# Neural-Captions
Neural Captions is a project intended for generating accurate AI Subtitles, with Proper Sync System, such that the subs match with the dialogue in the Audio Track. 
> **Note:** This project is currently in its Beta Version.

## Functioning
### Tools
- The Project uses [OpenAI Whisper](https://github.com/openai/whisper), [PyTorch](https://github.com/pytorch/pytorch) and [Faster Whisper](https://github.com/SYSTRAN/faster-whisper), as the basic Audio Transcribing Library.
- [librosa](https://github.com/librosa/librosa), [webrtcvad](https://github.com/wiseman/py-webrtcvad) and [Demucs](https://github.com/adefossez/demucs) for Audio Speech Detection & Analysis, used for Syncing Audio.
- [Numpy](https://github.com/numpy/numpy) and [Pandas](https://pandas.pydata.org/) for other required Processing.

  
### Logic
#### Full Version
1. When the Video is selected by the user, the Audio Track Gets Extracted by [FFmpeg](https://www.ffmpeg.org/).
2. Then the audio of a voice is detected and the extracted.
3. The extraced Voice Audio is then Processed and Cut into timestamps based of whether there is a voice or not.
4. Then Based on the timestamps the Audio is transcribed and saved into a SRT file.

#### Light Version
The Light Version is about 7.5 to 8 times faster, offering the Same or Better Accuracy of Transcription with insane speed.
<br>
For Context the following Data Can Be Referred.

> **Testing Specs**  
>  
> - **CPU:** Intel i3-7100U (Laptop Mobile Chip)  
> - **RAM:** 4GB (DDR3 2133MHz)  
> - **GPU:** None  

<br>


| Media | Full Version | Light Version |
|----------|----------|----------|
| 1.5 Minutes   | 15 Minutes   | 1.2 Minutes   |
| 22 Minutes   | 2 Hours   | 20 Minutes   |
| 2.5 Hours   | N/A   | 2.4 Hours   |


1. When the Video is selected by the user, the Audio Track Gets Extracted by [FFmpeg](https://www.ffmpeg.org/).
2. The Audio is transcribed with [Faster Whisper](https://github.com/SYSTRAN/faster-whisper).
3. Then Silero VAD is used to detect and Sync TimeStamps.
4. Then saved into a SRT file.

## System Requirements
> Optimized it to use all the Threads of the CPU and the Utilization was at 100% for the duration of the Test.
### Specs

|  | Minimum | Recommended |
|----------|----------|----------|
| CPU   | Intel i3 6th Generation Equivalent   | Intel i5 7th Generation or Equivalent   |
| GPU   | N/A   | RTX 1060 or Equivalent   |
| RAM   | 4 GB   | 8 GB (Video + System)   |


## To Be Added
- Better Optimisation and Faster Running On Older Hardware.
- Charecter Speech Detection
  > Enabling the User to type in the Name of Charecters & an Audio Sample, which can be used to detect who is saying what & implement in Captions
- Easy UIx with PyQt6, for Users to Access.


## Contact
Email: mainakh.cloud@gmail.com
