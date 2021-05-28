# k8s
## Sumário


- [Sumário](#sumário)


# Kubernets

- Para conectar no cluster

```
az aks get-credentials --resource-group terraform-aks-dev  --name terraform-aks-dev-cluster --admin
```

Foi realizada a utilização do deployment, secrets e hpa 

- Para criar o name space de dev e production

- Criação dos Namespace
```
kubectl create namespace dev
kubectl create namespace production
```
- Aplicar o pods nos namespaces dev

```
kubectl apply -f kube-manifests/Apps/ --namespace dev 
kubectl apply -f kube-manifests/hpa-manifest/ --namespace dev 
```
- Aplicar o pods nos namespaces production

```
kubectl apply -f kube-manifests/Apps/ --namespace production 
kubectl apply -f kube-manifests/hpa-manifest/ --namespace production
```








