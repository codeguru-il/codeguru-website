# Codeguru Xtreme Website
The [CodeGuru Xtreme](https://codeguru.co.il/Xtreme/) competition submission and management website, written in python using Django.

## Required stack
For local run:
- A postgres DB
- Storage: Create a `data` directory inside the repo's root, and add `files` and `submissions` as subdirectories.
- Health check:
  - Add a `.alive` file to `data/files`

For running on Azure (production):
- A postgres DB
- Storage: An accessible Azure Storage account with the `files` and `submissions` blob containers. Authorization is
  handled with system-assigned identities.

## Legal
This project is licensed under the [MIT License](/LICENSE.md).

The repository was initially created from [idosharon/codeguru-website](https://github.com/idosharon/codeguru-website).
