```mermaid
---
config:
layout: dagre
---
flowchart TB
	subgraph Controller_Layer["Controller Layer"]
	UC["UserController"]
	EC["ManagerController"]
	PC["ProductController"]
	OC["OrderController"]
	CC["CartController"] 
end
  
subgraph Service_Layer["Service Layer"]
	US["UserService"]
	PS["ProductService"]
	OS["OrderService"]
end

subgraph DB["Database / Repository"]
	UserTable[("User Table")]
	ProdTable[("Product Table")]
	ManTable[("Manager Table")]
	LikeTable[("Like Table")]
	PreviousSearchTable[("PreviousSearch Table")]
	CartTable[("Cart Table")]
	ProblemOrderTable[("ProblemOrder Table")]
	RecentWatchingTable[("RecentWatching Table")]
	SystemQATable[("System Q&A Table")]
	ProductQATable[("Product Q&A Table")]
end

User(("고객")) -- signIn / signUp / findId / findPassword / editProfile / checkLikeProduct --> UC
User -- viewProducts / SearchProduct / addCart --> PC
User -- checkOrder / checkProblemOrder --> OC
SysManager(("시스템 관리자/System Manager")) -- manageOrders --> EC
SysManager -- addProduct / removeProduct --> PC
ProdManager(("상품 관리자/Product Manager")) -- addProduct / removeProduct / editProduct --> PC

UC --> US
EC --> US
PC --> PS
US --> UserTable
PS --> ProdTable

UserTable --> LikeTable & PreviousSearchTable & CartTable & ProblemOrderTable & RecentWatchingTable
ProdTable --> ProductQATable

```
  