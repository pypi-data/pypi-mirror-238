import pathlib
from raga import *
import pandas as pd


def image_url(x):
    return f"https://ragatesitng-dev-storage.s3.ap-south-1.amazonaws.com/1/BarrenLands_image/{pathlib.Path(x).name}"


def csv_parser(file_path):
    df = pd.read_csv(file_path).head(5)
    data_frame = pd.DataFrame()
    data_frame["ImageId"] = df["ImageId"].apply(lambda x: StringElement(x))
    data_frame["ImageUri"] = df["SourceLink"].apply(lambda x: StringElement(image_url(x)))
    return data_frame

data_frame = csv_parser("./assets/BarrenLands.csv")


schema = RagaSchema()
schema.add("ImageId", PredictionSchemaElement())
schema.add("ImageUri", ImageUriSchemaElement())

test_session = TestSession(project_name="testingProject", 
                           run_name= "Embedding Generator Run Test", 
                           profile="dev")

#create test_ds object of Dataset instance
test_ds = Dataset(test_session=test_session, 
                  name="model-distribution-test-v1", 
                  type=DATASET_TYPE.IMAGE,
                  data=data_frame, 
                  schema=schema)

# #load schema and pandas data frame
test_ds.load()


model_exe_fun = ModelExecutorFactory().get_model_executor(test_session=test_session, 
                                                          model_name="Satsure Embedding Model", 
                                                          version="0.1.1")

df = model_exe_fun.execute(init_args={"device": "cpu"}, 
                           execution_args={"input_columns":{"img_paths":"ImageUri"}, 
                                           "output_columns":{"embedding":"ImageEmbedding"},
                                           "column_schemas":{"embedding":ImageEmbeddingSchemaElement(model="Satsure Embedding Model")}}, 
                           data_frame=test_ds)

test_ds.load()