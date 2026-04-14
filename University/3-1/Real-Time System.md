release time + relative deadline = absolute deadline -> 잘 알아두기
$$P_i (주기)$$ 
4-tuple ($r_i, p_i, e_i, D_i$)



```mermaid
usecaseDiagram{
    actor "고객" as Customer
    
    package "쪽문 관리 시스템" {
        usecase "쪽문 수동 개폐" as UC1
        usecase "쪽문 개폐 로그 조회" as UC2
        usecase "쪽문 개폐 시간 설정" as UC3
    }
    
    Customer --> UC1
    Customer --> UC2
    Customer --> UC3
}
```
