import os, sys
sys.path.append(os.path.dirname(__file__))

from dsort import track as track_dsort
from sort import track as track_sort

class Tracker:
    def __init__(self, method:str='sort', 
                 sort_cfg: dict = {'max_age':1, 'min_inits':3, 'iou_threshold':0.3},
                 deepsort_cfg: dict = {'reid_ckpt': './deep_sort/deep/checkpoint/ckpt.t7', 'max_dist': 0.2, 'min_confidence': 0.3,
                                    'nms_max_overlap': 0.5, 'max_iou_distance': 0.7, 'max_age': 70, 'n_init': 3, 'nn_budget': 100}, 
                 gpu:bool=True):
        '''
        
        '''
        self.method = method
        self.sort_cfg = sort_cfg
        self.dsort_cfg = deepsort_cfg
        self.gpu = gpu 
        
    
    def track(self, det_file:str, out_file:str, video_file:str=None, video_index:int=None, total_videos:int=None):
        if self.method == 'sort':
            track_sort(det_file, out_file, self.sort_cfg['max_age'], self.sort_cfg['min_inits'], 
                       self.sort_cfg['iou_threshold'], video_index, total_videos)
        elif self.method == 'dsort':
            if video_file:
                track_dsort(video_file=video_file, det_file=det_file, out_file=out_file, gpu=self.gpu, reid_ckpt = self.dsort_cfg['reid_ckpt'],
                            max_dist=self.dsort_cfg['max_dist'], min_confidence=self.dsort_cfg['min_confidence'], 
                            nms_max_overlap=self.dsort_cfg['nms_max_overlap'], max_iou_distance=self.dsort_cfg['max_iou_distance'],
                            max_age=self.dsort_cfg['max_age'], n_init=self.dsort_cfg['max_age'], nn_budget=self.dsort_cfg['nn_budget'],
                            video_index=video_index, total_videos=total_videos)
            else:
                print('Invalid video file for deep sort tracking!')
        else:
            print('Invalid tracking method!')
    
    def track_batch(self, det_files=list[str], video_files=list[str], output_path:str=None, 
                    is_overwrite:bool=False, is_report:bool=True)->list[str]:
        results = []
        total_videos = len(det_files)
        count=0
        for det_file in det_files:
            count+=1

            base_filename = os.path.splitext(os.path.basename(det_file))[0].replace("_iou", "")
            if output_path:
                if not os.path.exists(output_path):
                    os.mkdir(output_path)
                track_file = os.path.join(output_path, base_filename+"_track.txt")

            if not is_overwrite:
                if os.path.exists(track_file):
                    if is_report:
                        results.append(track_file)    
                    continue 
            
            video_file = None
            if self.method=="dsort":
                video_file = video_files[count-1]

            self.track(det_file=det_file, out_file=track_file, video_file=video_file, video_index=count, total_videos=total_videos)

            results.append(track_file)

        return results
    
    @staticmethod
    def export_default_cfg(method:str = 'dsort'):
        '''
        Export default tracking model configuration
        '''
        if method == 'sort':
            return {'max_age':1, 'min_inits':3, 'iou_threshold':0.3}
        elif method == 'dsort':
            return {'reid_ckpt': './deep_sort/deep/checkpoint/ckpt.t7', 'max_dist': 0.2, 'min_confidence': 0.3,
                                    'nms_max_overlap': 0.5, 'max_iou_distance': 0.7, 'max_age': 70, 'n_init': 3, 'nn_budget': 100}
        else:
            return None
    
