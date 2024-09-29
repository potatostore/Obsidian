- 옆에 있는 수와 비교를 통해 더 작은(큰) 값을 옮기는 것

```cpp title='오른차순 + 큰 값 옮기기' hl:11-15
	#include <iostream>
	#include <vector>
	
	using namespace std;
	
	vector <int> v = {1,10,5,8,7,6,4,3,2,9};
	
	void swap(int &a, int &b);
	
	int main(void){
		for(int i=0;i<v.size();++i){
			for(int j=0;j<v.size()-i-1;++j){
				if(v[j] > v[j+1]) swap(v[j], v[j+1]);
			}
		}
	
		for(auto i : v) cout << i << " ";
	
		return 0;
	}
	
	void swap(int&a, int &b){
		int temp = a;
		a = b;
		b = temp;
	}
```

버블 정렬같은 경우는 붙어있는 두 개의 원소를 대소비교하여 바꿔주면 되는데, 위 13줄의 대소를 반대로 하게 되면 내림차순으로 정렬 할 수 있다고 생각하면 안된다. 

```c++ title='line 11~15'
for(int i=0;i<s.sisze();++i){
	for(int j=i;j<s.size()-1;++j){
		if(v[j] < v[j+1]) swap(v[j], v[j+1]);
	}
}
```

11줄부터 15줄까지를 위 코드로 바꿔야 하는데, 이는 버블 정렬의 특성 때문이다.
오름차순으로 정렬을 하게 되면 바깥반복문을 한 번 돌릴때마다 배열의 맨 우측이 최댓값으로 생각되고 하나씩 줄여가며 대소비교를 하기 때문에 이 점을 유의하여 버블 정렬을 사용해야 한다.

특징
1. 시간복잡도는 [[Selection Sort]]와 동일하게 O(n^2)이다.
2. 유의점이 존재하기에 코테와 같은 바쁜 와중에 신경을 쓰며 하기에는 꼬일 수 있다.

*결론 : 시간복잡도가 길고, 컴파일이 꼬일 수 있다는 점에서 실전에서 절대 사용하지 않을 알고리즘인 것 같다.*
