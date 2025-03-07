# **Portman Agent - Azure Deployment and Usage Guide** 🚀  

This repository **Portman Agent** contains **Terraform configurations and GitHub Actions workflows** for provisioning and managing infrastructure on Azure, including:  
✅ **Azure Function App with http-trigger launching Portman function**  
✅ **PostgreSQL Database (Azure Database for PostgreSQL flexible server)**  
✅ **Networking and Security Rules**  
✅ **Application Insights & Monitoring**  

---

## **📌 Local Deployment Instructions**  

### **📌 Prerequisites**
Before deploying **locally**, ensure you have:

✅ **Terraform Installed**: [Download Terraform](https://developer.hashicorp.com/terraform/downloads)  
✅ **Azure CLI Installed**: [Download Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)  
✅ **Logged into Azure**:
```bash
az login
```
✅ **Backend Storage for Terraform State** (Azure Storage Account with blob container)

### **1️⃣ Select Environment**  
#### **🔹 Choose Environment (`development`, `testing`, `production`)**  
```bash
cd environments/<environment>
```

### **2️⃣ Define Azure storage for storing Terraform state and Set Up Terraform**  
There are defaults defined (`storage_account_name`, `resource_group_name`, `container_name`) for saving Terraform state in Azure in `backend.tf`. Set these according to your Azure account. Resource group and storage account can be different than used in `terraform plan` step.

Then initialize Terraform.
```bash
terraform init -upgrade
```

### **3️⃣ Create Terraform Deployment Plan for Infrastructure**  
```bash
terraform plan -var-file=terraform.tfvars \
  -var="resource_group_name=<resource_group_name>" \
  -var="naming_prefix=<naming_prefix>" \
  -var="storage_account_name=<storage_account_name>" \
  -var="admin_password=<postgres_admin_password>" -out=main.tfplan
```

### **4️⃣ Deploy Infrastructure**  
```bash
terraform apply main.tfplan
```
✅ **Terraform provisions resources for the selected environment.**  

---

### **📌 Destroy Infrastructure Locally**  
**To safely destroy all resources:**  
```bash
terraform destroy -var-file=terraform.tfvars \
  -var="resource_group_name=<resource_group_name>" \
  -var="naming_prefix=<naming_prefix>" \
  -var="storage_account_name=<storage_account_name>" \
  -var="admin_password=<postgres_admin_password>" -auto-approve
```
✅ **Destroys all resources for the selected environment.**  

---

## **📌 Deploy via GitHub Actions**  

### **📌 Prerequisites**
Before deploying via **GitHub Actions**, ensure you have:  
✅ **Existing Azure Resource Group in which you want to deploy Azure insfrastructure**  
✅ **Azure User-assigned Managed Identity with Federated GitHub Credentials**  
- Defined in the same Azure resource group
- Instructions in [SiiliHub](https://siilihub.atlassian.net/wiki/spaces/SW/pages/4166254596/Azure+CI+CD+authentication#Usage-with-Github-environment)

✅ **GitHub Actions Secrets/Variables Configured** (For automated deployment)  
✅ **Backend Storage for Terraform State** (Azure Storage Account with blob container)  

### **1️⃣ Set Up GitHub Environment Secrets**  
Go to **GitHub Repository → Settings → Secrets & Variables → Actions** and add/set these for desired environment (`development`, `testing`, `production`):  

| Secret Name | Description |
|------------|-------------|
| **`AZURE_CLIENT_ID`** | Azure Client ID from your User-assigned Managed Identity |
| **`AZURE_TENANT_ID`** | Azure Tenant ID from your User-assigned Managed Identity |
| **`AZURE_SUBSCRIPTION_ID`** | Azure Subscription ID of your Azure account |
| **`BACKEND_RESOURCE_GROUP`** | Resource Group for Terraform Backend |
| **`BACKEND_STORAGE_ACCOUNT`** | Azure Storage Account for Terraform State |
| **`BACKEND_CONTAINER_NAME`** | Azure Blob Container for Terraform State |
| **`DB_HOST`** | PostgreSQL Server Host |
| **`DB_PASSWORD`** | PostgreSQL Admin Password |

| Variable Name | Description |
|------------|-------------|
| **`AZURE_FUNCTIONAPP_NAME`** | Name of the Azure Function App service |
| **`AZURE_RESOURCE_GROUP`** | Resource Group for Azure resources |
| **`NAMING_PREFIX`** | Naming prefix for Azure resources |

✅ **GitHub Actions will securely use these secrets/vars during deployment.**  

---

### **2️⃣ Deploy Infrastructure via GitHub Actions**  
#### **🔹 Automatic Deployment (Pull Request to `main`)**
- **Terraform Deployment workflow is launched**
- **Changes made in Azure infrastructure can be verified from `Terraform Plan` job**
- **Once the Pull Request is merged, the `Terraform Apply` job is automatically launched and changes deployed to Azure**

✅ **GitHub Actions automatically deploys the infrastructure.**  

---

### **3️⃣ Manually Deploy Specific Environments**
#### **🔹 Run Workflow from GitHub Actions UI**  
- **Go to GitHub Actions → Terraform Deployment**  
- **Click "Run Workflow"**  
- **Select Branch (`develop`, `test`, `main`)**  
- **Select Deployment Environment (`development`, `testing`, `production`)**  
- **Click "Run workflow"**  

✅ **Terraform will now deploy the selected environment.**  

---
### **📌 Destroy Infrastructure via GitHub Actions**  
Destroying infrastructure needs manual approval on created GitHub Issue.  

**To destroy resources manually from GitHub Actions:**  
- **Go to GitHub Actions → Terraform Destroy**  
- **Click "Run Workflow"**  
- **Select Branch (`develop`, `test`, `main`)**  
- **Select Deployment Environment (`development`, `testing`, `production`)**  
- **Click "Run workflow"**  
- **Review the plan in GitHub Actions logs** 
- **Go to GitHub issues and select the issue regarding this destroy deployment**  
- **Follow the instructions on issue and either approve or decline the destroyment**  
- **If approved, the "Terraform Apply Destroy" job will be launched automatically**  

✅ **Prevents accidental resource deletion.**  

---

## **📌 Usage**
**The Portman Agent function URL can be found from:**  
- **Azure Portal -> Function App -> Functions -> PortmanHttpTrigger**  
- **GitHub Actions Deployment log**  

**Invoke the Portman Agent function:**  
- **Use the function URL with `code` parameter**
- **Define trackable vessels with `imo` parameter (optional)**  

**Query `voayges` and `arrivals` from Postgres DB:**  
- **Use the GitHub Environment secret value `DB_HOST` as a Postgres DB host**  
- **Use the GitHub Environment secret value `DB_USER` as a Postgres DB user**  
- **Use the GitHub Environment secret value `DB_PASSWORD` or the admin password defined in local deployment process as a Postgres DB password**  

---

## **📌 Troubleshooting**
| Issue | Solution |
|------|---------|
| **Terraform state locked** | Run `terraform force-unlock <LOCK_ID>` |
| **CORS settings not applied** | Check with `az functionapp cors show` |
| **Deployment failed in GitHub Actions** | Go to **Actions → Terraform Deployment → Logs** |
| **Database connection refused** | Ensure firewall rules allow your IP (`az postgres flexible-server firewall-rule create`) |
