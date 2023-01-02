import wandb
import os

os.environ["WANDB_API_KEY"] = "48454db87872b0da16c749491c7e362e5933ceee"
os.environ["WANDB_MODE"] = "online"
user = "calisircihan21"
project = "XPlane11"
display_name = "XplaneDeneme"

wandb.init(entity=user, project=project, name=display_name)


for i in range(100):
  wandb.log({"accuracy": i})