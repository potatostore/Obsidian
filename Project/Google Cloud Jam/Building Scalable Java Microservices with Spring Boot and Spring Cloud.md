
Google cloud servieces provide options to developers for solution architecture.

1.  Cloud Function : compute and hosting services that completely serverless execution environment(Faas)
2.  App Engine : Paas
3.  Google  Kubernetes Engine : Caas
4. Compute Engine : Iaas
5. Cloud Run : serverless managed compute platform that lets you run stateless containers by using web Pub/Sub events

At first, we'll work on demo application or compute engine virtual machine instances

Later, For deploying refiguration and repackage application, we'll work app engine and google kubernetes engine.

During the lab, For storage datas, we'll use Cloud SQL which can comprehense your data contorl avility and set data auto manager.

---

# 0. Dictionary

- Pub/Sub : 
# 1. Spring boot

Spring boot is Spring Framework designed to simplify the bootstrapping and development of stand-alone. 

It provide quick-start and Spring flatform third-party library.

https://github.com/GoogleCloudPlatform/spring-cloud-gcp

# 2. Bootstrapping Frontend and Backend

Google provides how to build demo application for using Google cloud service(App Engine, Compute Engine...)

#### Cloud Shell
 It means Providing command line access to the virtual machine instance in terminal window that opens in the GCP console. It is small compute virtual machine that running on linux operate system.

기존의 서비스를 자신의 서버나 데이터베이스에 이식을 하는 행위는 의존성을 개발자 본인이 책임지기에 복제에 큰 문제가 발생하지 않음. 하지만 Cloud serviecs를 사용하는 경우 이러한 문제를 본인이 책임지는 것이 아닌 서비스 제공자가 관리하기 때문에 

