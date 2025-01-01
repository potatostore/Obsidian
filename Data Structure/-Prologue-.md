
컴퓨터 과학에서 효율적인 접근 및 수정을 가능케 하는 자료의 조직, 관리, 저장 등을 자료구조라고 말한다.

쉽게 말해서 컴퓨터가 메모리에 접근을 용이하게 하거나 메모리의 수정을 편하게 하기 위해 자료를 체계적으로 관리하는 행위가 필요하고, 이를 다루는 학문이 자료구조라고 볼 수 있다.

아주 좋은 비유가 있어서 가지고 와봤다.

책장(메모리)에 수많은 책(데이터)을 넣기 위해서 무작위로 넣는 것은 추후에 책을 책장에서 꺼낼 때 비효율적으로 변한다. 따라서 종류별로 책을 정렬할 것인지, 페이지 수를 기준으로 넣을 것인지 등등 책장에 책을 넣기 위해 다양한 방식을 고안할 수 있고, 이것을 자료구조라고 비유할 수 있다. 

그렇게 책장에 책을 넣고, 특정한 책을 빠른 방법으로 찾기 위한 방법이 바로 알고리즘이다. 

그렇기에 알고리즘과 자료구조는 뗄래야 뗄 수 없는 조합인 것이다.

--- 

자료구조는 크게 *단순 자료구조* 와 *복잡 자료구조*로 나눌 수 있다.

단순 자료구조는 우리가 언어를 배우면서 자연스럽게 습득할 수 있는 자료형이다. 

int, char, float, double이 이에 해당하며, 언어별로 존재하는 자료형은 조금씩 다르다.

따라서 이 Data Structure폴더 내에서는 *복잡 자료구조*를 중점으로 다루어 볼 것이다.

---

*복잡 자료구조*는 Array, Lists, Files 세 가지로 나눌 수 있으며, 이 중 Lists는 나열 가능한가 불가능한가의 기준에 따라 선형(Linear), 비선형(Non-Linear)로 나뉠 수 있다.

선형 리스트는 stack, queue로 나뉘고, 비선형 리스트는 graph, tree로 나뉜다.

앞서 말한대로 자료구조에 따라 알고리즘이 바뀔 수 있는데 다음 표를 확인해 보자.

## Common Data Structure Operations

| Data Structure                                                                            | Time Complexity |             |             |             |             |             |             |             | Space Complexity |
| ----------------------------------------------------------------------------------------- | --------------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ---------------- |
|                                                                                           | Average         |             |             |             | Worst       |             |             |             | Worst            |
|                                                                                           | Access          | Search      | Insertion   | Deletion    | Access      | Search      | Insertion   | Deletion    |                  |
| [Array](http://en.wikipedia.org/wiki/Array_data_structure)                                | `Θ(1)`          | `Θ(n)`      | `Θ(n)`      | `Θ(n)`      | `O(1)`      | `O(n)`      | `O(n)`      | `O(n)`      | `O(n)`           |
| [Stack](http://en.wikipedia.org/wiki/Stack_(abstract_data_type))                          | `Θ(n)`          | `Θ(n)`      | `Θ(1)`      | `Θ(1)`      | `O(n)`      | `O(n)`      | `O(1)`      | `O(1)`      | `O(n)`           |
| [Queue](http://en.wikipedia.org/wiki/Queue_(abstract_data_type))                          | `Θ(n)`          | `Θ(n)`      | `Θ(1)`      | `Θ(1)`      | `O(n)`      | `O(n)`      | `O(1)`      | `O(1)`      | `O(n)`           |
| [Singly-Linked List](http://en.wikipedia.org/wiki/Singly_linked_list#Singly_linked_lists) | `Θ(n)`          | `Θ(n)`      | `Θ(1)`      | `Θ(1)`      | `O(n)`      | `O(n)`      | `O(1)`      | `O(1)`      | `O(n)`           |
| [Doubly-Linked List](http://en.wikipedia.org/wiki/Doubly_linked_list)                     | `Θ(n)`          | `Θ(n)`      | `Θ(1)`      | `Θ(1)`      | `O(n)`      | `O(n)`      | `O(1)`      | `O(1)`      | `O(n)`           |
| [Skip List](http://en.wikipedia.org/wiki/Skip_list)                                       | `Θ(log(n))`     | `Θ(log(n))` | `Θ(log(n))` | `Θ(log(n))` | `O(n)`      | `O(n)`      | `O(n)`      | `O(n)`      | `O(n log(n))`    |
| [Hash Table](http://en.wikipedia.org/wiki/Hash_table)                                     | `N/A`           | `Θ(1)`      | `Θ(1)`      | `Θ(1)`      | `N/A`       | `O(n)`      | `O(n)`      | `O(n)`      | `O(n)`           |
| [Binary Search Tree](http://en.wikipedia.org/wiki/Binary_search_tree)                     | `Θ(log(n))`     | `Θ(log(n))` | `Θ(log(n))` | `Θ(log(n))` | `O(n)`      | `O(n)`      | `O(n)`      | `O(n)`      | `O(n)`           |
| [Cartesian Tree](https://en.wikipedia.org/wiki/Cartesian_tree)                            | `N/A`           | `Θ(log(n))` | `Θ(log(n))` | `Θ(log(n))` | `N/A`       | `O(n)`      | `O(n)`      | `O(n)`      | `O(n)`           |
| [B-Tree](http://en.wikipedia.org/wiki/B_tree)                                             | `Θ(log(n))`     | `Θ(log(n))` | `Θ(log(n))` | `Θ(log(n))` | `O(log(n))` | `O(log(n))` | `O(log(n))` | `O(log(n))` | `O(n)`           |
| [Red-Black Tree](http://en.wikipedia.org/wiki/Red-black_tree)                             | `Θ(log(n))`     | `Θ(log(n))` | `Θ(log(n))` | `Θ(log(n))` | `O(log(n))` | `O(log(n))` | `O(log(n))` | `O(log(n))` | `O(n)`           |
| [Splay Tree](https://en.wikipedia.org/wiki/Splay_tree)                                    | `N/A`           | `Θ(log(n))` | `Θ(log(n))` | `Θ(log(n))` | `N/A`       | `O(log(n))` | `O(log(n))` | `O(log(n))` | `O(n)`           |
| [AVL Tree](http://en.wikipedia.org/wiki/AVL_tree)                                         | `Θ(log(n))`     | `Θ(log(n))` | `Θ(log(n))` | `Θ(log(n))` | `O(log(n))` | `O(log(n))` | `O(log(n))` | `O(log(n))` | `O(n)`           |
| [KD Tree](http://en.wikipedia.org/wiki/K-d_tree)                                          | `Θ(log(n))`     | `Θ(log(n))` | `Θ(log(n))` | `Θ(log(n))` | `O(n)`      | `O(n)`      | `O(n)`      | `O(n)`      | `O(n)`           |

* Big-O cheet sheet 사이트를 이용하면 한 눈에 파악할 수 있다.


