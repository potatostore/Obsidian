-가장 작은(큰) 것을 맨 앞으로 보낸다

```cpp
// 1 10 5 8 7 6 4 3 2 9
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
특징을 간단하게 살펴보면
1. 