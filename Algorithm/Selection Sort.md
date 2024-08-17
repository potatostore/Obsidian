-가장 작은(큰) 것을 맨 앞으로 보낸다

```cpp
// 1 10 5 8 7 6 4 3 2 9
#include <iostream>
#include <vector>

using namespace std;
vector <int> v = {1,10,5,8,7,6,4,3,2,9};

void swap(int &a, int &b);

int main(void){
	int min = 11, minIndex; // *max_element(v.begin(), v.end()) + 1
	for(int i=0;i<v.size();++i){
		for(int j=i;j<v.size();++j){
			if(v[j] < min){
				minIndex = j;
			}
		}
		swap(v[i], v[j]);
	}
}

void swap(int &a, int &b){
	int temp = a;
	a = b;
	b = a;
}
```