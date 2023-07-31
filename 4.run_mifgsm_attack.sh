# Description: Run mi-fgsm attack

python mifgsm_attack.py  --resume /data/longnv/_saved/models/LA_SENet34_LPSseg_uf_seg600/20230224_155356/model_best.pth \
						--epsilon 5.0 \
                  		--protocol_file /data/Dataset/ASVspoof/LA/ASVspoof2019_LA_cm_protocols/ASVspoof2019.LA.cm.eval.trl.txt \
						--asv_score_file /data/Dataset/ASVspoof/LA/ASVspoof2019_LA_asv_scores/ASVspoof2019.LA.asv.eval.gi.trl.scores.txt  \
                	    --device 3


