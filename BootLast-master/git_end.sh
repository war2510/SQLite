echo Введите описание коммита:
read commit_message

FILE="git_end.log"
if [ -f "$FILE" ]; then
    rm "$FILE"
fi
exec &>"$FILE"

echo "$FILE"
date

for COMM in "git add ." "git commit -m \"$commit_message\"" "git push" "git status" "git log --oneline --all --graph"; do
    echo
    echo "*****************************************"
    echo Выполняется "$COMM"
    eval $COMM
done
