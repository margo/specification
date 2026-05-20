#!/usr/bin/env bash

TMP=$(mktemp)
trap 'rm -f "$TMP"' EXIT
set -eu

ROOT_DIR="$(git rev-parse --show-toplevel)"
TGT_DIR="${ROOT_DIR}/spec/generated/diagrams"
KROKI="https://kroki.io/plantuml"

if command -v poetry &>/dev/null; then
  RUN="poetry run"
else
  for cmd in linkml curl; do
    command -v "$cmd" &>/dev/null || { echo "Missing: $cmd"; exit 1; }
  done
  RUN=""
fi

mkdir -p "$TGT_DIR"

# Holistic class diagram
$RUN linkml generate plantuml \
  "${ROOT_DIR}/spec/data-model/margo.linkml.yaml" \
  | sed "s/@enduml/DeploymentAnnotations ..> ApplicationDescription\n@enduml/" \
  | sed "s/@enduml/DeploymentStatusManifest ..> ApplicationDeployment\n@enduml/" \
  | sed "s/@enduml/DesiredStateManifest ..> ApplicationDeployment\n@enduml/" \
  > "$TMP"
curl -sH "Content-Type: text/plain" --data-binary @"$TMP" "$KROKI/svg" \
  -o "$TGT_DIR/DataModel-ClassDiagram.svg"
curl -sH "Content-Type: text/plain" --data-binary @"$TMP" "$KROKI/png" \
  -o "$TGT_DIR/DataModel-ClassDiagram.png"

[[ $# -lt 1 ]] && exit 0

# ApplicationDescription
$RUN linkml generate plantuml \
  --classes ApplicationDescription --classes ApplicationMetadata \
  --classes Parameter --classes Configuration \
  --classes DeploymentProfileDescription \
  "${ROOT_DIR}/spec/data-model/application/description.linkml.yaml" \
  | sed "/Component.*{$/,/}/d" > "$TMP"
curl -sH "Content-Type: text/plain" --data-binary @"$TMP" "$KROKI/svg" \
  -o "$TGT_DIR/ApplicationDescription-ClassDiagram.svg"

# DeploymentStatusManifest
$RUN linkml generate plantuml \
  --classes DeploymentStatusManifest --classes ApplicationDeployment \
  --classes DeploymentProfile \
  "${ROOT_DIR}/spec/data-model/margo.linkml.yaml" \
  | sed "s/@enduml/DeploymentStatusManifest ..> ApplicationDeployment\n@enduml/" \
  | sed "s/@enduml/ComponentStatus ..> Component\n@enduml/" > "$TMP"
curl -sH "Content-Type: text/plain" --data-binary @"$TMP" "$KROKI/svg" \
  -o "$TGT_DIR/DeploymentStatusManifest-ClassDiagram.svg"

# DesiredStateManifest
$RUN linkml generate plantuml \
  --classes DesiredStateManifest \
  "${ROOT_DIR}/spec/data-model/margo.linkml.yaml" \
  | sed "s/@enduml/DesiredStateManifest ..> ApplicationDeployment\n@enduml/" > "$TMP"
curl -sH "Content-Type: text/plain" --data-binary @"$TMP" "$KROKI/svg" \
  -o "$TGT_DIR/DesiredStateManifest-ClassDiagram.svg"

# DeviceCapabilities
$RUN linkml generate plantuml \
  --classes DeviceCapabilitiesManifest --classes Properties --classes Resources \
  "${ROOT_DIR}/spec/data-model/margo.linkml.yaml" > "$TMP"
curl -sH "Content-Type: text/plain" --data-binary @"$TMP" "$KROKI/svg" \
  -o "$TGT_DIR/DeviceCapabilities-ClassDiagram.svg"

# ApplicationDeployment
$RUN linkml generate plantuml \
  --classes ApplicationDeployment --classes DeploymentMetadata \
  --classes DeploymentAnnotations --classes Spec --classes Parameter \
  --classes DeploymentProfile --classes ComposeDeploymentProfile \
  --classes HelmDeploymentProfile --classes Component \
  "${ROOT_DIR}/spec/data-model/application-deployment.linkml.yaml" \
  | sed "s/@enduml/DeploymentAnnotations ..> ApplicationDescription\n@enduml/" > "$TMP"
curl -sH "Content-Type: text/plain" --data-binary @"$TMP" "$KROKI/svg" \
  -o "$TGT_DIR/ApplicationDeployment-ClassDiagram.svg"
