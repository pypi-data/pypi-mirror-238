import ast
import random
from raga import *
import pandas as pd
import datetime

label_to_classname = {
    0: "No Data",
    1: "Natural Vegetation",
    2: "Forest",
    3: "Corn",
    4: "Soybeans",
    5: "Wetlands",
    6: "Developed/Barren",
    7: "Open Water",
    8: "Winter Wheat",
    9: "Alfalfa",
    10: "Fallow/Idle Cropland",
    11: "Cotton",
    12: "Sorghum",
    13: "Other"
  }


def get_timestamp_x_hours_ago(hours):
    current_time = datetime.datetime.now()
    delta = datetime.timedelta(days=90, hours=hours)
    past_time = current_time - delta
    timestamp = int(past_time.timestamp())
    return timestamp

def image_url(x):
    return f"https://raga-testing-storage.s3.ap-south-1.amazonaws.com/1/semantic_segmentation_demo_rgb/{x}"

def gt_mask_url(x):
    tif = x.split("/")[1]
    return f"https://raga-testing-storage.s3.ap-south-1.amazonaws.com/1/semantic_segmentation_demo_label/{tif}"

def model_mask_url(x):
    tif = x.split("/")[1]
    return f"https://raga-testing-storage.s3.ap-south-1.amazonaws.com/1/semantic_segmentation_demo_output/{tif}"

def attached_label(id, loss):
    return {id:loss}

def merge_loss_dicts(x):
    mistake_score = MistakeScore()
    x = ast.literal_eval(x)
    
    for key, value in x.items():
        mistake_score.add(key=key, value=value.get('mistake_score'), area=value.get('area'))
    return mistake_score

def imag_embedding(x):
    x = ast.literal_eval(x)
    Embeddings = ImageEmbedding()
    for embedding in x:
        Embeddings.add(Embedding(embedding))
    return Embeddings

def csv_parser(file_path):
    df = pd.read_csv(file_path)
    data_frame = pd.DataFrame()
    data_frame["ImageId"] = df["id"].apply(lambda x: StringElement(x))
    data_frame["ImageUri"] = df["id"].apply(lambda x: StringElement(image_url(f"{x}_merged.tif")))
    data_frame["TimeOfCapture"] = df.apply(lambda row: TimeStampElement(get_timestamp_x_hours_ago(row.name)), axis=1)
    # data_frame["GT"] = df['ground_truth'].apply(lambda x:StringElement(gt_mask_url(x)))
    # data_frame["ModelInference"] = df['model_inference'].apply(lambda x:StringElement(model_mask_url(x)))
    data_frame["Embedding"] = df['embedding'].apply(lambda x: imag_embedding(x))
    # data_frame["MistakeScores"] = df['mistake_score'].apply(merge_loss_dicts)
    data_frame["Reflection"] = data_frame.apply(lambda row: StringElement(random.choice(["Yes", "No"])), axis=1)
    data_frame["Overlap"] = data_frame.apply(lambda row: StringElement(random.choice(["Yes", "No"])), axis=1)
    data_frame["CameraAngle"] = data_frame.apply(lambda row: StringElement(random.choice(["Yes", "No"])), axis=1)
    return data_frame


data_frame = csv_parser("./assets/field_data.csv")


schema = RagaSchema()
schema.add("ImageId", PredictionSchemaElement())
schema.add("ImageUri", ImageUriSchemaElement())
schema.add("TimeOfCapture", TimeOfCaptureSchemaElement())
# schema.add("GT", TIFFSchemaElement(label_mapping=label_to_classname, schema="tif", model="ModelGT"))
# schema.add("ModelInference", TIFFSchemaElement(label_mapping=label_to_classname, schema="tif", model="ModelA"))
schema.add("Embedding", ImageEmbeddingSchemaElement(model="imageModel"))
# schema.add("MistakeScores", MistakeScoreSchemaElement(ref_col_name="Annotations"))
schema.add('Reflection', AttributeSchemaElement())
schema.add('Overlap', AttributeSchemaElement())
schema.add('CameraAngle', AttributeSchemaElement())



run_name = f"loader_demo_semantic_segmentation-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

# create test_session object of TestSession instance
# test_session = TestSession(project_name="testingProject", run_name= run_name, access_key="LGXJjQFD899MtVSrNHGH", secret_key="TC466Qu9PhpOjTuLu5aGkXyGbM7SSBeAzYH6HpcP", host="http://3.111.106.226:8080")

test_session = TestSession(project_name="testingProject", run_name= run_name, access_key="GBEAALGlGsq7HrtU8M2c", secret_key="kpFKGZcP7Q0e1ONEH0kZNOIMS19G4P1f6710ddC0", host="http://13.126.220.245:8080")

cred = DatasetCreds(arn="arn:aws:iam::527593518644:role/s3-role")

#create test_ds object of Dataset instance
test_ds = Dataset(test_session=test_session, 
                  name="test_demo_field_data-v2", 
                  type=DATASET_TYPE.IMAGE,
                  data=data_frame, 
                  schema=schema)

# #load schema and pandas data frame
test_ds.load()
