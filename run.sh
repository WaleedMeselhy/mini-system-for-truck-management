echo "Press <D> to stop."
docker-compose up --build &
while true; do
    echo "Press <D> or <d> to stop."
    for ((n = 0; n < 6; n++)); do
        sleep 1
        IFS= read -r -t 0.25 -n 1 -s holder && var="$holder"
        if [[ $var = "d" ]] || [[ $var = "D" ]]; then
            docker-compose down
            break 2
        fi
    done
done
exit 0
