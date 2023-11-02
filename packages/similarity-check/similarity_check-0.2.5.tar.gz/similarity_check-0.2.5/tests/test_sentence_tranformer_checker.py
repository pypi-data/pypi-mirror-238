from src.similarity_check.utils import _get_enviroment_variables, _get_s3_resource
from src.similarity_check.checkers import sentence_tranformer_checker
import pandas as pd 
import os

def get_stc_test_data():
    X = pd.DataFrame({
        'text': ['Cholera, a unspecified', 'remove test'],
        'id': [1, 2],
    }
    )

    y = pd.DataFrame({
        'new_text': ['Cholera', 'stop the test', 'testing'],
        'new_id': [1, 2, 3],
        'tags': ['pos', 'neg', 'pos'],
        'num': [10, 22, 40],
        'day': [3, 5, 2],
    }
    )
    
    return X, y


def test_stc_match_accuracy():
    X, y = get_stc_test_data()

    stc = sentence_tranformer_checker()
    stc.init_targets(y, target_cols='new_text', target_group='tags')

    df_match = stc.match(X, source_mapping=[('new_text', 'text', 1)])

    assert df_match['new_text'].iloc[0] == 'Cholera', "Cholera, a unspecified wasn't matched correctly"
    assert df_match['new_text'].iloc[1] == 'stop the test', "remove test wasn't matched correctly"


def test_stc_match_only_include():
    X, y = get_stc_test_data()

    stc = sentence_tranformer_checker()
    stc.init_targets(y, target_cols='new_text', target_group='tags', only_include=[])

    df_match = stc.match(X, source_mapping=[('new_text', 'text', 1)], topn=10)
    
    assert len(df_match.columns) == 22, f"the result match didn't include all top 10 matches details, it should include 22 columns but {len(df_match.columns)} columns was found"


def test_stc_match_topn():
    X, y = get_stc_test_data()

    stc = sentence_tranformer_checker()
    stc.init_targets(y, target_cols='new_text', target_group='tags')

    df_match = stc.match(X, source_mapping=[('new_text', 'text', 1)], topn=10)

    assert len(df_match.columns) == 62, f"the result match didn't include all top 10 matches details, it should include 62 columns but {len(df_match.columns)} columns was found"


def _targets_file_system_save():
    X, y = get_stc_test_data()
    stc = sentence_tranformer_checker()
    stc.init_targets(y, target_cols='new_text', target_group='tags')
    stc.save_targets('targets_test/')


def test_stc_targets_save_file_system():
    _targets_file_system_save()

    assert os.path.exists('targets_test/targets.pickle'), "'targets' was not saved"
    assert os.path.exists('targets_test/group_ids.pickle'), "'group_ids' was not saved"
    assert os.path.exists('targets_test/target_df.pickle'), "'target_df' was not saved"
    assert os.path.exists('targets_test/encoded_targets_dict.pickle'), "'encoded_targets_dict' was not saved"

    for root, dirs, files in os.walk('targets_test/', topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))


def test_stc_targets_load_file_system():
    _targets_file_system_save()

    stc = sentence_tranformer_checker()
    stc.load_targets('targets_test/')
    
    assert stc.targets is not None, "'targets' was not loaded"
    assert stc.group_ids is not None, "'group_ids' was not loaded"
    assert stc.target_df is not None, "'target_df' was not loaded"
    assert stc.encoded_targets_dict is not None, "'encoded_targets_dict' was not loaded"

    for root, dirs, files in os.walk('targets_test/', topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))


def _targets_s3_save():
    endpoint, bucket_name, access_key, secret_key = _get_enviroment_variables()
    s3  = _get_s3_resource(endpoint, access_key, secret_key)
    X, y = get_stc_test_data()
    stc = sentence_tranformer_checker()
    stc.init_targets(y, target_cols='new_text', target_group='tags')
    stc.save_targets('targets_test/', save_to='s3')

    return s3, bucket_name


def test_stc_targets_save_s3():
    s3, bucket_name = _targets_s3_save()

    assert s3.Object(bucket_name,'targets_test/targets.pickle').get()['ResponseMetadata']['HTTPStatusCode'] == 200
    assert s3.Object(bucket_name, 'targets_test/group_ids.pickle').get()['ResponseMetadata']['HTTPStatusCode'] == 200
    assert s3.Object(bucket_name, 'targets_test/targets.pickle').get()['ResponseMetadata']['HTTPStatusCode'] == 200
    assert s3.Object(bucket_name, 'targets_test/targets.pickle').get()['ResponseMetadata']['HTTPStatusCode'] == 200
    
    bucket = s3.Bucket(bucket_name)
    bucket.objects.filter(Prefix="targets_test/").delete()


def test_stc_targets_load_s3():
    s3, bucket_name = _targets_s3_save()

    stc = sentence_tranformer_checker()
    stc.load_targets('targets_test/', load_from='s3')
    
    assert stc.targets is not None, "'targets' was not loaded"
    assert stc.group_ids is not None, "'group_ids' was not loaded"
    assert stc.target_df is not None, "'target_df' was not loaded"
    assert stc.encoded_targets_dict is not None, "'encoded_targets_dict' was not loaded"

    bucket = s3.Bucket(bucket_name)
    bucket.objects.filter(Prefix="targets_test/").delete()