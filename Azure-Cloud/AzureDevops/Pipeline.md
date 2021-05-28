# Azure Pipelines
## Sumário


- [Sumário](#sumário)


# CloudAzure

Foi realizada a utilização da azuredevops para subir a infra-estrutura do Kubernets

- Definida a branch main para realizar o triger
```
trigger:
- main
```
- Definida Imagem ubuntu-latest para executar o pipeline
```
pool:
  vmImage: 'ubuntu-latest'
```

- Declarada as variáveis

```
variables:
- name: DEV_ENVIRONMENT
  value: dev
```

- Utilizada o componente TerraformCLI@0 e TerraformInstaller@0 para executar os passos de criação do Kubernets

```
stages:
- stage: TerraformValidate 
  jobs:
    - job: TerraformValidateJob
      continueOnError: false
      steps:
      - task: PublishPipelineArtifact@1
        displayName: Publish Artifacts
        inputs:
          targetPath: '$(System.DefaultWorkingDirectory)/terraform-manifests'
          artifact: 'terraform-manifests-out'
          publishLocation: 'pipeline'
```
- Utilizando versão 0.13.5 do terraform via pipeline TerraformInstaller@0

```
      - task: TerraformInstaller@0
        displayName: Terraform Install
        inputs:
          terraformVersion: '0.13.5'
      - task: TerraformCLI@0
        displayName: Terraform Init
        inputs:
          command: 'init'
          workingDirectory: '$(System.DefaultWorkingDirectory)/terraform-manifests'
          backendType: 'azurerm'
          backendServiceArm: 'terraform-aks-azurerm-svc-con'
          backendAzureRmResourceGroupName: 'RG-Terraform'
          backendAzureRmStorageAccountName: 'terraformtoragepipeline'
          backendAzureRmContainerName: 'container'
          backendAzureRmKey: 'aks-base.tfstate'
          allowTelemetryCollection: false
```

- Validar todos os arquivo de terraform para identificar problemas de syntaxe

```
      - task: TerraformCLI@0
        displayName: Terraform Validate
        inputs:
          command: 'validate'
          workingDirectory: '$(System.DefaultWorkingDirectory)/terraform-manifests'
          allowTelemetryCollection: false
```
- Definido Estágio de cluster

```
- stage: DeployAKSClusters
  jobs:
    - deployment: DeployDevAKSCluster
      displayName: DeployDevAKSCluster
      pool:
        vmImage: 'ubuntu-latest'
      environment: $(DEV_ENVIRONMENT)      
      strategy:
        runOnce:
          deploy:
            steps:            

```
- Chave utilizada para criação do Cluster Kubernets, adicionada em variáveis seguras

```

            - task: DownloadSecureFile@1
              displayName: Download SSH Key
              name: sshkey
              inputs:
                secureFile: 'aks-terraform-devops-ssh-key-ububtu.pub'
```

- Executando Terraform Init utilizando os arquivos do terraform 

```
            - task: TerraformCLI@0
              displayName: Terraform Init
              inputs:
                command: 'init'
                workingDirectory: '$(Pipeline.Workspace)/terraform-manifests-out'
                backendType: 'azurerm'
                backendServiceArm: 'terraform-aks-azurerm-svc-con'
                backendAzureRmResourceGroupName: 'RG-Terraform'
                backendAzureRmStorageAccountName: 'terraformtoragepipeline'
                backendAzureRmContainerName: 'container'
                backendAzureRmKey: 'aks-$(DEV_ENVIRONMENT).tfstate'
                allowTelemetryCollection: false
```

- Executa o Terraform Plan para criar um plano de execução passando parametros de credenciais.

```
            - task: TerraformCLI@0
              displayName: Terraform Plan
              inputs:
                command: 'plan'
                workingDirectory: '$(Pipeline.Workspace)/terraform-manifests-out'
                environmentServiceName: 'terraform-aks-azurerm-svc-con'
                commandOptions: '-var ssh_public_key=$(sshkey.secureFilePath) -var environment=$(DEV_ENVIRONMENT) -out $(Pipeline.Workspace)/terraform-manifests-out/$(DEV_ENVIRONMENT)-$(Build.BuildId).out'
                allowTelemetryCollection: false
```

- Executa o Terraform apply para aplicar a criação do Kubernets

```

            - task: TerraformCLI@0
              displayName: Terraform Apply
              inputs:
                command: 'apply'
                workingDirectory: '$(Pipeline.Workspace)/terraform-manifests-out'
                environmentServiceName: 'terraform-aks-azurerm-svc-con'
                commandOptions: '$(Pipeline.Workspace)/terraform-manifests-out/$(DEV_ENVIRONMENT)-$(Build.BuildId).out'
                allowTelemetryCollection: false
```             