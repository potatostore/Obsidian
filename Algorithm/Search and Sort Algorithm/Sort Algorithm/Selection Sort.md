- 가장 작은(큰) 것을 맨 앞으로 보낸다

```cpp title='오름차순'
#include <iostream>
#include <vector>

using namespace std;
vector <int> v = {1,10,5,8,7,6,4,3,2,9};

void swap(int &a, int &b);

int main(void){
	int minIndex;
	
	for(int i=0;i<v.size();++i){
	    int min = 11; // *max_element(v.begin(), v.end()) + 1
	    
		for(int j=i;j<v.size();++j){
			if(v[j] < min){
				minIndex = j;
				min = v[j];
			}
		}
		
		swap(v[i], v[minIndex]);
	}
	
	for(auto i : v) cout << i << " ";
	
	return 0;
}

void swap(int &a, int &b){
	int temp = a;
	a = b;
	b = temp;
}
```

위 예제를 통해 1~10까지의 수를 선택정렬로 나타내어 보았다. 

수행 시간은 *O(n ( n+1) / 2) = O(n^2)*으로 나타낼 수 있다.

특징을 간단하게 살펴보면
1. 시간복잡도가 O(n^2)이다 : 많은 수의 예제를 컴파일하게 되면 기하급수적인 시간이 소요됨.
2. 간단하다 : swap 함수와 반복문 두 가지로 쉽게 구현할 수 있다.

*결론 : 예제의 수가 적으면 빠르게 이용 가능하다는 장점이 존재하지만, 예제의 수가 많아질수록 사용할 이유가 전혀 존재하지 않음*