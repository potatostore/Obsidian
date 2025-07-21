
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

```
!pip install -U transformers

import torch
import transformers
import sagemaker
from sagemaker.huggingface import HuggingFace
from sagemaker import get_execution_role

role=get_execution_role() # role에 arn주소 attach

sagemaker_session=sagemaker.Session()

from sagemaker.huggingface import HuggingFace

huggingface_estimator=HuggingFace(
    
)
```