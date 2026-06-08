OSI에서 정의한 TP(Transport Protocol)는 5개의 서비스로 분류한다.



클래스 0 - 기본 기능

클래스 1 - 기본 오류 복구 기능

클래스 2 - 멀티플렉싱 기능

클래스 3 - 오류 복구, 멀티플렉싱

클래스 4 - 오류 검출 및 복구 , 멀티플렉싱



**OSI TP의 서비스 프리미티브**

TP가 제공하는 전송 서비스에는 연결형과 비연결형이 있다.



**-연결형**

T-CONNECT / DISCONNECT를 사용해 연결 설정과 해제를 하고

T-DATA / T-EXPEDITED-DATA를 사용해 일반 데이터와 긴급 데이터를 구분한다.

전송 계층의 TP는 전송 오류가 없는 서비스를 제공하기에 긍정 응답이나 부정 응답은 정의하지 않는다.



**-비연결형**

연결 설정과 해제가 불필요하기에 데이터 전송을 위한 T-UNITDATA만 존재한다.



**-연결 설정 프리미티브 흐름**

연결 설정

\-**T-CONNECT.request-> / T-CONNECT.indication**

**T-CONNECT.confirm / <-T-CONNECT.response-**

데이터 전송

**-T-DATA.request-> / T-DATA.indication**

연결 해제

**-T-DISCONNECT.request-> / T-DISCONNECT.inidication**

