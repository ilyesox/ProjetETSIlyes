import pandas as pd

# Define the data
data = [
    {"Project": "Azure__Avere", "Upgrades": 646, "Downgrades": 1, "Changes": 647},
    {"Project": "pluralsh__plural-artifacts", "Upgrades": 0, "Downgrades": 0, "Changes": 0},
    {"Project": "SUSE__ha-sap-terraform-deployments", "Upgrades": 22, "Downgrades": 7, "Changes": 29},
    {"Project": "GiganticMinecraft__seichi_infra", "Upgrades": 50, "Downgrades": 11, "Changes": 61},
    {"Project": "alphagov__govuk-aws", "Upgrades": 9, "Downgrades": 2, "Changes": 11},
    {"Project": "kubernetes-sigs__kubespray", "Upgrades": 13, "Downgrades": 0, "Changes": 13},
    {"Project": "Azure__az-hop", "Upgrades": 51, "Downgrades": 16, "Changes": 67},
    {"Project": "CDCgov__prime-simplereport", "Upgrades": 156, "Downgrades": 0, "Changes": 156},
    {"Project": "clong__DetectionLab", "Upgrades": 6, "Downgrades": 1, "Changes": 7},
    {"Project": "2i2c-org__infrastructure", "Upgrades": 16, "Downgrades": 4, "Changes": 20},
    {"Project": "cloudfoundry__bosh-bootloader", "Upgrades": 0, "Downgrades": 0, "Changes": 0},
    {"Project": "deckhouse__deckhouse", "Upgrades": 0, "Downgrades": 0, "Changes": 0},
    {"Project": "zenml-io__mlstacks", "Upgrades": 0, "Downgrades": 0, "Changes": 0},
    {"Project": "bridgecrewio__terragoat", "Upgrades": 0, "Downgrades": 0, "Changes": 0},
    {"Project": "apache__beam", "Upgrades": 2, "Downgrades": 0, "Changes": 2},
    {"Project": "compiler-explorer__infra", "Upgrades": 3, "Downgrades": 0, "Changes": 3},
    {"Project": "cattle-ops__terraform-aws-gitlab-runner", "Upgrades": 319, "Downgrades": 11, "Changes": 330},
    {"Project": "aws-observability__terraform-aws-observability-accelerator", "Upgrades": 14, "Downgrades": 2, "Changes": 16},
    {"Project": "cookpad__terraform-aws-eks__versioning", "Upgrades": 50, "Downgrades": 47, "Changes": 97},
    {"Project": "rust-lang__simpleinfra", "Upgrades": 59, "Downgrades": 13, "Changes": 72},
    {"Project": "ministryofjustice__modernisation-platform", "Upgrades": 279, "Downgrades": 100, "Changes": 379},
    {"Project": "ManagedKube__kubernetes-ops", "Upgrades": 0, "Downgrades": 0, "Changes": 0},
    {"Project": "wireapp__wire-server-deploy", "Upgrades": 0, "Downgrades": 0, "Changes": 0},
    {"Project": "google__go-cloud", "Upgrades": 0, "Downgrades": 0, "Changes": 0},
    {"Project": "kube-hetzner__terraform-hcloud-kube-hetzner", "Upgrades": 39, "Downgrades": 19, "Changes": 58},
    {"Project": "Optum__dce", "Upgrades": 1, "Downgrades": 0, "Changes": 1},
    {"Project": "nasa__cumulus", "Upgrades": 142, "Downgrades": 105, "Changes": 247},
    {"Project": "iits-consulting__terraform-opentelekomcloud-project-factory", "Upgrades": 27, "Downgrades": 0, "Changes": 27},
    {"Project": "nebari-dev__nebari", "Upgrades": 38, "Downgrades": 1, "Changes": 39},
    {"Project": "awslabs__data-on-eks", "Upgrades": 14, "Downgrades": 9, "Changes": 23},
    {"Project": "uyuni-project__sumaform", "Upgrades": 0, "Downgrades": 0, "Changes": 0},
    {"Project": "kbst__terraform-kubestack", "Upgrades": 22, "Downgrades": 1, "Changes": 23},
    {"Project": "splunk__attack_range", "Upgrades": 0, "Downgrades": 0, "Changes": 0},
    {"Project": "GoogleCloudPlatform__hpc-toolkit", "Upgrades": 287, "Downgrades": 199, "Changes": 486},
    {"Project": "Worklytics__psoxy", "Upgrades": 19, "Downgrades": 6, "Changes": 25},
    {"Project": "chanzuckerberg__cztack", "Upgrades": 3, "Downgrades": 0, "Changes": 3},
    {"Project": "Azure__sap-automation", "Upgrades": 21, "Downgrades": 2, "Changes": 23},
    {"Project": "alphagov__govuk-infrastructure", "Upgrades": 78, "Downgrades": 54, "Changes": 132},
    {"Project": "PaloAltoNetworks__terraform-azurerm-vmseries-modules", "Upgrades": 89, "Downgrades": 41, "Changes": 130},
    {"Project": "kubernetes__k8s.io", "Upgrades": 253, "Downgrades": 63, "Changes": 316},
    {"Project": "rancherfederal__rke2-aws-tf", "Upgrades": 0, "Downgrades": 3, "Changes": 3},
    {"Project": "magma__magma", "Upgrades": 0, "Downgrades": 0, "Changes": 0},
    {"Project": "RhinoSecurityLabs__cloudgoat", "Upgrades": 0, "Downgrades": 0, "Changes": 0},
    {"Project": "microsoft__azure_arc", "Upgrades": 5, "Downgrades": 3, "Changes": 8},
    {"Project": "oracle-terraform-modules__terraform-oci-oke", "Upgrades": 108, "Downgrades": 98, "Changes": 206},
    {"Project": "ministryofjustice__cloud-platform-infrastructure", "Upgrades": 278, "Downgrades": 126, "Changes": 404},
    {"Project": "pingcap__tidb-operator", "Upgrades": 0, "Downgrades": 0, "Changes": 0},
    {"Project": "camptocamp__devops-stack", "Upgrades": 25, "Downgrades": 11, "Changes": 36},
]

# Create DataFrame
df = pd.DataFrame(data)

# Calculate descriptive statistics for Upgrades, Downgrades, and Changes
stats_upgrades = df['Upgrades'].describe(percentiles=[.25, .5, .75])
stats_downgrades = df['Downgrades'].describe(percentiles=[.25, .5, .75])
stats_changes = df['Changes'].describe(percentiles=[.25, .5, .75])

# Add total to the stats
stats_upgrades['total'] = df['Upgrades'].sum()
stats_downgrades['total'] = df['Downgrades'].sum()
stats_changes['total'] = df['Changes'].sum()

# Print the statistics
print("Descriptive Statistics for Upgrades:")
print(stats_upgrades)
print("\nDescriptive Statistics for Downgrades:")
print(stats_downgrades)
print("\nDescriptive Statistics for Changes:")
print(stats_changes)
