The entire system is defined in GitLab pojects and repos. Once initial ingest of project documents is conducted, the entire GitLab hive for the project will be cloned locally here via SSH. Must validate that SSH is running and user alias is @roy.mayfield.

The GitLab root project is located at https://gitlab.com/atlas-datascience/lion
The entire hive underneath atlas-datascience/lion should be cloned here locally 

(exclude all these folders and files from the root repo via .gitignore in root folder to avoid conflicts between root repo (GitHub) and GitLab subfolders being created in this hive (GitLab))

We want to be able to conduct git operations in both in root project (prd-assembly) and in GitLab nested folders (prd-assembly/user-documents-input/gitlab-repos-hierarchical/<cloned-gitlab-hive-under-atlas-datascience-slash-lion>)
