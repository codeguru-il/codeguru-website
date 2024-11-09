# Codeguru Xtreme Website
The official repo of the [CodeGuru Xtreme](https://codeguru.co.il/Xtreme/) competition submission and management website, written in python using Django.

## Required stack
For local run:
- A postgres DB
- A Redis cache
- Storage: Create a `data` directory inside of the repo's root, and add `files` and `submissions` as subdirectories.
- Health check:
  - Add a `.alive` file to `data/files`

For running on Azure (production):
- A postgres DB
- A redis cache
- Storage: An accessible Azure Storage account with the `files` and `submissions` blob containers. Authorization is
  handled with system-assigned identities.
