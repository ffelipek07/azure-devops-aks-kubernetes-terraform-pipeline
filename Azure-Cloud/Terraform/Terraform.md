# Terraform
## Sumário


- [Sumário](#sumário)



# Terraform

Foi realizada a utilização do Kubernets para subir a infra-estrutura do Kubernets

- Estrutura básica do Terraform
```
01 - main.tf
```         
- Definicao das variaveis
```
02 - variables.tf
```
- Definicao do grupo de recursos
```
03 - resource-group.tf
```
- Definicao do Datasource Azure AKS
```
04 - aks-versions-datasource.tf
```    
- Definicao recurso log analytics
```
05-log-analytics-workspace
```    
- Definicao recurso AD Azure
```
06-aks-administrators-azure-ad.tf 
```    
- Definicao do Cluster AKS
```
07 - aks-cluster.tf 
```    
- Definicao dos outputs
```
08 - outputs.tf 
```    
- Definicao dos node linux (Não utilizado)
```
09 - aks-cluster-linux-user-nodepools.tf 
```
- Definicao dos node windows (Não utilizado)
```
10 - aks-cluster-windows-user-nodepools.tf 
```  