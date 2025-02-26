초창기 웹 개발에서 진화된 업무로서 구조는 controller(요청분기), service(요청처리), repository(데이터 처리)있다.

``` mermaid
graph LR
	A1["USER"] --> A2["Controller"] <--> A3["Service"] <--> A4["Repository"] <--> A5[("DB")]
```

이러한 개발구조를 무조건 따르는 것은 아니지만, 대부분의 업계에선 가이드라인으로 세운다.

php가 대표적인 언어인데, 이전에 c를 이용한 gcc, perl 언어가 존재했지만, mySQL과 연동을 통해 대중화된 사례는 php가 대표적이기 때문이다.

절차진행 언어인 php는 데이터처리와 html조립을 번갈아가며 진행하는 구조를 가지기에 초기투자비용이 현저히 적지만, 유지보수에 사용되는 비용이 큰 만큼 점차 선택받는일이 줄어들었다.
또한 코드진행과 동시에 결과값을 미리 확인해볼 수 있었는데, 이는 데이터베이스와의 연동을 테스트하고 안정화하는 방법이 없기 때문에 단점이 부각되었다.

backend는 model1에서 model2로 진화되었는데, model2를 *MVC model*이라고 한다.

*MVC model*은 virtual machine을 사용하는 Java,C#과 같은 컴파일러 언어에서 사용이 되다가 점차 php,asp,jsp와 같은 스크립트 언어에서도 채택되어 사용되었다.

``` mermaid
flowchart LR
	A1["User"] --> B2["controller"]
	subgraph MVC model
	B2 --> A4["View"]
	B2 <--> A3["Model"] -.- A4
	end
	A4 --> A1
	A3 <--> A5[("DB")]
	
```
``` mermaid
graph LR
	A1["Controller"] <--> A2["Service"]
	subgraph Model
	A2 <--> A3["Repository"]
	end
```


위 model2(MVC model)은 요청분석을 통해 분기처리 후 데이터 처리 및 결과값을 생성하여 사용자가 요청한 json, xml등의 파일로 응답해주는 형식이다. 요청과 결과처리가 분리 되어 결과값 출력 및 테스트가 가능한 구조이다.

가장 큰 장점은 유저(호스트)의 수가 증가하거나, 테이블(DB)의 수가 증가하여도 내부 구조의 변동이 비교적 자유로워진다는 점이다. model1에서는 테이블 수가 증가함에 따라 repository가 증가하면, 그에 따른 결과값을 array형식으로 받는데, 이때 