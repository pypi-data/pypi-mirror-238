import ast
import pathlib
import random
from raga import *
import pandas as pd
import datetime

def get_timestamp_x_hours_ago(hours):
    current_time = datetime.datetime.now()
    delta = datetime.timedelta(days=90, hours=hours)
    past_time = current_time - delta
    timestamp = int(past_time.timestamp())
    return timestamp

def replace_img_url(old_value):
    url = f"https://ragatesitng-dev-storage.s3.ap-south-1.amazonaws.com/1/{old_value}"
    return StringElement(url)

def replace_label_url(old_value):
    url = f"https://ragatesitng-dev-storage.s3.ap-south-1.amazonaws.com/1/{old_value}"
    return StringElement(url)

def replace_embedding(old_value):
    embeddings = ImageEmbedding()
    embeddings_list = ast.literal_eval(old_value)
    for embedding in embeddings_list:
        embeddings.add(Embedding(embedding))
    return embeddings

label_to_classname = {
    1: "unhealthy"
}

def merge_loss_dicts(x):
    mistake_score = MistakeScore()
    mistake_score.add(key=1, value=0, area=0)  
    return mistake_score

def csv_parser(csv_path):
    df = pd.read_csv(csv_path)
    data_frame = pd.DataFrame()
    data_frame["ImageId"] = df["label"].apply(lambda x: StringElement(pathlib.Path(x).stem))
    data_frame["ImageUri"] = df['rgb_img_tif'].apply(lambda x: replace_img_url(x))
    data_frame["TimeOfCapture"] = df.apply(lambda row: TimeStampElement(get_timestamp_x_hours_ago(row.name)), axis=1)
    data_frame["Reflection"] = df.apply(lambda row: StringElement(random.choice(["Yes", "No"])), axis=1)
    data_frame["Overlap"] = df.apply(lambda row: StringElement(random.choice(["Yes", "No"])), axis=1)
    data_frame["CameraAngle"] = df.apply(lambda row: StringElement(random.choice(["Yes", "No"])), axis=1)
    data_frame["Annotations"] = df['label'].apply(lambda x: replace_label_url(x))
    data_frame["MistakeScores"] = df['label'].apply(merge_loss_dicts)
    return data_frame


pd_data_frame = csv_parser("./assets/tree_health_segmentation.csv")


schema = RagaSchema()
schema.add("ImageId", PredictionSchemaElement())
schema.add("ImageUri", ImageUriSchemaElement())
schema.add("TimeOfCapture", TimeOfCaptureSchemaElement())
schema.add("Reflection", AttributeSchemaElement())
schema.add("Overlap", AttributeSchemaElement())
schema.add("CameraAngle", AttributeSchemaElement())
schema.add("Annotations", TIFFSchemaElement(label_mapping=label_to_classname, schema="tiff", model="ModelA"))
schema.add("MistakeScores", MistakeScoreSchemaElement(ref_col_name="Annotations"))




run_name = f"loader_failure_mode_analysis_semantic_segmentation-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

# create test_session object of TestSession instance
# test_session = TestSession(project_name="testingProject", run_name= run_name, access_key="LGXJjQFD899MtVSrNHGH", secret_key="TC466Qu9PhpOjTuLu5aGkXyGbM7SSBeAzYH6HpcP", host="http://3.111.106.226:8080")

# test_session = TestSession(project_name="SatelliteImagery", run_name= run_name, access_key="XGgIC7lSNgoP5U3UtLjs", secret_key="vHWY3ENWN56Sbv8BoKyW3dQWXcDDEOAjL1YU6s3M", host="http://13.126.220.245:8080")
test_session = TestSession(project_name="Semantic Segmentation - Images", run_name= run_name, access_key="DlGhu2Y9D7Kbc955Y0tz", secret_key="euSZgU49jkIV4CTekcKvpqdk93sQpZdRe338ym1N", host="http://13.126.220.245:8080")

cred = DatasetCreds(arn="arn:aws:iam::527593518644:role/s3-role")

#create test_ds object of Dataset instance
test_ds = Dataset(test_session=test_session,
                  name="tree_health_segmentation_dataset",
                  type=DATASET_TYPE.IMAGE,
                  data=pd_data_frame,
                  schema=schema,
                  creds=cred)

#load to server
test_ds.load()
