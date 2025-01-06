
counting sort는 여태 배운 정렬 알고리즘과 다른 매커니즘으로 작동한다.

비교를 통해 배열을 정렬해 갔던 앞선 방식들과 다르게 counting sort는 비교하지 않고 숫자의 빈도를 확인해 이를 기반으로 정렬을 하는 알고리즘이다.

---

1. 범위 확인 : 최댓값, 최솟값을 확인하여 값의 범위를 확인한다.
2. 빈도 계산 : 숫자의 빈도를 계산해서 기록하는 배열(카운트 배열)에 저장한다.
3. 누적 빈도 계산 : 저장한 배열을 통해 값이 정렬되었을 때의 위치를 계산한다.
4. 출력 배열 생성 : result배열을 생성하여 카운트 배열을 바탕으로 원소를 집어넣는다.

---


```c++
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

// Counting Sort 구현
void countingSort(vector<int>& arr) {
    if (arr.empty()) return;

    // 배열의 최댓값, 최솟값 찾기
    int minVal = *min_element(arr.begin(), arr.end());
    int maxVal = *max_element(arr.begin(), arr.end());
    int range = maxVal - minVal + 1;

    // 카운팅 배열 생성
    vector<int> count(range, 0);

    // 각 요소의 빈도 계산
    for (int num : arr) {
        count[num - minVal]++;
    }

    // 입력 배열에 정렬된 값 저장
    int index = 0;
    for (int i = 0; i < range; ++i) {
        while (count[i] > 0) {
            arr[index++] = i + minVal;
            count[i]--;
        }
    }
}

int main() {
    vector<int> arr = {4, 2, 2, 8, 3, 3, 1};

    cout << "정렬 전: ";
    for (int num : arr) {
        cout << num << " ";
    }
    cout << endl;

    countingSort(arr);

    cout << "정렬 후: ";
    for (int num : arr) {
        cout << num << " ";
    }
    cout << endl;

    return 0;
}
```