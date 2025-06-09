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


shell sort의 구현을 자세히 보면, 이중 반복문 중 내부 반복문의 조건이 상당히 특이하다는 것을 알 수 있다.
하지만 복잡하게 생각할 필요 없이 직역하면
j >= gap은 j-=gap을 시행했을때, arr을 가르킬 수 있는 범위내에 있는지 확인하는 조건이고, 
arr[j-gap] > temp는 대소비교를 한 후, 더 클 경우 swap을 진행한다. 

이때 swap을 진행할 경우 한쪽 값만 입력이 되므로, 앞에 temp = arr[i]를 통해 값을 미리 저장해두고, 맨 마지막에 값이 변환되는 것을 알 수 있다.

특이하게 shell sort를 진행하게 되면 반복문 한 사이클에 2개 이상의 원소를 정렬할 수 있는데, gap=2이고, 위와 같이 정렬문을 돌렸을때, [1,3,5]번째 원소들의 정렬을 한번에 이뤄낼 수 있다는 점이다.

시간복잡도는 

최선 : O(n log n)
평균 : O(n^3/2 ~ n^7/6)
최악 : O(n^2)

이 된다.

삽입 정렬의 향상된 버전이라고 생각하면 간편하지만, 시간복잡도가 높다는 점과 안정성이 떨어진다는 면에서 사용하기 어렵다는 평가다.

하지만 추가 메모리의 사용이 거의 없고, 간단한 구현 덕분에 인베디드 시스템과 같은 저메모리로 높은 효율을 요구하는 곳에서는 쓰일만 하다.