import torch
import torchvision
from libcom.utils.model_download import download_pretrained_model
from libcom.utils.process_image import *
from libcom.utils.environment import *
import torch 
import os
import torchvision.transforms as transforms

cur_dir   = os.path.dirname(os.path.abspath(__file__))
# change to your model types
model_set = ['template1', 'template2'] 

class TemplateModel:
    def __init__(self, device=0, model_type='template1', **kwargs):
        '''
        device: gpu id, type=str/torch.device
        model_type: predefined model type, type=str
        kwargs: other parameters for building model, type=dict
        '''
        assert model_type in model_set, f'Not implementation for {model_type}'
        self.model_type = model_type
        self.option = kwargs
        # insert your code here: modify the model name
        weight_path = os.path.join(cur_dir, 'pretrained_models', 'template.pth')
        download_pretrained_model(weight_path)
        self.device = check_gpu_device(device)
        self.build_pretrained_model(weight_path)
        self.build_data_transformer()

    def build_pretrained_model(self, weight_path):
        # insert your code here: build your network
        model = torchvision.models.resnet18(False)
        model.load_state_dict(torch.load(weight_path, map_location='cpu'))
        self.model = model.to(self.device).eval()
        
    def build_data_transformer(self):
        # insert your code here: define image transformations
        self.image_size = 256
        self.transformer = transforms.Compose([
            transforms.Resize((self.image_size, self.image_size)),
            transforms.ToTensor(),
        ])
    
    def inputs_preprocess(self, composite_image, composite_mask):
        # insert your code here: define the pipeline of input data preparation
        # read_image_pil/read_mask_pil: convert image_path or numpy array to PIL format.
        # read_image_opencv/read_mask_opencv: convert image_path or PIL.Image to numpy array. 
        img  = read_image_pil(composite_image)
        img  = self.transformer(img)
        mask = read_mask_pil(composite_mask)
        mask = self.transformer(mask)
        cat_img = torch.cat([img, mask], dim=0)
        cat_img = cat_img.unsqueeze(0).to(self.device)
        return cat_img
    
    def outputs_postprocess(self, outputs):
        # insert your code here:
        score   = torch.softmax(outputs, dim=-1)[0, 1].cpu().item()
        return score
    
    # you can add/replace inputs to fit your task, other input types including:
    # foreground_image, foreground_mask, background_image, bounding_box
    @torch.no_grad()
    def __call__(self, composite_image, composite_mask):
        '''
        composite_image, composite_mask: type=str or numpy array or PIL.Image
        '''
        # insert your code here: define inference pipeline
        inputs    = self.inputs_preprocess(composite_image, composite_mask)
        outputs   = self.model(inputs)
        preds     = self.outputs_postprocess(outputs)
        return preds