## AdvDefenseCM
### Change Log
- 2023-11-16 Additional Note
- 2023-09-01 Accepted & Early Access
- 2023-08-03 MI-FGSM, SNR measurement added
- 2023-07-27 First Decision: Major revision
- 2023-07-09 Submitted to IEEE Access

### Introduction
This repository implements the paper "On the Defense of Spoofing Countermeasures against Adversarial Attacks". This is our attempt to defend against `FGSM` and `PGD` attacks using `band-pass filter` and `VisuShrink denoising` techniques.
We made [several changes](https://github.com/ano-demo/AdvAttacksASVspoof/compare/master...nguyenvulong:AdvDefenseCM:master) to the base repository, please refer to the full credits below.
### Installation
`conda env create -f env.yml`
Make sure to resolve any problems regarding dependencies.
### Usage
We have re-factored the codebase so that it can be run step-by-step, but make sure to modify files in the`_config/` folder and the code arguments below. Two augmentation techniques should be run independently for the two experiments. Make sure to spare 1TB (one terabyte) of hard drive for a complete experiment. Otherwise, one can run an attack on a single model (for example, `FGSM` attack on an `LCNN` occupies 150GB of disk space.) 

<p align="center"><img src="https://github.com/nguyenvulong/AdvDefenseCM/assets/1311412/a23ab358-2d7d-49ff-a285-f5d575925289" width=150></p>


### Evaluation
<p align="center">
<img src="https://github.com/nguyenvulong/AdvDefenseCM/assets/1311412/d41c7cd8-b6a6-43d7-9242-217f03496f48" width=800>
<img src="https://github.com/nguyenvulong/AdvDefenseCM/assets/1311412/011a506c-e0f1-4e84-b9ec-43c88880f282" width=800>
<img src="https://github.com/nguyenvulong/AdvDefenseCM/assets/1311412/448fac89-0322-4997-a0e8-6dd90d0af3ae" width=350>
<img src="https://github.com/nguyenvulong/AdvDefenseCM/assets/1311412/5178d4db-b5a2-484b-a2c5-ce7ceb4053fa" width=350>
<img src="https://github.com/nguyenvulong/AdvDefenseCM/assets/1311412/c14c5518-ea72-43a4-b9a7-da4f5b44b788" width=800>
</p>

### Audio samples (CLICK to toggle)
Github **does not** allow embedding `audio` contents so I have to used `mp4` embedding instead. Make sure to turn on the speaker buttons below.
<details>
<summary> Bandpass filter has the strongest effect of removing noise from the original audio, whereas adversarial sample does not necessarily have noisier output.  </summary>
  
**Original sample** 

https://github.com/nguyenvulong/AdvDefenseCM/assets/1311412/1f57d32a-74dd-4ec6-8bbc-e79224e75aa8

**Adversarial sample** 

https://github.com/nguyenvulong/AdvDefenseCM/assets/1311412/1d3d2d6f-1f3f-41d5-ba2f-71c9e297e357

**Denoised sample**

https://github.com/nguyenvulong/AdvDefenseCM/assets/1311412/f150bef2-8916-4ab9-93a6-6d2ccacba96e

**Bandpassed sample**

https://github.com/nguyenvulong/AdvDefenseCM/assets/1311412/050ea798-31e8-4bb5-8ee9-7c496983c760
</details>

## Other notes
- Some parts of the code are for `distillation` process. They are not required to reproduce the result of the current paper.
- During experiments, we used similar settings for fair comparison.
- The upstream implementation of the authors can be slightly different from report in their paper.  
  
## Full credits
- `VisuShrink` denoising: https://github.com/AP-Atul/Audio-Denoising
- `sox` for band-pass filter: https://sox.sourceforge.net
- `Adversarial Robustness toolbox (ART)`: https://github.com/Trusted-AI/adversarial-robustness-toolbox
- `torchattacks`: https://adversarial-attacks-pytorch.readthedocs.io/
- We thank the authors of the paper "Adversarial Attacks on Spoofing Countermeasures of automatic speaker verification" for their code base of the two models `LCNN` and `SENet`. Their code base can be found here: https://github.com/ano-demo/AdvAttacksASVspoof. Previously I created a fork from this repo, which is located https://github.com/nguyenvulong/AdvDefenseCM_legacy.

- Today (2023-11-16), I discovered a paper name _"DOMPTEUR: Taming Audio Adversarial Examples"_ where the authors also did a similar technique to limit the frequencty to `300−5000Hz`. Unfortunately, my finding was too late so I could not reference this paper in my manuscript. **Even though the our study was independently conducted, I would like to shout out to the authors since they are way earlier** than us in using this method to defend against adversarial attacks in Automatic Speech Recognition (ASR) systems. While our study is about spoofing countermeasures, the effect should be very similar if not identical.
