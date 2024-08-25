  locals {
    layer_definitions = [
      {
        "identifier" : "layer1",
        "description" : "Contains some python packages",
        "path" : "layers/layer1",
        "compatible_runtimes" : ["python3.8", "python3.9", "python3.10", "python3.11"]
      },
      {
        "identifier" : "layer2",
        "description" : "Contains some python packages",
        "path" : "layers/layer2",
        "compatible_runtimes" : ["python3.8", "python3.9", "python3.10", "python3.11"]
      },
    
    ]

  # Map of layers info for the layers need to be build with this Terraform -> {layer_identifier:{layer_definitions }}
  layers_info = { for i in local.layer_definitions : i.identifier => i }
}
#   # List of layers names
#   layer_names = [for i in local.layer_definitions : i.identifier]

#   # Accounts that should have permission on layer version
#   allowed_accounts = ["AWS_ACCOUNT_ID_1", "AWS_ACCOUNT_ID_2"]

#   # Mapping layers -> aws accounts for permission on layer version
#   layers_to_accounts = flatten([for layer in local.layer_names : [for account in local.allowed_accounts : { id = "${layer}-${account}", layer = layer, account = account }]])
  
#   # Map to be used by for_each loop for resource
#   layers_to_accounts_map = { for item in local.layers_to_accounts : item.id => item }
# }
