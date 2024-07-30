### Git Configuration

- **Set username globally:**
  ```bash
  git config --global user.name "Your Name"
  ```

- **Set email globally:**
  ```bash
  git config --global user.email "your.email@example.com"
  ```

- **List all configurations:**
  ```bash
  git config --list
  ```

- **Show help for Git configuration:**
  ```bash
  git config help
  ```

- **Show help for configuring Git:**
  ```bash
  git help config
  ```

---

### Simple Git Commands

#### Repository Initialization and Status
- **Initialize a new Git repository:**
  ```bash
  git init
  ```

- **Display the status of the repository:**
  ```bash
  git status
  ```

#### Adding and Committing Changes
- **Add all changes to the staging area:**
  ```bash
  git add .
  ```

- **Add specific file(s) to the staging area:**
  ```bash
  git add <filename>
  ```

- **Add all changes including untracked files to the staging area:**
  ```bash
  git add -A
  ```

- **Commit changes with a specified message:**
  ```bash
  git commit -m "Your commit message here"
  ```

- **Amend the last commit message:**
  ```bash
  git commit --amend -m "New commit message"
  ```

- **Amend the last commit without changing the message:**
  ```bash
  git commit --amend
  ```

#### Branch Operations
- **Create a new branch:**
  ```bash
  git branch branch_name
  ```

- **Switch to the specified branch:**
  ```bash
  git checkout branch_name
  ```

- **Create and switch to a new branch:**
  ```bash
  git checkout -b branch_name
  ```

- **List all branches, including remote-tracking branches:**
  ```bash
  git branch -a
  ```

- **Delete the specified branch:**
  ```bash
  git branch -d branch_name
  ```

#### Remote Operations
- **Add a remote repository:**
  ```bash
  git remote add origin remote_repository_url
  ```

- **List all remote repositories:**
  ```bash
  git remote -v
  ```

- **Clone a repository from a remote URL:**
  ```bash
  git clone <remote-repo-url>
  ```

- **Push changes to a remote repository and set the upstream branch:**
  ```bash
  git push -u origin branch_name
  ```

- **Fetch and merge changes from a remote repository:**
  ```bash
  git pull origin branch_name
  ```

---

### Intermediate Git Commands

#### Viewing and Comparing Commits
- **Display commit history:**
  ```bash
  git log
  ```

- **Display compact commit history:**
  ```bash
  git log --oneline
  ```

- **Display commit history with file changes:**
  ```bash
  git log --stat
  ```

- **Show the difference between two commits:**
  ```bash
  git diff commit-hash1 commit-hash2
  ```

- **Show the difference in unstaged files:**
  ```bash
  git diff
  ```

#### Merging and Rebasing
- **Merge changes from another branch into the current branch:**
  ```bash
  git merge branch_name
  ```

- **Rebase the current branch onto another:**
  ```bash
  git rebase branch_name
  ```

#### Stashing and Cleaning
- **Stash changes in a dirty working directory:**
  ```bash
  git stash
  ```

- **Apply stashed changes and remove them from the stash list:**
  ```bash
  git stash pop
  ```

- **Clean up untracked files and directories:**
  ```bash
  git clean -df
  ```

#### Resetting and Reverting
- **Unstage a file from the staging area:**
  ```bash
  git reset <filename>
  ```

- **Unstage all files from the staging area:**
  ```bash
  git reset
  ```

- **Soft reset to a specific commit, keeping changes in the staging area:**
  ```bash
  git reset --soft commit-hash
  ```

- **Mixed reset (default) to a specific commit, keeping changes in the working directory:**
  ```bash
  git reset commit-hash
  ```

- **Hard reset to a specific commit, discarding all changes:**
  ```bash
  git reset --hard commit-hash
  ```

- **Revert a specific commit by creating a new commit:**
  ```bash
  git revert commit-hash
  ```

#### Cherry-Picking
- **Apply the changes from a specific commit to the current branch:**
  ```bash
  git cherry-pick commit-hash
  ```

---

### Advanced Git Commands

#### Managing Remote Repositories and Tags
- **Fetch changes from all remotes:**
  ```bash
  git fetch --all
  ```

- **Fetch and merge changes from the remote "main" branch:**
  ```bash
  git pull origin main
  ```

- **Push changes to the remote "main" branch:**
  ```bash
  git push origin main
  ```

- **Fetch and prune deleted remote branches:**
  ```bash
  git fetch --prune
  ```

- **Push tags to the remote repository:**
  ```bash
  git push --tags
  ```

- **Delete a branch from the remote repository:**
  ```bash
  git push origin --delete branch_name
  ```

#### Advanced Branch Operations
- **Start an interactive rebase:**
  ```bash
  git rebase -i HEAD~n
  ```

- **Squash commits during a merge:**
  ```bash
  git merge --squash branch_name
  ```

- **List branches that have been merged into the current branch:**
  ```bash
  git branch --merged
  ```

- **Show branches that contain a specific commit:**
  ```bash
  git branch --contains commit-hash
  ```

#### Miscellaneous Advanced Commands
- **View reflog to see the history of all references to HEAD:**
  ```bash
  git reflog
  ```

- **Use bisect to find the commit that introduced a bug:**
  ```bash
  git bisect start
  ```

- **Manage multiple working trees:**
  ```bash
  git worktree add <path> <branch>
  ```

- **Show the details of a specific commit:**
  ```bash
  git show commit-hash
  ```

- **Pack unpacked objects in the repository:**
  ```bash
  git gc
  ```

- **Verify the connectivity and validity of objects in the database:**
  ```bash
  git fsck
  ```

- **Create an archive of files from a named tree:**
  ```bash
  git archive -o <file>.zip HEAD
  ```

This list covers essential Git commands across different levels of complexity, providing a comprehensive overview for learners at various stages. Use these commands to manage your repositories efficiently and effectively.
