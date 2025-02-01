@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

echo 1. To fix 'ref HEAD' error
echo 2. To create new commit
echo 3. To start commiting
echo 4. To fix the error like "error: failed to push some refs to <<repository>>"
echo 5. To fix the error like "error: bad signature 0x00000000. fatal: index file corrupt"
ECHO 6. To remove sensitive information from commits
echo 7. To remove a commmit
echo 0. To skip everything

set /p op=": "

IF "%op%"=="1" 
(
    :: Check for Stale Lock Files: Sometimes, a previous Git operation might have left a lock file behind. You can remove it manually:
    del .git\refs\heads\main.lock

    :: Prune Old Branches: Remove references to branches that no longer exist on the remote repository:
    git remote prune origin

    :: Garbage Collection: Run Git's garbage collection to clean up and optimize your repository:
    git gc

    :: Recreate the Branch: If the reference is broken, you might need to recreate the branch:
    git checkout -b new-branch
    git branch -D main
    git checkout -b main

    git log
    git status

    timeout /t 4

    git branch
    git add .

    set /p userCommit="Please enter your commit description: "
    echo You entered: %userCommit%
    git commit -m "%userCommit%"

    set /p push="Enter (1) to push, (0) to stop: "

    IF "%push%"=="1" 
    (
        timeout /t 4
        echo ========= Starting pushing the commits ...
        git push -u origin main
    ) 
    ELSE 
    (
        echo ========= Process ended =========.
    )
) 
ELSE IF "%op%"=="2" 
(
    timeout /t 4
    echo ========= Starting pushing the commits ...

    git add .

    set /p newcommit="Please enter your commit description: "

    echo You entered: %newcommit%

    git commit -m "%newcommit%"

    git push -u origin main

    git status

) 
ELSE IF "%op%"=="3" 
(
    echo You've entered %op%
) 
ELSE IF "%op%"=="4" 
(
    echo You've entered %op%
    echo Starting with pull request

    :: Fetch and Merge Changes: Update your local repository with the latest changes from the remote repository.
    git pull origin main

    :: Rebase Your Changes: If the above command doesn't work, try rebasing your changes.
    git pull --rebase origin main

    :: Force Push (Use with Caution): If you are sure that your local changes should overwrite the remote changes, you can force push. Be careful with this command as it can overwrite changes in the remote repository.
    git push -f origin main

    echo Finished ...

)
ELSE IF "%op%"=="5"
(
	
    REM Display the current directory path
    echo Current directory: %cd%

    REM Get the current directory path
    set current_path=%cd%

    REM Access the .git directory
    cd /d "%current_path%\.git" || (
        echo .git directory not found. Exiting...
        pause
        exit /b 1
    )

    REM Delete the index file
    del /f /q "index"

    REM Go back to the original directory and reset the Git index
    cd /d "%current_path%"
    git reset

    echo The index file has been reset. You can now commit your changes.
    pause

)
ELSE IF "%op%"=="6" 
(
    REM branch or BFG Repo-Cleaner to remove sensitive information from your commit history.
    :: Using git filter-branch
    git filter-branch --force --index-filter \ 'git rm --cached --ignore-unmatch path/to/secret/file' \ --prune-empty --tag-name-filter cat -- --all
    git push origin --force --all
    git push origin --force --tags

    ::CALL bfg --delete-files path/to/secret/file
    git reflog expire --expire=now --all && git gc --prune=now --aggressive
    git push origin --force --all
    git push origin --force --tags

)
ELSE IF ELSE IF "%op%"=="7"
(
    git log
    echo Enter the number of the commit
    set /p commit_number=": "
    # Start an interactive rebase session
    git rebase -i HEAD~%commit_number%

    echo Enter the new commit description
    set /p new_commit=": "
    git add .

    # Amend the commit to save changes
    git commit --amend --no-edit

    git commit -m "%new_commit%"

    # Continue the rebase process
    git rebase --continue

    git push origin --force
) 
ELSE 
(
    echo ========= Process ended =========.
)

echo ========= Push process ended =========.

ENDLOCAL