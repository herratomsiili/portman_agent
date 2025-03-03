variable "allowed_ip_start" {
  description = "Allowed ip range start for firewall rule."
  type        = string
}

variable "allowed_ip_end" {
  description = "Allowed ip range end for firewall rule."
  type        = string
}

variable "allowed_ip_local" {
  description = "Allowed local ip for firewall rule."
  type        = string
}

variable "postgres_server_id" {
  description = "ID of the PostgreSQL Flexible Server"
  type        = string
}
