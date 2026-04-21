## 1. 실시간 시스템의 기초 (Basic Concepts)
- **Real-Time System**: 작업의 결과물뿐만 아니라 그 결과가 도출되는 **시간(Timing)**이 시스템의 정식성(Correctness)에 영향을 주는 시스템.
- **Hard Real-Time**: 마감 시간(Deadline) 위반 시 시스템에 치명적인 실패(Catastrophic failure)가 발생하는 시스템.
- **Soft Real-Time**: 마감 시간을 어겨도 성능 저하는 있으나 시스템 전체가 실패하지는 않는 시스템.
- **Predictability (예측 가능성)**: 시스템이 정해진 시간 안에 작업을 완료할 수 있음을 미리 보장할 수 있는 성질.
## 2. 태스크 모델 (Task Model)
- **Periodic Task ($T_i$)**: 일정한 주기($p_i$)마다 반복적으로 발생하는 작업.
    - **Phase ($\phi_i$)**: 첫 번째 Job이 릴리즈되는 시점.
    - **Execution Time ($e_i$)**: 작업이 실행되는 데 걸리는 최대 시간.
    - **Relative Deadline ($D_i$)**: 작업 발생 시점부터 완료되어야 하는 시점까지의 시간 간격.
    - **Absolute Deadline ($d_i$)**: 실제 시스템 시간상의 마감 시점 ($d_i = r_i + D_i$).
- **Aperiodic Task**: 발생 시점이 정해져 있지 않으며(비주기적), 마감 시간이 없거나 유연한 태스크.
- **Sporadic Task**: 비주기적으로 발생하지만, 엄격한 마감 시간(Hard Deadline)을 가진 태스크.
## 3. 스케줄링 파라미터 (Scheduling Parameters)
- **Release Time ($r_i$)**: 작업이 실행될 준비가 되어 큐에 들어가는 시점.
- **Utilization ($U$)**: 프로세서 사용률. 단일 태스크 $u_i = e_i / p_i$이며, 전체 이용률 $U = \sum u_i$.
- **Hyperperiod ($H$)**: 모든 주기적 태스크의 주기의 최소공배수($\text{LCM}$)로, 전체 스케줄링 패턴이 반복되는 단위 시간.
- **Laxity (Slack Time)**: 여유 시간. (남은 마감 시간 - 남은 실행 시간). 이 값이 0이면 즉시 실행해야 함.
## 4. 스케줄링 알고리즘 (Scheduling Algorithms)
- **SJF (Shortest Job First)**: 실행 시간이 가장 짧은 작업 우선.
- **SRTF (Shortest Remaining Time First)**: 선점형 SJF. 남은 실행 시간이 가장 짧은 작업 우선.
- **EDF (Earliest Deadline First)**: 마감 시간이 가장 가까운 작업에 가장 높은 우선순위를 부여하는 동적 우선순위 방식.
- **LRT (Latest Release Time)**: 작업을 마감 시간부터 역방향(Backward)으로 배치하여 실행을 최대한 뒤로 미루는 방식.
- **LST (Least Slack Time)** : Laxity(여유 시간)을 통해 태스크의 여유시간이 가장 적은 태스크부터 실행
- **Effective Release Time / Deadline**: 선후 관계(Precedence)가 있을 때 이를 고려하여 조정한 실제 유효 시간.
## 5. 클록 기반 스케줄링 (Clock-Driven Scheduling)
- **Cyclic Schedule**: 정해진 시간표에 따라 반복적으로 실행되는 정적 스케줄링.
- **Frame ($f$)**: 타이머 인터럽트가 발생하는 최소 시간 단위.
- **Frame 제약 조건**:
    1. $f \geq \max(e_i)$: 프레임은 어떤 작업의 실행 시간보다도 커야 함 (작업 분할 방지).
    2. $H \pmod f = 0$: 하이퍼피리어드는 프레임 크기로 나누어떨어져야 함.
    3. $2f - \gcd(p_i, f) \leq D_i$: 작업이 마감 시간 안에 완료됨을 보장하기 위한 조건.

