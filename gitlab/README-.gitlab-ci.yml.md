# Sample .gitlab-ci.yml file
Sample .gitlab-ci.yml file is included to show basic functionality of a GItlab CI/CD workflow that uses:
* Worflow rules that apply with priority over other jobs rules defined
* Simple build, test and deploy stages in workflow
* Pre-build job for checking available variables common to all stages
* Other two pre-build jobs that triggering depending on Merge Requests operation vs Branch Commits
* build-job in build stage that triggers if changes in Dockerfile, node-web-server.js or package.json are detected. Sample files are included and Manual Approval is required. 
Docker build and push into local Gitlab Registry is also performed.
* Two test-jobs in test stage with job dependency setup.
* deploy-job in deploy stage that triggers only when the Merges Request is going to be pushed to the main/master branch. Docker build and push into local Gitlab Registry is performed using two tags (CI_COMMIT_SHORT_SHA and latest).