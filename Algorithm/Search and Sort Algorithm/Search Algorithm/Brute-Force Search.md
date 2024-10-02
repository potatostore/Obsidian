완전 탐색이라고 불리는 Brute-Force Search는 가장 직관적인 알고리즘이라고 볼 수 있다. 완전 탐색이라는 이름에 걸맞게 가능한 모든 경우를 일일이 탐색하여 해를 찾는 방식이다. 당연히 효율성은 떨어지지만, 단순하다는 점이 장점으로 다가온다.

# 작동원리

- 해를 찾기위해 모든 집합을 하나하나 찾아보고, 해를 발견한 즉시 종료한다.

정확한 해를 보장하고, 직관적이지만, 효율성이 매우 떨어진다는 점을 확인할 수 있다.

# 시간복잡도

- 문제의 크기에 따라 달라지지만, 보통 O(n^k)와 같이 지수시간이다.

# 조건

- 별다른 조건 없이 어느 상황에서나 쓸 수 있다는 것이 큰 특징이다.

```c++ title='Ex : 문자열에서 특정 패턴 찾기'
#include <iostream>
#include <cstring>
using namespace std;

bool bruteForce(string text, string pattern){
	int textlength = text.length();
	int patternlength = pattern.length();

	for(int i = 0; i < n - m; i++){
		int j;

		for(j = 0; j < m; j++){
			if(text[i+j] != pattern[j]) break;
		}

		if(j == m) return true;
	}
	return false;
}
```


이처럼 완전 탐색은 반복문을 이중으로 겹쳐놓은 형태가 많기에 시간복잡도가 자연스럽게 기하급수적으로 상승하는 편이다.


완전탐색은 패턴문제나 모든 부분집합 탐색 문제 처럼 특정조건에 부합하는 해를 찾는 문제가 아닌 정확한 해를 찾는 경우에 쓰면 좋은 탐색 알고리즘이다.

# 장단점
- 장점 : 
	- 단순, 직관적
	- 최적해 보장
	- 모든 문제에 적용 가능
- 단점 :
	- 크기에 비례해 기하급수적으로 증가하는 시간복잡도
	- 비효율적

입력의 크기가 작거나, 다른 방안이 떠오르지 않으면 시도할 알고리즘이다.