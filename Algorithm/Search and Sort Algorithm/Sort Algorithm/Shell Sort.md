- 일정 간격만큼 떨어져 있는 원소 두 개를 비교하고, 정렬해낸다.

말그대로 *gap*을 설정하고(보통 n = arr/2), gap만큼 떨어져 있는 원소 두 개의 대소 관계를 비교하여 자리를 바꾸는 형식이다.

```c++
#include <iostream>
#include <vector>
using namespace std;

// Shell Sort 구현
void shellSort(vector<int>& arr) {
    int n = arr.size();

    // 간격 설정
    for (int gap = n / 2; gap > 0; gap /= 2) {
        // 삽입 정렬 수행
        for (int i = gap; i < n; ++i) {
            int temp = arr[i];
            int j;
            for (j = i; j >= gap && arr[j - gap] > temp; j -= gap) {
                arr[j] = arr[j - gap];
            }
            arr[j] = temp;
        }
    }
}

int main() {
    vector<int> arr = {23, 12, 1, 8, 34, 54, 2, 3};
    
    cout << "정렬 전: ";
    for (int num : arr) {
        cout << num << " ";
    }
    cout << endl;
    
    shellSort(arr);

    cout << "정렬 후: ";
    for (int num : arr) {
        cout << num << " ";
    }
    cout << endl;

    return 0;
}
```


shell sort의 구현을 자세히 보면, 