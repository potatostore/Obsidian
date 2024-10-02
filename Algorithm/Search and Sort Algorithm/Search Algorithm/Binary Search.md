이진 탐색은 기본적으로 정렬된 데이터 집합 내에서 특정 값을 찾기 위해 사용된다.

# 작동원리

정렬된 데이터 집합을 반으로 나눈 후 두 집합중 찾으려는 특정값이 해당하는 부분을 선택한다. 선택된 집합의 중간값이 특정값이면 값을 출력/반환을 하지만, 일치하지 않으면 다시 반으로 나누어 특정값이 해당하는 부분을 선택하는 방식을 반복한다.

이진탐색은 정렬된 데이터 집합 내에서 특정 값을 찾을 때 매우 효율적으로 작동을 하는데 반으로 계속 나누어 찾는 다는 점이 큰 특징이다.

# 시간복잡도 
- 이진 탐색의 시간복잡도는 O(log n)이며 배열의 크기가 커지면 커질수록 탐색 횟수는 매우 느리게 상승하기에 효율적이라고 볼 수 있다.

# 조건
- 데이터 집합이 정렬되어 있어야 한다.
- 선형 자료구조에서만 사용 가능하다.
- 중간 값이 존재하여 해집합의 크기를 반으로 줄일 수 있는 경우에 적합하다.

```c++ title='Ex'
#include <iostream>
using namespace std;

//return index
int binarySearch(vector<int>& arr, int target){
	int left = 0;
	int right = arr.size()-1;
	while(right >= left){
		if(arr[(left+right) / 2] == target) return (left+right)/2;
		else if(arr[left+right / 2] < target) left = (left+right)/2 + 1;
		else right = (left+right)/2;
	}
	return -1;
}

int main(void){
	vector<int> arr = {40,30,50,20,10};//정렬되지 않은 배열
	sort(arr.begin(), arr.end());//정렬시키기

	int n;
	cin >> n;
	cout << binarySearch(arr, n);
	return 0;
}
```
