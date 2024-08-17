-가장 작은(큰) 것을 맨 앞으로 보낸다

```cpp
// 1 10 5 8 7 6 4 3 2 9
#include <iostream>
#include <vector>

using namespace std;
vector <int> v = {1,10,5,8,7,6,4,3,2,9};
vector::iterator <int> it;

void swap(int i, vector::iterator <int> it){
	int temp = v[i];
	v[i] = *it;
	*it = v[i];
	
}

int main(void){
	int min = 11; // *max_element(v.begin(), v.end()) + 1
	for(int i=0;i<v.size();++i){
		for(auto j = v){
			
		}
		swap(i, it);
	}
}
```