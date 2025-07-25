
AI 작업을 위한 툴, machine learning을 위한 jupyter부터 Rstudio, code Editor등 다양한 AI Editor application을 실행하고 다룰 수 있다.

EFS를 통해 데이터를 저장하고, 불러오기에 비용이 매우 비쌈

sagemaker를 통해 어플리케이션에 접근하여 s3의 데이터를 다루기 위해서는 도메인설정이 필요하다.
# 도메인

도메인을 저장소로 활용하여 sagemaker에 필요한 jupyter와 같은 툴을 저장하고, 실행 가능하게 만들어준다.
또한 사용자 설정이 필요한데, 사용자를 설정하고, s3버킷에 연결해야 s3버킷에 있는 데이터로 작업이 가능해진다.

#### 사용자 오류
sagemaker에서 도메인을 생성할 경우, 사용자가 자동으로 생성이 되는데, 사용자가 생성이 안되었을 경우 사용자를 직접 생성해주면 된다.

#### 접근 오류
s3버킷과 연결을 할때, s3버킷의 이름에 "sagemaker"가 없을 경우, sagemaker에서 맵핑이 불가능해져 역할부여가 안된다. 따라서 sagemaker를 직접 넣어서 s3버킷을 생성하거나, iam에서 직접 권한을 부여하여 생성하는 방법을 통해 sagemaker 접근 오류를 해결한다.

1. s3 bucket에 "sagemaker"이름 넣기
2. iam에서 s3readandwriteaccess에서 직접 할당해주기

---

도메인 설정이 끝난 경우 사용자를 통해 도메인에 저장된 어플리케이션에 접근할 수 있는데, sagemaker-studio에 접근되었다면, 어플리케이션에서 필요한 어플을 실행하면 된다.


# Jupyter(script)

```python title='setting aws learning machine model with jupyter computer'
!pip install -U transformers
---
import torch
import transformers
import sagemaker
from sagemaker.huggingface import HuggingFace
from sagemaker import get_execution_role
---
role=get_execution_role() # role에 arn주소 attach
---
sagemaker_session=sagemaker.Session()
---
from sagemaker.huggingface import HuggingFace
---
huggingface_estimator=HuggingFace(
    entry_point='script.py',  
    source_dir=',/',
    role=role,
    instance_count=1,
    instance_type='ml.t3.2xlarge',
    transformers_version='4.6',
    pytorch_version='1.8',
    output_path='s3://new-sagemaker-bucketawrg34/output/*',
    py_version='py36',
    hyperparameters={
        'apochs':2,           # model을 검토하는 횟수
        'train_batch_size':4, # 데이터를 읽어오는 양
        'valid_batch_size':2, # 처리할 때 단위
        'learning_rate':1e-05 # 데이터의 가중치 의미
    },
    enable_sagemaker_matrix=True
)
```

```python title='script.py'
#info about training architecture, training data
import torch
import numpy as np
from torch.utils.data import DataLoader, Dataset
from transformers import DistilBertTokenizer, DistilBertModel #Google LLM
from tqdm import tqdm
import argparse 
import os
import pandas as pd

s3_path = 's3://new-sagemaker-bucketawrg34/train_data/newsCorpora.csv'
df = pd.read_csv(s3_path, sep='\t', names=['ID',
                                           'TITLE',
                                           'URL',
                                           'PUBLISHER',
                                           'CATEGORY',
                                           'STORY',
                                           'HOSTNAME',
                                           'TIMESTAMP'])

df = df[['TITLE', 'CATEGORY']]

my_dict = {
    'e': 'Entertainment',
    'b': 'Business',
    't': 'Technology',
    'm': 'Health'
}

def update_cat(x):
    return my_dic[x]

df['CATEGORY'] = df['CATEGORY'].apply(lambda x : update_cat(x))

print(df)

#Machine Learning -> Fraction(단위구분)
df = df.sample(frac=0.05, random_state=1)
df = df.reset_index(drop=True)
```


# Encoding

머신러닝에서 인코딩은 사람의 언어를 기계가 학습하거나 이해할 수 있는 형태로 바꾸는 작업을 뜻한다.

#### 종류
- Label Encoding : 고유 카테고리에 0부터 번호를 붙여 맵핑
- One-Hot-Encoding : 각 카테고리에 해당하는 열을 만들어 0/1로 매핑
- Target Encoding :
- Binary Encoding :




