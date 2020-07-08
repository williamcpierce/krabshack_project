resource "digitalocean_droplet" "personal-site" {
  image = "ubuntu-18-04-x64"
  name = var.server_name
  region = "nyc3"
  size = "s-1vcpu-1gb"
  monitoring = true
  ssh_keys = [
    var.ssh_fingerprint
  ]
  user_data = templatefile(
    "cloud-config.yaml", {
      username = var.username,
      pub_key = var.pub_key,
      fullname = var.fullname,
      email = var.email
    }
  )
}