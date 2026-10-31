# Execution and supply-chain scope

The verification suite needs no network access at run time after dependency installation. Review scripts before execution. Dependency artefacts are hash-locked; the Docker base and CI actions are pinned. No automated publication, external API write, credential access or privileged command is implemented.

Docker build/run was not tested here. Hashes provide integrity checks, not publisher authenticity or author authorization. Do not treat this repository as an encrypted or confidential data store. Keep tokens, keys and private raw data out of release archives.
