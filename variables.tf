variable "name_prefix" {
  default     = "therranen-portman"
  description = "Prefix of the resource name."
}

variable "location" {
  default     = "northeurope"
  description = "Location of the resource."
}

variable "allowed_ip_start" {
  default     = "88.148.163.0"
  description = "Allowed ip range start for firewall rule."
}

variable "allowed_ip_end" {
  default     = "88.148.163.255"
  description = "Allowed ip range end for firewall rule."
}

variable "admin_password" {
  description = "PostgreSQL Admin Password"
  type        = string
  sensitive   = true
}