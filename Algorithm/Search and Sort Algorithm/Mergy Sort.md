- 데이터를 반으로 나눈 후 나중에 합쳐서 정렬을 한다

```c++
#include <iostream>  
#include <vector>  
#include <cmath>  
  
using namespace std;  
  
int input[8] = {7,6,5,8,3,5,9,1};  
int sorted[8];  
  
void merge(int a[], int m, int middle, int n) {  
    int i = m;  
    int j = middle+1;  
    int k = m;  
    while(i <= middle && j <= n) {  
        if(a[i] <= a[j]) {  
            sorted[k] = a[i];  
            i++;  
        }  
        else {  
            sorted[k] = a[j];  
            j++;  
        }  
        k++;  
    }  
    if(i > middle) {  
        for(int l = j; l <= n; l++, k++) {  
            sorted[k] = a[l];  
        }  
    }  
    else {  
        for(int l = i; l <= middle; l++, k++) {  
            sorted[k] = a[l];  
        }  
    }  
    for(int l = 0; l <= n; l++) {  
        a[l] = sorted[l];  
    }  
}  
  
void mergeSort(int a[], int left, int right) {  
    if(left < right) {  
        int middle = (left + right) / 2;  
        mergeSort(a, left, middle);  
        mergeSort(a, middle + 1, right);  
        merge(a, left, middle, right);  
    }  
}  
  
int main() {  
    mergeSort(input, 0, sizeof(input)/4-1);  
    for(auto i : input) {  
        cout << i << " ";  
    }  
    return 0;  
}
```

상당히 까다로운 알고리즘이였던 이유는 배열을 몇 개 설정할지 감이 안잡히기 때문이다. 
배열을 3개를 잡기에는 복잡하고, 1개의 배열 내에 인덱스를 쪼개서 가져 가자니 이것대로 더 복잡하게 코드를 짤 것 같았기 때문이다. 어쩔 수 없이 답안을 조금씩 보며 답을 얻게 되었는데, 기존에 쪼개 놓은 배열 하나와 그걸 정렬해서 넣을 배열 하나, 총 두 개를 통해 병합정렬을 수행할 수 있다는 것을 알았다.

병합정렬은 상당히 좋은 알고리즘으로 선택이 되는데, 이진탐색처럼 반으로 쪼개고 또 쪼개 최종적으로 자신이 원하는 값을 얻어가는 과정이 있기 때문이라고 생각한다.

특징
1. 시간복잡도 O(nlogn)
2. 퀵정렬은 O(logn)이지만, 특정 상황(정렬이 되어있는 상황)에는 O(n^2)까지 걸리 수 있는데 반해 병합 정렬은 일정하게 O(nlogn)을 지원하기에 꽤나 좋다.

*결론 : 퀵정렬이 사용하기 꺼려질 때 차선책으로 사용할 수 있는 정렬방식으로 생각할 수 있을 것 같다.*