
가상 메모리는 과거 ram의 메모리 문제에서 파생된 개념이다.

## 원인

- RAM memory overflow
과거에는 프로그램에 필요한 데이터들이 ram에 전부 올라와 있어야 사용할 수 있다. 하지만 ram의 용량에는 한계가 있고, 따라서 ram보다 큰 용량의 프로그램을 돌릴 수 없는 문제가 발생했다. 또한 ram용량에 맞추어서 프로그램이 돌아간다고 해도, 여러 프로그램을 돌리게 되면 자연스럽게 ram이 가득 차게 되어 다양한 프로그램을 한 번에 작업하는 것이 제한되었다. 

- OS/Process 메모리 관련 문제
또한 OS와 프로세스(app)가 같은 레벨에서 실행이 됐었는데, kernel층과 user층의 분리가 이루어지지 않고, 동등한 관계에서 실행이 되었다. 이는 즉 ram일부를 OS실행을 위해 할당했다는 뜻이다(현재도 ram일부는 OS가 차지한다). 이때 가장 큰 문제점은 앱이 실행된 이후 종료되었을때 앱에 할당되었던 메모리가 해제되지 않고, 그대로 사용못하는 메모리로 남아 다음 앱이 실행되었을때 해당 메모리에 접근을 못했다(메모리 릭 - memory leak). 프로세스에 OS가 메모리를 할당해주지 않고, 직접 메모리를 차지하는 방식이다 보니 프로세스에 문제가 생겨 데드락이 걸리면 OS도 같이 튕기는 현상이 빈번했다. 

- 멀티테스킹시 같은 주소 메모리 로딩
다양한 프로그램이 돌아간다고 해도 문제는 여전했다. 프로그램들이 서로 멀티테스킹을 하며 메모리의 같은 위치에 존재하는 데이터를 불러 읽으며 서로 오작동이 발생했다.

따라서 OS를 통해 사용하지 않는 기능에 대한 메모리는 다시 디스크로 넣고, 필요한 기능을 콜업한 후 프로그램별로 메모리를 나누어 할당해주면 해결된다는 생각을 갖고 만들어진게 가상 메모리이다.

---
## 해결

- RAM memory overflow
필요한 기능을 상위메모리에 콜업하고, 사용하지 않거나 , 빈도가 제일 적은 기능은 하위메모리로 다시 돌려보내는 Swap을 통해 해결하였는데, ram뿐만 아니라 디스크(ssd, 하드디스크)의 일부에 swap영역을 만들어 swap을 진행하며 ram의 메모리인 것처럼 활용한다.

- OS/Process 메모리 관련 문제
가상메모리를 통해 위 문제 중 ram에 할당된 메모리를 해제할 수 있도록 만들었다. 가상메모리가 중앙(OS)에서 메모리를 관리하여 할당/해제를 할 수 있도록 만들었다.

- 멀티테스킹시 같은 주소 메모리 로딩
가상메모리가 각 프로세스에 독립적인 주소를 할당하고 OS가 이를 관리하여 문제를 해결했다. 이는 프로그램간의 메모리 충돌 문제를 방지하는 것 뿐만 아니라 서로의 메모리를 보호하는 역할도 수행한다.

	여기서 궁금한 점은 OS가 할당된 메모리를 해제할 수 있게 되었으면, 굳이 가상화할 이유가 있나? 라는 것이다. OS가 메모리 할당/해제 권한을 갖는 것과 메모리의 가상화가 무슨 상관관계가 있나 라는 것이다. 굳이 가상화가 이루어지지 않아도, OS에 의해 메모리는 회수할 수 있을 것이다. 하지만 가상메모리는 메모리의 회수문제 뿐만 아니라 보안 등 다목적에 의해 만들어진 것이다. 특히 보안을 위해 user/kernel층으로 분리를 하며 user층이 메모리에 접근할 수 없게 되었는데, 이때 가상메모리를 통해 간접적으로 접근하게 되며 해제할 권리를 OS에 부여하는 방식이 된다. 따라서 가상메모리를 사용하지 않으면 프로그램이 메모리에 접근하는 순간 데드록이 발생하기에 가상메모리를 통해 해결하는 것이다.

---
## 특징

1. 메모리 용량 부족 해결 : ram에 한정된 개념이 아닌 가상메모리라는 개념은 cache와 ram, ram과 디스크 사이에서 자유롭게 적용될 수 있으며, 이는 상위 메모리가 메모리 용량 부족시 *스왑*을 통해 해결할 수 있다.

2. 프로세스의 독립성 보장 : 각 프로그램이 같은 위치의 데이터를 읽어 오작동이 발생하는 상황을 막기 위해 각 프로세스가 독립된 하나의 메모리 공간을 사용하는 것처럼 분리를 시킨다.

---

## 주요 개념

1. 스왑(swap) : 스왑은 상위메모리에서 사용하지 않는 데이터를 하위메모리로 빼고, 프로세스가 필요한 기능에 대한 데이터를 콜업하는 방식으로 메모리 용량이 부족하지 않도록 예방한다.

2. 매핑(mapping) : 매핑은 가상메모리의 주소에 실제 메모리의 주소를 대응시키는 과정이다. 이를 통해 