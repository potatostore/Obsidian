이름에서 예상할 수 있던 것처럼 피보나치 수열을 사용하여 탐색을 하는 알고리즘이다.
이진 탐색과 유사하지만, Fibonacci Search는 정렬된 데이터 집합을 피보나치 비율에 기반하여 그룹화한 후 목표값을 찾는 것이 특징이다.

# 작동원리

- 피보나치 수열의 인덱스를 사용하여 배열을 세 구역으로 나눈다.
- 탐색 범위를 좁힐 때 피보나치 비율을 사용하여 좁힌다.

설명만으로는 매우 이해가 안된다.
먼저 피보나치 비율로 데이터 집합을 그룹화 하는 것이 탐색을 효율적으로 하는 것과 무슨 연관이 있는지 상상이 안되기 때문이다. 

1. 피보나치 비율을 이용하여 배열을 분해한 후
2. 배열의 길이와 가장 가까운 피보나치 수를 찾는다.
3. 피보나치 인덱스를 사용해 배열을 세 구간으로 나눈다.
4. 찾고자 하는 값이 현재 피보나치 인덱스보다 큰지, 작은지 대소비교후 범위를 조정한다.
5. 위 과정을 반복하며 값을 찾는다.

친근하지 않은 탐색방법이라서 그런지 이해가 아직 잘 되지 않는다. 시간복잡도 학습 후 예제를 통해 알아보자.

# 시간복잡도

- [[Algorithm/Search and Sort Algorithm/Search Algorithm/Binary Search|Binary Search]] 와 동일하게 O(log n)이다.

# 예시

arr[] = [10,22,35,40,45,50,80,82,85,90,100]에서 85를 찾는다고 가정을 하자.

1. 배열의 크기(n = 11)에 가장 가까운 피보나치 수를 찾는다.
2. F(k) = 13, 이때 배열의 크기보다 큰 가장 가까운 피보나치 수를 찾아야 한다.
3. index = min(offset + F(k-2), n-1)을 통해 인덱스를 구한다.
	* 초기 offset = -1, index = min(-1+5, 10) = 4
4. arr[4] = 45는 target = 85보다 작으므로 offset = 4, F(k-1) = F(k), F(k-2) = F(k-1)로 설정한다.
	- F(k) = 13이였으므로 F(k) = 8, F(k-1) = 5가 된다.(F(k-2) = 3)
5. 반복


이를 코드로 구현해보면

```c++ title='FibonacciSearch Ex'
#include <iostream>
using namespace std;
#define t 10; //testcase

//Fibonacci Search
bool fibonacciSearch(int arr[], int target){
	int arrsize = sizeof(arr) / 4;
	int offset = -1;
	int fstfib = 0, sndfib = 1, thdfib = fstfib + sndfib;

	//배열의 크기보다 크면서 가장 가까운 피보나치 수 찾기
	while(arrsize > thdfib){
		fstfib = sndfib;
		sndfib = thdfib;
		thdfib = fstfib + sndfib;
	}

	while(thdfib != 0){
		int index = min(offset + fstfib, arrsize);
		if(arr[index] == target) return true;
		else if(arr[index] < target)
	}
}

int main(void){
	int arr[t];
	int target;
	
	for(int i=0;i<t;i++) cin >> arr[i];
	cin >> target;

	cout << "Is target in array? : " << fibonacciSearch(arr, target);

	return 0;
}
```


