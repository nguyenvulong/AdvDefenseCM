
import torch
from torch import nn
from tqdm import tqdm
import torchattacks
import numpy as np
import sys, os
import argparse
import collections
import torch
import numpy as np
import data_loader.data_loaders as module_data
import model.loss as module_loss
import model.metric as module_metric
import model as module_arch
from parse_config import ConfigParser
from trainer import TrainerDistillation
from trainer import new_model
import model as module_arch

# import SENet34 model
# model = new_model(output_layer='avgpool')
# generate a test sample using numpy
# attack = torchattacks.MIFGSM(model, eps=8/255, steps=10, decay=1.0)

class ModelWrapper(nn.Module):
    def __init__(self, model):
        super(ModelWrapper, self).__init__()
        self.model = model

    def forward(self, x):
        # Call the original model's forward method
        outputs = self.model(x)
        # Assuming the model returns a tuple, we select the first element (logits)
        return outputs[0]

def main(config, resume, sysid, protocol_file, asv_score_file, epsilon):
    logger = config.get_logger('PGD-attack')

    data_loader = getattr(module_data, config['dev_data_loader']['type'])(
        scp_file=None,
        data_dir=config['dev_data_loader']['args']['data_dir'],
        batch_size=8,
        shuffle=False,
        validation_split=0.0,
        num_workers=1,
        eval=True,
        read_protocol=True, 
        protocol_file=protocol_file  # ASVspoof2019.LA.cm.eval.trl.txt
    )


    # data_dir = config['dev_data_loader']['args']['data_dir']
    output_dir = os.path.join(os.path.dirname(resume), f'mifgsm_{sysid}_{epsilon}')
    os.makedirs(output_dir, exist_ok=True)

    if 'lcnn' in resume:
        loss_fn = config.initialize('loss', module_loss)
    else:
        loss_fn = nn.CrossEntropyLoss(reduction='none')

    if hasattr(loss_fn, 'it'):
        loss_fn.it = inf

    # build model architecture
    model = config.initialize('arch', module_arch)
    model = ModelWrapper(model)
    # logger.info(model)


    logger.info('Loading checkpoint: {} ...'.format(resume))
    checkpoint = torch.load(resume)
    state_dict = checkpoint['state_dict']
    if config['n_gpu'] > 1:
        model = torch.nn.DataParallel(model)
    model.load_state_dict(state_dict, strict=False)

    # prepare model for testing
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)
    model.eval()

    epsilon = float(epsilon)
    num_iters = 10

    attack = torchattacks.MIFGSM(model, eps=8/255, steps=10, decay=1.0)

    for i, (utt_list, data, target) in enumerate(tqdm(data_loader)):
        data, target = data.to(device), target.to(device)

        # Normalize the input data to [0, 1] using the maximum and minimum values
        data_normalized = data - data.min()
        data_normalized = data_normalized / data_normalized.max()

        # Call the model's forward method to get the output logits
        output = model(data_normalized)

        _, predicted_labels = torch.max(output, 1)
        print("predicted_labels: ", predicted_labels)
        print("predicted_labels.shape: ", predicted_labels.shape)

        # Pass the predicted labels and target to the attack function
        delta = attack(data_normalized, predicted_labels)

        delta_shifted = delta * (data.max() - data.min())
        data_perturbed = data + delta_shifted
        with torch.no_grad():
            data_perturbed = data_perturbed.squeeze_().cpu().numpy()
        for index, utt_id in enumerate(utt_list):
            cur_data = data_perturbed[index]
            np.save(os.path.join(output_dir, f"{utt_id}.npy"), cur_data, allow_pickle=False)




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ASVSpoof2019 project')

    parser.add_argument('-r', '--resume', default=None, type=str,
                        help='path to latest checkpoint (default: None)')
    parser.add_argument('-s', '--sysid', default=None, type=str,
                        help='system id (default: None)')
    parser.add_argument('-e', '--epsilon', default=None, type=str,
                        help='epsilon')
    parser.add_argument('-f', '--protocol_file', default=None, type=str,
                        help='Protocol file: e.g., data/ASVspoof2019.PA.cm.dev.trl.txt')
    parser.add_argument('-a', '--asv_score_file', default=None, type=str,
                        help='Score file: e.g., data/ASVspoof2019_PA_dev_asv_scores_v1.txt')    
    parser.add_argument('-d', '--device', default=None, type=str,
                        help='indices of GPUs to enable (default: all)')


    args = parser.parse_args()
    config = ConfigParser(args)

    main(config, args.resume, args.sysid, args.protocol_file, args.asv_score_file, args.epsilon)
