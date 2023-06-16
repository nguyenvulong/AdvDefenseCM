## AdvDefenseCM

This repository implements the paper "On the Defense of Spoofing Countermeasures against Adversarial Attacks". This is our attempt to defend against `FGSM` and `PGD` attacks using `band-pass filter` and `VisuShrink denoising` techniques.
We made [several changes](https://github.com/ano-demo/AdvAttacksASVspoof/compare/master...nguyenvulong:AdvDefenseCM:master) to the base repository, please refer to the full credits below.

### Usage
We have re-factored the codebase so that it can be run step-by-step, but make sure to modify files in the`_config/` folder and the code arguments below. Two augmentation techniques should be run independently for the two experiments. Make sure to spare 1TB (one terabyte) of hard drive for a complete experiment. Otherwise, one can run an attack on a single model (for example, `FGSM` attack on an `LCNN` occupies 150GB of disk space.) 

<p align="center"><img src="https://github.com/nguyenvulong/AdvDefenseCM/assets/1311412/a23ab358-2d7d-49ff-a285-f5d575925289" width=200></p>

### Evaluation
<p align="center">
<img src="https://github.com/nguyenvulong/AdvDefenseCM/assets/1311412/d41c7cd8-b6a6-43d7-9242-217f03496f48" width=800>
<img src="https://github.com/nguyenvulong/AdvDefenseCM/assets/1311412/011a506c-e0f1-4e84-b9ec-43c88880f282" width=800>
<img src="https://github.com/nguyenvulong/AdvDefenseCM/assets/1311412/448fac89-0322-4997-a0e8-6dd90d0af3ae" width=350>
<img src="https://github.com/nguyenvulong/AdvDefenseCM/assets/1311412/5178d4db-b5a2-484b-a2c5-ce7ceb4053fa" width=350>
<img src="https://github.com/nguyenvulong/AdvDefenseCM/assets/1311412/c14c5518-ea72-43a4-b9a7-da4f5b44b788" width=800>
</p>

## Other notes
- Some parts of the code are for `distillation` process. They are not required to reproduce the result of the current paper.
- During experiments, we used similar settings for fair comparison.
- The upstream implementation of the authors can be slightly different from report in their paper.  
  
## Full credits
- VisuShrink denoising: https://github.com/AP-Atul/Audio-Denoising
- sox for band-pass filter: https://sox.sourceforge.net
- We thank the authors of the paper "Adversarial Attacks on Spoofing Countermeasures of automatic speaker verification" for their code base of the two models `LCNN` and `SENet`.
