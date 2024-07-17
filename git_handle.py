import git
import os
import subprocess
import requests

# 配置
GIT_URL = 'https://github.com/your-repo.git'
NEW_BRANCH = 'feature/DXP_AI_Migration'
REPLACE_TARGET = 'abc'
REPLACE_WITH = '123'
COMMIT_MESSAGE = 'HPA-DXP_AI_Migration'
GITHUB_API_URL = 'https://api.github.com'
REPO_OWNER = 'your-github-username'
REPO_NAME = 'your-repo'
JENKINS_URL = 'http://your-jenkins-url/job/your-job/build'
JENKINS_USER = 'your-jenkins-username'
JENKINS_TOKEN = 'your-jenkins-token'
GITHUB_TOKEN = 'your-github-token'

# 1. 克隆仓库并创建新分支
repo = git.Repo.clone_from(GIT_URL, 'local_repo', branch='master')
repo.git.checkout('HEAD', b=NEW_BRANCH)

# 2. 修改代码
for root, dirs, files in os.walk('local_repo'):
    for file in files:
        if file.endswith('.py'):  # 修改所有 .py 文件
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                content = f.read()
            new_content = content.replace(REPLACE_TARGET, REPLACE_WITH)
            with open(file_path, 'w') as f:
                f.write(new_content)

# 3. 添加和提交代码
repo.git.add(update=True)
repo.index.commit(COMMIT_MESSAGE)
repo.git.push('origin', NEW_BRANCH)

# 4. 创建 Pull Request
pr_data = {
    'title': 'HPA-DXP_AI_Migration',
    'body': '自动创建的迁移PR',
    'head': NEW_BRANCH,
    'base': 'master'
}
headers = {'Authorization': f'token {GITHUB_TOKEN}'}
response = requests.post(f'{GITHUB_API_URL}/repos/{REPO_OWNER}/{REPO_NAME}/pulls', json=pr_data, headers=headers)

if response.status_code == 201:
    print('Pull Request created successfully')
else:
    print('Failed to create Pull Request')
    print(response.json())

# 5. 调用 Jenkins 部署
jenkins_response = requests.post(JENKINS_URL, auth=(JENKINS_USER, JENKINS_TOKEN))

if jenkins_response.status_code == 201:
    print('Jenkins job started successfully')
else:
    print('Failed to start Jenkins job')
    print(jenkins_response.text)
