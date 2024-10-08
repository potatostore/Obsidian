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

```c++ title='Ex : 반복문을 통해 이진 탐색 후 index 반환하기'
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

출력 시 index값이 정확하게 출력되는 것을 확인 할 수 있다.

여기서 더 나아가 데이터 집합에 찾으려는 값이 여러 개 존재한다면 어떻게 해야 할까?

간단하다.

정렬 후 이진 탐색을 여러 번 돌리며 컨테이너 내에 원소를 찾을 경우 인덱스값을 남긴 뒤 지우고, 없을 경우 남긴 인덱스값들을 출력해주면 된다.

위와 같이 반복문을 통해 만들 수 있지만, 재귀 함수를 통해서도 만들 수 있다. 
재귀 함수를 통해 이진탐색을 하는 방법은 지양하는 편인데 매개변수에 left, right값을 넣어야 하고, 
이는 [[Clean Code]]에 위배되는 행동이라고 생각한다.

# 장단점 
- 장점 : 
	- 효율적이다.
	- 정렬된 데이터에 사용되면 매우 빠르다. 위와 같은 sort()함수를 사용하면 O(log n) + O(log n)(C++ STL sort()는 개편된 퀵정렬을 사용하기에 이와 같은 시간복잡도를 갖는다)의 시간복잡도를 확인할 수 있다.
- 단점 : 
	- 정렬된 데이터가 필요하다.
	- 동적 데이터에 효율적이지 못하다. 삽입/삭제가 빈번이 일어날 경우 비효율적으로 작동한다.

왜 동적 데이터에 대해 효율적이지 못할까? 이는 데이터 삽입 및 삭제가 일어날 때, 정렬 상태가 깨지거나, 데이터 재구성 비용이 발생하기 때문이다.

위에서 보여준 방식대로 비정렬된 배열을 정렬하기 위해 재구성 비용이 발생하였다.
또한 이진 탐색 도중에 삽입/삭제가 발생할 경우 원하는 값을 얻지 못할 가능성도 생긴다는 얘기다.

내가 생각하기에 이진 탐색은 꽤나 효율적인 탐색 알고리즘이라고 생각이 든다. 그렇기에 만약 내가 동적 데이터에 대해 이진 탐색을 하고 싶으면 위에 우려되는 사항을 무마 시키면 된다는 생각도 들었다.

	정렬이 깨진다 -> 삭제 시 자동으로 사이즈가 조절되는 컨테이너를 사용하고, 삽입 시 삽입 정렬을 통해 정렬된 배열의 상태를 유지한다.

재구성 비용이 발생한다는 점에서는 보완점을 생각하지 못했지만, 위와 같은 정렬 유지를 하는 것만으로도 왠만한 비선형 자료구조 탐색 알고리즘과 시간복잡도 면에서는 우위를 점하지 않을까 라는 생각을 해보았다.