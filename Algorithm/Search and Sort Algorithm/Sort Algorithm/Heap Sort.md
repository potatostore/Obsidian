- 힙 트리 구조(Heap Tree Structure)을 이용하여 정렬하는 방법


*이진트리(Binary Tree) : 데이터를 표현하는 방식 중 하나로, 각 데이터를 노드에 담은 후 뒤에 노드를 두 개씩 이어 붙이는 형태이다.*
![[스크린샷 2024-08-23 오후 11.05.14.png]]


*완전 이진 트리(Complete Binary Tree) : 데이터가 루트부터 시작하여 리프까지 노드에 빠짐 없이 빽빽히 차있는 형태 (위 사진도 완전 이진 트리라고 볼 수 있다.)

*힙(Heap) : 최솟값이나 최댓값을 빠르게 찾기 위해 완전 이진 트리를 기반으로 하는 트리*
	- 최대힙 : '부모 노드' > '자식 노드'인 완전 이진 트리로, 최상단 노드인 루트가 가장 큰 값을 갖는다.
	- 최소힙 : '부모 노드' < '자식 노드'인 완전 이진 트리로, 최상단 노드인 루트가 가장 작은 값을 갖는다.

하지만 완전 이진 트리 모두가 최대힙 혹은 최소힙에 만족하는 형태로 데이터가 저장이 되어 있지는 않다. 이를 위해 힙 정렬을 수행해 최대힙, 최소힙의 조건에 부합해야 하는데, 이를 '힙 생성 알고리즘(Heapify Algorithm)'이라고 한다.


```c++
#include <iostream>

using namespace std;

int main(void){

}
```