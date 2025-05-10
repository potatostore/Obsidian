
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
Google Cloud Shell is a virtual machine that is loaded with development tools. It means Providing command line access to the virtual machine instance in terminal window that opens in the GCP console. It is small compute virtual machine that running on linux operate system.

기존의 서비스를 자신의 서버나 데이터베이스에 이식을 하는 행위는 의존성을 개발자 본인이 책임지기에 복제에 큰 문제가 발생하지 않음(개발에 어려움은 있지만 책임의 문제가 크게 발생하지 않는다는 의미). 하지만 Cloud serviecs를 사용하는 경우 이러한 문제를 본인이 책임지는 것이 아닌 서비스 제공자가 관리하기 때문에 책임의 문제를 클라우드 서비스를 통해 해결하는 방법을 알려줌.
(fully managed services를 강조)

1. Configure Cloud Shell to run a multi-part Java application locally.
    
2. Use Apache Maven to launch Java applications in Cloud Shell.
    
3. Use `curl` and the Cloud Shell web preview to test connectivity to web applications running locally in Cloud Shell.