from raga import *
import datetime


run_name = f"lm-inference-test-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"


# create test_session object of TestSession instance
test_session = TestSession(project_name="testingProject", run_name= run_name, access_key="LGXJjQFD899MtVSrNHGH", secret_key="TC466Qu9PhpOjTuLu5aGkXyGbM7SSBeAzYH6HpcP", host="http://3.111.106.226:8080")


filters = Filter()
filters.add(TimestampFilter(gte="2022-03-15T00:00:00Z", lte="2030-03-15T00:00:00Z"))


# lightmetrics_inference_generator(test_session=test_session, 
#                    dataset_name="test-lm-loader-30-oct-v1", 
#                    filter=filters, 
#                    model_name="Production-America-Stop", 
#                    event_inference_col_name="Production-America-Stop-Event", 
#                    model_inference_col_name="Production-America-Stop-Model")

lightmetrics_inference_generator(test_session=test_session, 
                   dataset_name="test-lm-loader-30-oct-v1", 
                   filter=filters, 
                   model_name="Complex-America-Stop", 
                   event_inference_col_name="Complex-America-Stop-Event", 
                   model_inference_col_name="Complex-America-Stop-Model")