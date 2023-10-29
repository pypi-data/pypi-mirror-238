import pandas as pd
from shapely import geometry, LineString, Polygon
import geopandas as gpd
from tqdm import tqdm

class Filter:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def filter_iou(detections: pd.DataFrame, zones: geometry.multipolygon = None, class_list: list[int] = None, score_threshold: float = 0):

        detections = detections.loc[detections[6]>=score_threshold].copy()

        # filter classess        
        if class_list:
            detections = detections.loc[detections[7].isin(class_list)].copy()

        if zones:
            # filter locations
            g = [geometry.Point(xy) for xy in zip((detections[2] + detections[4]/2), (detections[3] + detections[5]/2))]
            geo_detections = gpd.GeoDataFrame(detections, geometry=g)

            frames = geo_detections.loc[geo_detections.geometry.within(zones)].drop(columns='geometry')

            if frames:
                results = pd.concat(frames)
                results = results[~results.index.duplicated()].reset_index(drop=True)
            else:
                results = pd.DataFrame()
                
        else:
            results = detections

        return results

    @staticmethod
    def filter_tracks(tracks:pd.DataFrame, 
                    include_zones: geometry.MultiPolygon = None, 
                    exclude_zones: geometry.MultiPolygon = None, 
                    video_index:int = None, video_tot:int = None):

        g = [geometry.Point(xy) for xy in zip((tracks[2] + tracks[4]/2), (tracks[3] + tracks[5]/2))]
        geo_tracks = gpd.GeoDataFrame(tracks, geometry=g)
           
        track_ids = tracks[1].unique()
        include_ids = []
        exclude_ids = []

        pbar = tqdm(total=len(track_ids), unit=' tracks')
        if video_index and video_tot: 
            pbar.set_description_str("Filtering zones {} of {}".format(video_index, video_tot))
        else:
            pbar.set_description_str("Filtering zones ")
        
        for track_id in track_ids:
            if include_zones:
                selected_tracks = geo_tracks.loc[(geo_tracks[1]==track_id) & (geo_tracks.geometry.within(include_zones))]
                if len(selected_tracks)>0:
                    include_ids.append(track_id)
            
            if exclude_zones:
                selected_tracks = geo_tracks.loc[(geo_tracks[1]==track_id) & (geo_tracks.geometry.within(exclude_zones))]
                if len(selected_tracks)>0:
                    exclude_ids.append(track_id)
            
            pbar.update()

        pbar.close()

        if len(include_ids)>0:
            results = tracks.loc[tracks[1].isin(include_ids)].copy()
        else:
            results = tracks.copy()

        if len(exclude_ids)>0:
            results = results.loc[~results[1].isin(exclude_ids)].copy()

        return results
    
    @staticmethod
    def filter_tracks_by_lines(tracks:pd.DataFrame, 
                    lines: list[LineString]= None, 
                    method: str = 'include',
                    video_index:int = None, video_tot:int = None) -> pd.DataFrame:
        '''
        Filter tracks by lines
        Inputs:
            tracks - a DataFrame of tracks, [FRAME, TRACK_ID, TOPX, TOPY, WIDTH, LENGTH, RESERVED, RESERVED, RESERVED]
            lines - a list of LineString
            method - filtering method, include (default) - including tracks crossing the lines, exclude - exclude tracks crossing the lines
            video_index - the index of video for processing
            video_tot - the total number of videos
        Return:
            a DataFrame of [FRAME, TRACK_ID, TOPX, TOPY, WIDTH, LENGTH, RESERVED, RESERVED, RESERVED]
        '''
        
        track_ids = tracks[1].unique()
        ids = []

        pbar = tqdm(total=len(track_ids), unit=' tracks')
        if video_index and video_tot: 
            pbar.set_description_str("Filtering tracks {} of {}".format(video_index, video_tot))
        else:
            pbar.set_description_str("Filtering tracks ")
            
        for track_id in track_ids:
            selected = tracks.loc[(tracks[1]==track_id)].copy()
            if len(selected)>0:
                g = selected.apply(lambda track: Polygon([(track[2], track[3]), (track[2] + track[4], track[3]), 
                                (track[2] + track[4], track[3] + track[5]), (track[2], track[3] + track[5])]), axis =1)
                intersected = True
                for line in lines:
                    intersected = intersected and any(line.intersects(g).values.tolist())    

                if intersected:
                    ids.append(track_id)
                    
            pbar.update()

        pbar.close()

        results = []
        if method=='include':    
            results = tracks.loc[tracks[1].isin(ids)].copy()
        elif method=='exclude':
            results = tracks.loc[~tracks[1].isin(ids)].copy()

        results.sort_values(by=[0, 1], inplace=True)
        return results

if __name__=='__main__':
    pass

    