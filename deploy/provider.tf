variable "do_token" {}
variable "ssh_fingerprint" {}
variable "pub_key" {}
variable "username" {}
variable "server_name" {}
variable "fullname" {}
variable "email" {}

provider "digitalocean" {
  token = var.do_token
}