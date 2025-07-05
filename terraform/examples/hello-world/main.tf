# main.tf

# This block defines the Terraform version constraints and required providers.
# The `hashicorp/local` provider is used here to interact with the local filesystem.
terraform {
  required_providers {
    local = {
      source = "hashicorp/local"
      version = "~> 2.0" # Use a compatible version of the local provider
    }
  }
}

# This resource block creates a local file on your system.
# It's a simple way to demonstrate Terraform's ability to create resources
# without needing cloud provider credentials.
resource "local_file" "hello_world_file" {
  # The filename where the content will be written.
  # It will be created in the directory where you run 'terraform apply'.
  filename = "hello_world.txt"

  # The content to be written into the file.
  # This is our "Hello, World!" message.
  content  = "Hello, World from Terraform!"

  # Optional: Set file permissions (e.g., 0644 for read/write by owner, read-only by others)
  file_permission = "0644"
}

# This output block defines a value that will be displayed after Terraform applies the configuration.
# It's useful for showing information about the created resources.
output "file_path" {
  # The value to output, which is the absolute path of the created file.
  value = local_file.hello_world_file.id
  # A descriptive message for the output.
  description = "The path to the 'Hello, World' file created by Terraform."
}

output "file_content" {
  # The content of the file that was written.
  value = local_file.hello_world_file.content
  # A descriptive message for the output.
  description = "The content of the 'Hello, World' file."
}
