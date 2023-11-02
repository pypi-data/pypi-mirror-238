from gensim.models import KeyedVectors
import gensim.downloader as api
from src.similarity_check.utils import upload_object, download_object
from typing import Union, List, Optional, Dict
import os
from nltk.stem import PorterStemmer
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk import download
from sentence_transformers import SentenceTransformer
from string import punctuation
from nltk.stem import PorterStemmer
from nltk.stem.isri import ISRIStemmer
from tqdm import tqdm
from collections import Counter
from huggingface_hub.utils._errors import HTTPError
import re
import pickle
download('stopwords')
        

def preprocess(
    sentence: str, 
    replace_file_path: str=None,
    remove_punct: bool=False, 
    separate_punct: bool=False,
    remove_stop_words: bool=False, 
    stemm: bool=False, 
    separate_numbers: bool=False,
    lang: str='en'
) -> str: 
    sentence = str(sentence) # ensure all sentences are string, even if they are some texts with number only
    try:
        if isinstance(replace_file_path, str):
            df = pd.read_excel(replace_file_path)
            replace_dict = dict(zip(df['from'], df['to']))
        else:
            replace_dict = {}
    except NameError:
        print(f'provided replace file doesn\'t have required columns, available columns are : {df.columns}')
        replace_dict = {}
    except FileNotFoundError:
        print(f'provided replace file doesn\'t exists')
        replace_dict = {}

    ps = PorterStemmer()
    # separate numbers from characters
    if separate_numbers:
        sentence = re.sub(r' ?(\d+) ?', r' \1 ', sentence)

    if remove_punct: # remove punctuations
        sentence = sentence.translate(str.maketrans('', '', punctuation))
    elif separate_punct: # separate punctuations
        for punct in punctuation:
            sentence = sentence.replace(punct, f' {punct} ')
    if lang.lower() == 'en':
        ps = PorterStemmer()
        # remove stop words and stem
        if remove_stop_words and stemm:
            stop_words = stopwords.words('english')
            return ' '.join([ps.stem(replace_dict.get(w, w)) for w in sentence.lower().split() if w not in stop_words])
        # stem only
        elif not remove_stop_words and stemm:
            return ' '.join([ps.stem(replace_dict.get(w, w)) for w in sentence.lower().split()])
        else:
            # lower case and remove extra white spaces
            return ' '.join([replace_dict.get(w, w) for w in sentence.lower().split()])
    elif lang.lower() == 'ar':
        st = ISRIStemmer()
        # remove stop words and stem
        if remove_stop_words and stemm:
            download('stopwords')
            stop_words = stopwords.words('arabic')
            return ' '.join([st.stem(w) for w in sentence.lower().split() if w not in stop_words])
        # stem only
        elif not remove_stop_words and stemm:
            return ' '.join([st.stem(w) for w in sentence.lower().split()])
        else:
            # lower case and remove extra white spaces
            return ' '.join([w for w in sentence.lower().split()])
    else:
        raise Exception('non recognized language please specify either en|ar')

    
class sentence_tranformer_checker():
    def __init__(
        self, 
        device: Optional[str] = None,
        model: Optional[str]=None, 
        lang: Optional[str]='en', 
        encode_batch: Optional[int] = 32,
        show_prograss: Optional[bool] = False,
        separate_numbers: Optional[bool]=True,
        separate_punct: Optional[bool]=True,
        remove_punct: Optional[bool]=False, 
        remove_stop_words: Optional[bool]=False, 
        stemm: Optional[bool]=False,
        replace_file_path: str=None
    ):    
        """
        parameters:
            device: the device to do the encoding on operations in (cpu|cuda),
            model (optional): a string of the sentence tranformer model, to use instead of the default one, for more [details](https://www.sbert.net/).
            lang (optional): the languge of the model ('en'|'ar').
            only_include (optional): used only for dataframe matching, allow providing a list of column names to only include for the target matches, provide empty list to get only target_col.
            encode_batch (optional): the number of sentences to encode in a batch.
            encode_target: boolean flag to indicate whatever to enocde the targets when initilizing the object (to cache target encoding).
            remove_punct: boolean flag to indicate whatever to remove punctuations. 
            remove_stop_words: boolean flag to indicate whatever to remove stop words.
            stemm: boolean flag to indicate whatever to do stemming.
        """

        self.encode_batch = encode_batch
        self.remove_punct = remove_punct
        self.remove_stop_words = remove_stop_words
        self.stemm = stemm
        self.lang = lang 
        self.show_prograss = show_prograss
        self.separate_numbers = separate_numbers
        self.separate_punct = separate_punct
        self.replace_file_path = replace_file_path
            
        if device is None:
            self.device = None
        else:
            self.device = device.lower()

        # for target in self.targets.values():
        #     if pd.isnull(target).any():
        #         raise ValueError('Targets contain null values')

        if model is not None:
            try:
                self.model = SentenceTransformer(model, device=self.device)
                if self.show_prograss:
                    print('done...')
            except HTTPError:
                raise HTTPError('entered model name is not defined')
        # if no model is provided use the default model
        else:
            if self.show_prograss:
                print('initializing the model...')
            if lang.lower() == 'en':
                self.model = SentenceTransformer('all-MiniLM-L6-v2', device=self.device)
                if self.show_prograss:
                    print('done...')
            else:
                self.model = SentenceTransformer('distiluse-base-multilingual-cased-v1', device=self.device)
                if self.show_prograss:
                    print('done...')


    # used to make sure that if the object targets are updated, the cached targets embeddings are deleted
    def __setattr__(self, key, value):
        # self.key = value
        if key == 'targets' or key == 'target_df':
            if hasattr(self, 'encoded_targets_dict'):
                del self.encoded_targets_dict     
        super().__setattr__(key, value)


    def init_targets(
        self,
        targets: Union[List[str], pd.DataFrame], 
        target_group: Optional[Union[List[str], List[int]]]=None,
        target_cols: Optional[List[str]]=None, 
        only_include: Optional[List[str]]=None,
    ):
        """
        targets: dataframe or list of targets text to compare with.
        target_group (optional): goups ids for the target to match only a single target for each group, can either provide list of ids,
        or the column name in the target dataframe.
        target_cols (partially optional): the target column names used to match, *must be specified for dataframe matching*.
        """
        if isinstance(target_cols, str):
            target_cols = [target_cols]

        if isinstance(targets, pd.DataFrame):
            targets = targets.copy(deep=True)

            for target_col in target_cols:
                if target_col not in targets.columns:
                    raise KeyError('target_col not found in target DataFrame cloumns')
                else:
                    targets.loc[:, target_col] = targets[target_col].fillna('')

            if target_group is not None:
                if isinstance(target_group, str):
                    if target_group not in targets.columns:
                        raise KeyError('target_group not found in target DataFrame cloumns')
                    self.group_ids = targets[target_group].tolist()
                else:
                    self.group_ids = target_group
            else:
                self.group_ids = None
                
            if only_include is not None:
                for col_name in only_include:
                    if col_name not in targets.columns:       
                        raise KeyError(f'only_include value:({col_name}) not found not found in target DataFrame cloumns')    
                for target_col in target_cols:
                    only_include.insert(0, target_col)
                
                targets = targets.loc[:, only_include]
                

            self.target_df = targets.reset_index(drop=True)
            self.targets = {target_col: [
                        preprocess(
                        sent, 
                        self.replace_file_path,
                        self.remove_punct, 
                        self.separate_punct,
                        self.remove_stop_words, 
                        self.stemm, 
                        self.separate_numbers,
                        self.lang)  
                        for sent in targets[target_col].tolist()
                    ] 
                for target_col in target_cols}
        elif isinstance(targets, list):
            if isinstance(target_group, list):
                self.group_ids = target_group
            else:
                if target_group is None:
                    self.group_ids = target_group
                else:
                    raise TypeError('if target are a list, provided groups must also be a list')
        
            if not targets:
                raise TypeError('Targets are empty') 

            self.target_df = pd.DataFrame({'target': targets})
            self.targets = {'target': [
                    preprocess(
                    sent, 
                    self.replace_file_path,
                    self.remove_punct, 
                    self.separate_punct,
                    self.remove_stop_words, 
                    self.stemm, 
                    self.separate_numbers,
                    self.lang)  
                for sent in targets]
            }
        else:
            msg = f'targets must be a dataframe or a list, instead a source of type {str(type(targets))} was passed'
            raise TypeError(msg)
          
        if self.show_prograss:
            print('enocding targets: ')
            
        self.encoded_targets_dict = {(k): (self.model.encode(v, batch_size=self.encode_batch, show_progress_bar=self.show_prograss,  normalize_embeddings=True)) for k, v in self.targets.items()} # encode the targets
        

    def save_targets(self, targets_save_path, save_to='file_system'):
        if not hasattr(self, 'encoded_targets_dict'):
            raise ValueError('The targets was not initialized, please use one of the following functions to initialize the encoded_targets_dict: (init_targets, load_targets)')
        if save_to == 'file_system':
            if not os.path.exists(targets_save_path):
                os.makedirs(targets_save_path)

            # for encoded_target_name, encoded_target in self.encoded_targets_dict.items():  
                
                
            #     if not os.path.exists(encoded_target_dir):
            #         os.mkdir(encoded_target_dir)
                    
            #     np.save(os.path.join(encoded_target_dir, f'{encoded_target_name}.npy'), encoded_target)

            with open(os.path.join(targets_save_path, 'targets.pickle'), 'wb') as f:
                pickle.dump(self.targets, f)
                
            with open(os.path.join(targets_save_path, 'group_ids.pickle'), 'wb') as f:
                pickle.dump(self.group_ids, f)

            with open(os.path.join(targets_save_path, 'target_df.pickle'), 'wb') as f:
                pickle.dump(self.target_df, f)

            # self.target_df.to_csv(os.path.join(targets_save_path, 'target_df.csv'), index=False)    

            with open(os.path.join(targets_save_path, 'encoded_targets_dict.pickle'), 'wb') as f:
                pickle.dump(self.encoded_targets_dict, f)
        elif save_to == 's3':
            upload_object(self.targets, targets_save_path, 'targets.pickle')
            upload_object(self.group_ids, targets_save_path, 'group_ids.pickle')
            upload_object(self.target_df, targets_save_path, 'target_df.pickle')
            upload_object(self.encoded_targets_dict, targets_save_path, 'encoded_targets_dict.pickle')
        else:
            raise ValueError(f"save_to accept only 'file_system', or 's3' the following value was passed {save_to}")
        
    def load_targets(self, targets_save_path, load_from='file_system'):
        try:
            if load_from == 'file_system':
                with open(os.path.join(targets_save_path, 'targets.pickle'), 'rb') as f:
                    self.targets = pickle.load(f)
                    
                with open(os.path.join(targets_save_path, 'group_ids.pickle'), 'rb') as f:
                    self.group_ids = pickle.load(f)
                    
                with open(os.path.join(targets_save_path, 'target_df.pickle'), 'rb') as f:
                    self.target_df = pickle.load(f)

                # self.target_df = pd.read_csv(os.path.join(targets_save_path, 'target_df.csv'))   

                # encoded_targets_dict must be loaded at the end, as setting target_df or targets will delete the encoded_targets_dict
                with open(os.path.join(targets_save_path, 'encoded_targets_dict.pickle'), 'rb') as f:
                    self.encoded_targets_dict = pickle.load(f)    
            elif load_from == 's3':
                self.targets = download_object(targets_save_path, 'targets.pickle')
                self.group_ids = download_object(targets_save_path, 'group_ids.pickle')
                self.target_df = download_object(targets_save_path, 'target_df.pickle')
                self.encoded_targets_dict = download_object(targets_save_path, 'encoded_targets_dict.pickle')
            else:
                raise ValueError(f"load_from accept only 'file_system', or 's3' the following value was passed {load_from}")       
            # self.encoded_targets_dict = {
            #     os.path.splitext(encoded_target_path)[0]: np.load(os.path.join(targets_save_path, 'encoded_targets_dict', encoded_target_path))
            #     for encoded_target_path in os.listdir(os.path.join(targets_save_path, 'encoded_targets_dict'))
            # }
        except FileNotFoundError as e:
            raise FileNotFoundError(f'a target file was not found {e}')
        
    
    def match(
        self, 
        source: Union[List[str], pd.DataFrame], 
        source_mapping: Optional[Union[str, List]]=None, 
        topn: Optional[int]=1, 
        threshold: Optional[float]=0.5, 
        batch_size: Optional[int]=128
    ) -> pd.DataFrame:
        '''
        Main match function. return only the top candidate for every source string.
        parameters:
            source: dataframe or list of input texts to find closest match for.
            source_mapping (partially optional) *must be specified for dataframe matching*: a list with each element being a tuple with the following three values (the target column name, source column name, the weight for this match), if a string is passed it and one target was only passed it will be mapped to the that target, with a the full weight of 1.0, note that the the overall weights must equal 1.0.
            topn: number of matches to return.
            threshold: the lowest threeshold to ignore matches below it.
            batch_size: the size of the batch in inputs to match with targets (to limit space usage).
        returns:
            a data frame with 3 columns (source, target, score), and two extra columns for each extra match (target_2, score_2 ...)
        ''' 
        if isinstance(source, pd.DataFrame) and not hasattr(self, 'target_df'):
            msg = 'if target is a dataframe source must also be a dataframe'
            raise TypeError(msg)

        if len(self.targets) == 1 and isinstance(source_mapping, str):
            source_mapping = [(list(self.targets.keys())[0], source_mapping, 1)]

        if isinstance(source, pd.DataFrame):
            source = source.copy(deep=True)

            overall_weight = 0.0
            for _, source_col, weight in source_mapping:
                if source_col not in source.columns:
                    msg = f'the following source_col ({source_col}) not found in source DataFrame cloumns'
                    raise KeyError(msg)
                else:
                    source.loc[:, source_col] = source[source_col].fillna('')
                overall_weight += weight
                
            if overall_weight != 1.0:
                msg = f'the sum of the provided weights must equal 1.0, the provided weights sum is: {overall_weight}'
                raise ValueError(msg)
            
            self.source_df = source.reset_index(drop=True)
            sources = {source_col: [
                    preprocess(
                    sent, 
                    self.replace_file_path,
                    self.remove_punct, 
                    self.separate_punct,
                    self.remove_stop_words, 
                    self.stemm, 
                    self.separate_numbers,
                    self.lang)  
                for sent in source[source_col].tolist()] 
                for _, source_col, __ in source_mapping
            }
        elif isinstance(source, list):
            source = pd.DataFrame({'source': source})
            self.source_df = source
            if not source_mapping:
                if len(self.targets) > 1:
                    msg = 'there are multiple target columns to map with the source, please provide a costume source_mapping, or adjust the target columns to one specific columns'
                    raise ValueError(msg)
                source_mapping = [(list(self.targets.keys())[0], 'source', 1)]
            sources = {source_col: [
                    preprocess(
                    sent, 
                    self.replace_file_path,
                    self.remove_punct, 
                    self.separate_punct,
                    self.remove_stop_words, 
                    self.stemm, 
                    self.separate_numbers,
                    self.lang)  
                for sent in source[source_col].tolist()] 
            for _, source_col, __ in source_mapping
            }
        else:
            msg = f'source must be a dataframe or a list, instead a source of type {str(type(source))} was passed'
            raise TypeError(msg)
        # else:
        #     self.source_df = pd.DataFrame({'source': source})
        #     sources = {'source': [preprocess(sent, self.remove_punct, self.remove_stop_words, self.stemm, self.lang) for sent in source]}

        if not hasattr(self, 'encoded_targets_dict'):
            raise ValueError('The encoded_targets_dict was not defined, please use one of the following functions to initialize the encoded_targets_dict: (init_targets, load_targets)')
        else:
            encoded_targets_dict = self.encoded_targets_dict

        inputs_length = len(list(sources.values())[0])
        targets_length = len(list(self.targets.values())[0])

        top_cosine = np.full((inputs_length, topn), None)
        match_idxs = np.full((inputs_length, topn), None)

        if self.show_prograss:
            print('matching prograss:')

        for i in tqdm(range(0, inputs_length, batch_size), disable=(not self.show_prograss)):
            encoded_inputs = {(k): (self.model.encode(v[i:i+batch_size], batch_size=self.encode_batch, normalize_embeddings=True)) for k, v in sources.items()} # encode the inputs
            batch_inputs_length = len(list(encoded_inputs.values())[0])
            # encoded_inputs = self.model.encode(self.source_names[i:i+batch_size], batch_size=self.encode_batch, normalize_embeddings=True) # encode the inputs
    
            batch_top_cosine, batch_match_idxs = self.max_cosine_sim(encoded_inputs, encoded_targets_dict, source_mapping , topn, threshold, batch_inputs_length, targets_length)
            top_cosine[i:i+batch_size, :] = batch_top_cosine
            match_idxs[i:i+batch_size, :] = batch_match_idxs
        
        match_output = self._make_matchdf(top_cosine, match_idxs, inputs_length)

        return match_output


    def max_cosine_sim(self, encoded_inputs, encoded_targets_dict, source_mapping, topn, threshold, inputs_length, targets_length):
        scores = np.zeros((inputs_length, targets_length), dtype=np.float32) # initialize with zeros
  
        for combinition_target, combinition_input, weight in source_mapping:
            if len(encoded_inputs[combinition_input].shape) == 1:
                encoded_inputs[combinition_input] = np.expand_dims(encoded_inputs[combinition_input], axis=0)

            if len(encoded_targets_dict[combinition_target].shape) == 1:
                encoded_targets_dict[combinition_target] = np.expand_dims(encoded_targets_dict[combinition_target], axis=0)

            scores += np.matmul(encoded_inputs[combinition_input], encoded_targets_dict[combinition_target].T) * weight

        if self.group_ids is None:
            max_matches = min((targets_length-1, topn))
        else:
            max_matches = min((targets_length-1, topn * Counter(self.group_ids).most_common()[0][1]))
        
        top_sorted_idxs = np.argpartition(scores, -max_matches, axis=1)[:, -max_matches:] 
        
        # resort the result as the partition sort doesn't completly sort the result
        for i, idxs in enumerate(top_sorted_idxs):
            top_sorted_idxs[i, :] = top_sorted_idxs[i, np.argsort(-scores[i, idxs])]

        max_cosines = np.full((inputs_length, topn), None)
        match_idxs = np.full((inputs_length, topn), None)
            
        # loop over top results to extract the index, target, and score for each match
        if self.group_ids is not None:
            for i, row in enumerate(top_sorted_idxs):
                column_id = 0
                previous_group_id = float('inf')
                for highest_score_idx in row:
                    if column_id >= topn or scores[i, highest_score_idx] < threshold:
                        break
                    if self.group_ids[highest_score_idx] == previous_group_id:
                        continue
                    match_idxs[i, column_id] = highest_score_idx
                    max_cosines[i, column_id] = scores[i, highest_score_idx]
                    
                    column_id += 1
                    previous_group_id = self.group_ids[highest_score_idx]
        else:
            for i, row in enumerate(top_sorted_idxs):
                column_id = 0
                for highest_score_idx in row:
                    if column_id >= topn or scores[i, highest_score_idx] < threshold:
                        break
                    match_idxs[i, column_id] = highest_score_idx
                    max_cosines[i, column_id] = scores[i, highest_score_idx]
                    
                    column_id += 1
                    
        return max_cosines, match_idxs


    def _make_matchdf(self, top_cosine, match_idxs, inputs_length)-> pd.DataFrame:
        ''' Build dataframe for result return '''
        arr_temp = np.full((inputs_length, len(self.target_df.columns)+1), None)

        for i, (match_idx, score) in enumerate(zip(match_idxs.T[0], top_cosine.T[0])):
            if match_idx in self.target_df.index:
                    temp = self.target_df.iloc[match_idx].tolist()
                    temp.insert(0, score)
                    arr_temp[i, :] = temp

        cols = self.target_df.columns.tolist() 
        cols.insert(0, 'score_1')
        match_df= pd.DataFrame(arr_temp, columns=cols)

        # concat targets matches into one dataframe
        for match_num in range(1, len(match_idxs.T)):
            arr_temp = np.full((inputs_length, len(self.target_df.columns)+1), None)
            for i, (match_idx, score) in enumerate(zip(match_idxs.T[match_num], top_cosine.T[match_num])):
                if match_idx in self.target_df.index:
                    temp = self.target_df.iloc[match_idx].tolist()
                    temp.insert(0, score)
                    arr_temp[i, :] = temp

            cols = self.target_df.columns.tolist() 
            cols.insert(0, f'score_{match_num+1}')
            df_temp= pd.DataFrame(arr_temp, columns=cols)
            match_df = match_df.merge(df_temp, left_index=True, right_index=True, suffixes=(f'_{match_num}', f'_{match_num+1}'))

        # merge matches with source
        match_df = self.source_df.reset_index(drop=True).merge(match_df, left_index=True, right_index=True, suffixes=(f'_source', f'_target'))

        return match_df
    

class word_mover_distance():
    def __init__(self, source_names, target_names, model):
        if not source_names:
            raise Exception('Inputs are empty')
        
        if not target_names:
            raise Exception('Targets are empty') 
               
        if pd.isnull(source_names).any():
            raise Exception('Inputs contain null values')
        
        if pd.isnull(target_names).any():
            raise Exception('Targets contain null values')
        
        self.source_names = source_names
        self.target_names = target_names
        self.model = model
        # if no model is provided use the default model
        if model is None:
            print('initializing the model (English model)...')
            self.model = api.load('glove-wiki-gigaword-300')

    def match(self, topn=1, return_match_idx=False):
        '''
        Main match function. return only the top candidate for every source string.
        '''
        self.topn = topn
        self.return_match_idx = return_match_idx
        
        self.top_wmd_distance()

        match_output = self._make_matchdf()

        return match_output


    def clean_data(self, remove_punct=True, remove_stop_words=True, stemm=False, lang='en'): 
        self.source_names = [preprocess(sent, remove_punct, remove_stop_words, stemm, lang) for sent in self.source_names]
        self.target_names = [preprocess(sent, remove_punct, remove_stop_words, stemm, lang) for sent in self.target_names]


    def min_wmd_distance(self, input):
        wmd_results = np.array([self.model.wmdistance(input, target) for target in self.target_names])
        
        # get topn results
        wmd_sorted = np.sort(np.unique(wmd_results))
        scores = []
        indexes = []
        for x in wmd_sorted:
            if len(indexes) == self.topn:
                break
            for y in np.where(wmd_results == x)[0]:
                scores.append(float(1 - x)) # convert distance to score
                indexes.append(y)
                if len(indexes) == self.topn:
                    break    
        targets = [self.target_names[idx] for idx in indexes]
        
        # fill empty topn results 
        while len(targets) < self.topn:
            indexes.append(None)
            targets.append(None)
            scores.append(None)
        return targets, scores, indexes
    

    def top_wmd_distance(self):
        results = np.array([self.min_wmd_distance(input) for input in self.source_names])
        self.targets = results[:, 0]
        self.top_scores = results[:, 1]
        self.match_idxs = results[:, 2]


    def _make_matchdf(self):
        ''' Build dataframe for result return '''
        if not self.return_match_idx:
            match_list = []
            for source, targets, top_scores in zip(self.source_names, self.targets, self.top_scores):
                row = []
                row.append(source)
                if targets is not None:
                    # loop over results of multi matches
                    for target, top_score in zip(targets, top_scores):
                        row.append(target)
                        row.append(top_score) 
                match_list.append(tuple(row))

            # prepare columns names
            colnames = ['source', 'prediction', 'score']
            
            for i in range(2, self.topn+1):
                colnames.append(f'prediction_{i}')
                colnames.append(f'score_{i}')

            match_df = pd.DataFrame(match_list, columns=colnames)
        else:
            match_list = []
            for source, targets, top_scores, match_idxs in zip(self.source_names, self.targets, self.top_scores, self.match_idxs):
                row = []
                row.append(source)
                if targets is not None:
                    # loop over results of multi matches
                    for target, top_score, match_idx in zip(targets, top_scores, match_idxs):
                        row.append(target)
                        row.append(top_score) 
                        row.append(match_idx)
                match_list.append(tuple(row))

            # prepare columns names
            colnames = ['source', 'prediction', 'score', 'match_idx']
            
            for i in range(2, self.topn+1):
                colnames.append(f'prediction_{i}')
                colnames.append(f'score_{i}')
                colnames.append(f'match_idx_{i}')

            match_df = pd.DataFrame(match_list, columns=colnames)  
        
        return match_df