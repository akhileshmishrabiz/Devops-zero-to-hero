output "network" {
  value       = google_compute_network.default.name
  description = "vpc name"
}
output "subnet" {
  value       = google_compute_subnetwork.default.name
  description = "subnet name"
}