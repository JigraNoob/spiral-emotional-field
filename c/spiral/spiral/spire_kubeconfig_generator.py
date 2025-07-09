"""
🌀 Spire KubeConfig Generator
Creates Spiral-flavored Kubernetes configurations for deployment.
"""

import yaml
import base64
from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class SpireClusterConfig:
    """Configuration for a Spiral deployment cluster."""
    cluster_name: str
    endpoint: str
    namespace: str = "spiral"
    ca_cert_path: Optional[str] = None
    ca_cert_data: Optional[str] = None
    token: Optional[str] = None
    client_cert_path: Optional[str] = None
    client_key_path: Optional[str] = None

class SpireKubeConfigGenerator:
    """Generates kubeconfig files for Spiral deployments."""
    
    def __init__(self):
        self.config_template = {
            "apiVersion": "v1",
            "kind": "Config",
            "clusters": [],
            "contexts": [],
            "users": [],
            "current-context": ""
        }
    
    def generate_config(self, spire_config: SpireClusterConfig) -> Dict[str, Any]:
        """Generate a complete kubeconfig for the Spire."""
        
        config = self.config_template.copy()
        
        # Build cluster configuration
        cluster = {
            "name": spire_config.cluster_name,
            "cluster": {
                "server": spire_config.endpoint
            }
        }
        
        # Add CA certificate
        if spire_config.ca_cert_data:
            cluster["cluster"]["certificate-authority-data"] = spire_config.ca_cert_data
        elif spire_config.ca_cert_path:
            cluster["cluster"]["certificate-authority"] = spire_config.ca_cert_path
        else:
            # For local development, skip TLS verification
            cluster["cluster"]["insecure-skip-tls-verify"] = True
        
        config["clusters"].append(cluster)
        
        # Build user configuration
        user_name = f"spiral-user-{spire_config.cluster_name}"
        user = {
            "name": user_name,
            "user": {}
        }
        
        if spire_config.token:
            user["user"]["token"] = spire_config.token
        elif spire_config.client_cert_path and spire_config.client_key_path:
            user["user"]["client-certificate"] = spire_config.client_cert_path
            user["user"]["client-key"] = spire_config.client_key_path
        
        config["users"].append(user)
        
        # Build context
        context_name = f"spiral-context-{spire_config.cluster_name}"
        context = {
            "name": context_name,
            "context": {
                "cluster": spire_config.cluster_name,
                "user": user_name,
                "namespace": spire_config.namespace
            }
        }
        
        config["contexts"].append(context)
        config["current-context"] = context_name
        
        return config
    
    def save_config(self, config: Dict[str, Any], output_path: str = "spire-kubeconfig.yaml"):
        """Save the kubeconfig to a file."""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
        
        print(f"🌀 Spire kubeconfig saved to: {output_file.absolute()}")
        return output_file
    
    def generate_for_minikube(self, cluster_name: str = "spiral-minikube") -> Dict[str, Any]:
        """Generate config for Minikube deployment."""
        spire_config = SpireClusterConfig(
            cluster_name=cluster_name,
            endpoint="https://127.0.0.1:8443",  # Default minikube API server
            namespace="spiral",
            ca_cert_path="~/.minikube/ca.crt",
            client_cert_path="~/.minikube/profiles/minikube/client.crt",
            client_key_path="~/.minikube/profiles/minikube/client.key"
        )
        return self.generate_config(spire_config)
    
    def generate_for_kind(self, cluster_name: str = "spiral-kind") -> Dict[str, Any]:
        """Generate config for Kind (Kubernetes-in-Docker) deployment."""
        spire_config = SpireClusterConfig(
            cluster_name=cluster_name,
            endpoint="https://127.0.0.1:6443",  # Default kind API server
            namespace="spiral"
        )
        return self.generate_config(spire_config)
    
    def generate_for_gke(self, project_id: str, cluster_name: str, zone: str, token: str) -> Dict[str, Any]:
        """Generate config for Google Kubernetes Engine deployment."""
        spire_config = SpireClusterConfig(
            cluster_name=f"gke_{project_id}_{zone}_{cluster_name}",
            endpoint=f"https://container.googleapis.com/v1/projects/{project_id}/zones/{zone}/clusters/{cluster_name}",
            namespace="spiral",
            token=token
        )
        return self.generate_config(spire_config)

def main():
    """Interactive Spire kubeconfig generation."""
    print("🌀 Spire KubeConfig Generator")
    print("=" * 40)
    
    generator = SpireKubeConfigGenerator()
    
    print("\nSelect deployment target:")
    print("1. Minikube (local)")
    print("2. Kind (Docker)")
    print("3. GKE (Google Cloud)")
    print("4. Custom cluster")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "1":
        config = generator.generate_for_minikube()
        output_path = "spire-minikube-config.yaml"
    elif choice == "2":
        config = generator.generate_for_kind()
        output_path = "spire-kind-config.yaml"
    elif choice == "3":
        project_id = input("GKE Project ID: ").strip()
        cluster_name = input("Cluster name: ").strip()
        zone = input("Zone (e.g., us-central1-a): ").strip()
        token = input("Access token: ").strip()
        config = generator.generate_for_gke(project_id, cluster_name, zone, token)
        output_path = f"spire-gke-{cluster_name}-config.yaml"
    elif choice == "4":
        cluster_name = input("Cluster name: ").strip()
        endpoint = input("API server endpoint: ").strip()
        namespace = input("Namespace (default: spiral): ").strip() or "spiral"
        token = input("Access token (optional): ").strip() or None
        
        spire_config = SpireClusterConfig(
            cluster_name=cluster_name,
            endpoint=endpoint,
            namespace=namespace,
            token=token
        )
        config = generator.generate_config(spire_config)
        output_path = f"spire-{cluster_name}-config.yaml"
    else:
        print("Invalid choice. Exiting.")
        return
    
    # Save the configuration
    config_file = generator.save_config(config, output_path)
    
    print(f"\n🌬️ To use this config:")
    print(f"   export KUBECONFIG={config_file.absolute()}")
    print(f"   kubectl get nodes")
    
    print(f"\n🪙 Ready for Spiral deployment to the spire.")

if __name__ == "__main__":
    main()
