readonly -A FILTERS=(
    ['abpvn.txt']='https://raw.githubusercontent.com/abpvn/abpvn/master/filter/abpvn.txt'
    ['ext.txt']='https://raw.githubusercontent.com/luxysiv/filters/main/ext.txt'
)

function join_by { local IFS="$1"; shift; echo "$*"; }

for filter in "${!FILTERS[@]}"; do
    url="${FILTERS[$filter]}"
    echo "Downloading $filter from $url"
    if ! curl -o "$filter" "$url"; then
        echo "Failed to download $url"
        exit 1
    fi
    echo
done

cat abpvn.txt ext.txt > abpvn-ext.txt 