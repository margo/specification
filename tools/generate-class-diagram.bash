#!/usr/bin/env bash

TMP_PLANTUML_FILE=$(mktemp)

cleanup() {
  rm "${TMP_PLANTUML_FILE}"
}

trap cleanup EXIT

set -eu

THIS_SCRIPT="$(readlink -f "${0}")"
THIS_DIR="$(dirname "${THIS_SCRIPT}")"

ROOT_DIR="$(dirname "${THIS_DIR}")"

TGT_DIR="${ROOT_DIR}/build/artifacts/diagrams"

if command -v poetry &>/dev/null; then
  RUN="poetry run"
else
  if ! command -v linkml &>/dev/null; then
    echo "The command 'linkml' is missing"
    exit 1
  fi
  if ! command -v curl &>/dev/null; then
    echo "The command 'curl' is missing"
    exit 1
  fi
  RUN=""
fi

mkdir -p "${TGT_DIR}"

# Holistic class diagram
${RUN} linkml generate plantuml "${ROOT_DIR}/model/margo-data-model.linkml.yaml" |
  sed "s/@enduml/DeploymentAnnotations ..> ApplicationDescription\n@enduml/" |
  sed "s/@enduml/DeploymentStatusManifest ..> ApplicationDeployment\n@enduml/" |
  sed "s/@enduml/DesiredStateManifest ..> ApplicationDeployment\n@enduml/" >"${TMP_PLANTUML_FILE}"

curl -H "Content-Type: test/plain" --silent --data-binary @"${TMP_PLANTUML_FILE}" https://kroki.io/plantuml/svg -o "${TGT_DIR}/DataModel-ClassDiagram.svg"
curl -H "Content-Type: test/plain" --silent --data-binary @"${TMP_PLANTUML_FILE}" https://kroki.io/plantuml/png -o "${TGT_DIR}/DataModel-ClassDiagram.png"

if [ "$#" -lt 1 ]; then
  exit
fi

# Class diagram focused on ApplicationDescription
${RUN} linkml generate plantuml \
  --classes ApplicationDescription \
  --classes ApplicationMetadata \
  --classes Parameter \
  --classes Configuration \
  --classes DeploymentProfileDescription \
  "${ROOT_DIR}/model/application-description.linkml.yaml" |
  sed "/Component.*{$/,/}/d" \
    >"${TMP_PLANTUML_FILE}"

curl -H "Content-Type: test/plain" --silent --data-binary @"${TMP_PLANTUML_FILE}" https://kroki.io/plantuml/svg -o "${TGT_DIR}/ApplicationDescription-ClassDiagram.svg"

# Class diagram focused on DeploymentStatusManifest
${RUN} linkml generate plantuml \
  --classes DeploymentStatusManifest \
  --classes ApplicationDeployment \
  --classes DeploymentProfile \
  "${ROOT_DIR}/model/margo-data-model.linkml.yaml" |
  sed "s/@enduml/DeploymentStatusManifest ..> ApplicationDeployment\n@enduml/" |
  sed "s/@enduml/ComponentStatus ..> Component\n@enduml/" \
    >"${TMP_PLANTUML_FILE}"

curl -H "Content-Type: test/plain" --silent --data-binary @"${TMP_PLANTUML_FILE}" https://kroki.io/plantuml/svg -o "${TGT_DIR}/DeploymentStatusManifest-ClassDiagram.svg"

# Class diagram focused on DesiredStateManifest
${RUN} linkml generate plantuml \
  --classes DesiredStateManifest \
  "${ROOT_DIR}/model/margo-data-model.linkml.yaml" |
  sed "s/@enduml/DesiredStateManifest ..> ApplicationDeployment\n@enduml/" \
    >"${TMP_PLANTUML_FILE}"

curl -H "Content-Type: test/plain" --silent --data-binary @"${TMP_PLANTUML_FILE}" https://kroki.io/plantuml/svg -o "${TGT_DIR}/DesiredStateManifest-ClassDiagram.svg"

# Class diagram focused on DeviceCapabilities
${RUN} linkml generate plantuml \
  --classes DeviceCapabilitiesManifest \
  --classes Properties \
  --classes Resources \
  "${ROOT_DIR}/model/margo-data-model.linkml.yaml" \
  >"${TMP_PLANTUML_FILE}"

curl -H "Content-Type: test/plain" --silent --data-binary @"${TMP_PLANTUML_FILE}" https://kroki.io/plantuml/svg -o "${TGT_DIR}/DeviceCapabilities-ClassDiagram.svg"

# Class diagram focused on ApplicationDeployment
${RUN} linkml generate plantuml \
  --classes ApplicationDeployment \
  --classes DeploymentMetadata \
  --classes DeploymentAnnotations \
  --classes Spec \
  --classes Parameter \
  --classes DeploymentProfile \
  --classes ComposeDeploymentProfile \
  --classes HelmDeploymentProfile \
  --classes Component \
  "${ROOT_DIR}/model/application-deployment.linkml.yaml" |
  sed "s/@enduml/DeploymentAnnotations ..> ApplicationDescription\n@enduml/" \
    >"${TMP_PLANTUML_FILE}"

curl -H "Content-Type: test/plain" --silent --data-binary @"${TMP_PLANTUML_FILE}" https://kroki.io/plantuml/svg -o "${TGT_DIR}/ApplicationDeployment-ClassDiagram.svg"
