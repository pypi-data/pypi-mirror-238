from raga import *

# # create test_session object of TestSession instance
test_session = TestSession(project_name="testingProject", run_name= "LM-Model-Upload-Run-Test-v1", access_key="LGXJjQFD899MtVSrNHGH", secret_key="TC466Qu9PhpOjTuLu5aGkXyGbM7SSBeAzYH6HpcP", host="http://3.111.106.226:8080")

lightmetrics_model_upload(test_session=test_session, file_path="/home/ubuntu/developments/testing-platform-python-client/raga/examples/assets/Production-Vienna-Stop.zip", name="Test", version="0.0.1")
